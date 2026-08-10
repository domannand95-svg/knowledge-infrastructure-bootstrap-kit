---
document_id: DF-003
version: 1.0
status: Published Finding (Commissioning Evidence)
last_revised: 2026-08-08
---

# DF-003 — Windows UTF-8 BOM Parser Boundary

## 1. Context and Discovery

During the empirical execution of the initial commissioning test (`TC-VAL-001`), the test fixture initially failed at Stage 1 with a strict frontmatter syntax rejection (`ERR_FM_SYNTAX`), despite containing valid YAML and matching content between source and candidate.

Hexadecimal inspection of the fixture files revealed the presence of the byte sequence `EF BB BF` preceding the expected frontmatter delimiter (`---`).

## 2. Root Cause Analysis

The test fixtures were generated via automated shell operations (`PowerShell`) under a Windows environment and were written with a UTF-8 Byte Order Mark (BOM).

The frontmatter regular expression and YAML parsing pipeline expected the file stream to commence immediately with the ASCII hyphen bytes (`2D 2D 2D`).

When the fixtures were explicitly rewritten as UTF-8 without BOM, yielding starting bytes `2D 2D 2D 0A`, the exact, unchanged validator test passed without error.

## 3. Engineering Implications

This investigation established that text encoding and BOM handling represent a concrete deterministic input boundary that cannot be silently assumed by parser logic.

Real-world repositories may contain varying encoding signatures introduced by cross-platform contributor environments. Encoding behavior therefore requires explicit treatment within the normalization architecture rather than reliance on environmental defaults.

## 4. Policy Follow-Up

During the upcoming parser robustness refactoring preceding `TC-VAL-008`, the following behavior must be explicitly implemented and tested:

- **Source Ingestion:** The parser must either transparently strip leading UTF-8 BOM signatures or enforce explicit error routing, determining whether BOM-bearing legacy sources are accepted/read-normalized or rejected by policy.
- **Candidate Compliance:** Candidate output files must remain strictly conforming to UTF-8 without BOM under `MD-001` standards.

## 5. Commissioning Evidence

The observed execution sequence was:

1. `TC-VAL-001` executed against byte-identical source and candidate fixtures.
2. Validation returned `FAIL — QUARANTINE` with `ERR_FM_SYNTAX`.
3. Hexadecimal inspection identified leading bytes `EF BB BF 2D 2D 2D`.
4. Source and candidate fixtures were rewritten as UTF-8 without BOM without altering their substantive contents.
5. Hexadecimal inspection confirmed the new opening sequence `2D 2D 2D 0A`.
6. `TC-VAL-001` was rerun against the unchanged validator implementation.
7. The test returned `PASS`.

## 6. Finding

`TC-VAL-001` demonstrated that deterministic Markdown validation requires an explicit encoding contract.

The failure was attributable to an unspecified input-encoding boundary rather than invalid Markdown content or a substantive validation error.

BOM handling and line-ending behavior must therefore be addressed explicitly during parser robustness implementation before broader normalization commissioning proceeds.