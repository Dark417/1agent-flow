# 05 — Orchestrator–Workers

A central **orchestrator** LLM dynamically breaks a task into subtasks, delegates
each to a **worker**, and synthesizes the results.

## The idea

[Parallelization](04-parallelization.md) splits work along lines *you* decide in
advance. But for many real tasks you don't know the subtasks until you see the
input — how many files a code change touches, how many sub-questions a research
query implies. The **orchestrator** pattern hands that decision to an LLM: it
plans the breakdown at runtime, spins up workers, and combines what they return.

```
                         ┌────────────────────┐
   task  ─────────────►  │     Orchestrator   │  plans subtasks (dynamic!)
                         └───────┬────────────┘
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
        ┌──────────┐       ┌──────────┐       ┌──────────┐
        │ Worker 1 │       │ Worker 2 │  ...  │ Worker k │  (k decided at runtime)
        └────┬─────┘       └────┬─────┘       └────┬─────┘
              └──────────────────┼──────────────────┘
                                 ▼
                         ┌────────────────────┐
                         │     Orchestrator   │  synthesizes final answer
                         └────────────────────┘
```

The key difference from parallelization: **the number and nature of the subtasks
is determined by the model, not hard-coded.**

## How it works

1. The orchestrator receives the task and **produces a plan** — a list of
   subtasks.
2. For each subtask it **delegates** to a worker (often the same worker prompt
   with different inputs, or specialized workers).
3. Workers run (possibly in parallel) and return results.
4. The orchestrator **synthesizes** the results into the final output, possibly
   looping to dispatch follow-up subtasks.

## When to use it

- The subtasks **can't be predicted** ahead of time.
- The work benefits from a "lead" that maintains the big picture while
  "specialists" go deep.
- Examples: multi-file code changes, research that spawns sub-questions, complex
  report generation.

## Pitfalls

- **Cost & latency** are the highest of the workflow patterns — a planning call,
  k worker calls, and a synthesis call, sometimes looped.
- **Plan quality is everything** — a bad decomposition can't be rescued by good
  workers. Invest in the orchestrator prompt.
- **Coordination overhead** — passing the right context to each worker, and the
  right results back, is the hard engineering.
- Cap the number of workers/iterations to bound cost.

## Orchestrator–workers vs. autonomous agent

This pattern still has a clear two-phase shape (plan → delegate → synthesize)
that *your* code coordinates. The [Autonomous Agent](07-autonomous-agent.md)
dissolves even that structure into a single open-ended loop. Orchestrator is the
"controlled" version of dynamic delegation.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Orchestrator | an `LlmAgent` whose tools/sub-agents are the workers | an `Agent` whose `@tool`s are themselves agents ("agents as tools") |
| Workers | `AgentTool(worker_agent)` or sub-agents | agent-wrapping functions, or a `GraphBuilder`/`Swarm` |
| Synthesis | the orchestrator's final turn | the orchestrator agent's final response |

See [`patterns/google-adk/05-orchestrator-workers/`](../../patterns/google-adk/05-orchestrator-workers/)
and [`patterns/amazon-strands/05-orchestrator-workers/`](../../patterns/amazon-strands/05-orchestrator-workers/).

---

*Workflow pattern with dynamic delegation. See Anthropic's "orchestrator-workers."*
