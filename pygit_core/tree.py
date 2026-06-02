from pygit_core import objects, index


class TreeEntry:
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha


def write_tree(repo):
    """
    Create tree object from index entries
    """
    entries = index.read_index(repo)

    if not entries:
        raise Exception("nothing to commit")

    entries.sort(key=lambda e: e.path)

    tree_data = b""

    for entry in entries:
        mode = format(entry.mode, "o").encode("utf-8")
        path = entry.path.encode("utf-8")
        sha_bytes = bytes.fromhex(entry.sha)

        tree_data += mode + b" " + path + b"\x00" + sha_bytes

    tree_sha = objects.write_object(
        repo,
        b"tree",
        tree_data
    )

    return tree_sha


def read_tree(repo, tree_sha):
    """
    Read tree object and return list of TreeEntry
    """
    obj_type, data = objects.read_object(
        repo,
        tree_sha
    )

    if obj_type != b"tree":
        raise Exception("Not a tree object")

    entries = []

    i = 0

    while i < len(data):

        # Read mode
        space_idx = data.index(b" ", i)
        mode = int(
            data[i:space_idx].decode(),
            8
        )

        # Read path
        null_idx = data.index(
            b"\x00",
            space_idx
        )

        path = data[
            space_idx + 1:null_idx
        ].decode("utf-8")

        # Read SHA (20 bytes)
        sha_bytes = data[
            null_idx + 1:null_idx + 21
        ]

        sha = sha_bytes.hex()

        entries.append(
            TreeEntry(
                mode,
                path,
                sha
            )
        )

        i = null_idx + 21

    return entries