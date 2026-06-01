"""Pattern 06 — Evaluator-Optimizer (Google ADK).

A LoopAgent alternates a `generator` and an `evaluator`, capped at
max_iterations. The generator writes/revises a haiku; the evaluator either
approves it (by calling the `exit_loop` tool, which stops the loop) or writes
specific feedback that the generator addresses on the next pass.

Design doc: docs/design/06-evaluator-optimizer.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent, LoopAgent  # noqa: E402
from google.adk.tools.tool_context import ToolContext  # noqa: E402


def exit_loop(tool_context: ToolContext) -> dict:
    """Approve the current draft and stop the refinement loop.

    Call this ONLY when the draft fully meets the criteria.
    """
    tool_context.actions.escalate = True  # escalate ends the LoopAgent
    return {"status": "approved"}


# Generator: writes, or revises using {feedback} if it exists ('?' = optional).
generator = LlmAgent(
    name="generator",
    model=MODEL,
    output_key="draft",
    instruction=(
        "Write a haiku (3 lines, 5-7-5 syllables) about the user's topic.\n"
        "If feedback is provided below, REVISE to address it:\n{feedback?}\n\n"
        "Output ONLY the haiku."
    ),
)

# Evaluator: approve via exit_loop, or emit one concrete fix as {feedback}.
evaluator = LlmAgent(
    name="evaluator",
    model=MODEL,
    output_key="feedback",
    instruction=(
        "Evaluate this haiku for 5-7-5 structure and vivid imagery:\n\n{draft}\n\n"
        "If it fully passes, call the `exit_loop` tool. Otherwise output ONE "
        "specific, actionable improvement (and do NOT call the tool)."
    ),
    tools=[exit_loop],
)

# The loop: generate -> evaluate, up to 3 rounds (the guardrail).
root_agent = LoopAgent(
    name="refine_haiku",
    sub_agents=[generator, evaluator],
    max_iterations=3,
)


if __name__ == "__main__":
    require_api_key()
    topic = "the first snowfall"
    print("Topic:", topic)
    print("\n--- Result (after up to 3 refine rounds) ---\n")
    print(run(root_agent, topic))
