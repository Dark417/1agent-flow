# 04 — Parallelization (Amazon Strands)

Three reviewers (pros / cons / risks) analyze a proposal **concurrently** via a
`ThreadPoolExecutor`; a synthesizer merges their outputs.

- **Design doc:** [`docs/design/04-parallelization.md`](../../../docs/design/04-parallelization.md)
- **Strands approach:** `concurrent.futures.ThreadPoolExecutor` for the fan-out,
  a synthesizer `Agent` for the fan-in. (Strands' `Swarm` is an alternative.)

## Run

```bash
python patterns/amazon-strands/04-parallelization/agent.py
```

## What to watch

The three analyses run at the same time, then the synthesizer runs once on the
combined result. Compare with Google's first-class `ParallelAgent` — same shape,
here the concurrency is visible Python.
