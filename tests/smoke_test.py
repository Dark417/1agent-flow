"""Smoke tests for the 1agent-flow repository.

Dependency-free and credential-free: validates that every example *compiles*,
that the two provider implementations stay structurally parallel, and that no
real secrets leaked in (only placeholders are allowed).

Run directly:      python tests/smoke_test.py
Run with pytest:   pytest tests/smoke_test.py
"""

from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS = REPO_ROOT / "patterns"
PROVIDERS = ["google-adk", "amazon-strands"]
EXPECTED_PATTERNS = [
    "01-tool-use",
    "02-prompt-chaining",
    "03-routing",
    "04-parallelization",
    "05-orchestrator-workers",
    "06-evaluator-optimizer",
    "07-autonomous-agent",
]

# Patterns that would match a *real* leaked credential (not a placeholder).
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),          # AWS access key id
    re.compile(r"AIza[0-9A-Za-z_\-]{35}"),    # Google API key
    re.compile(r"sk-[A-Za-z0-9]{20,}"),       # generic provider secret key
]


def _all_py_files() -> list[Path]:
    return sorted(PATTERNS.rglob("*.py"))


def test_every_example_compiles() -> None:
    """Every Python file under patterns/ must compile."""
    files = _all_py_files()
    assert files, "no python files found under patterns/"
    for path in files:
        py_compile.compile(str(path), doraise=True)


def test_providers_have_all_patterns() -> None:
    """Both providers implement the same set of patterns, each with agent.py + README."""
    for provider in PROVIDERS:
        for pattern in EXPECTED_PATTERNS:
            folder = PATTERNS / provider / pattern
            assert (folder / "agent.py").is_file(), f"missing {folder}/agent.py"
            assert (folder / "README.md").is_file(), f"missing {folder}/README.md"


def test_no_real_secrets_committed() -> None:
    """Only placeholder credentials may appear anywhere in the tracked tree."""
    suffixes = {".py", ".md", ".txt", ".example", ".env"}
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix not in suffixes and path.name != ".env.example":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            assert not pat.search(text), f"possible real secret in {path}"


def test_env_example_uses_placeholders() -> None:
    """.env.example must exist and use 'your-...-here' placeholders, not real keys."""
    env = REPO_ROOT / ".env.example"
    assert env.is_file(), ".env.example is missing"
    text = env.read_text(encoding="utf-8")
    assert "your-" in text, ".env.example should contain placeholder values"


def main() -> int:
    tests = [
        test_every_example_compiles,
        test_providers_have_all_patterns,
        test_no_real_secrets_committed,
        test_env_example_uses_placeholders,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {test.__name__}: {exc}")
        else:
            print(f"ok    {test.__name__}")
    print(f"\n{len(tests) - failures}/{len(tests)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
