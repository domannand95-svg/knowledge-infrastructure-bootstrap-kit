# Knowledge Infrastructure Bootstrap Kit (BKI)

## Overview

The Knowledge Infrastructure Bootstrap Kit (BKI) is a governed knowledge infrastructure framework for intake, classification, normalization, validation, provenance preservation, and controlled promotion workflows.

BKI establishes explicit boundaries between raw information, processed artifacts, validated evidence, and authoritative records.

BKI does not determine truth automatically.

BKI does not automatically promote knowledge into authoritative state.

BKI provides deterministic structure, validation boundaries, and traceable evidence workflows that support explicit governance decisions.

---

## Core Principle

> **Evidence does not become authority by observation alone.**

BKI separates:

- information intake;
- structural validation;
- normalization;
- classification;
- evidence records;
- governance decisions; and
- authoritative promotion.

A validated artifact is not automatically an approved artifact.

A normalized document is not automatically authoritative.

A passing validation result is not permission to mutate governed state.

---

## Current Baseline

BKI development is centred around the BKI-001 framework baseline.

Current implemented foundations include:

- governed knowledge intake workflows;
- deterministic Markdown classification and validation;
- structural normalization boundaries;
- protected-content preservation;
- provenance-aware transformation handling;
- validation command contracts;
- fail-closed handling of incomplete validation states;
- read-only validation operation; and
- compatibility boundaries for integration with external governance systems.

The validator boundary verifies defined contracts.

It does not independently authorize promotion, repository mutation, or external publication.

---

## Evidence Lifecycle

BKI structures knowledge processing through explicit lifecycle stages:

    Raw Intake
        |
        v
    Classification
        |
        v
    Normalization
        |
        v
    Validation
        |
        v
    Governed Evidence Record
        |
        v
    Explicit Governance Decision
        |
        v
    Authoritative Promotion (if approved)

Each transition requires an explicit boundary.

No stage silently inherits authority from the previous stage.

---

## Validation Boundary

The BKI validator provides deterministic checks for:

- document structure;
- schema conformity;
- protected region preservation;
- normalization safety;
- classification outcomes;
- validation contract compliance; and
- failure-state handling.

Validation outcomes represent the result of defined checks.

They do not represent automatic approval.

A validator confirms that an artifact satisfies a defined contract.

It does not decide whether that artifact should become authoritative.

---

## Repository Structure

    docs/
    |-- master/              authoritative framework indexes
    |-- governance/          governance rules and decision records
    |-- architecture/        architecture decisions and boundaries
    |-- ai/                  governed AI operation material
    |-- commissioning/       commissioning records, experiments, findings

    tooling/
    `-- normalization/       deterministic parser, classifier, validator tooling

    tests/
    `-- validation fixtures and validator test coverage

    reconciliation/
    `-- baseline authority and scope records

---

## Relationship With Sovereign Operating Layer

BKI and Sovereign Operating Layer (SOL) operate as separate but complementary boundaries.

BKI governs:

- knowledge intake;
- evidence organization;
- normalization;
- validation;
- provenance preservation.

SOL governs:

- authority boundaries;
- capability admission;
- deterministic execution controls;
- governed effects.

The relationship is:

    Information
        |
        v
    [BKI]
    Classification / Normalization / Validation
        |
        v
    Governed Evidence
        |
        v
    [SOL]
    Authority Checks / Admission Boundaries / Execution Controls
        |
        v
    Bounded Effects

BKI does not acquire execution authority.

SOL does not automatically treat knowledge artifacts as authoritative.

The boundary between evidence and authority remains explicit.

---

## Development Principles

BKI development follows these principles:

- Evidence before promotion.
- Provenance before transformation.
- Deterministic validation before trust.
- Explicit governance before authority.
- Reversible changes where possible.
- Fail closed where required context is unavailable.
- Preserve raw lineage through all transformations.

---

## Local Development

BKI tooling is developed using Python-based validation infrastructure.

Typical workflow:

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -m pytest

Validation tooling should remain deterministic and should not silently bypass governance boundaries.

---

## Contributor Workflow

Changes should:

1. Occur on a dedicated branch.
2. Preserve existing provenance and validation boundaries.
3. Include appropriate validation coverage.
4. Avoid introducing implicit promotion authority.
5. Clearly distinguish implemented behaviour from proposals.

Documentation, specifications, tooling, and governance records should remain traceable through normal repository history.

---

## Current Direction

Near-term BKI priorities:

1. Maintain stability of validation contracts.
2. Expand adversarial validation coverage.
3. Preserve Wind# Sovereign Operating Layer (SOL)

**Probabilistic intelligence; deterministic authority.**

Sovereign Operating Layer (SOL) is an experimental Rust control plane exploring deterministic authority boundaries around probabilistic intelligence.

SOL does not attempt to make models deterministic.

Instead, it places deterministic, auditable, fail-closed infrastructure around probabilistic components.

Models may reason, propose, classify, search, and request capabilities.

The surrounding control plane determines:

- what authority exists;
- which state is authoritative;
- what may be admitted;
- what may cause external effects; and
- what must be retained for audit and replay.

> **Intelligence may explore beyond the boundary. Effects may not.**

---

# Programme Scope and Naming

- **Repository:** `sovereign-os`
- **Implemented architecture:** Sovereign Operating Layer (SOL)
- **Future architectural horizon:** Sovereign Operating System

The repository name reflects the broader programme vision.

The currently implemented system is a governed control layer, not a complete operating system.

---

# Current Status

The current implementation focuses on deterministic authority validation foundations.

Implemented areas include:

- Capability V1 validation contracts;
- Registry v2 compatibility boundaries;
- canonical encoding and decoding;
- deterministic validation gates;
- governed evidence records;
- adversarial authority evaluation;
- deterministic replay foundations;
- persistence integrity boundaries.

The validation sequence includes:

1. Structural decoding.
2. Internal coherence checks.
3. Registry reference resolution.
4. Authoritative identity resolution.
5. Deterministic temporal validation.
6. Issuer eligibility validation.
7. Governing-policy authorization boundaries.

These components provide deterministic validation contracts.

They do not yet represent a complete production admission orchestrator.

---

# Core Architectural Principle

SOL separates intelligence from authority.

External or local models may remain:

- probabilistic;
- adaptive;
- provider-neutral; and
- exploratory.

Authority is constrained through deterministic infrastructure:

- explicit schemas;
- canonical encoding;
- content-addressed objects;
- authoritative state references;
- fail-closed validation;
- bounded capabilities;
- deterministic replay;
- provenance preservation; and
- independently reviewable decisions.

The governing rule:

> **Proposal is not authorization. Capability is not permission. Intelligence is not authority.**

Ambient authority is never inferred.

Missing, unresolved, substituted, stale, malformed, unauthorized, or disconnected context fails closed.

---

# Deterministic Validation

SOL validation boundaries enforce:

- canonical representation;
- schema correctness;
- semantic consistency;
- authoritative reference resolution;
- identity binding;
- temporal correctness;
- policy evaluation boundaries; and
- adversarial failure handling.

Validation determines whether a candidate satisfies defined authority requirements.

Validation does not create authority.

---

# Governed Evidence

SOL includes governed evidence foundations.

Implemented structures include:

- objective records;
- claim records;
- source records;
- method records;
- uncertainty records;
- failed attempt records;
- reviewer findings;
- provenance preservation;
- deterministic encoding;
- audit-oriented validation.

Evidence remains epistemic.

Evidence does not authorize execution.

---

# Knowledge Infrastructure Bootstrap Kit

The Knowledge Infrastructure Bootstrap Kit (BKI) operates as a complementary knowledge governance boundary.

BKI provides:

- intake;
- classification;
- normalization;
- validation;
- provenance preservation.

SOL provides:

- authority boundaries;
- capability admission;
- deterministic execution controls.

The relationship:

    Information
        |
        v
    BKI
    Classification / Normalization / Validation
        |
        v
    Governed Evidence
        |
        v
    SOL
    Authority Checks / Admission / Execution Boundaries
        |
        v
    Bounded Effects

Neither system silently inherits the authority of the other.

---

# Workspace

The root Cargo workspace contains:

    crates/
    |-- sovereign-core-asm/
    |-- sovereign-ledger/
    |-- sovereign-registry/
    |-- sovereign-policy/
    |-- sovereign-engine/
    |-- sovereign-audit/
    `-- sovereign-discovery/

---

# Verification

Run:

    cargo fmt --all -- --check

    cargo clippy --workspace --all-targets --locked -- -D warnings

    cargo test --workspace --all-targets --locked

Boundary-affecting changes should also verify:

- deterministic replay;
- fail-closed behaviour;
- substitution resistance;
- authoritative context binding.

---

# Development Principles

SOL development follows:

- specifications before authority-bearing implementation;
- explicit acceptance boundaries;
- small reviewable changes;
- deterministic testing;
- adversarial validation;
- separation between proposals and permissions;
- clear distinction between research and implementation.

---

# License

Licensed under the Apache License 2.0.ows and Linux compatibility.
4. Improve commissioning evidence.
5. Maintain explicit integration boundaries with external systems.

---

## License

Licensed under the Apache License 2.0.
