# 04 — Parallelization

Run multiple LLM calls **at the same time** and combine their results. Two
flavors: **sectioning** (split a task into independent parts) and **voting** (run
the same task several times and aggregate).

## The idea

LLM calls in a workflow are often independent of each other. Doing them
sequentially wastes time; doing them in parallel cuts latency. Parallelization
also unlocks a reliability trick — ask the *same* question multiple times and
take a consensus.

### Flavor A — Sectioning (fan-out / fan-in)

Break a task into parts that don't depend on each other, run them concurrently,
then merge.

```
                 ┌──► [ Worker: Pros    ] ──┐
   input ──split─┼──► [ Worker: Cons    ] ──┼──► [ Aggregator ] ──► output
                 └──► [ Worker: Risks   ] ──┘
```

### Flavor B — Voting

Run the same prompt N times (often at higher temperature, or with varied
phrasing) and combine via majority vote, union, or a judge.

```
   input ──┬──► [ LLM run 1 ] ──┐
           ├──► [ LLM run 2 ] ──┼──► [ Vote / aggregate ] ──► output
           └──► [ LLM run 3 ] ──┘
```

## How it works

1. **Fan out:** launch the independent calls concurrently.
2. Wait for all to finish.
3. **Fan in:** an aggregator step (code or another LLM) merges the outputs.

## When to use it

- **Sectioning:** the task has genuinely independent components (e.g. analyze a
  document from several angles; review code for security *and* style *and*
  performance separately).
- **Voting:** you want higher confidence/coverage — multiple looks catch more
  issues, and consensus reduces variance on subjective calls.

## Pitfalls

- **False independence** — if section B actually needs section A's output, this
  is really [Prompt Chaining](02-prompt-chaining.md).
- **Cost multiplies** — N parallel calls cost N times as much even though they
  finish faster.
- **Aggregation is its own design problem** — deciding *how* to merge (union?
  majority? a synthesis LLM?) matters as much as the parallel step.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Fan-out | `ParallelAgent(sub_agents=[…])` runs sub-agents concurrently | run agents in a `ThreadPoolExecutor` (or use `Swarm`) |
| Fan-in | a following `LlmAgent` reads each sub-agent's `output_key` | a synthesizer `Agent` reads the collected results |

Google has a built-in `ParallelAgent`; the Strands example uses
`concurrent.futures` so the concurrency is visible in plain Python.

See [`patterns/google-adk/04-parallelization/`](../../patterns/google-adk/04-parallelization/)
and [`patterns/amazon-strands/04-parallelization/`](../../patterns/amazon-strands/04-parallelization/).

---

*Workflow pattern. See Anthropic's "parallelization (sectioning & voting)."*
