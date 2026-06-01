"""Pattern 02 — Prompt Chaining (Google ADK).

A SequentialAgent runs three LlmAgents in a fixed order: outline -> draft ->
polish. Each writes its output to shared session state via `output_key`, and the
next step reads it by templating `{key}` into its instruction.

Design doc: docs/design/02-prompt-chaining.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent, SequentialAgent  # noqa: E402


# Step 1: turn the topic into a tight outline. -> state["outline"]
outliner = LlmAgent(
    name="outliner",
    model=MODEL,
    output_key="outline",
    instruction=(
        "Create a tight 3-bullet outline for a short article about the user's "
        "topic. Output ONLY the three bullets."
    ),
)

# Step 2: expand the outline into a draft. reads {outline} -> state["draft"]
drafter = LlmAgent(
    name="drafter",
    model=MODEL,
    output_key="draft",
    instruction=(
        "Write a ~150-word article that follows this outline exactly:\n"
        "{outline}\n\nOutput ONLY the article."
    ),
)

# Step 3: polish the draft. reads {draft} -> state["final"]
polisher = LlmAgent(
    name="polisher",
    model=MODEL,
    output_key="final",
    instruction=(
        "Polish this draft for clarity, flow, and a strong opening line. "
        "Keep it ~150 words.\n\n{draft}\n\nOutput ONLY the polished article."
    ),
)

# The chain: each sub-agent runs in order, output feeding the next.
root_agent = SequentialAgent(
    name="article_pipeline",
    sub_agents=[outliner, drafter, polisher],
)


if __name__ == "__main__":
    require_api_key()
    topic = "Why prompt chaining beats one giant prompt"
    print("Topic:", topic)
    print("\n--- Final article ---\n")
    print(run(root_agent, topic))
