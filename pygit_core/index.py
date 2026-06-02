import struct
from pathlib import Path


class IndexEntry:
    def __init__(self, mode, sha, path):
        self.mode = mode
        self.sha = sha
        self.path = path


def write_index(repo, entries):
    """
    Write entries to .pygit/index
    """
    index_path = repo.gitdir / "index"

    index_path.parent.mkdir(parents=True, exist_ok=True)

    with open(index_path, "wb") as f:
        # Header
        f.write(b"DIRC")
        f.write(struct.pack("!LL", 2, len(entries)))

        for entry in entries:
            path_bytes = entry.path.encode("utf-8")

            f.write(struct.pack("!L", entry.mode))
            f.write(bytes.fromhex(entry.sha))
            f.write(struct.pack("!H", len(path_bytes)))
            f.write(path_bytes)
            f.write(b"\x00")


def read_index(repo):
    """
    Read .pygit/index and return entries
    """
    index_path = repo.gitdir / "index"

    if not index_path.exists():
        return []

    entries = []

    try:
        with open(index_path, "rb") as f:

            header = f.read(4)

            if header != b"DIRC":
                return []

            header_data = f.read(8)

            if len(header_data) < 8:
                return []

            version, count = struct.unpack("!LL", header_data)

            if version != 2:
                return []

            for _ in range(count):

                mode_data = f.read(4)
                if len(mode_data) < 4:
                    break

                mode = struct.unpack("!L", mode_data)[0]

                sha_bytes = f.read(20)
                if len(sha_bytes) < 20:
                    break

                sha = sha_bytes.hex()

                path_len_data = f.read(2)
                if len(path_len_data) < 2:
                    break

                path_len = struct.unpack("!H", path_len_data)[0]

                path_bytes = f.read(path_len)
                if len(path_bytes) < path_len:
                    break

                path = path_bytes.decode("utf-8")

                f.read(1)  # null byte

                entries.append(
                    IndexEntry(
                        mode=mode,
                        sha=sha,
                        path=path
                    )
                )

    except Exception:
        return []

    return entries