# 05 — Orchestrator–Workers (Google ADK)

An `orchestrator` agent decides — at runtime — how many sub-questions a request
needs, calls a `researcher` worker for each, then a `writer` worker to compose
the brief.

- **Design doc:** [`docs/design/05-orchestrator-workers.md`](../../../docs/design/05-orchestrator-workers.md)
- **ADK construct:** worker `LlmAgent`s wrapped as `AgentTool` and handed to the
  orchestrator as `tools`.

## Run

```bash
python patterns/google-adk/05-orchestrator-workers/agent.py
```

## What to watch

Unlike [parallelization](../04-parallelization/), the number of `researcher`
calls is **not** fixed in code — the orchestrator LLM chooses it based on the
task. That dynamic planning is the difference.
