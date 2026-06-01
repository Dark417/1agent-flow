# 03 — Routing

**Classify** the input, then dispatch it to the specialist best suited to handle
it.

## The idea

When inputs fall into distinct categories that each deserve different handling,
trying to serve them all with one prompt makes that prompt mediocre at
everything. Routing splits the problem: a small **router** decides the category,
then hands off to a **specialist** agent tuned for exactly that case.

```
                       ┌──────────────────┐
   input ───────────►  │      Router      │  classify into one of N
                       └───────┬──────────┘
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │ Billing  │     │ Technical│     │ General  │   specialists
        │  agent   │     │  agent   │     │  agent   │
        └────┬─────┘     └────┬─────┘     └────┬─────┘
             └────────────────┼────────────────┘
                              ▼
                           output
```

## How it works

1. The **router** (an LLM classifier, or a cheap model, or even rules) maps the
   input to one of N labels.
2. Your code uses that label to select the matching specialist.
3. The specialist handles the request with a focused prompt and its own tools.

This is **separation of concerns**: each specialist prompt stays simple and
accurate because it only ever sees inputs it was designed for.

## When to use it

- Inputs have **distinct categories** with clearly different best-handling.
- A single combined prompt would be bloated or would degrade some categories.
- You want to route **easy** cases to cheap/fast models and **hard** ones to
  stronger models (cost optimization).

## Pitfalls

- **Misclassification** cascades — the best specialist can't help if it got the
  wrong input. Make routing categories distinct and add a "general/fallback"
  bucket.
- **Too many categories** become their own maintenance burden.
- Keep the router **cheap and fast** — it's on the critical path of every
  request.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Idiomatic form | a coordinator `LlmAgent` with `sub_agents=[…]`; the LLM emits a transfer to the right sub-agent | a router `Agent` returns a label; Python `if/elif` calls the chosen specialist `Agent` |
| Alternative | wrap specialists as `AgentTool`s | wrap specialists as `@tool`s (agents-as-tools) |

Google's framework can perform the handoff *for* you via automatic delegation;
the Strands example shows the routing decision explicitly in Python so you can
see the branch.

See [`patterns/google-adk/03-routing/`](../../patterns/google-adk/03-routing/)
and [`patterns/amazon-strands/03-routing/`](../../patterns/amazon-strands/03-routing/).

---

*Workflow pattern. See Anthropic's "routing."*
