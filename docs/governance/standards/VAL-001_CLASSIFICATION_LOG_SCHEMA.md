---
document_id: VAL-001-LOG-001
version: 1.0
status: Commissioning Schema
last_revised: 2026-08-10
---

# VAL-001 Classification Log Schema

## Purpose

This schema defines the deterministic, human-readable classification events returned by the commissioned VAL-001 pilot. It provides an itemized explanation of accepted and rejected deltas without authorizing repository writes or new transformation classes.

## Record Format

Each event is a UTF-8 string with exactly three pipe-separated fields:

```text
STAGE|DECISION|DETAIL
```

- `STAGE` identifies the validation gate or content unit.
- `DECISION` is one of `NONE`, `AUTHORIZED`, `PRESERVED`, `REJECTED`, `COMPLIANT`, `NORMALIZED`, or `QUARANTINE`.
- `DETAIL` is a deterministic semicolon-separated sequence of lowercase keys and stable values, or a stable fixed phrase when no key/value detail is needed.

Events appear in execution order. Repeating the same validation with identical inputs must produce an identical sequence.

## Current Stages

| Stage | Meaning |
| --- | --- |
| `SOURCE_PREPARATION` | Legacy source-only preparation, including BOM removal or line-ending normalization. |
| `PARSE` | A source or candidate parse rejected before delta classification. |
| `DELTA` | Prepared source and candidate are identical. |
| `METADATA` | Metadata-key migration or metadata protection result. |
| `PROTECTED_CONTENT` | Ordered fenced-code protection result. |
| `BODY` | Whole-body comparison result. |
| `BODY_LINE` | A specific one-based line in the parsed Markdown body was classified. |
| `FINAL` | The single terminal validation outcome. |

## Terminal Event

Every result ends with exactly one terminal event:

```text
FINAL|COMPLIANT|error=NONE
FINAL|NORMALIZED|error=NONE
FINAL|QUARANTINE|error=ERR_...
```

## Safety Boundary

Classification events explain the current validator decision. They do not confer authority to transform, write, commit, publish, promote, or delete repository content.
