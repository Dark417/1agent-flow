# 00 — Agentic Workflow Overview

This document gives you the mental model that the rest of the design docs build
on. Read it once; refer back to it whenever a pattern feels arbitrary.

## 1. What problem are agents solving?

A bare LLM call is a pure function: text in, text out. That's powerful but
limited — it can't look anything up, can't take actions in the world, can't
break a hard problem into steps, and can't check its own work.

**Agentic systems** wrap one or more LLM calls in *structure* — tools, memory,
control flow, and feedback — so the system can tackle tasks a single call can't.
The design patterns in this repo are the recurring shapes that structure takes.

## 2. The two big categories

> **Workflow** — LLMs and tools orchestrated through **predefined code paths**.
> **Agent** — the **LLM dynamically directs** its own process and tool use.

Think of it as a spectrum of *who holds the control flow*:

```
  Less autonomy / more predictable                More autonomy / more flexible
  <------------------------------------------------------------------------->
  Single call → Prompt Chaining → Routing → Parallelization → Orchestrator → Autonomous
                |___________ workflows (you write the flow) ___________|  |__ agent __|
```

Rule of thumb: **start at the left.** Add autonomy only when the task genuinely
needs it. More autonomy means more capability *and* more cost, latency, and
unpredictability.

## 3. The foundational building block

Every pattern is built from the **Augmented LLM** (pattern 01): a model enhanced
with three capabilities.

```
                +-------------------+
   input  --->  |   Augmented LLM   |  ---> output
                |                   |
                |  • Tools (act)    |
                |  • Retrieval      |
                |  • Memory         |
                +-------------------+
```

- **Tools** let the model *do* things (search, calculate, call APIs).
- **Retrieval** lets the model *pull in* relevant external knowledge.
- **Memory** lets the model *carry state* across steps.

Once you have this atom, the patterns are just different ways of *composing*
multiple augmented LLMs.

## 4. The pattern catalog at a glance

| Pattern | Shape | Control flow lives in | Use when |
| --- | --- | --- | --- |
| **Prompt Chaining** | A → B → C | Your code (fixed) | The task cleanly splits into ordered subtasks. |
| **Routing** | classify → {A \| B \| C} | Your code (branch) | Distinct input categories need different handling. |
| **Parallelization** | split → [A, B, C] → merge | Your code (fan-out/in) | Subtasks are independent, or you want multiple votes. |
| **Orchestrator–Workers** | lead plans → delegates → synthesizes | The orchestrator LLM | Subtasks can't be known in advance. |
| **Evaluator–Optimizer** | generate ↔ critique (loop) | Your code (loop) | You have clear quality criteria and iteration helps. |
| **Autonomous Agent** | reason → act → observe (loop) | The agent LLM | Open-ended tasks with unpredictable step counts. |

## 5. How to choose

Ask, in order:

1. **Can one good prompt do it?** → Just call the model. Don't build an agent.
2. **Is the flow fixed and known?** → Use a *workflow* (chaining / routing /
   parallelization).
3. **Must the system decide steps at runtime?** → Use *orchestrator–workers* or
   an *autonomous agent*.
4. **Do you have measurable quality criteria?** → Wrap the above in an
   *evaluator–optimizer* loop.

## 6. Cross-cutting concerns (true for every pattern)

- **Cost & latency** scale with the number of LLM calls. Every arrow in a
  diagram is money and milliseconds.
- **Observability** — log each step's input/output. Agents fail silently
  otherwise.
- **Guardrails** — validate tool inputs/outputs; cap loop iterations; set
  budgets. (Notice every loop pattern in this repo has a `max_iterations`.)
- **Error handling** — a step *will* fail. Decide: retry, route to a fallback,
  or surface to a human.
- **Stateless vs. stateful** — workflows are mostly stateless between runs;
  agents accumulate state (memory) that you must manage.

## 7. How this maps to the two SDKs

| Concept | Google ADK | Amazon Strands |
| --- | --- | --- |
| One augmented LLM | `LlmAgent` | `Agent` |
| Fixed sequence | `SequentialAgent` | call agents in order in Python |
| Fan-out | `ParallelAgent` | `concurrent.futures` / `Swarm` |
| Loop | `LoopAgent(max_iterations=…)` | a `while` loop in Python |
| Delegation | sub-agents / `AgentTool` | agents-as-tools / `GraphBuilder` / `Swarm` |
| A tool | a typed Python function | a `@tool`-decorated function |

The patterns are identical; only the spelling changes. That's the whole point of
this repo.

---

*Synthesized from Anthropic's "Building Effective Agents," Google ADK docs, and
Amazon Strands Agents docs.*
