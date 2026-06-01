# 01 — Augmented LLM (Tool Use)

The atom that every other pattern is built from: a single LLM enhanced with
**tools**, **retrieval**, and **memory**.

## The idea

A plain LLM can only produce text from its training. An *augmented* LLM can also
**act** — call functions you give it — and **observe** the results, looping until
it can answer. The model itself decides *which* tool to call and *with what
arguments*; your job is to provide good tools and clear descriptions.

```
                          ┌─────────────────────────────┐
   user query  ─────────► │            LLM              │
                          │   "I should call search()"  │
                          └───────────────┬─────────────┘
                                          │ tool call: search("…")
                                          ▼
                                   ┌──────────────┐
                                   │    Tool      │  (your code / an API)
                                   └──────┬───────┘
                                          │ result
                          ┌───────────────▼─────────────┐
                          │            LLM              │ ──► final answer
                          │  "Given the result, answer" │
                          └─────────────────────────────┘
```

## How it works (the loop)

1. The model receives the query **plus a list of tool definitions** (name,
   description, parameter schema).
2. It either answers directly, or emits a **tool call** (structured JSON).
3. The framework runs the tool and feeds the **result** back to the model.
4. Repeat until the model produces a final text answer.

This reason→act→observe loop is also the engine of the
[Autonomous Agent](07-autonomous-agent.md); the difference is only how much
freedom you give it.

## Designing good tools

The model is only as capable as your tools are *legible*:

- **Name** tools by what they do (`get_weather`, not `tool1`).
- **Describe** them in plain language — this is prompt-engineering, the
  description is what the model reasons over.
- **Type** every parameter and document it. Schemas reduce malformed calls.
- **Keep them focused.** One tool, one job.
- **Return useful errors.** "City not found, try a country code" beats a stack
  trace — the model can recover from a good error message.

## When to use it

Always — it's the baseline. Reach for it the moment a task needs information or
actions the model can't produce from memory: live data, math it shouldn't do in
its head, calls to your systems.

## Pitfalls

- **Too many tools** confuse the model. If you have dozens, you probably want
  [Routing](03-routing.md) or [Orchestrator–Workers](05-orchestrator-workers.md).
- **Unbounded loops** — always cap how many tool round-trips are allowed.
- **Tool output bloat** — huge results blow your context window; summarize or
  paginate.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Agent | `LlmAgent(model=…, tools=[…])` | `Agent(model=…, tools=[…])` |
| A tool | a plain typed function with a docstring | a function decorated with `@tool` |
| The loop | handled by the `Runner` | handled by the `Agent` event loop |

See [`patterns/google-adk/01-tool-use/`](../../patterns/google-adk/01-tool-use/)
and [`patterns/amazon-strands/01-tool-use/`](../../patterns/amazon-strands/01-tool-use/).

---

*Foundational pattern — see also Anthropic's "augmented LLM," the ReAct paper
(Yao et al.), and the function-calling docs of both SDKs.*
