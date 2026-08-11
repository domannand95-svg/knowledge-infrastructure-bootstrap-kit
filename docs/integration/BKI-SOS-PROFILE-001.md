---
document_id: BKI-SOS-PROFILE-001
version: 1.0
status: Proposed Compatibility Profile
last_revised: 2026-08-11
---

# BKI and Sovereign OS Language Compatibility Profile v1

## Purpose

`bki.sovereign.profile.v1` defines the shared metadata vocabulary and semantic
boundaries used when BKI validates a designated Sovereign OS artifact. It lets
the repositories exchange deterministic records without making either
repository's internal vocabulary authoritative over the other.

## Canonical Metadata

| Shared field | BKI source key | Sovereign OS source key | Rule |
| --- | --- | --- | --- |
| `document_id` | `document_id` | `ID` | Required non-empty string; identity is never inferred from a title or path |
| `version` | `version` | `Version` | Required and represented as a string in the profile |
| `status.value` | `status` | `Status` | Required literal source value; no lifecycle meaning is inferred |
| `status.namespace` | `bki` | `sovereign` | Required namespace preventing status-name collisions |
| `last_revised` | `last_revised` | `Last Updated` | Required RFC 3339 full date (`YYYY-MM-DD`) |

Sovereign fields such as `Document`, `Owner`, `Reviewers`, `Evidence`,
`Depends On`, and `Supersedes` remain Sovereign-governed extension metadata.
They are not silently discarded, reinterpreted as BKI authority, or copied into
the shared core. A future extension requires a new reviewed profile version or
an explicitly governed extension schema.

## Alias and Collision Rules

1. Translation is enabled only when the caller explicitly selects
   `bki.sovereign.profile.v1`.
2. A source must use exactly one source vocabulary for every shared field.
3. If canonical and aliased keys are both present, translation fails closed,
   even when their displayed values appear equal.
4. Missing, null, ambiguous, duplicate, or type-incompatible values fail closed.
5. Values are preserved; the profile translates keys, not meaning.
6. Unknown profile versions fail closed.

These rules prevent a permissive alias from becoming a metadata-confusion or
authority-escalation path.

## Shared Semantic Vocabulary

| Term | Shared meaning |
| --- | --- |
| Artifact | A bounded, identified object under evaluation or governance |
| Evidence | Attributable information considered by a validator or decision authority |
| Validation outcome | A BKI evaluator result: `COMPLIANT`, `NORMALIZED`, or `QUARANTINE` |
| Disposition | A Sovereign decision: accept for review, reject, defer, quarantine, supersede, or revoke |
| Quarantine | Fail-closed isolation; never deletion, approval, or promotion |
| Promotion | A separately authorized Sovereign governance transition |
| Capability | Explicitly granted authority to perform a bounded operation |
| Profile | A versioned translation contract; never an authority grant |

The word `quarantine` is intentionally shared, but its record type remains
namespaced. A BKI quarantine is validation evidence that a Sovereign policy may
consider. It is not itself a Sovereign disposition.

## Authority Invariants

- `PASS — COMPLIANT` and `PASS — NORMALIZED` are evidence only.
- A BKI result cannot create a Sovereign disposition, capability, policy
  decision, registry mutation, execution permission, or promotion.
- A Sovereign disposition cannot rewrite the BKI result that informed it.
- Unknown terms, versions, mappings, or status namespaces fail closed.
- Each repository pins the profile version and schema digest before beta use.

## Conformance

Canonical metadata records must validate against
`bki-sovereign-profile-v1.schema.json`. Implementations must cover canonical BKI
input, aliased Sovereign input, missing fields, conflicting aliases, invalid
dates, unknown namespaces, unknown profile versions, and authority-confusion
attempts before beta activation.
