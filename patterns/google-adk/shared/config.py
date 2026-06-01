"""Shared configuration and helpers for the Google ADK examples.

Loads credentials from the repo-root `.env`, exposes the model name, validates
that a real API key is present, and provides a small `run()` wrapper around the
ADK Runner so each example can stay focused on the *pattern*.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

# Load the repo-root .env regardless of where the example is launched from.
REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / ".env")

# Default model — overridable via .env (GOOGLE_MODEL).
MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")


def require_api_key() -> None:
    """Fail fast with a friendly message if the API key is missing/placeholder."""
    key = os.getenv("GOOGLE_API_KEY", "")
    if not key or key.startswith("your-"):
        raise SystemExit(
            "GOOGLE_API_KEY is missing or still set to the placeholder.\n"
            "1) cp .env.example .env\n"
            "2) add a real key from https://aistudio.google.com/apikey\n"
        )


def run(agent, prompt: str, *, app_name: str = "oneagentflow",
        user_id: str = "learner") -> str:
    """Run an ADK agent against a single prompt and return the final text.

    ADK is async under the hood; this hides the event loop and the event
    streaming so the examples read top-to-bottom.
    """
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    async def _run() -> str:
        runner = InMemoryRunner(agent=agent, app_name=app_name)
        session = await runner.session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        message = types.Content(role="user", parts=[types.Part(text=prompt)])
        final_text = ""
        async for event in runner.run_async(
            user_id=user_id, session_id=session.id, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_text = event.content.parts[0].text or final_text
        return final_text

    return asyncio.run(_run())
