# 04 — Parallelization (Google ADK)

Three reviewers (pros / cons / risks) analyze a proposal **concurrently**, then a
synthesizer merges their outputs into one recommendation.

- **Design doc:** [`docs/design/04-parallelization.md`](../../../docs/design/04-parallelization.md)
- **ADK construct:** `ParallelAgent` for the fan-out; a trailing `LlmAgent`
  (inside a `SequentialAgent`) for the fan-in.

## Run

```bash
python patterns/google-adk/04-parallelization/agent.py
```

## What to watch

The three analyses are independent, so ADK runs them at the same time — faster
than chaining. The synthesizer only runs once all three have landed in state.
