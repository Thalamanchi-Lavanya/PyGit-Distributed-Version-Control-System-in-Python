import os
from pygit_core import index, objects, commit, tree


def get_working_files(repo):
    """
    Get all files in working directory except ignored folders
    """
    files = []

    ignore_dirs = {
        ".pygit",
        ".git",
        "venv",
        "__pycache__",
        ".pytest_cache",
        "tests"
    }

    for root, dirs, filenames in os.walk(repo.worktree):

        # Ignore unwanted folders
        dirs[:] = [
            d for d in dirs
            if d not in ignore_dirs
        ]

        for filename in filenames:

            path = os.path.join(root, filename)

            rel_path = os.path.relpath(
                path,
                repo.worktree
            )

            files.append(
                rel_path.replace("\\", "/")
            )

    return set(files)


def get_head_tree(repo):
    """
    Get file -> SHA mapping from HEAD commit
    """
    head_sha = commit.get_head_commit(repo)

    if not head_sha:
        return {}

    obj_type, commit_data = objects.read_object(
        repo,
        head_sha
    )

    tree_sha = None

    for line in commit_data.decode("utf-8").split("\n"):
        if line.startswith("tree "):
            tree_sha = line[5:]
            break

    if not tree_sha:
        return {}

    tree_entries = tree.read_tree(
        repo,
        tree_sha
    )

    return {
        entry.path: entry.sha
        for entry in tree_entries
    }


def status_check(repo):

    working_files = get_working_files(repo)

    index_entries = {
        entry.path: entry.sha
        for entry in index.read_index(repo)
    }

    head_tree = get_head_tree(repo)

    staged = []
    modified = []
    untracked = []

    # Staged changes
    for path, index_sha in index_entries.items():

        head_sha = head_tree.get(path)

        if index_sha != head_sha:
            staged.append(path)

    # Modified files
    for path in working_files:

        if path in index_entries:

            try:
                working_sha = objects.object_hash(
                    path,
                    repo,
                    write=False
                )

                if working_sha != index_entries[path]:
                    modified.append(path)

            except Exception:
                pass

    # Untracked files
    for path in working_files:

        if path not in index_entries:
            untracked.append(path)

    return {
        "staged": sorted(staged),
        "modified": sorted(modified),
        "untracked": sorted(untracked)
    }


def format_status(data):

    output = []

    if data["staged"]:
        output.append("Changes to be committed:")

        for f in data["staged"]:
            output.append(f"  staged: {f}")

        output.append("")

    if data["modified"]:
        output.append("Changes not staged for commit:")

        for f in data["modified"]:
            output.append(f"  modified: {f}")

        output.append("")

    if data["untracked"]:
        output.append("Untracked files:")

        for f in data["untracked"]:
            output.append(f"  {f}")

        output.append("")

    if (
        not data["staged"]
        and not data["modified"]
        and not data["untracked"]
    ):
        output.append(
            "nothing to commit, working tree clean"
        )

    return "\n".join(output).strip()