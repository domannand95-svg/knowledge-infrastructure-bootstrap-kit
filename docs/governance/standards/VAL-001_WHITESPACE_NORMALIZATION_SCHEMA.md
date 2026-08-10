---
document_id: VAL-001-WS-001
version: 1.0
status: Commissioning Schema
last_revised: 2026-08-10
---

# VAL-001 Whitespace Normalization Schema

## Purpose

This schema defines the complete whitespace transformations authorized by the VAL-001 pilot. Anything not explicitly listed remains unauthorized and must fail closed.

## Authorized Source Transformations

The legacy source may be normalized in memory through:

1. UTF-8 BOM removal at the start of the file.
2. CRLF or CR line-ending conversion to LF.
3. Removal of trailing spaces and tabs outside protected regions.
4. Collapse of two or more consecutive blank lines to one outside protected regions.

Candidates must already use the canonical representation. These transformations are source-tolerance rules, not candidate repair authority.

## Protected Regions

Whitespace is never normalized inside:

- fenced code blocks;
- indented code blocks;
- GFM tables; or
- raw HTML blocks.

Typed protected values for inline code, URLs and citation keys remain invariant. Line offsets may shift when source-only blank lines are collapsed, but protected type, content, cardinality and relative order must remain unchanged.

## Explicitly Unauthorized Transformations

The validator does not authorize:

- prose reflow or wrapping;
- leading-indentation changes;
- internal word-spacing changes;
- list indentation changes;
- table alignment or padding changes;
- code-block whitespace changes;
- blank-line insertion;
- removal of the sole structural blank line between blocks; or
- candidate-side whitespace repair.

## Outcomes

A candidate containing noncanonical trailing whitespace or repeated blank lines is quarantined with `ERR_UNAUTHORIZED_DELTA`. A change inside a typed protected element is quarantined with `ERR_PROTECTED_CONTENT`.

## Safety Boundary

Normalization occurs only in the in-memory comparison representation. This schema does not authorize rewriting either input or writing any repository file.
