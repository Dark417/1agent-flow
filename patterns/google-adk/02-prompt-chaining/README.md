# 02 — Prompt Chaining (Google ADK)

`topic → outline → draft → polished article`, as a fixed three-step
`SequentialAgent`.

- **Design doc:** [`docs/design/02-prompt-chaining.md`](../../../docs/design/02-prompt-chaining.md)
- **ADK construct:** `SequentialAgent(sub_agents=[...])`; steps pass data through
  shared state using `output_key` + `{key}` templating.

## Run

```bash
python patterns/google-adk/02-prompt-chaining/agent.py
```

## What to watch

Three LLM calls happen in order. Each step only does one job, which is what makes
the final result more reliable than asking for a polished article in one shot.
