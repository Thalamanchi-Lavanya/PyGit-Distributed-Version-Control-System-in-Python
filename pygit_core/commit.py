import time
import os
from pygit_core import objects, tree


def get_head_commit(repo):
    """
    Get current HEAD commit SHA
    """
    head_file = repo.gitdir / "HEAD"

    if not head_file.exists():
        return None

    ref_content = head_file.read_text().strip()

    # ref: refs/heads/main
    if ref_content.startswith("ref: "):
        ref_path = repo.gitdir / ref_content[5:]

        if ref_path.exists():
            commit_sha = ref_path.read_text().strip()
            return commit_sha if commit_sha else None

    else:
        # Detached HEAD
        return ref_content if ref_content else None

    return None


def update_head(repo, commit_sha):
    """
    Update HEAD to point to new commit
    """
    head_file = repo.gitdir / "HEAD"

    if not head_file.exists():
        # First commit
        ref_path = repo.gitdir / "refs" / "heads" / "main"

        ref_path.parent.mkdir(parents=True, exist_ok=True)

        ref_path.write_text(commit_sha)
        head_file.write_text("ref: refs/heads/main")

        return

    ref_content = head_file.read_text().strip()

    if ref_content.startswith("ref: "):
        ref_path = repo.gitdir / ref_content[5:]

        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text(commit_sha)

    else:
        # Detached HEAD
        head_file.write_text(commit_sha)


def write_commit(repo, message, author=None):
    """
    Create commit object
    """

    # Create tree
    tree_sha = tree.write_tree(repo)

    # Parent commit
    parent_sha = get_head_commit(repo)

    # Author
    if author is None:
        username = (
            os.getenv("USERNAME")
            or os.getenv("USER")
            or "unknown"
        )

        author = f"{username} <{username}@pygit.local>"

    timestamp = int(time.time())
    timezone = "+0000"

    lines = [
        f"tree {tree_sha}"
    ]

    if parent_sha:
        lines.append(f"parent {parent_sha}")

    lines.append(
        f"author {author} {timestamp} {timezone}"
    )

    lines.append(
        f"committer {author} {timestamp} {timezone}"
    )

    lines.append("")
    lines.append(message)

    commit_data = "\n".join(lines).encode("utf-8")

    # Write commit object
    commit_sha = objects.write_object(
        repo,
        b"commit",
        commit_data
    )

    # Update HEAD
    update_head(repo, commit_sha)

    return commit_sha
