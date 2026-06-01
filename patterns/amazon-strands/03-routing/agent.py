"""Pattern 03 — Routing (Amazon Strands).

A cheap `router` agent classifies the message into one label; plain Python then
dispatches to the matching specialist agent. Making the branch explicit in Python
shows exactly how routing works.

Design doc: docs/design/03-routing.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent  # noqa: E402

model = make_model()

# The router: outputs ONLY a category label.
router = Agent(model=model, system_prompt=(
    "You are a classifier. Read the user's message and reply with EXACTLY one "
    "word from: billing, technical, general. No other text."))

# The specialists, each with a focused prompt.
specialists = {
    "billing": Agent(model=model, system_prompt=(
        "You are a billing specialist. Answer billing questions (payments, "
        "refunds, invoices) clearly and empathetically.")),
    "technical": Agent(model=model, system_prompt=(
        "You are a technical support specialist. Help the user diagnose and fix "
        "their problem with concrete steps.")),
    "general": Agent(model=model, system_prompt=(
        "You are a friendly general-support agent. Answer helpfully.")),
}


def handle(message: str) -> str:
    """Classify, then dispatch to the chosen specialist (fallback: general)."""
    label = str(router(message)).strip().lower()
    specialist = specialists.get(label, specialists["general"])
    print(f"   [router -> {label if label in specialists else 'general'}]")
    return str(specialist(message))


if __name__ == "__main__":
    require_credentials()
    for msg in [
        "I was charged twice for my subscription this month.",
        "The app crashes every time I click export.",
        "What are your support hours?",
    ]:
        print(f"\nUSER: {msg}")
        print(f"BOT : {handle(msg)}")
