# Google ADK implementations

Each pattern from [`docs/design/`](../../docs/design/) implemented with Google's
[Agent Development Kit](https://google.github.io/adk-docs/) (Gemini models).

| # | Pattern | Key ADK construct |
| --- | --- | --- |
| 01 | [Tool Use](01-tool-use/) | `LlmAgent(tools=[…])` |
| 02 | [Prompt Chaining](02-prompt-chaining/) | `SequentialAgent` |
| 03 | [Routing](03-routing/) | coordinator `LlmAgent` + `sub_agents` (auto-delegation) |
| 04 | [Parallelization](04-parallelization/) | `ParallelAgent` |
| 05 | [Orchestrator–Workers](05-orchestrator-workers/) | `LlmAgent` + `AgentTool` workers |
| 06 | [Evaluator–Optimizer](06-evaluator-optimizer/) | `LoopAgent(max_iterations=…)` |
| 07 | [Autonomous Agent](07-autonomous-agent/) | one `LlmAgent`, open-ended toolset |

## Setup

```bash
pip install -r ../../requirements-google.txt
cp ../../.env.example ../../.env   # then set GOOGLE_API_KEY
```

## Run

```bash
python patterns/google-adk/02-prompt-chaining/agent.py
```

Each `agent.py` is self-contained and runnable. Shared helpers (env loading,
credential check, a tiny `Runner` wrapper) live in [`shared/config.py`](shared/config.py).

> All credentials are read from `.env`. The repo ships with **placeholders
> only** — set your real `GOOGLE_API_KEY` before running.
