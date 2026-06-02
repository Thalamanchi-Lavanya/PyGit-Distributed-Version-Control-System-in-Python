"""
Diff implementation for PyGit.
Shows changes between working directory and last commit.
"""

import difflib
import os

from pygit_core import commit
from pygit_core import tree
from pygit_core import objects


def get_head_commit(repo):
    """
    Get HEAD commit SHA
    """
    return commit.get_head_commit(repo)


def get_commit_tree(repo, commit_sha):
    """
    Extract tree SHA from commit
    """
    obj_type, data = objects.read_object(
        repo,
        commit_sha
    )

    if obj_type != b"commit":
        return None

    for line in data.decode("utf-8").split("\n"):
        if line.startswith("tree "):
            return line[5:]

    return None


def get_blob_content(repo, blob_sha):
    """
    Read blob content from blob object
    """
    obj_type, data = objects.read_object(
        repo,
        blob_sha
    )

    if obj_type != b"blob":
        return ""

    return data.decode(
        "utf-8",
        errors="replace"
    ).replace("\r\n", "\n")


def diff_files(
    path,
    old_content,
    new_content
):
    """
    Generate unified diff
    """

    old_lines = old_content.splitlines(
        keepends=True
    )

    new_lines = new_content.splitlines(
        keepends=True
    )

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        lineterm=""
    )

    return "".join(diff)


def show_diff(repo):
    """
    Compare working directory with HEAD commit
    """

    head_sha = get_head_commit(repo)

    if not head_sha:
        return ""

    tree_sha = get_commit_tree(
        repo,
        head_sha
    )

    if not tree_sha:
        return ""

    tree_entries = tree.read_tree(
        repo,
        tree_sha
    )

    output = []

    for entry in tree_entries:

        file_path = os.path.join(
            repo.worktree,
            entry.path
        )

        try:

            old_content = get_blob_content(
                repo,
                entry.sha
            )

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as f:

                new_content = f.read().replace(
                    "\r\n",
                    "\n"
                )

            if old_content != new_content:

                diff_text = diff_files(
                    entry.path,
                    old_content,
                    new_content
                )

                if diff_text:
                    output.append(diff_text)

        except FileNotFoundError:

            output.append(
                f"Deleted: {entry.path}"
            )

    return "\n".join(output)