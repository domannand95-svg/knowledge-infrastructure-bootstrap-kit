# Experiment Record: Heading Structure Comparison (`EXP-003`)

| Property | Value |
| --- | --- |
| **Experiment ID** | EXP-003 |
| **Version** | 1.2 |
| **Status** | Completed |
| **Document Owner** | @domannand95 |
| **Effective Date** | 2026-08-08 |

> **Objective**
> Determine whether reducing full Markdown repository documents to their extracted heading hierarchy improves the reliability of lineage classification performed by the local inference engine (Mistral/Ollama).

---

# Background

Following the publication of **DF-001**, direct comparison of complete Markdown documents was shown to be unreliable.

`EXP-001` demonstrated that single-document metadata extraction was feasible.

`EXP-002` demonstrated that comparison of extracted metadata profiles still resulted in incorrect classification.

This experiment isolates document structure by comparing extracted heading hierarchies rather than complete documents or metadata summaries.

---

# Experimental Method

Two versions of `BKI-003` were used:

* Document A (earlier / reduced structure)
* Document B (later / expanded structure)

For each document, the local model was instructed to extract only:

* Document ID
* Version
* Status
* Heading hierarchy

No body text, summaries, or semantic interpretation were requested.

The resulting heading profiles were then compared using the repository lineage classification categories defined by `ECP-002` v0.7.

---

# Results

## Heading Extraction

The model successfully extracted the heading hierarchy from both documents.

The extracted structures preserved the overall document organization and hierarchical relationships.

The extracted heading hierarchy for Document B contained additional structural detail relative to Document A.

---

## Heading Comparison

The comparison stage identified structural differences between the two extracted heading profiles.

Examples included:

* Additional nested headings;
* Expanded governance hierarchy;
* Operational Validation section;
* Richer architectural decomposition.

Despite acknowledging these structural differences, the model classified the profiles as:

**Exact Duplicate**

---

# Outcome

**Result:** Partial Pass

The experiment demonstrates that heading extraction successfully reduces repository documents into structured representations suitable for comparison.

However, the downstream classification stage remained unreliable.

The model recognised structural differences but failed to incorporate those differences into the final repository lineage classification.

---

# Interpretation

The observed behaviour suggests that the comparison workflow consists of multiple independent stages:

1. Document extraction;
2. Structural normalization;
3. Difference detection;
4. Repository lineage classification.

Within the tested workflow:

* Stages 1–3 showed measurable improvement.
* Stage 4 continued to produce incorrect repository lineage classifications.

This indicates that reducing document size alone is insufficient to ensure reliable lineage classification.

---

# Conclusion

The hypothesis that heading-only preprocessing would fully resolve the comparison failures identified in `DF-001` is **not supported**.

However, the experiment demonstrates measurable improvement in structural extraction and difference detection.

The evidence suggests that the principal limitation lies downstream of heading extraction, with the repository lineage classification stage remaining the leading candidate for further investigation.

---

# Follow-on Experiment

Proceed to:

**EXP-004 — Deterministic Structural Fingerprint Comparison**

Evaluate whether replacing natural-language heading hierarchies with deterministic structural fingerprints further improves repository lineage classification reliability.

---

# Related Documents

* DF-001 — Document Length & Attention Degradation
* EXP-001 — Single Document Metadata Extraction
* EXP-002 — Metadata Profile Comparison
* TC-01 — Divergent Same-Identifier
* TC-02 — Exact Duplicate
* ECP-002 v0.7