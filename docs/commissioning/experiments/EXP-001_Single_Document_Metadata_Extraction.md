# Experiment Record: Single Document Metadata Extraction (`EXP-001`)

| Property | Value |
| --- | --- |
| **Experiment ID** | EXP-001 |
| **Version** | 1.0 |
| **Status** | Completed |
| **Document Owner** | @domannand95 |
| **Effective Date** | 2026-08-08 |

> **Objective**
> Determine whether the local inference engine (Mistral/Ollama) can reliably extract structured metadata from a single Markdown repository document prior to repository lineage comparison.

---

# Background

Following regression tests TC-01 and TC-02, DF-001 identified unreliable behaviour when comparing complete Markdown repository documents directly.

This experiment evaluates whether separating document extraction from document comparison provides a more reliable workflow.

---

# Experimental Method

A single repository document (`BKI-003` v1.2) was supplied to the local model.

The model was instructed to extract structured metadata only.

No comparison task was performed.

Requested extraction included:

- Document ID
- Version
- Status
- Owner
- Effective Date
- Purpose
- Primary Module
- Section Headings
- Revision History
- Design Principle

---

# Results

Observed behaviour:

- Successfully extracted Document ID.
- Successfully extracted Version.
- Successfully extracted Status.
- Successfully extracted Document Owner.
- Successfully extracted Effective Date.
- Successfully extracted Purpose.
- Successfully extracted Section Headings.
- Successfully extracted Design Principle.
- Successfully recognised document structure.

Observed limitations:

- Primary Module returned "Not Found."
- Revision History extraction was inconsistent during early runs before prompt refinement.

---

# Outcome

The experiment demonstrated that structured metadata extraction from a single Markdown document is substantially more reliable than direct comparison of two complete repository documents within a single prompt.

The extracted profile provides a compact representation that may be suitable for downstream comparison workflows.

---

# Conclusion

**Result:** PASS

The tested local model can reliably perform single-document metadata extraction under the evaluated workflow.

This establishes metadata extraction as a viable preprocessing stage for subsequent lineage analysis experiments.

---

# Follow-on Experiment

Proceed to:

**EXP-002 — Metadata Profile Comparison**

Evaluate whether two extracted metadata profiles can be compared more reliably than their original full Markdown documents.

---

# Related Documents

- DF-001 — Document Length & Attention Degradation
- ECP-002 v0.7
- TC-01 — Divergent Same-Identifier
- TC-02 — Exact Duplicate