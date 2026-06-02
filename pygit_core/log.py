import time
from pygit_core import objects, commit


def get_commit_data(repo, sha):
    """
    Read commit object and parse data
    """
    obj_type, data = objects.read_object(repo, sha)

    if obj_type != b"commit":
        raise Exception(f"Object {sha} is not a commit")

    lines = data.decode("utf-8").split("\n")

    commit_info = {
        "tree": None,
        "parent": None,
        "author": "Unknown",
        "timestamp": 0,
        "message": ""
    }

    message_start = 0

    for i, line in enumerate(lines):

        if line.startswith("tree "):
            commit_info["tree"] = line[5:]

        elif line.startswith("parent "):
            commit_info["parent"] = line[7:]

        elif line.startswith("author "):

            author_line = line[7:]

            if ">" in author_line:
                author_part, rest = author_line.split(">", 1)

                commit_info["author"] = author_part.strip() + ">"

                rest_parts = rest.strip().split()

                if len(rest_parts) >= 1:
                    commit_info["timestamp"] = int(rest_parts[0])

        elif line == "":
            message_start = i + 1
            break

    commit_info["message"] = (
        "\n".join(lines[message_start:]).strip()
    )

    return commit_info


def log_history(repo):
    """
    Return commit history from HEAD
    """
    sha = commit.get_head_commit(repo)

    if not sha:
        return "No commits yet"

    output = []

    while sha:

        data = get_commit_data(repo, sha)

        date_str = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(data["timestamp"])
        )

        # Short SHA display
        output.append(f"commit {sha[:7]}")
        output.append(f"Author: {data['author']}")
        output.append(f"Date:   {date_str}")
        output.append("")
        output.append(f"    {data['message']}")
        output.append("")

        sha = data["parent"]

    return "\n".join(output).strip()