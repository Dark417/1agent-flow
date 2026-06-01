# ai/skills

**Skills** are reusable, self-contained capabilities an agent can load when it's
relevant. Each skill lives in its own folder with a `SKILL.md` file that begins
with YAML frontmatter (`name`, `description`) followed by instructions.

This is the [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
format: the `description` is what an agent reads to decide *whether* to use the
skill; the body is what it reads *once it decides to*.

```
ai/skills/
├── web-research/
│   └── SKILL.md
└── text-summarization/
    └── SKILL.md
```

## How skills relate to the patterns

Skills are the *capabilities*; the [patterns](../../docs/design/) are the *control
flow* that composes them. For example, the
[Orchestrator–Workers](../../docs/design/05-orchestrator-workers.md) pattern might
have workers that each use the **web-research** skill, and a final step that uses
**text-summarization**.

## Authoring a skill

1. `name`: lowercase, hyphenated, matches the folder.
2. `description`: one or two sentences, written so an agent can decide when to
   invoke it. Lead with *when to use it*.
3. Body: concrete, step-by-step instructions and constraints.
