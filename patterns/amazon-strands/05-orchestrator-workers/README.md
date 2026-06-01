# 05 — Orchestrator–Workers (Amazon Strands)

The **agents-as-tools** idiom: `research` and `write_brief` are `@tool`s that
each spin up a worker agent. The orchestrator decides at runtime how many
sub-questions to research, then composes the brief.

- **Design doc:** [`docs/design/05-orchestrator-workers.md`](../../../docs/design/05-orchestrator-workers.md)
- **Strands approach:** wrap worker agents in `@tool` functions and give them to
  the orchestrator. (Strands' `GraphBuilder`/`Swarm` are heavier alternatives.)

## Run

```bash
python patterns/amazon-strands/05-orchestrator-workers/agent.py
```

## What to watch

The number of `research` calls is chosen by the orchestrator LLM, not fixed in
code — that dynamic decomposition is what separates this from
[parallelization](../04-parallelization/).
