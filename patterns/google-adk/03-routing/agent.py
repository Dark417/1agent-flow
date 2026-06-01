"""Pattern 03 — Routing (Google ADK).

A coordinator LlmAgent with three specialist sub-agents. ADK's automatic
delegation lets the coordinator transfer the conversation to the single most
appropriate specialist instead of answering itself.

Design doc: docs/design/03-routing.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent  # noqa: E402


# --- Specialists -----------------------------------------------------------
# `description` is critical: the coordinator routes based on these.
billing = LlmAgent(
    name="billing",
    model=MODEL,
    description="Handles billing: payments, refunds, invoices, charges, pricing.",
    instruction="You are a billing specialist. Answer the user's billing question "
                "clearly and empathetically. Stay strictly on billing topics.",
)

technical = LlmAgent(
    name="technical",
    model=MODEL,
    description="Handles technical support: errors, bugs, setup, troubleshooting.",
    instruction="You are a technical support specialist. Help the user diagnose "
                "and fix their technical problem with concrete steps.",
)

general = LlmAgent(
    name="general",
    model=MODEL,
    description="Handles general questions that are not billing or technical.",
    instruction="You are a friendly general-support agent. Answer the user's "
                "question helpfully.",
)

# --- Coordinator (the router) ----------------------------------------------
root_agent = LlmAgent(
    name="support_router",
    model=MODEL,
    instruction=(
        "You are a support router. Read the user's message and transfer it to "
        "the single most appropriate specialist: `billing`, `technical`, or "
        "`general`. Do NOT answer the question yourself — just route it."
    ),
    sub_agents=[billing, technical, general],
)


if __name__ == "__main__":
    require_api_key()
    for msg in [
        "I was charged twice for my subscription this month.",
        "The app crashes every time I click export.",
        "What are your support hours?",
    ]:
        print(f"\nUSER: {msg}")
        print(f"BOT : {run(root_agent, msg)}")
