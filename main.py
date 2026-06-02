import typer
from pathlib import Path

from pygit_core import repository
from pygit_core import objects
from pygit_core import index
from pygit_core import diff as diff_module
from pygit_core import branch as branch_module
from pygit_core import checkout as checkout_module

app = typer.Typer()


@app.callback()
def main():
    """
    PyGit - Distributed Version Control System
    """
    pass


# ---------------- INIT ----------------

@app.command()
def init():
    """
    Initialize a new PyGit repository
    """
    try:
        repo = repository.Repo()
        repo.init()

        typer.echo(
            "Initialized empty PyGit repository"
        )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- HASH OBJECT ----------------

@app.command("hash-object")
def hash_object(file: str):
    """
    Compute SHA-1 hash and store blob object
    """
    try:
        repo = repository.Repo()

        if not Path(file).exists():
            raise Exception(
                f"File not found: {file}"
            )

        sha = objects.object_hash(
            file,
            repo,
            write=True
        )

        typer.echo(sha)

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- ADD ----------------

@app.command()
def add(file: str):
    """
    Add file to staging area
    """
    try:
        repo = repository.Repo()

        if not Path(file).exists():
            raise Exception(
                f"fatal: pathspec '{file}' did not match any files"
            )

        sha = objects.object_hash(
            file,
            repo,
            write=True
        )

        mode = 0o100644

        entries = index.read_index(repo)

        updated = False

        for i, entry in enumerate(entries):

            if entry.path == file:
                entries[i] = index.IndexEntry(
                    mode,
                    sha,
                    file
                )

                updated = True
                break

        if not updated:
            entries.append(
                index.IndexEntry(
                    mode,
                    sha,
                    file
                )
            )

        index.write_index(
            repo,
            entries
        )

        typer.echo(
            f"Added '{file}'"
        )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- COMMIT ----------------

@app.command()
def commit(
    message: str = typer.Option(
        ...,
        "-m",
        "--message",
        help="Commit message"
    )
):
    """
    Create a commit
    """
    from pygit_core import commit as commit_module

    try:
        repo = repository.Repo()

        sha = commit_module.write_commit(
            repo,
            message
        )

        typer.echo(
            f"[{sha[:7]}] {message}"
        )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- LOG ----------------

@app.command()
def log():
    """
    Show commit history
    """
    from pygit_core import log as log_module

    try:
        repo = repository.Repo()

        history = log_module.log_history(
            repo
        )

        typer.echo(history)

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- STATUS ----------------

@app.command()
def status():
    """
    Show working tree status
    """
    from pygit_core import status as status_module

    try:
        repo = repository.Repo()

        data = status_module.status_check(
            repo
        )

        output = status_module.format_status(
            data
        )

        typer.echo(output)

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )


# ---------------- DIFF ----------------

@app.command()
def diff():
    """
    Show file differences
    """
    try:
        repo = repository.Repo()

        output = diff_module.show_diff(
            repo
        )

        if output:
            typer.echo(
                output,
                nl=False
            )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )

# ---------------- BRANCH ----------------

@app.command()
def branch(
    name: str = typer.Argument(
        None,
        help="Branch name"
    )
):
    """
    List branches or create a branch
    """
    try:
        repo = repository.Repo()

        if name is None:

            branches = branch_module.list_branches(
                repo
            )

            for b in branches:
                typer.echo(b)

        else:

            branch_module.create_branch(
                repo,
                name
            )

            typer.echo(
                f"Branch '{name}' created"
            )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )
        
# ---------------- CHECKOUT ----------------

@app.command()
def checkout(branch_name: str):
    """
    Switch branch
    """
    try:
        repo = repository.Repo()

        checkout_module.checkout_branch(
            repo,
            branch_name
        )

        typer.echo(
            f"Switched to branch '{branch_name}'"
        )

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True
        )      

# ---------------- ENTRY POINT ----------------

if __name__ == "__main__":
    app()