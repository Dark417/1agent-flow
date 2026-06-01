# 02 — Prompt Chaining (Amazon Strands)

`topic → outline → draft → polished article`, expressed as plain Python that
calls three agents in order.

- **Design doc:** [`docs/design/02-prompt-chaining.md`](../../../docs/design/02-prompt-chaining.md)
- **Strands approach:** no special construct — `str(agent_a(...))` feeds
  `agent_b(...)`. The chain *is* the Python.

## Run

```bash
python patterns/amazon-strands/02-prompt-chaining/agent.py
```

## What to watch

Compare with the Google version's `SequentialAgent`. Here the hand-off between
steps is visible as ordinary function calls — useful for understanding exactly
what data each step receives.
