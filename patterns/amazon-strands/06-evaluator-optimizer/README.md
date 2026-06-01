# 06 — Evaluator–Optimizer (Amazon Strands)

A `generator` writes a haiku; an `evaluator` returns `PASS`/`FAIL` + one specific
fix. A capped `for` loop revises until PASS or 3 rounds.

- **Design doc:** [`docs/design/06-evaluator-optimizer.md`](../../../docs/design/06-evaluator-optimizer.md)
- **Strands approach:** a plain Python loop with `MAX_ROUNDS` as the guardrail and
  an explicit `break` on PASS.

## Run

```bash
python patterns/amazon-strands/06-evaluator-optimizer/agent.py
```

## What to watch

The `[round N] PASS/FAIL` lines show the loop working. Compare with Google's
`LoopAgent(max_iterations=3)` — same idea, here the stopping condition is an
ordinary `if`/`break`.
