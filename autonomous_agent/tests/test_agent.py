from unittest import mock

import pytest

from autonomous_agent.agent import ReActAgent


@mock.patch("autonomous_agent.agent.git_commit")
@mock.patch("autonomous_agent.agent.run_command", return_value="ok")
@mock.patch("autonomous_agent.agent.write_file")
@mock.patch("autonomous_agent.agent.read_file", return_value="content")
@mock.patch("autonomous_agent.agent.openai.ChatCompletion.create")
def test_agent_step(mock_create, mock_read, mock_write, mock_run, mock_commit):
    mock_create.return_value = mock.Mock(choices=[mock.Mock(message={"content": '{"name": "finish"}'})])
    agent = ReActAgent(goal="test", max_steps=1)
    agent.step(1)
    assert mock_create.called
    assert mock_commit.called
