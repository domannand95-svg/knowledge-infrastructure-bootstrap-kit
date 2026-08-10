---
document_id: VAL-001-PROTECTED-001
version: 1.0
status: Commissioning Schema
last_revised: 2026-08-10
---

# VAL-001 Protected Element Schema

## Purpose

This schema defines the typed Markdown elements whose values, cardinality, and order must remain invariant between source and candidate documents.

## Protected Types

| Type | Extraction rule |
| --- | --- |
| `CODE_BLOCK` | Content of a fenced backtick or tilde code block as parsed by Markdown-It CommonMark. |
| `INLINE_CODE` | Content of a Markdown inline-code token. |
| `TABLE` | Exact source lines covered by a GFM table token, including header and delimiter rows. |
| `URL` | Literal HTTP or HTTPS URL outside whitespace or Markdown delimiter characters; terminal prose punctuation is excluded. |
| `CITATION_KEY` | Bracketed uppercase identifier containing at least one hyphen, such as `[REF-001]`, stored without brackets. |

YAML values remain protected separately through frontmatter dictionary comparison.

## Ordering

Protected elements are ordered by zero-based body line, then column, then stable extraction sequence. Repeated parsing of identical input must produce an identical ordered sequence.

## Failure Behavior

Any difference in protected-element type, content, cardinality, or ordering produces:

```text
FAIL — QUARANTINE
ERR_PROTECTED_CONTENT
```

## Safety Boundary

Protection is validation-only. This schema does not authorize transforming, repairing, rewriting, or persisting protected content.
