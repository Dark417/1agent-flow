# 01 — Tool Use (Google ADK)

The foundational pattern: one `LlmAgent` with tools. The model chooses when to
call `calculate` and `get_population`, observes the results, and answers.

- **Design doc:** [`docs/design/01-augmented-llm-tool-use.md`](../../../docs/design/01-augmented-llm-tool-use.md)
- **ADK construct:** `LlmAgent(tools=[...])` — a tool is a typed Python function.

## Run

```bash
python patterns/google-adk/01-tool-use/agent.py
```

## What to watch

The agent should call `get_population("Tokyo")` and `get_population("Paris")`,
then `calculate("37400000 + 11100000")`, rather than guessing the sum. That hand-
off from reasoning to tool calls *is* the pattern.
