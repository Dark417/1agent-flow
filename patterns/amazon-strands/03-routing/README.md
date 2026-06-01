# 03 — Routing (Amazon Strands)

A `router` agent returns one label (`billing` / `technical` / `general`); Python
dispatches the message to the matching specialist.

- **Design doc:** [`docs/design/03-routing.md`](../../../docs/design/03-routing.md)
- **Strands approach:** the router is a tiny classifier agent; a dict lookup
  performs the branch (with `general` as the fallback).

## Run

```bash
python patterns/amazon-strands/03-routing/agent.py
```

## What to watch

The `[router -> …]` line shows the classification before the specialist answers.
In the Google version ADK performs the handoff automatically; here the branch is
visible in Python.
