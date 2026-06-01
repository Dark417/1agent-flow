# 03 — Routing (Google ADK)

A `support_router` coordinator classifies each message and hands it to the
`billing`, `technical`, or `general` specialist via ADK's automatic delegation.

- **Design doc:** [`docs/design/03-routing.md`](../../../docs/design/03-routing.md)
- **ADK construct:** an `LlmAgent` with `sub_agents=[...]`. The model emits a
  transfer to the chosen sub-agent; each specialist's `description` is what the
  router routes on.

## Run

```bash
python patterns/google-adk/03-routing/agent.py
```

## What to watch

Three different messages should reach three different specialists. The billing
message never touches the technical prompt — that separation is the whole point.
