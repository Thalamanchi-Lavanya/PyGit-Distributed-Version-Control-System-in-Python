def checkout_branch(repo, branch_name):
    """
    Switch to another branch.
    """

    branch_path = (
        repo.gitdir /
        "refs" /
        "heads" /
        branch_name
    )

    if not branch_path.exists():
        raise Exception(
            f"fatal: branch '{branch_name}' does not exist"
        )

    head_path = repo.gitdir / "HEAD"

    with open(
        head_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            f"ref: refs/heads/{branch_name}\n"
        )

    return branch_name