# AGENTS.md

Guidance for AI coding agents (and humans) working in **1agent-flow**. This file
follows the [agents.md](https://agents.md) convention: a predictable place for
agents to learn how to build, test, and contribute to this project.

## Project overview

This is a **teaching repository** for agentic AI workflow design patterns. Every
pattern exists in three forms that must stay in sync:

1. A **design document** under `docs/design/`.
2. A **Google ADK** implementation under `patterns/google-adk/<pattern>/`.
3. An **Amazon Strands** implementation under `patterns/amazon-strands/<pattern>/`.

When you add or change a pattern, update all three.

## Project structure

```
docs/design/                 Pattern design documents (the source of truth for concepts)
ai/skills/<name>/SKILL.md     Reusable skills (capability + instructions)
ai/agents/<name>.md           Agent role definitions (frontmatter + system prompt)
patterns/google-adk/          Google ADK implementations, one folder per pattern
patterns/amazon-strands/      Amazon Strands implementations, one folder per pattern
```

Each `patterns/*/<pattern>/` folder contains `agent.py` (runnable) and `README.md`.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-google.txt    # for Google ADK examples
pip install -r requirements-amazon.txt    # for Amazon Strands examples
cp .env.example .env                       # then fill in real credentials
```

## How to run an example

```bash
python patterns/google-adk/<pattern>/agent.py
python patterns/amazon-strands/<pattern>/agent.py
```

## How to test

The smoke tests need no API keys or SDKs — they compile every example, check the
two providers stay structurally parallel, and verify no real secrets leaked.

```bash
make smoke            # or: python tests/smoke_test.py
```

## Conventions

- **Never commit real secrets.** API keys are always placeholders read from the
  environment via `.env`. The only key-like strings in the repo are
  `your-...-here` placeholders. Do not replace them with live values.
- **Keep the two implementations conceptually parallel.** The Google and Amazon
  versions of a pattern should solve the same illustrative task so they can be
  compared directly.
- **Code is for learning.** Favor clarity over cleverness. Comment the *why* of
  the pattern, not the syntax.
- Python ≥ 3.10. Format with `black`, line length 88.
- Pattern folders are numbered (`01-…`, `02-…`) to suggest a reading order.

## Adding a new pattern

1. Write `docs/design/NN-<pattern>.md` explaining the concept.
2. Create `patterns/google-adk/NN-<pattern>/{agent.py,README.md}`.
3. Create `patterns/amazon-strands/NN-<pattern>/{agent.py,README.md}`.
4. Link the new doc from `docs/design/README.md` and the root `README.md`.

## Validation checklist for agents

Before considering a change complete:

- [ ] `make smoke` passes (compiles examples, checks structure + secrets).
- [ ] No real credentials were introduced (the smoke test enforces this).
- [ ] Google + Amazon implementations of a touched pattern still match conceptually.
- [ ] The relevant design doc reflects any behavior change.

## Safety

This repo is for **authorized, educational** agent development. Do not add code
that exfiltrates credentials, targets third-party systems, or disables safety
features of the underlying SDKs.
