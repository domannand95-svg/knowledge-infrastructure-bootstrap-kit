# Commissioning Diagnostic Finding: Document Length & Attention Degradation (`DF-001`)

| Property | Value |
| --- | --- |
| **Finding ID** | DF-001 |
| **Version** | 1.0 |
| **Status** | Preliminary Evidence |
| **Evidence Status** | Preliminary |
| **Document Owner** | @domannand95 |
| **Effective Date** | 2026-08-08 |

> **Operational Directive**
> Published as Version 1.0. No additional functional changes or schema modifications shall be made to `ECP-002` based solely on the evidence contained within `DF-001`. Commissioning shall resume only after one or more follow-up experiments have been completed.

---

## Status

* **Repeatability:** Not yet confirmed
* **Impacted Specification:** ECP-002 v0.7 (No changes recommended)

## Related Documents

* `ECP-001` — Engineering Commissioning Execution
* `ECP-002` v0.7 — Repository Lineage Classification Extension
* `TC-01` — Divergent Same-Identifier
* `TC-02` — Exact Duplicate

---

# Diagnostic Summary

### Objective

Determine whether the local inference engine (Mistral/Ollama) can reliably compare long-form repository documents under the ECP-002 adjudication protocol.

### Method

Executed comparative test case TC-01 using the two conflicting `BKI-003` v1.2 documents alongside the ECP-002 schema, contrasted against a control test using short-form text strings (the fruit comparison test). All document comparisons were performed using complete Markdown documents supplied within a single prompt unless otherwise noted.

---

# Evidence

* **TC-01:** FAIL (Model reported full-length conflicting `BKI-003` documents as identical)
* **TC-02:** FAIL (Model failed to identify two identical long-form documents as exact duplicates)
* **Diagnostic Control Test (Short Text Comparison):** PASS (Model successfully discriminated between short-form test strings)

---

# Working Hypothesis & Root Cause Analysis

The observed behaviour is consistent with one or more of the following:

* Long-form document comparison exceeds the model's reliable comparative capability under the current prompting strategy.
* The combined task (large-document comparison plus schema-driven adjudication) introduces sufficient complexity that the model simplifies the task rather than executing the requested comparison.

*Further experimentation is required to distinguish between these possibilities.*

---

# Architectural Conclusion

Current evidence does not support using single-prompt comparison of large repository documents as a reliable commissioning workflow for the tested local model, prompt design, and evaluation procedure. Additional experimentation is required before generalizing this conclusion to other models or workflows.

* **Specification Status:** `ECP-002` v0.7 remains **Feature Frozen**. No schema edits are required; the issue is methodological, not lexical.

---

# Recommended Follow-up Experiments

* **Priority 1:** Compare heading structures only.
* **Priority 2:** Compare section-by-section rather than whole documents.
* **Priority 3:** Compare semantically compressed document summaries generated deterministically prior to comparison.
* **Priority 4:** Generate deterministic structural fingerprints before LLM comparison.
* **Priority 5:** Evaluate alternative local models using the same regression suite.
* **Priority 6:** Compare deterministic diff tooling with LLM-assisted adjudication.

---

## Next Action

No changes shall be made to `ECP-002` based solely on `DF-001`.

Resume commissioning only after one or more follow-up experiments have been completed and the finding has either been confirmed, refuted, or refined through additional empirical evidence.

---

## Closure

This finding records an observed commissioning outcome and associated working hypotheses. It does not constitute a modification to the Bootstrap Kit, `ECP-002`, or any constitutional baseline. Any future changes shall be justified through additional empirical evidence gathered during commissioning.