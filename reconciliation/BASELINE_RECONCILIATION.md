# BKI baseline reconciliation

Date: 2026-08-10

Source examined: `C:\Users\doman\OneDrive\Documents\WindowsPowerShell\Knowledge Infrastructure Bootstrap Kit`

## Included

| Artifact family | Role | Authority assessment | Repository destination | Action |
| --- | --- | --- | --- | --- |
| BKI-001 v1.2 | Master governed index | Authoritative active baseline | `docs/master/` | Preserve |
| BKI-003 v1.2 | Project-neutral co-evolution architecture | Candidate baseline pending validation | `docs/governance/` | Preserve with stated status |
| MD-001 v1.0 | Markdown structural specification | Frozen initial pilot | `docs/governance/standards/` | Preserve |
| VAL-001 v1.0 | Deterministic validator specification | Frozen initial pilot | `docs/governance/standards/` | Preserve |
| ADR material | Project-neutral architectural rationale | Governed BKI material | `docs/architecture/` | Preserve Markdown sources |
| Governed AI documents | BKI operational/governance layer | Listed by BKI-001 | `docs/ai/` | Preserve Markdown sources |
| DF-001 through DF-003 | Published commissioning findings | Evidence supporting normalization work | `docs/commissioning/findings/` | Preserve |
| EXP-001 and EXP-003 | Located experiment records | Commissioning evidence | `docs/commissioning/experiments/` | Preserve |
| FP-001 | Deterministic fingerprint scaffold | Provisional tooling associated with fingerprint work | `tooling/fingerprinting/` | Preserve |
| VAL-001 commissioning records | Validator test and closure history | Supporting evidence | `docs/commissioning/validation/` | Preserve |
| Normalization Python implementation | Parser/classifier/validator | Current provisional implementation | `tooling/normalization/` | Preserve |
| TC-VAL-001 through TC-VAL-008 | Validator fixtures and expectations | Current test corpus | `tests/fixtures/` | Preserve |

## Excluded from the repository baseline

- `Archive/`: historical composites, imports, superseded and working material.
- `Projects/`: domain projects, including Sovereign OS and New Waste Order.
- `Sovereign_OS_Adversarial_Agent_Governance_Intake_2026-08-09.md`: provisional Sovereign OS research intake.
- `.md.txt`/`.ps1.txt` companions: duplicate or placeholder transport artifacts requiring no runtime use.
- `.docx` companions: presentation-format duplicates rather than canonical repository sources.
- `.pytest_cache/`, `__pycache__/`, `.pyc`: generated files.
- Prior general workstation logs and recovery material not required to define or reproduce BKI.

## Discrepancies and unresolved history

- EXP-002 and EXP-004 were referenced historically but no corresponding record was located by filename.
- FP-001 exists as a PowerShell scaffold and is preserved; its relationship to the missing EXP-004 record remains historical rather than fully evidenced.
- Historical filenames `00_Knowledge_Governance_Framework.md`, `01_Architecture_Decisions.md`, and `02_Governance_Changelog.md` were not found.
- Both unversioned and v1.2 BKI-003 candidates existed. The explicit v1.2 candidate is retained as the newer governed candidate; the source remains preserved in OneDrive.
- The source corpus remains untouched as recovery evidence.
