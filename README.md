# Knowledge Infrastructure Bootstrap Kit (BKI)

BKI is a governed, deterministic validation boundary for knowledge artifacts. It classifies proposed normalization, protects meaning-bearing content, and emits reproducible evidence without acquiring publication, promotion, repository-write, or execution authority.

## Governing Boundary

BKI answers a narrow question: does a candidate artifact preserve the governed source under the normalization rules implemented by `VAL-001 v1.0`?

It may:

- parse source and candidate Markdown;
- classify structural and formatting differences;
- validate authorized normalization;
- protect metadata, prose, code, tables, URLs, and citation keys;
- emit deterministic outcomes, classification logs, diffs, and audit metadata; and
- translate designated metadata through an explicitly selected compatibility profile.

It may not transform source material autonomously, write back to a repository, publish or promote evidence, grant capabilities, authorize effects, or mutate Sovereign state. A successful validation result is evidence for a later governed decision, not that decision itself.

## Current Baseline

The BKI repository baseline is commissioned and `VAL-001 v1.0` is closed. The active implementation provides:

- a Python library validator;
- a read-only command-line adapter;
- deterministic `COMPLIANT`, `NORMALIZED`, and `QUARANTINE` outcomes;
- fail-closed structural, prose, and protected-content checks;
- immutable audit metadata and deterministic classification logs;
- `bki.validation.v1` result serialization; and
- the active read-only-beta `bki.sovereign.profile.v1` metadata compatibility boundary.

Historical commissioning records remain evidence of the state and test counts at their recorded dates. The current test suite is the operational repository regression gate.

## Validation Model

```text
governed source + candidate artifact
                |
                v
        parse and classify
                |
                v
     deterministic validation
                |
                v
  compliant | normalized | quarantine
                |
                v
     evidence for human review
```

The validator authorizes only implemented source-preserving normalization. It fails closed when frontmatter is invalid, heading structure is unsafe, protected content changes, prose changes, or a delta is not explicitly recognized.

Protected elements include:

- frontmatter metadata;
- fenced and inline code;
- GitHub-flavored Markdown tables;
- literal HTTP and HTTPS URLs; and
- citation keys.

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `tooling/normalization/` | Parser, classifier, validation model, CLI, and deterministic validator |
| `tooling/integration/` | Sovereign compatibility-profile translation |
| `tests/` | Positive, negative, serialization, CLI, audit, and compatibility regressions |
| `docs/validator/` | Operational validator guidance |
| `docs/commissioning/` | Commissioning, closure, and implementation traceability evidence |
| `docs/governance/` | Architecture and co-evolutionary governance model |
| `docs/integration/` | BKI/Sovereign contracts, schemas, and compatibility reviews |
| `docs/master/` | Canonical document index |
| `reconciliation/` | Baseline reconciliation and recovery checkpoints |
| `tooling/fingerprinting/` | Deterministic fingerprint support |

## Local Verification

Python 3.11 or later is recommended. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider
```

The CI validator runs the governed regression suite on Windows and Ubuntu.

## Read-Only CLI

```powershell
python -m tooling.normalization.cli `
  --source source.md `
  --candidate candidate.md `
  --format bki.validation.v1
```

Exit status `0` means compliant or governed normalization, `2` means quarantine, and `3` means the invocation or contract failed closed. The adapter accepts explicitly named regular UTF-8 files, emits one schema-valid JSON object, and does not write files or contact network services.

See [`docs/validator/USAGE.md`](docs/validator/USAGE.md) for the library interface, outcome definitions, and error taxonomy.

## Relationship to Sovereign OS

BKI and Sovereign OS are independent repositories with complementary responsibilities:

- BKI validates knowledge artifacts and produces provenance-rich validation evidence.
- Sovereign OS determines whether a candidate may cross an explicit admission or authority boundary and whether any governed state transition is permitted.

The active read-only-beta `bki.sovereign.profile.v1` contract aligns selected metadata without collapsing those responsibilities. BKI quarantine is validation evidence, not a Sovereign disposition. BKI success does not authorize registry mutation, evidence admission, promotion, capability creation, tool execution, or any other effect.

Compatibility or integration becomes active only through its own pinned, reviewed, tested, and explicitly approved gate.

### Current cross-repository status

Sovereign OS now has an experimental `AGENT-BETA-018` runtime path that can accept candidate proposals from OpenAI-compatible local models, negotiate capabilities, bind grants to exact targets and records, and verify execution replay deterministically. This strengthens the consumer boundary; it does not expand BKI's authority.

The safe integration route remains:

```text
BKI validation result
        |
        v
Sovereign observation / evidence
        |
        v
independent policy evaluation
        |
        v
Sovereign capability registry
```

A BKI result cannot sign a policy evaluation, create or consume a capability grant, authorize a tool, or execute an effect. The `bki.sovereign.profile.v1` profile is activated only for the pinned read-only beta boundary defined in [`docs/integration/BKI-SOS-BETA-001.md`](docs/integration/BKI-SOS-BETA-001.md) and [`docs/integration/BKI-SOS-PROFILE-001.md`](docs/integration/BKI-SOS-PROFILE-001.md).

The Sovereign cross-repository suite passed locally on Windows against the
exact pinned BKI runtime commit. The activated release is
`bki-sovereign-v1.0.0-beta.1`; release CI verifies the same boundary on Windows
and Linux.

## Engineering Rules

- Architecture and governed contracts define the implementation boundary.
- Validation must remain deterministic and reproducible.
- Unknown profiles, malformed inputs, metadata collisions, and unauthorized deltas fail closed.
- Protected content must not be altered implicitly.
- Evidence generation must remain separate from promotion and effect authority.
- Repository changes proceed through bounded branches, review, and cross-platform verification.
