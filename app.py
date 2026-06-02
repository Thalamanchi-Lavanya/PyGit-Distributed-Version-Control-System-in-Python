from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🚀 PyGit - Distributed Version Control System</h1>
    <p>Built from scratch in Python.</p>

    <h2>Features</h2>
    <ul>
        <li>Repository Initialization</li>
        <li>SHA-1 Object Storage</li>
        <li>Add / Commit</li>
        <li>Log History</li>
        <li>Status</li>
        <li>Diff</li>
        <li>Branch</li>
        <li>Checkout</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)