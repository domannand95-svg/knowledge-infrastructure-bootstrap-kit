---
document_id: MD-001
version: 1.0
status: Normative Specification (Frozen for Initial Pilot)
last_revised: 2026-08-08
scope: Repository-wide structural Markdown standardization for the Knowledge Infrastructure Bootstrap Kit (BKI-001).
---

# MD-001 — Repository Markdown Style Guide

## 1. Purpose and Scope

This document establishes the normative structural rules and allowable transformation boundaries for all Markdown files within the repository. It serves as the authoritative contract for human contributors, transformer-based normalization proposals, and automated validation layers.

## 2. Normative Rules for Document Structure

### 2.1. Frontmatter Schema

Every repository document must begin with a valid YAML frontmatter block enclosed by triple dashes (`---`). To ensure deterministic parsing across tooling, all metadata keys must use snake_case identifiers without spaces.

- **Required Keys:** `document_id`, `version`, `status`, `last_revised`.
- **Rule:** Frontmatter must begin on line 1 of the file. Exactly one blank line must separate the closing frontmatter delimiter (`---`) from the primary document title.

### 2.2. Heading Hierarchy and Syntax

- **Single H1:** Each document must contain exactly one H1 heading (`#`) representing the primary document title, placed directly after the required blank line following the YAML frontmatter.
- **Sequential Nesting:** Headings must scale sequentially (H1 through H6: `#`, `##`, `###`, `####`, `#####`, `######`). Skipping heading levels (e.g., jumping from an H2 directly to an H4) is strictly prohibited.
- **Heading Normalization Authority:** A visually styled standalone line (e.g., text enclosed in bold markers `**...**` or capitalized on its own line) may only be proposed for conversion to an explicit Markdown heading (`## ...`) if it satisfies **all** of the following conditions:
  1. It appears on its own line surrounded by blank lines.
  2. It functions structurally as a section boundary or chapter title.
  3. It contains no inline code fences, links, or trailing punctuation characteristic of running prose (such as terminal periods).
  4. It is not part of a list item, table cell, or blockquote.

**Note on Authority:** Transformer identification of a logical section boundary constitutes a normalization proposal only. It does not constitute validation evidence. The validator MUST independently verify all mechanically testable eligibility conditions and MUST reject transformations outside the authorized classes defined in Section 3.2.

### 2.3. Inline and Block Elements

- **Code Blocks:** Code fences must use triple backticks with an optional language identifier. Unclosed or mismatched code fences are non-compliant.
- **Lists and Tables:** Lists must use consistent markers (`*`, `-`, or numbered lists) with standard GFM indentation. Tables must maintain valid pipe (`|`) and hyphen (`-`) alignment.
- **Links and Citations:** Inline references, footnotes, and citation keys must be preserved character-for-character.

### 2.4. Special-Purpose Exclusions

Files matching any of the following criteria are **exempt** from standard YAML frontmatter and strict H1 requirements, but must still comply with general Markdown syntax:

- Root-level `README.md` files.
- Explicitly designated templates (`*.template.md`).
- Vendored material or external reference documents imported without modification.
- Automated changelogs and build logs.

## 3. Validator Compliance Specification: Authorized Transformation Invariant

The validation layer does not rely on heuristic character stripping or fuzzy token matching. Instead, validation operates on a **Strict Authorized Transformation** model.

### 3.1. The Invariant Principle

> **The normalized document may differ from the source exclusively through transformations explicitly authorized by MD-001.**

Any byte-level or structural difference that cannot be classified under an explicitly permitted transformation category results in an immediate validation **FAIL** and routes the document to quarantine.

### 3.2. Permitted Transformation Classes

During a normalization run, the validator checks every delta against the following allowed categories:

1. **Heading Syntax Injection:** Addition of Markdown heading markers (`#` through `######`) and corresponding adjustments to whitespace immediately preceding or following the heading, provided the text string matches an authorized heading candidate under Section 2.2.
2. **Visual Styling Removal:** Stripping of bold (`**`) or italic (`*`, `_`) markers strictly from lines identified and converted to explicit headings under Section 2.2.
3. **Whitespace Normalization:** Elimination of trailing whitespace, harmonization of line endings (LF), and normalization of blank lines bounded strictly to Markdown structural boundaries (excluding fenced code contents and raw block interiors).
4. **Metadata Key Standardization:** Migration of legacy spaced YAML keys to standard snake_case keys (`document_id`, etc.) *only* when explicitly flagged as a permitted migration task.

### 3.3. Prohibited Transformations (Automatic Failures)

The following deltas will trigger an immediate validation failure:

- Any modification, addition, deletion, or reordering of substantive prose words, numbers, or symbols.
- Alteration of code block contents, inline code, URLs, citation keys, or table data.
- Changes to YAML metadata values (as opposed to key formatting).
- Skipping heading levels or generating multiple H1 headings.

### 3.4. Validation Outcomes

Each processed document must receive exactly one deterministic outcome:

- **PASS — COMPLIANT:** The source document already satisfies MD-001. No transformation is required.
- **PASS — NORMALIZED:** The source was non-compliant, all resulting deltas belong exclusively to permitted transformation classes, and the output satisfies MD-001.
- **FAIL — QUARANTINE:** The proposed output contains one or more unauthorized transformations, ambiguous structural changes, malformed Markdown/YAML, or other conditions preventing deterministic verification.