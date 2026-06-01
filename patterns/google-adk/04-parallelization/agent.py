"""Pattern 04 — Parallelization / sectioning (Google ADK).

A ParallelAgent runs three independent reviewers concurrently (pros, cons,
risks). A following synthesizer reads all three results from state and writes a
balanced recommendation. The whole thing is wrapped in a SequentialAgent so the
synthesis runs after the fan-out completes.

Design doc: docs/design/04-parallelization.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent  # noqa: E402


# --- Independent workers (run in parallel) ---------------------------------
pros = LlmAgent(
    name="pros", model=MODEL, output_key="pros",
    instruction="List the 3 strongest PROS of the user's proposal. Bullets only.",
)
cons = LlmAgent(
    name="cons", model=MODEL, output_key="cons",
    instruction="List the 3 strongest CONS of the user's proposal. Bullets only.",
)
risks = LlmAgent(
    name="risks", model=MODEL, output_key="risks",
    instruction="List the 3 biggest RISKS of the user's proposal. Bullets only.",
)

# Fan-out: these three have no dependency on each other, so run them together.
gather = ParallelAgent(name="gather_views", sub_agents=[pros, cons, risks])

# Fan-in: combine the three independent analyses into one recommendation.
synthesizer = LlmAgent(
    name="synthesizer", model=MODEL, output_key="verdict",
    instruction=(
        "Given these three analyses:\n\nPROS:\n{pros}\n\nCONS:\n{cons}\n\n"
        "RISKS:\n{risks}\n\nWrite a balanced 4-sentence recommendation."
    ),
)

root_agent = SequentialAgent(
    name="parallel_review",
    sub_agents=[gather, synthesizer],
)


if __name__ == "__main__":
    require_api_key()
    proposal = "We should rewrite our monolith as microservices this quarter."
    print("Proposal:", proposal)
    print("\n--- Recommendation ---\n")
    print(run(root_agent, proposal))
