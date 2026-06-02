from pathlib import Path


def resolve_ref(repo, ref):
    """
    Convert a ref (e.g. refs/heads/main)
    to its commit SHA.
    """
    ref_path = repo.gitdir / ref

    if not ref_path.exists():
        return None

    return ref_path.read_text(
        encoding="utf-8"
    ).strip()


def update_ref(repo, ref, sha):
    """
    Write commit SHA to a ref file.
    """
    ref_path = repo.gitdir / ref

    ref_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ref_path.write_text(
        sha + "\n",
        encoding="utf-8"
    )


def is_detached_head(repo):
    """
    Check whether HEAD is detached.
    """
    head_path = repo.gitdir / "HEAD"

    if not head_path.exists():
        return False

    head_content = head_path.read_text(
        encoding="utf-8"
    ).strip()

    return not head_content.startswith("ref: ")