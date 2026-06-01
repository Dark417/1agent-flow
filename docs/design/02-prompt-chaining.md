# 02 — Prompt Chaining

Decompose a task into a **fixed sequence** of LLM calls, where each step's output
feeds the next.

## The idea

Some tasks are hard to do well in one shot but easy as a series of smaller steps.
Prompt chaining hard-codes that sequence: step 1 produces something, step 2
refines or transforms it, step 3 finalizes it. *You* own the control flow — the
order is decided in advance, in code.

```
  input ──► [ Step A ]──► [ Step B ]──► [ Step C ]──► output
              outline       draft         polish
                 │
                 ▼ (optional)
            ┌──────────┐   gate fails → stop / fix
            │   gate   │   gate passes → continue
            └──────────┘
```

A common refinement is a **gate** (a programmatic or LLM check) between steps —
if the intermediate result is bad, bail early instead of compounding the error.

## How it works

1. Define N prompts, each doing one transformation.
2. Run them in order, passing output → input.
3. Optionally insert validation gates between steps.

Example used in this repo: **write a short article** as
`topic → outline → draft → polished draft`.

## When to use it

- The task **cleanly decomposes** into ordered subtasks.
- Each subtask is easier/more reliable than doing everything at once.
- You're willing to **trade latency for accuracy** (more calls, better result).

Classic uses: generate-then-translate, outline-then-write, extract-then-format,
draft-then-check-against-rules.

## When *not* to use it

If the steps aren't truly sequential, or which step comes next depends on the
content, you want [Routing](03-routing.md) or an
[Orchestrator](05-orchestrator-workers.md) instead.

## Pitfalls

- **Error propagation** — a weak early step poisons everything downstream. Add
  gates.
- **Latency** — N steps means N round-trips. Don't over-decompose.
- **Lost context** — make sure each step gets *enough* of the prior output, not
  a lossy summary, unless lossiness is intended.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Mechanism | `SequentialAgent(sub_agents=[a, b, c])` | call `agent_a()`, then `agent_b(...)`, then `agent_c(...)` |
| Passing state | each `LlmAgent` writes to an `output_key` in shared session state | pass the previous `result` string into the next call |

Google gives you a first-class `SequentialAgent`; in Strands the "chain" is just
ordinary Python sequencing, which makes the data flow very explicit.

See [`patterns/google-adk/02-prompt-chaining/`](../../patterns/google-adk/02-prompt-chaining/)
and [`patterns/amazon-strands/02-prompt-chaining/`](../../patterns/amazon-strands/02-prompt-chaining/).

---

*Workflow pattern. See Anthropic's "prompt chaining."*
