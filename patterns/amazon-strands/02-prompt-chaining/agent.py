"""Pattern 02 — Prompt Chaining (Amazon Strands).

Three single-purpose agents run in a fixed order: outline -> draft -> polish.
In Strands the "chain" is just ordinary Python — we call each agent and pass its
output (as a string) into the next. The data flow is fully explicit.

Design doc: docs/design/02-prompt-chaining.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent  # noqa: E402

model = make_model()

outliner = Agent(model=model, system_prompt=(
    "Create a tight 3-bullet outline for a short article about the given topic. "
    "Output ONLY the three bullets."))

drafter = Agent(model=model, system_prompt=(
    "Write a ~150-word article that follows the given outline exactly. "
    "Output ONLY the article."))

polisher = Agent(model=model, system_prompt=(
    "Polish the given draft for clarity, flow, and a strong opening line. "
    "Keep it ~150 words. Output ONLY the polished article."))


def run_chain(topic: str) -> str:
    """Outline -> draft -> polish, passing each output into the next step."""
    outline = str(outliner(f"Topic: {topic}"))
    draft = str(drafter(f"Outline:\n{outline}"))
    final = str(polisher(f"Draft:\n{draft}"))
    return final


if __name__ == "__main__":
    require_credentials()
    topic = "Why prompt chaining beats one giant prompt"
    print("Topic:", topic)
    print("\n--- Final article ---\n")
    print(run_chain(topic))
