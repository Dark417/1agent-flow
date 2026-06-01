---
name: web-research
description: Use when a task needs current, factual information from external sources — gathering, cross-checking, and citing findings on a topic. Not for tasks answerable from the model's own knowledge.
---

# Web Research

A skill for gathering reliable, current information and reporting it with
sources.

## When to use

- The question depends on **recent or factual** information the model can't be
  sure of.
- The answer should be **citable** and **verifiable**.

## Procedure

1. **Decompose** the question into 2–5 concrete sub-questions.
2. For each sub-question, **search** and collect the most relevant, credible
   sources.
3. **Cross-check** any claim that matters across at least two independent
   sources. Flag disagreements rather than hiding them.
4. **Extract** the specific facts that answer the question; discard the rest.
5. **Report** findings as concise bullets, each with its source.

## Output format

```
Finding: <one-sentence claim>
Source:  <url or title>
Confidence: high | medium | low
```

End with a short synthesis paragraph and an explicit list of anything that could
not be verified.

## Guardrails

- Never invent a source or a URL. If you can't verify a claim, say so.
- Prefer primary sources over aggregators.
- Distinguish *facts* from *opinions* and from your own *inference*.
