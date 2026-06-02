import os
from pathlib import Path

class Repo:
    def __init__(self, path="."):
        self.worktree = Path(path)
        self.gitdir = self.worktree / ".pygit"

    def init(self):
        """Initialize a new repository"""
        self.gitdir.mkdir(exist_ok=True)
        
        # Create objects dir
        (self.gitdir / "objects").mkdir(exist_ok=True)
        
        # Create refs/heads dir  
        (self.gitdir / "refs" / "heads").mkdir(parents=True, exist_ok=True)
        
        # Create HEAD pointing to main branch
        with open(self.gitdir / "HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        
        # Create empty index
        (self.gitdir / "index").touch()
        
        # Create config
        (self.gitdir / "config").touch()
