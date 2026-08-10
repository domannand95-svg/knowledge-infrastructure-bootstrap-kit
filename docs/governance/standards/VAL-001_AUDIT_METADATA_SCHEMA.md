---
document_id: VAL-001-AUDIT-001
version: 1.0
status: Commissioning Schema
last_revised: 2026-08-10
---

# VAL-001 Audit Metadata Schema

## Purpose

This schema defines the immutable execution metadata returned with every VAL-001 validation result. Audit metadata records when and under which validator version a decision occurred without granting persistence, publication, or repository write authority.

## Fields

| Field | Type | Requirement |
| --- | --- | --- |
| `executed_at_utc` | String | UTC timestamp in second-precision RFC 3339 form ending in `Z`. |
| `validator_version` | String | Governed validator implementation identifier. |
| `source_document_id` | String or null | Parsed source `document_id`, including recognized legacy `Document ID`; null when unavailable. |
| `candidate_document_id` | String or null | Parsed candidate `document_id`; null when candidate parsing fails before identity is established. |
| `outcome` | `ValidationOutcome` | The final `COMPLIANT`, `NORMALIZED`, or `QUARANTINE` outcome. |
| `error_code` | `ErrorCode` | `NONE` for passing outcomes or the explicit quarantine error. |

## Clock Requirements

The production validator uses the system UTC clock. Tests and deterministic replay harnesses may inject a clock, but it must return a timezone-aware value. Naive local timestamps are rejected to prevent ambiguous audit evidence.

## Version

The commissioned implementation identifier is:

```text
VAL-001 v1.0-pilot
```

Changing validator behavior or the audit schema requires a governed version decision. Runtime timestamps do not alter classification-log determinism.

## Safety Boundary

Audit metadata exists only in the returned in-memory result. This schema does not authorize writing logs to disk, transmitting telemetry, modifying source or candidate files, committing changes, or publishing results.
