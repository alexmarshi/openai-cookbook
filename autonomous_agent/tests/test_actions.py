import os
from unittest import mock

import pytest

from autonomous_agent import actions


def test_read_write_file(tmp_path):
    file_path = tmp_path / "test.txt"
    actions.write_file(str(file_path), "hello")
    assert actions.read_file(str(file_path)) == "hello"


def test_run_command():
    output = actions.run_command("echo hi")
    assert "hi" in output


def test_git_commit():
    with mock.patch("subprocess.run") as run_mock:
        actions.git_commit("msg")
        run_mock.assert_any_call(["git", "add", "-A"], check=True)
        run_mock.assert_any_call(["git", "commit", "-m", "msg"], check=True)
