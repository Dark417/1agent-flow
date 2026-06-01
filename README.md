# 1agent-flow

A hands-on learning project for understanding **agentic AI workflows**. It pairs
plain-language **design documents** that explain each agent design pattern with
**two parallel, runnable implementations** of every pattern — one built on
**Google ADK** (Gemini) and one on **Amazon Strands Agents** (Bedrock).

The goal: read the pattern, then compare the *same* idea expressed in two
different SDKs so the concept sticks rather than the framework.

---

## What's inside

| Path | What it is |
| --- | --- |
| [`docs/design/`](docs/design/) | Design documents. Start here — they explain every pattern, when to use it, and how it works. |
| [`ai/skills/`](ai/skills/) | Reusable **skills** (capabilities) in the `SKILL.md` format. |
| [`ai/agents/`](ai/agents/) | **Agent** definitions (role + instructions) in the agent-frontmatter format. |
| [`patterns/google-adk/`](patterns/google-adk/) | Each pattern implemented with Google's Agent Development Kit. |
| [`patterns/amazon-strands/`](patterns/amazon-strands/) | The same patterns implemented with Amazon's Strands Agents SDK. |
| [`AGENTS.md`](AGENTS.md) | Machine-readable guidance for AI coding agents working in this repo. |

## The patterns covered

These are the canonical building blocks of agentic systems. Each has a design
doc **and** a Google + Amazon implementation.

1. **[Augmented LLM / Tool Use](docs/design/01-augmented-llm-tool-use.md)** — the foundation: an LLM that can call tools, retrieve, and remember.
2. **[Prompt Chaining](docs/design/02-prompt-chaining.md)** — decompose a task into a fixed sequence of steps.
3. **[Routing](docs/design/03-routing.md)** — classify the input, then dispatch to a specialist.
4. **[Parallelization](docs/design/04-parallelization.md)** — run subtasks concurrently (sectioning) or in competition (voting).
5. **[Orchestrator–Workers](docs/design/05-orchestrator-workers.md)** — a lead agent dynamically plans and delegates to workers.
6. **[Evaluator–Optimizer](docs/design/06-evaluator-optimizer.md)** — generate, critique, refine in a loop.
7. **[Autonomous Agent](docs/design/07-autonomous-agent.md)** — an open-ended reason-act loop that decides its own steps.

A conceptual map of how these relate lives in
[`docs/design/00-agentic-workflow-overview.md`](docs/design/00-agentic-workflow-overview.md).

---

## Quick start

> **Note on API keys:** every example reads credentials from environment
> variables and ships with **placeholders only**. Nothing here contains a real
> key. Copy `.env.example` to `.env` and fill in your own.

```bash
cp .env.example .env
# edit .env and add your real keys
```

### Run a Google ADK example

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-google.txt
python patterns/google-adk/02-prompt-chaining/agent.py
```

### Run an Amazon Strands example

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-amazon.txt
python patterns/amazon-strands/02-prompt-chaining/agent.py
```

Each pattern folder has its own `README.md` describing what the example does and
what output to expect.

---

## How to use this repo to learn

1. Read [`docs/design/00-agentic-workflow-overview.md`](docs/design/00-agentic-workflow-overview.md) for the mental model.
2. Pick a pattern doc (e.g. *Prompt Chaining*) and read it end to end.
3. Open the **Google** implementation, then the **Amazon** one, side by side.
4. Notice what is the same (the *pattern*) and what differs (the *SDK*).
5. Tweak the example, rerun, and watch the behavior change.

## Provider notes

| | Google ADK | Amazon Strands Agents |
| --- | --- | --- |
| Package | `google-adk` | `strands-agents`, `strands-agents-tools` |
| Default model | `gemini-2.0-flash` | `anthropic.claude-3-5-sonnet` on Bedrock |
| Auth | `GOOGLE_API_KEY` | AWS credentials / `AWS_BEARER_TOKEN_BEDROCK` |
| Docs | https://google.github.io/adk-docs/ | https://strandsagents.com/ |

## License

Provided for educational use. See individual SDK licenses for the underlying
frameworks.
