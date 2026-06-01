"""Pattern 06 — Evaluator-Optimizer (Amazon Strands).

A capped Python loop alternates a generator and an evaluator. The generator
writes/revises a haiku; the evaluator returns a verdict line (PASS/FAIL) plus
feedback. We stop on PASS or when we hit MAX_ROUNDS — the loop guardrail is
plain and explicit.

Design doc: docs/design/06-evaluator-optimizer.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent  # noqa: E402

MAX_ROUNDS = 3  # the mandatory guardrail: never loop forever

model = make_model()

generator = Agent(model=model, system_prompt=(
    "Write a haiku (3 lines, 5-7-5 syllables) about the given topic. If revision "
    "feedback is included, address it. Output ONLY the haiku."))

evaluator = Agent(model=model, system_prompt=(
    "Evaluate the given haiku for 5-7-5 structure and vivid imagery. Reply with "
    "a first line of exactly 'PASS' or 'FAIL', then on the next line ONE "
    "specific, actionable improvement (only if FAIL)."))


def refine(topic: str) -> str:
    """Generate, then critique-and-revise until PASS or MAX_ROUNDS."""
    draft = str(generator(f"Topic: {topic}"))
    for round_no in range(1, MAX_ROUNDS + 1):
        verdict = str(evaluator(draft)).strip()
        print(f"   [round {round_no}] {verdict.splitlines()[0]}")
        if verdict.upper().startswith("PASS"):
            break
        draft = str(generator(
            f"Topic: {topic}\nPrevious haiku:\n{draft}\nFeedback:\n{verdict}"))
    return draft


if __name__ == "__main__":
    require_credentials()
    topic = "the first snowfall"
    print("Topic:", topic)
    print("\n--- Result (after up to 3 refine rounds) ---\n")
    print(refine(topic))
