"""Basic actions for the autonomous agent."""

import subprocess
from pathlib import Path
from typing import Optional


def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    return Path(path).read_text()


def write_file(path: str, content: str) -> None:
    """Write content to a file."""
    Path(path).write_text(content)


def run_command(command: str, timeout: Optional[int] = None) -> str:
    """Run a shell command and return its output."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout + result.stderr


def git_commit(message: str) -> None:
    """Commit all changes with the given message."""
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
