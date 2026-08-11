---
document_id: VAL-001-USAGE-001
version: 1.0
status: Operational Guidance
last_revised: 2026-08-10
---

# BKI Deterministic Validator Usage

## Supported Interface

The current validator is a Python library interface. It accepts source and candidate Markdown as strings and returns a `ValidationResult`. No command-line interface, transformer integration, or repository write-back mechanism is currently authorized or provided.

## Environment

From the repository root, create a Python 3.11 virtual environment and install the pinned dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the complete validation test matrix:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider
```

## Library Example

```python
from pathlib import Path

from tooling.normalization.validator import NormalizationValidator

source = Path("source.md").read_text(encoding="utf-8")
candidate = Path("candidate.md").read_text(encoding="utf-8")

result = NormalizationValidator().validate(source, candidate)

print(result.outcome.value)
print(result.error_code.value)
print(result.diff)
```

## Outcomes

- `PASS — COMPLIANT`: source and candidate are identical and the candidate satisfies the enforced structural rules.
- `PASS — NORMALIZED`: differences are classified entirely within the validator’s implemented authorized transformations.
- `FAIL — QUARANTINE`: parsing, structure, protected content, prose, or delta classification failed closed.

## Current Error Codes

| Error code | Meaning |
| --- | --- |
| `ERR_FM_SYNTAX` | Candidate frontmatter, BOM, required keys, or YAML syntax is invalid. |
| `ERR_H1_VIOLATION` | Candidate H1 count or placement is invalid. |
| `ERR_HEADING_NEST` | Candidate headings skip a structural level. |
| `ERR_PROTECTED_CONTENT` | Protected content or metadata changed, or a fenced code block is unclosed. |
| `ERR_PROSE_MUTATION` | Running prose changed. |
| `ERR_UNAUTHORIZED_DELTA` | A difference does not match an implemented authorized transformation. |

## Safety Boundary

Validation results are advisory repository evidence until reviewed by a human operator. The validator does not authorize autonomous write-back, transformer execution, publication, or promotion of quarantined material.

The current implementation populates deterministic classification logs and
immutable audit metadata for every validation result. It enforces the governed
protected-element categories for fenced code, inline code, GFM tables, literal
HTTP/HTTPS URLs, citation keys, and frontmatter metadata. See
`docs/commissioning/VAL-001_IMPLEMENTATION_TRACEABILITY.md` for the complete
implementation evidence and boundary record.
