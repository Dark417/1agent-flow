"""Shared configuration and helpers for the Amazon Strands examples.

Loads AWS credentials from the repo-root `.env`, exposes the Bedrock model id,
validates credentials are present, and builds a configured `BedrockModel`.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load the repo-root .env regardless of where the example is launched from.
REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / ".env")

# Default Bedrock model — overridable via .env (BEDROCK_MODEL_ID).
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
REGION = os.getenv("AWS_REGION", "us-east-1")


def require_credentials() -> None:
    """Fail fast if AWS credentials are missing or still placeholders."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
    bearer = os.getenv("AWS_BEARER_TOKEN_BEDROCK", "")
    has_keys = access_key and not access_key.startswith("your-")
    has_bearer = bearer and not bearer.startswith("your-")
    if not (has_keys or has_bearer):
        raise SystemExit(
            "AWS Bedrock credentials are missing or still placeholders.\n"
            "1) cp .env.example .env\n"
            "2) set AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY + AWS_REGION\n"
            "   (or AWS_BEARER_TOKEN_BEDROCK), and enable Bedrock model access.\n"
        )


def make_model():
    """Build a configured Bedrock model for the examples."""
    from strands.models import BedrockModel

    return BedrockModel(model_id=MODEL_ID, region_name=REGION)
