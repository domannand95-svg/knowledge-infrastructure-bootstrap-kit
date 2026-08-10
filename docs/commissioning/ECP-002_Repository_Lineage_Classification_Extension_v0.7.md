# Commissioning Provisional Specification: Repository Lineage Classification Extension (`ECP-002` v0.7)

| Property | Value |
| --- | --- |
| **Document ID** | ECP-002 |
| **Version** | 0.7 |
| **Status** | **Feature Frozen** — Active Stage 2 Regression Testing (Empirical Data Collection) |
| **Document Owner** | @domannand95 |
| **Effective Date** | 2026-08-08 |

> **Operational Directive**
>
> **Feature Frozen.**
>
> No additional functional changes or schema additions are permitted until regression testing has been completed.
>
> Only editorial corrections are permitted.

> **Purpose**
>
> Establish a provisional, non-governing classification overlay for local AI ingestion engines (Ollama / Mistral). This specification extends the baseline deterministic classification output format (`NWO-000` v1.3 Section 5) with precise operational state definitions, multi-source evidence arrays, structured confidence metrics, evidence sufficiency gating, explicit human review tagging, non-destructive promotion thresholds, and a structured empirical test suite to support deterministic assessment of repository lineage during commissioning without modifying the frozen constitutional register.

---

# Current Operational Status

- **Phase:** Bootstrap Commissioning
- **State:** Feature Frozen — Active Stage 2 Regression Testing (Empirical Data Collection)
- **Current Objective:** Execute the structured five-case regression test suite using `ECP-002` v0.7 to evaluate operational outcomes and record empirical findings against explicit promotion criteria prior to any consideration of constitutional baseline (`NWO-000`) integration.

---

# Provisional Extended Classification Schema

Local AI models executing Stage 2 regression testing must adhere strictly to the following extended output format.

```text
Classification Result

Source Document:
Primary Module:
Related Modules:
Evidence Status:

Repository Relationship:
Version Detected:
Identifier Detected:
Supersedes:
Superseded By:
Filename Consistent:
Content Relationship:
Duplicate:
Superseded:

Research Priority:
Deep Research Required:
Conflict Detected:

--- Adjudication & Evidence Metrics ---

Detection State:
Detection Confidence:

Resolution State:
Resolution Confidence:

Evidence Sufficiency:

Evidence Basis:
- Filename
- Document Metadata
- Internal Revision History
- Repository Metadata
- Content Comparison
- Human Annotation
- Unknown

Missing Metadata:

--- Automated Gating & Output ---

Automatic Classification:
Human Review Required:
Human Review Reason:

Canonical Candidate:

Reasoning:

Recommended Action:
```

---

# Controlled Vocabulary

## Repository Relationship

Allowed values:

- Canonical
- Older Revision
- Newer Revision
- Exact Duplicate
- Near Duplicate
- Divergent Same-Identifier
- Independent
- Unknown

---

## Content Relationship

Allowed values:

- Identical
- Subset
- Superset
- Overlapping
- Divergent
- Unrelated
- Unknown

---

## Detection State

- **PASS** — A repository relationship was successfully detected.
- **FAIL** — Detection could not execute because of malformed input, parse failure, or missing required identifiers.
- **INCONCLUSIVE** — Detection executed successfully but found no defensible relationship.

---

## Resolution State

- **PASS** — Canonical lineage determined from sufficient evidence.
- **FAIL** — Evidence was contradictory or violated deterministic constraints.
- **INCONCLUSIVE** — Evidence was insufficient to resolve lineage.

---

## Evidence Sufficiency

- **Sufficient** — Enough authoritative evidence exists to determine lineage.
- **Insufficient** — Required metadata is missing or incomplete.
- **Contradictory** — Available evidence conflicts.

---

# Same-Identifier Resolution Protocol

When two or more documents share the same Document ID, evaluate evidence in the following order:

1. Explicit supersession metadata
2. Explicit filename version suffix
3. Repository metadata (commit history, release tags, repository annotations, or other authoritative repository records)
4. Document internal revision history
5. Human review

---

## Resolution Rules

### Sufficient Evidence

If:

- Detection identifies **Divergent Same-Identifier**
- Evidence Sufficiency = **Sufficient**

then:

```text
Resolution State: PASS
Automatic Classification: PASS
Human Review Required: No
Canonical Candidate: <resolved document>
```

---

### Insufficient or Contradictory Evidence

If:

- Detection identifies **Divergent Same-Identifier**
- Evidence Sufficiency = **Insufficient** or **Contradictory**

then:

```text
Resolution State: INCONCLUSIVE
Automatic Classification: INCONCLUSIVE
Human Review Required: Yes
Canonical Candidate: Undetermined
```

The model shall not fabricate a canonical result.

---

# Promotion Criteria

`ECP-002` may only be considered for promotion into the constitutional baseline (`NWO-000`) after all of the following conditions have been satisfied:

- The complete five-case regression suite has been executed.
- All results have been recorded.
- No unresolved regressions remain.
- The overlay demonstrates repeatable improvement over baseline behaviour.
- Promotion does not reduce successful baseline performance on previously passing test cases.
- Human review confirms the additional metadata improves repository classification without introducing unnecessary operational complexity.

---

# Stage 2 Regression Test Suite

| Test Case | Target | Expected Behaviour | Actual Output | Result | Operational Notes |
|-----------|--------|--------------------|---------------|--------|-------------------|
| **TC-01** | Conflicting `BKI-003` v1.2 files | Detection: PASS<br>Resolution: INCONCLUSIVE<br>Conflict: Yes<br>Human Review: Yes | Pending | Pending | |
| **TC-02** | Exact duplicates | Detection: PASS<br>Resolution: PASS<br>Conflict: No<br>Human Review: No | Pending | Pending | |
| **TC-03** | Near duplicates | Detection: PASS<br>Resolution: PASS or INCONCLUSIVE (depending on evidence)<br>Human Review: Evidence dependent | Pending | Pending | |
| **TC-04** | Superseded revisions | Detection: PASS<br>Resolution: PASS<br>Canonical selected | Pending | Pending | |
| **TC-05** | Independent files | Detection: PASS<br>Repository Relationship: Independent<br>Resolution: PASS<br>Human Review: No | Pending | Pending | |

---

# Revision History

| Version | Date | Summary |
| --- | --- | --- |
| **0.1** | 2026-08-07 | Initial provisional specification introducing controlled vocabulary and same-ID conflict handling. |
| **0.2** | 2026-08-07 | Added evidence-based canonical selection precedence, structured confidence fields, and the `Undetermined` designation. |
| **0.3** | 2026-08-08 | Introduced two-phase Detection/Resolution architecture and Evidence Sufficiency gating. |
| **0.4** | 2026-08-08 | Added explicit state definitions and structured regression protocol. |
| **0.5** | 2026-08-08 | Simplified Evidence Basis and embedded regression ledger. |
| **0.6** | 2026-08-08 | Declared feature freeze and introduced promotion criteria. |
| **0.7** | 2026-08-08 | Final feature-frozen commissioning specification. Clarified commissioning scope, generalized repository metadata terminology, added non-regression promotion criteria, and finalized the regression suite for empirical execution. |

---

# Design Principle

> **Detect reliably. Resolve provably. Defer when evidence is insufficient.**

By separating detection from resolution and enforcing explicit evidence sufficiency gates, local AI models remain deterministic, auditable, and avoid fabricating repository lineage decisions when authoritative evidence is unavailable.