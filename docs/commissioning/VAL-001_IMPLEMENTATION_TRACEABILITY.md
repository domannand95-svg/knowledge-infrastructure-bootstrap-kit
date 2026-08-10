---
document_id: VAL-001-TRACE-001
version: 1.0
status: Commissioning Evidence
last_revised: 2026-08-10
---

# VAL-001 Implementation Traceability

## Purpose

This record maps the frozen `VAL-001 v1.0` pilot specification to the implementation and test evidence present in the canonical BKI repository. It distinguishes verified behavior from partial behavior and unimplemented specification commitments.

The specification remains authoritative. This record does not expand transformation authority or silently redefine incomplete requirements.

## Status Definitions

- **Verified:** Implemented and directly exercised by automated tests.
- **Implemented, untested:** Present in code without focused automated evidence.
- **Partial:** Some required behavior exists, but the complete specified behavior does not.
- **Not implemented:** No corresponding operational behavior exists in the current validator.

## Requirements Traceability

| VAL-001 requirement | Implementation evidence | Test evidence | Status | Required follow-up |
| --- | --- | --- | --- | --- |
| Accept source and candidate Markdown inputs | `NormalizationValidator.validate` | All 18 tests | Verified | None |
| Return exactly one deterministic outcome | `ValidationOutcome` and `NormalizationValidator.validate` | TC-VAL-001–008 and edge matrix | Verified | None |
| Produce a unified source/candidate diff | `difflib.unified_diff` in `validator.py` | TC-VAL-001, TC-VAL-002, TC-VAL-008 | Verified | Add focused quarantine-diff assertions later |
| Produce an itemized classification log | `ValidationResult.classification_log` exists but is never populated | None | Not implemented | Define deterministic log schema before implementation |
| Produce audit metadata | No result field or audit record exists | None | Not implemented | Govern version, timestamp, and identifier schema first |
| Legacy-tolerant source frontmatter parse | `DeterministicParser._prepare_source` and source YAML parse | TC-VAL-008; legacy BOM test | Verified | Add legacy-key boundary cases if required |
| Strict candidate frontmatter and required keys | `DeterministicParser.parse` | Missing-key, malformed-YAML, candidate-BOM tests | Verified | None |
| Exactly one H1 after the required blank line | `body_raw.startswith` and H1 count | TC-VAL-001; multiple-H1 test | Verified | Add zero-H1 focused test |
| Sequential heading nesting | AST heading traversal in `parser.py` | TC-VAL-005; skipped-depth test | Verified | None |
| Preserve fenced code blocks | Markdown AST fence extraction and ordered comparison | TC-VAL-004; unclosed-fence test | Verified | Add multiple-fence ordering case |
| Preserve YAML values | Normalized source/candidate frontmatter dictionary comparison | TC-VAL-006 | Verified | None |
| Preserve inline code as a typed protected element | No inline-code extraction | Mutation may be rejected only by general prose rules | Not implemented | Add typed extraction and focused tests |
| Preserve tables as typed protected elements | No table extraction | None | Not implemented | Select a GFM-capable parse contract before implementation |
| Preserve URLs as typed protected elements | No URL extraction | URL mutation rejected as `ERR_PROSE_MUTATION` | Partial | Add typed extraction if `ERR_PROTECTED_CONTENT` is required |
| Preserve citation keys as typed protected elements | No citation extraction | Citation mutation rejected as `ERR_PROSE_MUTATION` | Partial | Define citation grammar, then add typed extraction |
| Allow bold visual-heading conversion | `DeltaClassifier._verify_heading_conversion` | TC-VAL-002 | Verified | None |
| Allow italic visual-heading conversion | Classifier recognizes only `**...**` source headings | None | Not implemented | Specify ambiguity rules for `*` and `_` before implementation |
| Allow trailing-whitespace normalization | No explicit authorized-delta implementation | None | Not implemented | Add protected-boundary-aware classifier behavior and tests |
| Allow blank-line normalization | Equal line counts and unchanged surrounding lines are currently required | None | Not implemented | Define exact bounded transformations first |
| Harmonize source line endings to LF | Source preparation normalizes CRLF/CR; candidates require LF | Candidate CRLF and legacy-source tests | Verified for current strict-candidate interpretation | Reconcile wording between MD-001 and VAL-001 |
| Permit legacy metadata-key migration only | `LEGACY_METADATA_MAP` and metadata comparison | TC-VAL-008 | Verified | None |
| Reject prose mutation | `DeltaClassifier._is_running_prose_mutation` | TC-VAL-003; URL and citation mutation tests | Verified | None |
| Reject unauthorized structural changes | Delta classification fail-closed behavior | TC-VAL-007 | Verified | Add more line-cardinality cases |
| Reject unclosed fenced code blocks | Candidate fence-balance validation | Unclosed-fence test | Verified | Add tilde and variable-length fence cases |

## Commissioning Assessment

The validator is a functioning deterministic pilot with verified core outcomes, strict candidate parsing, heading checks, fenced-code protection, metadata protection, and fail-closed prose classification. It is not yet a complete implementation of every output and protected-element commitment in `VAL-001 v1.0`.

The largest closure gaps are:

1. deterministic classification logs;
2. governed audit metadata;
3. typed protection for inline code, tables, URLs, and citations;
4. explicitly bounded whitespace normalization; and
5. italic visual-heading conversion rules.

## Recommended Closure Order

1. Reconcile specification wording for candidate line endings and permitted whitespace normalization.
2. Define audit metadata and classification-log schemas without implementing repository write-back.
3. Extend protected-element extraction with focused adversarial tests.
4. Decide whether italic heading conversion remains authorized or should be removed from the next specification revision.
5. Run the complete matrix on Windows and Ubuntu before declaring VAL-001 implementation closure.
