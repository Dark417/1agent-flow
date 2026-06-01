"""Pattern 05 — Orchestrator-Workers (Amazon Strands).

The "agents as tools" idiom: each worker agent is wrapped in a @tool function.
The orchestrator agent is given those tools and decides — at runtime — how many
sub-questions to research and when to compose the brief. The decomposition is
dynamic, not hard-coded.

Design doc: docs/design/05-orchestrator-workers.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent, tool  # noqa: E402

model = make_model()


# --- Workers, exposed to the orchestrator as tools -------------------------
@tool
def research(sub_question: str) -> str:
    """Research ONE specific sub-question and return concise bullet findings."""
    worker = Agent(model=model, system_prompt=(
        "You are a researcher. Given a single sub-question, return 2-4 concise, "
        "factual bullets. If unsure, say so rather than inventing."))
    return str(worker(sub_question))


@tool
def write_brief(findings: str) -> str:
    """Write a clear ~200-word brief from the collected findings."""
    worker = Agent(model=model, system_prompt=(
        "You are a writer. Compose a clear ~200-word brief from the findings. "
        "Use a short intro and grouped points."))
    return str(worker(findings))


# --- Orchestrator ----------------------------------------------------------
orchestrator = Agent(model=model, tools=[research, write_brief], system_prompt=(
    "You are a research lead. Break the user's request into the RIGHT number of "
    "focused sub-questions (you decide how many). Call `research` once per "
    "sub-question, then call `write_brief` with all the findings to produce the "
    "final brief. Return that brief."))


if __name__ == "__main__":
    require_credentials()
    task = "Give me a brief on the trade-offs of remote work for software teams."
    print("Task:", task)
    print("\n--- Brief ---\n")
    print(orchestrator(task))
