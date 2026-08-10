---
document_id: MD-001-VH-001
version: 1.0
status: Commissioning Decision
last_revised: 2026-08-10
---

# MD-001 Visual Heading Conversion Decision

## Decision

Retain the MD-001 authority to convert narrowly defined bold or italic visual headings into explicit Markdown headings.

## Eligible Source Forms

The complete trimmed source line must match exactly one form:

```text
**Title**
*Title*
_Title_
```

The line must also:

1. be surrounded by blank lines;
2. function as the complete proposed section boundary;
3. preserve identical title text in the candidate;
4. contain no terminal prose punctuation;
5. not be a list item, table cell, blockquote, link or code element; and
6. produce a candidate that passes H1-count and sequential-nesting checks.

## Explicit Exclusions

Inline emphasis, list markers, unmatched delimiters, nested emphasis, identifiers containing underscores, and emphasized sentences ending in prose punctuation are not eligible.

## Classification

An accepted conversion produces two classification events for the same body line:

```text
VISUAL_STYLING_REMOVAL
HEADING_SYNTAX_INJECTION
```

Any ambiguity fails closed. This decision does not authorize a transformer, heuristic heading generation, or repository write-back.
