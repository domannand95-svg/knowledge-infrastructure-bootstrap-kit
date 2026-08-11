# Knowledge Infrastructure Bootstrap Kit

The Knowledge Infrastructure Bootstrap Kit (`BKI-001`) is an evidence-governed framework for commissioning, governing, operating, validating, and developing durable knowledge infrastructure.

## Current baseline

- Framework version: BKI-001 v1.2
- Phase: Validator commissioning complete; read-only integration boundary operational
- Engineering focus: Private beta readiness and contract stability
- MD-001 v1.0: frozen initial pilot specification
- VAL-001 v1.0: frozen initial pilot specification

## Repository map

- `docs/master/` — authoritative framework index
- `docs/governance/` — governance and structural standards
- `docs/architecture/` — project-neutral architecture decisions
- `docs/ai/` — governed AI operations material
- `docs/commissioning/` — commissioning specifications, findings, experiments, and validator records
- `tooling/normalization/` — deterministic parser, classifier, and validator
- `tests/` — validator test suite and fixtures
- `reconciliation/` — baseline authority and scope record

## Implemented validator boundary

The current validator provides:

- deterministic Markdown classification and validation;
- governed whitespace normalization with protected code, table, URL, and
  citation boundaries;
- itemized classification logging;
- typed protected-region handling;
- the versioned `bki.validation.v1` JSON command-line contract;
- fail-closed translation of unknown or incomplete validation states; and
- read-only operation with repository write-back and promotion outside its
  authority.

Sovereign OS pins a reviewed BKI revision and exercises this contract in live
Windows and Linux CI through a read-only deploy key. The repositories remain
independently testable and communicate through the versioned contract rather
than shared internal implementation assumptions.

## Local development

Use Python 3.11 and a project-local virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Model-generated transformations must not bypass deterministic validation. Repository write-back remains outside the authority of the current validator commissioning baseline.

## Contributor workflow

Changes must be made on a branch and submitted to `main` through a pull request.
The protected branch requires one approval, resolved review conversations, and
successful Python 3.11 checks on Windows and Ubuntu.

Before opening or approving a pull request, run:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider
```

The validator is an approval boundary, not a transformer. A passing validation
result does not authorize automatic repository write-back, artifact promotion,
or external AI integration. Human review and all required Windows and Ubuntu
checks must pass before `main` changes.

## Near-term direction

1. Keep `bki.validation.v1` stable and fail closed.
2. Expand adversarial fixtures without weakening protected-region invariants.
3. Maintain Windows and Linux parity.
4. Integrate with Sovereign OS only through explicit, versioned, read-only
   contracts until both projects reach private beta readiness.
