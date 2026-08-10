# Experiment Record: Deterministic Structural Fingerprint Comparison (`EXP-004`)

| Property | Value |
| --- | --- |
| **Experiment ID** | EXP-004 |
| **Version** | 1.1 |
| **Status** | In Progress / Ready for Execution |
| **Document Owner** | @domannand95 |
| **Effective Date** | 2026-08-08 |

> **Objective**
> Determine whether deterministic structural fingerprints improve the reliability of repository lineage classification by reducing semantic ambiguity presented to the local inference engine.

---

# Background

Following the publication of **DF-001** and subsequent empirical tests:

* **DF-001:** Direct comparison of large Markdown documents proved unreliable.
* **EXP-001 & EXP-002:** Single-document metadata extraction is viable, but profile comparison fails when descriptive text is included.
* **EXP-003:** Heading extraction successfully captures document organization, but downstream classification remains flawed due to lingering natural-language ambiguity.

`EXP-004` isolates the evaluation by eliminating natural language entirely, substituting objective, numerical, and categorical structural fingerprints.

---

# Experimental Workflow

1. Generate deterministic fingerprints from each Markdown document.
2. Verify the fingerprints for completeness.
3. Compare Fingerprint A and Fingerprint B using `ECP-002` v0.7.
4. Record the classification outcome.
5. Compare the model's classification against the known ground truth.

---

# Experimental Method

## 1. Fingerprint Schema Specification

For each target file (`BKI-003` variants), extract an isolated structural record adhering strictly to this schema:

* `Filename:`
* `File Size (bytes):`
* `Document Version:`
* `Document Status:`
* `Heading Count:`
* `H1 Count:`
* `H2 Count:`
* `H3 Count:`
* `Revision Entry Count:`

## 2. Comparative Adjudication Protocol

Supply *only* Fingerprint A and Fingerprint B to the local inference engine (Mistral/Ollama). The model is instructed to apply the classification matrix from `ECP-002` v0.7 solely based on the quantitative deltas between the two structured records. No prose, summaries, or full-text scanning are permitted in the prompt window.

---

# Ground Truth

Prior independent inspection of the source documents established that Document B contains additional structural information beyond Document A and therefore the documents are not exact duplicates.

EXP-004 evaluates whether the local inference engine reaches the same conclusion when provided only with deterministic structural fingerprints.

---

# Success Metrics

The experiment will be considered successful if:

* All fingerprint fields are interpreted correctly;
* Structural differences are identified correctly;
* Repository lineage classification matches the known ground truth;
* The model explains the reasoning using only the supplied fingerprint data.

---

# Experimental Limitations

This experiment evaluates repository lineage classification using deterministic structural fingerprints only.

It does not evaluate:

* semantic document similarity;
* body text interpretation;
* author intent;
* document quality; or
* correctness of the repository classification matrix defined by `ECP-002`.

Any observed failures should therefore be interpreted as limitations of fingerprint-based comparison under the tested workflow rather than deficiencies in the underlying repository documents.

---

# Evidence Capture

Record and archive the following:

* Fingerprint A
* Fingerprint B
* Prompt supplied to the local inference engine
* Raw model response (unaltered)
* Operator observations (if any)

These artifacts shall be stored alongside this experiment record to ensure repeatability and independent review.

---

# Expected Outcomes

* **Pass Criteria:** The model correctly classifies the relationship between Fingerprint A and Fingerprint B without reverting to default "Exact Duplicate" hallucinations.
* **Failure Criteria:** The model continues to output arbitrary or uniform classifications despite receiving completely distinct numerical inputs, indicating a fundamental limitation in the local model's relational reasoning logic.