# 07 — Autonomous Agent (Amazon Strands)

One `Agent` with three tools and an open-ended goal. It runs its own
reason→act→observe loop: look up the distance, look up the fuel price, then
compute the round-trip cost — choosing the order itself.

- **Design doc:** [`docs/design/07-autonomous-agent.md`](../../../docs/design/07-autonomous-agent.md)
- **Strands approach:** a single `Agent` with a toolset; the built-in event loop
  drives reasoning until the model produces a final answer.

## Run

```bash
python patterns/amazon-strands/07-autonomous-agent/agent.py
```

## What to watch

Nothing scripts "get distance, then price, then multiply" — the agent decides.
Compare with [pattern 01](../01-tool-use/): identical machinery, but the task is
open-ended and multi-step. Production use needs guardrails (step caps, budgets) —
see the design doc.
