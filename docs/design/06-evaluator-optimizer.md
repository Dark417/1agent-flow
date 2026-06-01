# 06 — Evaluator–Optimizer

One LLM **generates** a candidate; another **evaluates** it and returns feedback;
the generator **revises**. Loop until it passes (or you hit a limit).

## The idea

People rarely produce their best work in one pass — they draft, get feedback, and
revise. This pattern gives an LLM the same loop. A **generator** produces output;
an **evaluator** (often a different prompt, sometimes a different model) judges it
against explicit criteria and says what to fix; the generator tries again with
that feedback.

```
                  ┌───────────────┐
   task ───────►  │   Generator   │ ─── candidate ──►┐
            ┌───► │  (optimizer)  │                  │
            │     └───────────────┘                  ▼
            │                              ┌───────────────────┐
            │  feedback ("not yet, fix X") │     Evaluator     │
            └──────────────────────────────┤  PASS? ──► output │
                                           └───────────────────┘
                          (loop, capped at max_iterations)
```

This is the close cousin of **Reflection** — the special case where the generator
evaluates *itself*. Splitting generator and evaluator into separate roles usually
gives sharper critiques because the evaluator isn't defending its own work.

## How it works

1. **Generate** an initial candidate.
2. **Evaluate** it against criteria → a verdict (`PASS`/`FAIL`) plus specific,
   actionable feedback.
3. If `PASS` or the iteration cap is hit, return. Otherwise feed the feedback
   back to the generator and **regenerate**.

## When to use it

- You have **clear evaluation criteria** (a rubric, a spec, tests, a style
  guide).
- **Iterative refinement measurably helps** — the first draft is rarely the
  best.
- The evaluator can articulate *why* something fails, not just *that* it fails.

Classic uses: literary translation (nuance the first pass misses), code that must
satisfy tests, content that must meet a rubric, search that must reach a coverage
bar.

## Pitfalls

- **No exit condition** = infinite loop and runaway cost. **Always** set
  `max_iterations`.
- **Vague feedback** doesn't help the generator. The evaluator prompt must demand
  *specific, actionable* critiques.
- **Diminishing returns** — quality often plateaus after 2–3 rounds.
- If your criteria can be checked in code (e.g. tests pass), prefer a
  deterministic gate over an LLM evaluator where possible.

## In the two SDKs

| | Google ADK | Amazon Strands |
| --- | --- | --- |
| Loop | `LoopAgent(sub_agents=[generator, evaluator], max_iterations=N)` | a Python `for`/`while` loop, capped |
| Exit early | evaluator escalates / sets a state flag to stop the loop | check the evaluator's verdict; `break` on PASS |

Google's `LoopAgent` makes the loop a first-class construct; the Strands version
shows the loop as explicit Python so the stopping logic is obvious.

See [`patterns/google-adk/06-evaluator-optimizer/`](../../patterns/google-adk/06-evaluator-optimizer/)
and [`patterns/amazon-strands/06-evaluator-optimizer/`](../../patterns/amazon-strands/06-evaluator-optimizer/).

---

*Workflow pattern. See Anthropic's "evaluator-optimizer" and the broader
"reflection" literature.*
