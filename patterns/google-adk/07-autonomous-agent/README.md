# 07 — Autonomous Agent (Google ADK)

One `trip_planner` agent with three tools and an open-ended goal. It runs its own
reason→act→observe loop: look up the distance, look up the fuel price, then
compute the round-trip cost — choosing the order itself.

- **Design doc:** [`docs/design/07-autonomous-agent.md`](../../../docs/design/07-autonomous-agent.md)
- **ADK construct:** a single `LlmAgent` with a toolset; the `Runner` drives the
  loop until the model stops calling tools.

## Run

```bash
python patterns/google-adk/07-autonomous-agent/agent.py
```

## What to watch

Nothing in the code scripts "get distance, then price, then multiply." The agent
decides that sequence. Compare with [pattern 01](../01-tool-use/): same
machinery, but here the task is open-ended and multi-step. In production this
loop needs guardrails (step caps, budgets) — see the design doc.
