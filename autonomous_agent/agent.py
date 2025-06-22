"""Implementation of a simple ReAct autonomous agent."""

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

import openai
from dotenv import load_dotenv

from .actions import git_commit, read_file, run_command, write_file

load_dotenv()


@dataclass
class StepResult:
    reasoning: str
    action: Dict[str, Any]
    observation: str


@dataclass
class ReActAgent:
    goal: str
    max_steps: int = 10
    timeout: int = 300
    model: str = "o3/codex-1"
    history: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.start_time = time.time()
        self.history.append({"role": "system", "content": f"You are an autonomous agent with the goal: {self.goal}"})

    def call_model(self, prompt: str) -> str:
        """Call the OpenAI API with the given prompt."""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history + [{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()

    def parse_action(self, text: str) -> Dict[str, Any]:
        """Parse the assistant response into an action."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"name": "noop", "args": {"response": text}}

    def execute_action(self, action: Dict[str, Any]) -> str:
        name = action.get("name")
        args = action.get("args", {})
        if name == "read_file":
            return read_file(**args)
        if name == "write_file":
            write_file(**args)
            return "file written"
        if name == "run_command":
            return run_command(**args)
        if name == "git_commit":
            git_commit(**args)
            return "committed"
        if name == "finish":
            return "goal achieved"
        return f"unknown action: {name}"

    def step(self, step_id: int) -> StepResult:
        prompt = "Think step"  # placeholder
        assistant_reply = self.call_model(prompt)
        action = self.parse_action(assistant_reply)
        observation = self.execute_action(action)
        self.history.append({"role": "assistant", "content": assistant_reply})
        self.history.append({"role": "system", "content": f"Observation: {observation}"})
        git_commit(f"Agent step {step_id}")
        return StepResult(reasoning=assistant_reply, action=action, observation=observation)

    def run(self) -> None:
        for step_id in range(1, self.max_steps + 1):
            if time.time() - self.start_time > self.timeout:
                print("Timeout reached, exiting")
                break
            result = self.step(step_id)
            print(f"Step {step_id} reasoning: {result.reasoning}")
            print(f"Step {step_id} action: {result.action}")
            print(f"Step {step_id} observation: {result.observation}")
            if result.action.get("name") == "finish":
                print("Goal achieved")
                break


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run an autonomous agent")
    parser.add_argument("goal", help="Goal for the agent to accomplish")
    args = parser.parse_args()

    agent = ReActAgent(goal=args.goal)
    agent.run()


if __name__ == "__main__":
    main()
