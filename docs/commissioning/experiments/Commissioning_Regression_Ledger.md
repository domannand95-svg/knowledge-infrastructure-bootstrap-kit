# Commissioning Regression Ledger

| Property | Value |
| --- | --- |
| Framework | Knowledge Infrastructure Bootstrap Kit v1.x (BKI-001 v1.2) |
| Operational Phase | Active Commissioning |
| Specification | ECP-002 v0.7 |
| Status | Feature Frozen |
| Purpose | Record empirical commissioning results without modifying frozen specifications. |

---

## TC-01 — Divergent Same-Identifier

**Date:** 2026-08-08

**Expected**

- Detection: PASS
- Resolution: INCONCLUSIVE
- Conflict: Yes

**Observed**

Model classified conflicting documents as identical.

**Result**

FAIL

**Evidence**

- Raw output saved.
- Refer to DF-001.

---

## TC-02 — Exact Duplicate

**Date:** 2026-08-08

**Expected**

- Exact Duplicate

**Observed**

Model failed to classify identical documents as duplicates using the required workflow.

**Result**

FAIL

**Evidence**

- Raw output saved.
- Refer to DF-001.

---

## EXP-01 — Metadata Extraction

**Purpose**

Determine whether Mistral can reliably extract structured metadata from a single Markdown document.

**Result**

PASS

**Observations**

- Document ID extracted.
- Version extracted.
- Status extracted.
- Section headings extracted.
- Revision history extracted (one run more complete than another).

---

## EXP-02 — Metadata Profile Comparison

**Purpose**

Compare extracted profiles rather than full Markdown documents.

**Result**

PARTIAL

**Observed**

The model recognised that Profile B contained revision history, but still classified the profiles as Exact Duplicate.

This indicates that extraction succeeded while comparison logic remained inconsistent.

---

## Related Findings

- DF-001 v1.0