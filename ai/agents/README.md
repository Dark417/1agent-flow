# ai/agents

**Agent definitions** — each file describes one agent's role: who it is, when to
use it, and how it should behave. They use the subagent frontmatter format: YAML
frontmatter (`name`, `description`, and optional `tools`/`model`) followed by the
system prompt.

```
ai/agents/
├── researcher.md   gathers and verifies information
├── writer.md       turns material into clear prose
├── reviewer.md     critiques against criteria (the "evaluator")
└── router.md       classifies a request and picks a specialist
```

## How these map to the patterns

These roles are deliberately the same characters that appear in the
[design patterns](../../docs/design/) and the runnable examples:

- **researcher** → a worker in [Orchestrator–Workers](../../docs/design/05-orchestrator-workers.md).
- **writer** → a step in [Prompt Chaining](../../docs/design/02-prompt-chaining.md).
- **reviewer** → the evaluator in [Evaluator–Optimizer](../../docs/design/06-evaluator-optimizer.md).
- **router** → the classifier in [Routing](../../docs/design/03-routing.md).

## Frontmatter fields

| Field | Meaning |
| --- | --- |
| `name` | lowercase, hyphenated identifier (matches the filename). |
| `description` | when to invoke this agent — written for an orchestrator to read. |
| `tools` | optional: which tools/skills this agent may use. |
| `model` | optional: a hint for which model tier fits the role. |
