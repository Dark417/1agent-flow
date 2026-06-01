# 07 — Autonomous Agent

A single LLM driving an open-ended **reason → act → observe** loop, deciding its
own steps until the task is done.

## The idea

All the previous patterns keep the control flow in *your* hands — you decided the
sequence, the branches, the fan-out, the loop condition. An **autonomous agent**
hands the control flow to the model. You give it a goal and a set of tools; it
plans, acts, observes the result, re-plans, and continues — for as many steps as
it judges necessary.

```
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
   ┌─────────┐   tool call   ┌──────────┐  result      │
   │  Reason │ ────────────► │   Act    │ ───────┐     │
   │ (LLM)   │ ◄──────────── │ (tool)   │        │     │
   └─────────┘   observe     └──────────┘        │     │
        │                                        │     │
        │  "task complete" ──► final answer      └─────┘
        ▼                                     (loop until done
     output                                   or budget hit)
```

This is the **ReAct** loop (Reason + Act) scaled up: the same augmented-LLM
mechanism from [pattern 01](01-augmented-llm-tool-use.md), but trusted to run
many iterations and decide for itself when to stop.

## How it works

1. The agent gets a **goal** and a toolbox.
2. It **reasons** about the next step and **acts** (calls a tool).
3. It **observes** the result, updates its understanding, and decides whether to
   continue.
4. It stops when it believes the goal is met — or when a **guardrail** stops it.

## When to use it

- The task is **open-ended** and the number/order of steps **can't be known in
  advance**.
- The environment gives **reliable feedback** (tool results the agent can learn
  from).
- You can tolerate higher latency, cost, and variance in exchange for
  flexibility.

Examples: "investigate why this build is failing and fix it," "research this
topic and produce a brief," coding agents that edit-run-test-repeat.

## Why it's last (and used least)

Autonomy is powerful but expensive and unpredictable. **Most production value
comes from the simpler workflow patterns.** Reach for a fully autonomous agent
only when a workflow genuinely can't express the task. Anthropic's guidance is
blunt: find the simplest solution possible, and only increase complexity when it
demonstrably improves outcomes.

## Guardrails are mandatory

Because the model controls the loop, *you* control the limits:

- **Iteration / step cap** — never let it run forever.
- **Budget cap** — token and dollar ceilings.
- **Tool sandboxing** — least-privilege tools; validate every argument.
- **Human-in-the-loop** — checkpoints for irreversible or costly actions.
- **Observability** — log every reason/act/observe step for debugging and trust.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Form | a single `LlmAgent` with a rich toolset; the `Runner` drives the loop | a single `Agent` with `@tool`s; the built-in event loop drives it |
| Stopping | the model stops calling tools / `max` limits | the agent stops when it has a final answer / capped |

Both SDKs make the *simple* case look almost identical to pattern 01 — the
difference is conceptual: you've given the agent a harder, open-ended goal and a
broader toolbox, and you trust the loop.

See [`patterns/google-adk/07-autonomous-agent/`](../../patterns/google-adk/07-autonomous-agent/)
and [`patterns/amazon-strands/07-autonomous-agent/`](../../patterns/amazon-strands/07-autonomous-agent/).

---

*The "autonomous agent" end of the spectrum. See Anthropic's "agents" section and
the ReAct paper (Yao et al., 2022).*
