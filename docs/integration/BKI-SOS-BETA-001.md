---
document_id: BKI-SOS-BETA-001
version: 0.1
status: Proposed Beta Contract
last_revised: 2026-08-11
---

# BKI and Sovereign OS Read-Only Beta Integration Contract

## Purpose

This contract defines the proposed boundary by which Sovereign OS may request a
deterministic BKI validation and consume the result during beta testing. It does
not authorize implementation, production use, repository mutation, evidence
promotion, or execution inside the Sovereign OS production core.

## Governing Principles

1. BKI remains an independent repository and validator authority.
2. Sovereign OS remains an independent consumer and policy authority.
3. The consumer pins an exact BKI release and contract version.
4. The adapter receives two read-only Markdown files and emits one result.
5. A result is validation evidence only; it is never promotion authority.
6. Unknown versions, malformed output, timeouts, and adapter failures fail closed.
7. Neither repository receives ambient write access to the other.

## Proposed Invocation Boundary

The implementation phase may add a BKI-owned command-line adapter with this
conceptual interface:

```text
python -m tooling.normalization.cli \
  --source <read-only-source.md> \
  --candidate <read-only-candidate.md> \
  --format bki.validation.v1
```

The adapter shall:

- read only the two explicitly supplied files;
- reject URLs, directories, symbolic-link escapes, and unsupported encodings;
- perform no network access;
- write no files;
- emit exactly one UTF-8 JSON object to standard output;
- send diagnostics only to standard error;
- apply a caller-enforced timeout and resource budget; and
- produce output conforming to `bki-validation-result-v1.schema.json`.

This command is a proposed interface, not a currently implemented capability.

## Result Semantics

| Outcome | Adapter exit | Consumer action |
| --- | ---: | --- |
| `PASS — COMPLIANT` | 0 | Record validation evidence; no automatic promotion |
| `PASS — NORMALIZED` | 0 | Record validation evidence and reviewed delta; no automatic promotion |
| `FAIL — QUARANTINE` | 2 | Preserve result and route the candidate to quarantine |
| Invocation or contract failure | 3 | Fail closed; do not treat the document as validated |

Sovereign OS shall not translate a zero exit status into execution, publication,
registry mutation, or epistemic promotion authority.

## Version and Identity Requirements

The beta consumer shall pin all of the following:

- an immutable BKI release tag and commit SHA;
- `contract_version` equal to `bki.validation.v1`;
- the validator version reported in audit metadata;
- SHA-256 identifiers for the source and candidate bytes supplied; and
- the expected JSON Schema digest.

A mismatch in any pinned identity or version is a contract failure. Compatible
changes may add optional fields only. Renamed fields, removed fields, changed
outcome meanings, or expanded validation authority require a new contract version.

## Authority Separation

BKI acts only as a deterministic evaluator of the supplied source/candidate pair.
It does not become a Sovereign OS proposer, executor, policy authority, promotion
authority, or evidence custodian.

Sovereign OS may preserve the returned record as candidate evidence, but admission
to an authoritative ledger requires its own identity, provenance, policy, review,
and approval controls. BKI success cannot satisfy those controls by itself.

## Data Handling

- Beta fixtures should contain non-sensitive synthetic or approved content.
- Raw Markdown and unified diffs remain local to the isolated CI workspace.
- Logs shall not publish source content, candidate content, secrets, or tokens.
- The result envelope carries content hashes and governed classifications; any
  raw diff field must be treated as potentially sensitive evidence.
- Temporary workspaces are removed by the CI runner after the job completes.

## Compatibility Test Matrix

Before implementation is eligible for beta use, compatibility CI shall verify:

1. compliant input produces schema-valid `PASS — COMPLIANT`;
2. governed normalization produces schema-valid `PASS — NORMALIZED`;
3. protected-content mutation produces `FAIL — QUARANTINE` and exit 2;
4. prose mutation produces `FAIL — QUARANTINE` and exit 2;
5. malformed candidate frontmatter fails closed;
6. unknown contract version fails closed;
7. malformed or partial JSON fails closed in the consumer;
8. timeout and process failure cannot be interpreted as a pass;
9. input hashes match the exact bytes evaluated; and
10. the adapter performs no repository or network write.

The matrix shall run on Windows and Ubuntu before the beta interface is enabled.

## Activation Gates

Implementation may begin only after:

- BKI commissioning closure is merged;
- this contract is reviewed and accepted;
- the BKI result schema is frozen for `bki.validation.v1`;
- negative compatibility fixtures are approved; and
- both repositories identify accountable maintainers for contract changes.

Beta activation additionally requires a tagged BKI release, a pinned Sovereign OS
consumer, passing cross-repository compatibility CI, and explicit owner approval.

## Explicitly Out of Scope

- automatic document transformation;
- BKI write-back to either repository;
- Sovereign OS production-core execution;
- automatic evidence promotion or trust assignment;
- registry or ledger mutation by the adapter;
- network service exposure;
- model training or research ingestion; and
- weakening either repository's existing governance controls.

## Proposed Implementation Order

1. Review and freeze this contract.
2. Add deterministic JSON serialization to BKI.
3. Add the read-only BKI command-line adapter and negative tests.
4. Tag the first contract-bearing BKI pre-release.
5. Add a quarantined Sovereign OS consumer fixture.
6. Add cross-platform compatibility CI using the pinned release.
7. Review evidence and explicitly decide whether to activate beta testing.
