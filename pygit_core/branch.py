import os
from pygit_core import commit


def create_branch(repo, name):
    """
    Create a new branch pointing to HEAD commit.
    """

    head_sha = commit.get_head_commit(repo)

    if not head_sha:
        raise Exception(
            "fatal: Not a valid object name 'HEAD'. Make a commit first"
        )

    branch_path = (
        repo.gitdir /
        "refs" /
        "heads" /
        name
    )

    if branch_path.exists():
        raise Exception(
            f"fatal: A branch named '{name}' already exists"
        )

    os.makedirs(
        branch_path.parent,
        exist_ok=True
    )

    with open(
        branch_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(head_sha + "\n")

    return name


def get_current_branch(repo):
    """
    Get current branch from HEAD
    """

    head_path = repo.gitdir / "HEAD"

    if not head_path.exists():
        return None

    with open(
        head_path,
        "r",
        encoding="utf-8"
    ) as f:
        ref = f.read().strip()

    if ref.startswith("ref: refs/heads/"):
        return ref.replace(
            "ref: refs/heads/",
            ""
        )

    return None


def list_branches(repo):
    """
    List all branches.
    """

    heads_dir = (
        repo.gitdir /
        "refs" /
        "heads"
    )

    if not heads_dir.exists():
        return []

    current = get_current_branch(repo)

    branches = []

    for branch_file in sorted(
        heads_dir.iterdir()
    ):

        if branch_file.is_file():

            name = branch_file.name

            if name == current:
                branches.append(
                    f"* {name}"
                )
            else:
                branches.append(
                    f"  {name}"
                )

    return branches