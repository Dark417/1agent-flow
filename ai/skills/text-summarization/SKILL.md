---
name: text-summarization
description: Use to condense long text into a faithful, well-structured summary at a requested length or reading level. Use when the goal is compression without distortion, not analysis or opinion.
---

# Text Summarization

Condense source text into a shorter version that preserves meaning, proportion,
and key facts.

## When to use

- The input is **longer than needed** for the downstream consumer.
- Faithfulness matters more than commentary.

## Procedure

1. **Read fully** before writing. Identify the thesis and the supporting points.
2. **Preserve proportion** — give weight to ideas in line with the source, not
   your interests.
3. **Compress** to the requested length (default: ~15% of the original).
4. **Preserve key entities, numbers, and caveats** exactly.
5. **Do not add** information, opinion, or interpretation not in the source.

## Parameters (infer from the request if unstated)

- `length`: target size (words, %, or "one paragraph"). Default ~15%.
- `style`: bullets vs. prose. Default: prose, unless the source is list-like.
- `audience`: reading level / domain. Default: general professional.

## Output format

A title line, then the summary. If `style=bullets`, 3–7 bullets ordered by
importance.

## Guardrails

- No hallucinated facts or numbers — if it's not in the source, it's not in the
  summary.
- Keep the original's stance; don't soften or sharpen claims.
- Note explicitly if the source is ambiguous or self-contradictory.
