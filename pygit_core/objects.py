import hashlib
import zlib
from pathlib import Path


class GitObject:
    def __init__(self, repo, data=None):
        self.repo = repo

        if data is not None:
            self.deserialize(data)
        else:
            self.init()

    def init(self):
        pass

    def serialize(self):
        raise NotImplementedError()

    def deserialize(self, data):
        raise NotImplementedError()


class GitBlob(GitObject):
    type = b"blob"

    def init(self):
        self.blobdata = b""

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data


def object_write(obj):
    """
    Save GitObject and return SHA
    """
    data = obj.serialize()

    header = obj.type + b" " + str(len(data)).encode() + b"\x00"
    full_data = header + data

    sha = hashlib.sha1(full_data).hexdigest()

    obj_path = obj.repo.gitdir / "objects" / sha[:2] / sha[2:]
    obj_path.parent.mkdir(parents=True, exist_ok=True)

    with open(obj_path, "wb") as f:
        f.write(zlib.compress(full_data))

    return sha


def object_hash(file_path, repo, write=True):
    """
    Read file and create blob hash
    """
    with open(file_path, "rb") as f:
        data = f.read()

    obj = GitBlob(repo)
    obj.deserialize(data)

    if write:
        return object_write(obj)

    header = obj.type + b" " + str(len(data)).encode() + b"\x00"
    full_data = header + data

    return hashlib.sha1(full_data).hexdigest()


def write_object(repo, obj_type, data):
    """
    Generic object writer for blob/tree/commit
    """
    header = obj_type + b" " + str(len(data)).encode() + b"\x00"
    full_data = header + data

    sha = hashlib.sha1(full_data).hexdigest()

    obj_path = repo.gitdir / "objects" / sha[:2] / sha[2:]
    obj_path.parent.mkdir(parents=True, exist_ok=True)

    with open(obj_path, "wb") as f:
        f.write(zlib.compress(full_data))

    return sha


def read_object(repo, sha):
    """
    Read object from .pygit/objects
    """
    obj_path = repo.gitdir / "objects" / sha[:2] / sha[2:]

    if not obj_path.exists():
        raise Exception(f"Object not found: {sha}")

    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())

    null_index = raw.index(b"\x00")

    header = raw[:null_index]
    data = raw[null_index + 1:]

    obj_type, size = header.split(b" ", 1)

    if int(size) != len(data):
        raise Exception("Corrupt object")

    return obj_type, data