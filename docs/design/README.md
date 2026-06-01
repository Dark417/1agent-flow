# Design Documents — Agentic Workflow Patterns

These documents explain the design patterns used to build AI agent systems.
They are framework-agnostic: read them first, then look at the Google ADK and
Amazon Strands implementations under [`../../patterns/`](../../patterns/) to see
each pattern in code.

## Reading order

| # | Document | One-line idea |
| --- | --- | --- |
| 00 | [Agentic Workflow Overview](00-agentic-workflow-overview.md) | The map: workflows vs. agents, and how the patterns relate. |
| 01 | [Augmented LLM / Tool Use](01-augmented-llm-tool-use.md) | An LLM that can call tools, retrieve, and remember — the atom of every agent. |
| 02 | [Prompt Chaining](02-prompt-chaining.md) | Break a task into a fixed sequence of LLM steps. |
| 03 | [Routing](03-routing.md) | Classify the input, then send it to a specialist. |
| 04 | [Parallelization](04-parallelization.md) | Run subtasks at the same time (sectioning) or in competition (voting). |
| 05 | [Orchestrator–Workers](05-orchestrator-workers.md) | A lead agent plans dynamically and delegates to workers. |
| 06 | [Evaluator–Optimizer](06-evaluator-optimizer.md) | Generate, critique, and refine in a loop. |
| 07 | [Autonomous Agent](07-autonomous-agent.md) | An open-ended reason→act→observe loop that decides its own steps. |

## Key distinction: workflow vs. agent

- A **workflow** is a system where LLMs and tools are orchestrated through
  **predefined code paths**. *You* decide the control flow in advance.
- An **agent** is a system where the **LLM decides** its own control flow and
  tool usage dynamically at runtime.

Patterns 02–04 are firmly *workflows*. Patterns 05–07 give progressively more
control to the model. **Prefer the simplest thing that works** — most production
value comes from well-built workflows, not maximally autonomous agents.

## Credits / further reading

These patterns are synthesized from widely used industry references, including
Anthropic's *Building Effective Agents*, Google's *Agent Development Kit*
documentation, and Amazon's *Strands Agents* documentation. See each document's
footer for specifics.
