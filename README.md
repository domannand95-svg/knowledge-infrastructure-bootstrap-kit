# Knowledge Infrastructure Bootstrap Kit

The Knowledge Infrastructure Bootstrap Kit (`BKI-001`) is an evidence-governed framework for commissioning, governing, operating, validating, and developing durable knowledge infrastructure.

## Current baseline

- Framework version: BKI-001 v1.2
- Phase: Validator Commissioning Complete
- Engineering focus: Governed integration readiness
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
result does not authorize automatic repository write-back or external AI
integration.
