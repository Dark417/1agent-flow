"""Pattern 04 — Parallelization / sectioning (Amazon Strands).

Three independent reviewers (pros, cons, risks) run concurrently in a
ThreadPoolExecutor. A synthesizer then merges their outputs into one balanced
recommendation. The concurrency is plain Python, so the fan-out/fan-in is
explicit.

Design doc: docs/design/04-parallelization.md
"""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent  # noqa: E402

model = make_model()

reviewers = {
    "PROS": Agent(model=model, system_prompt=(
        "List the 3 strongest PROS of the given proposal. Bullets only.")),
    "CONS": Agent(model=model, system_prompt=(
        "List the 3 strongest CONS of the given proposal. Bullets only.")),
    "RISKS": Agent(model=model, system_prompt=(
        "List the 3 biggest RISKS of the given proposal. Bullets only.")),
}

synthesizer = Agent(model=model, system_prompt=(
    "You are given PROS, CONS, and RISKS analyses of a proposal. Write a "
    "balanced 4-sentence recommendation."))


def review(proposal: str) -> str:
    """Fan out the three analyses concurrently, then fan in to synthesize."""
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            label: pool.submit(lambda a=agent: str(a(proposal)))
            for label, agent in reviewers.items()
        }
        results = {label: fut.result() for label, fut in futures.items()}

    combined = "\n\n".join(f"{label}:\n{text}" for label, text in results.items())
    return str(synthesizer(combined))


if __name__ == "__main__":
    require_credentials()
    proposal = "We should rewrite our monolith as microservices this quarter."
    print("Proposal:", proposal)
    print("\n--- Recommendation ---\n")
    print(review(proposal))
