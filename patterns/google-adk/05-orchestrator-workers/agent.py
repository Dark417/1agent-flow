"""Pattern 05 — Orchestrator-Workers (Google ADK).

An orchestrator LlmAgent is given two worker agents wrapped as tools
(`AgentTool`). At runtime the orchestrator decides how many sub-questions the
request needs, calls the `researcher` tool for each, then calls the `writer`
tool to compose the final brief. The decomposition is dynamic — not hard-coded.

Design doc: docs/design/05-orchestrator-workers.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent  # noqa: E402
from google.adk.tools.agent_tool import AgentTool  # noqa: E402


# --- Workers ---------------------------------------------------------------
researcher = LlmAgent(
    name="researcher",
    model=MODEL,
    description="Researches ONE specific sub-question and returns concise, "
                "factual bullet findings.",
    instruction=(
        "You are a researcher. Given a single sub-question, return 2-4 concise, "
        "factual bullets answering it. If unsure, say so rather than inventing."
    ),
)

writer = LlmAgent(
    name="writer",
    model=MODEL,
    description="Writes a short, well-structured brief from collected findings.",
    instruction=(
        "You are a writer. Compose a clear ~200-word brief from the findings you "
        "are given. Use a short intro and grouped points."
    ),
)

# --- Orchestrator ----------------------------------------------------------
# The workers become callable tools. The orchestrator plans how to use them.
root_agent = LlmAgent(
    name="orchestrator",
    model=MODEL,
    instruction=(
        "You are a research lead. Break the user's request into the RIGHT number "
        "of focused sub-questions (you decide how many). Call the `researcher` "
        "tool once per sub-question to gather findings. Then call the `writer` "
        "tool with all the findings to produce the final brief. Return the "
        "writer's brief as your answer."
    ),
    tools=[AgentTool(agent=researcher), AgentTool(agent=writer)],
)


if __name__ == "__main__":
    require_api_key()
    task = "Give me a brief on the trade-offs of remote work for software teams."
    print("Task:", task)
    print("\n--- Brief ---\n")
    print(run(root_agent, task))
