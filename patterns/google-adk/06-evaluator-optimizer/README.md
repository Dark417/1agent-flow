# 06 — Evaluator–Optimizer (Google ADK)

A `generator` writes a haiku; an `evaluator` either approves it (stopping the
loop) or returns one specific fix to apply on the next pass. Capped at 3 rounds.

- **Design doc:** [`docs/design/06-evaluator-optimizer.md`](../../../docs/design/06-evaluator-optimizer.md)
- **ADK construct:** `LoopAgent(sub_agents=[generator, evaluator],
  max_iterations=3)`; the evaluator stops the loop by calling a tool that sets
  `tool_context.actions.escalate = True`.

## Run

```bash
python patterns/google-adk/06-evaluator-optimizer/agent.py
```

## What to watch

The `max_iterations` cap is the mandatory guardrail — without it, an evaluator
that's never satisfied would loop forever. Generate → critique → revise is how
quality climbs across rounds.
