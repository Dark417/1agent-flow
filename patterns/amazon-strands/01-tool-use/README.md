# 01 — Tool Use (Amazon Strands)

The foundational pattern: one Strands `Agent` with two `@tool` functions. The
model chooses when to call `calculate` and `get_population`, observes the
results, and answers.

- **Design doc:** [`docs/design/01-augmented-llm-tool-use.md`](../../../docs/design/01-augmented-llm-tool-use.md)
- **Strands construct:** `Agent(tools=[...])`; a tool is a `@tool`-decorated
  function.

## Run

```bash
python patterns/amazon-strands/01-tool-use/agent.py
```

## What to watch

The agent should call the population tool twice and the calculator once, rather
than guessing the sum. Compare with the Google version — same pattern, the only
difference is `@tool` vs. a bare function and `Agent` vs. `LlmAgent`.
