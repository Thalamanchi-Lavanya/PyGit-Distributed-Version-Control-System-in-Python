from flask import Flask, request
import subprocess

app = Flask(__name__)

def run_pygit_command(command):
    try:
        result = subprocess.run(
            ["python", "main.py"] + command,
            capture_output=True,
            text=True
        )

        output = result.stdout if result.stdout else result.stderr

        return f"""
        <html>
        <body style="font-family:Arial;background:#f5f5f5;padding:30px;">
            <h2>PyGit Output</h2>

            <div style="
                background:black;
                color:lime;
                padding:20px;
                border-radius:8px;
                white-space:pre-wrap;
                font-family:Consolas;
            ">
        {output}
            </div>

            <br>

            <a href="/">⬅ Back to Dashboard</a>
        </body>
        </html>
        """

    except Exception as e:
        return f"<h3>Error: {e}</h3>"


@app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():

    output = ""

    if request.method == "POST":

        command = request.form["command"]

        cmd = ["python", "main.py"] + command.split()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        output = result.stdout or result.stderr

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyGit Terminal</title>

        <style>

        body {{
            background:#1e1e1e;
            color:white;
            font-family:Consolas;
            padding:30px;
        }}

        h1 {{
            color:#4CAF50;
        }}

        input {{
            width:500px;
            padding:10px;
            font-size:16px;
        }}

        button {{
            padding:10px 20px;
            font-size:16px;
        }}

        pre {{
            background:black;
            color:#00ff00;
            padding:20px;
            margin-top:20px;
            min-height:300px;
            overflow:auto;
        }}

        </style>

    </head>

    <body>

        <h1>💻PyGit Terminal</h1>

        <form method="post">

            <input
                type="text"
                name="command"
                placeholder="status | branch | log | diff"
            >

            <button type="submit">
                Run
            </button>

        </form>

        <pre>{output}</pre>

    </body>

    </html>
    """


@app.route("/status")
def status():
    return run_pygit_command(["status"])


@app.route("/log")
def log():
    return run_pygit_command(["log"])


@app.route("/branch")
def branch():
    return run_pygit_command(["branch"])


@app.route("/diff")
def diff():
    return run_pygit_command(["diff"])


@app.route("/create_branch", methods=["GET", "POST"])
def create_branch():

    if request.method == "POST":

        branch_name = request.form["branch"]

        result = subprocess.run(
            ["python", "main.py", "branch", branch_name],
            capture_output=True,
            text=True
        )

        output = result.stdout or result.stderr

        return f"""
        <h2>Create Branch Result</h2>
        <pre>{output}</pre>
        <a href="/">Back</a>
        """

    return """
    <h2>Create New Branch</h2>

    <form method="post">

        Branch Name:
        <input type="text" name="branch">

        <br><br>

        <button type="submit">
            Create Branch
        </button>

    </form>

    <br>

    <a href="/">Back</a>
    """


@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":

        branch_name = request.form["branch"]

        result = subprocess.run(
            ["python", "main.py", "checkout", branch_name],
            capture_output=True,
            text=True
        )

        output = result.stdout or result.stderr

        return f"""
        <h2>Checkout Result</h2>
        <pre>{output}</pre>
        <a href="/">Back</a>
        """

    return """
    <h2>Checkout Branch</h2>

    <form method="post">

        Branch Name:
        <input type="text" name="branch">

        <br><br>

        <button type="submit">
            Checkout
        </button>

    </form>

    <br>

    <a href="/">Back</a>
    """


@app.route("/commit", methods=["GET", "POST"])
def commit():

    if request.method == "POST":

        message = request.form["message"]

        result = subprocess.run(
            [
                "python",
                "main.py",
                "commit",
                "-m",
                message
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout or result.stderr

        return f"""
        <h2>Commit Result</h2>
        <pre>{output}</pre>
        <a href="/">Back</a>
        """

    return """
    <h2>Create Commit</h2>

    <form method="post">

        Commit Message:
        <input type="text" name="message">

        <br><br>

        <button type="submit">
            Commit
        </button>

    </form>

    <br>

    <a href="/">Back</a>
    """


import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )