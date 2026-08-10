from pathlib import Path

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.validator import NormalizationValidator


VALID_DOCUMENT = """---
document_id: EDGE-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-10
---

# Edge Case

## Section

Stable prose with https://example.com/reference and citation [REF-001].
"""


def test_tc_val_001_compliant_document():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_001"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.COMPLIANT
    assert result.error_code == ErrorCode.NONE
    assert result.diff == ""


def test_tc_val_008_legacy_metadata_migration():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_008"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert result.diff != ""
    assert "document_id" in result.diff


def test_tc_val_002_heading_normalization():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_002"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert result.diff != ""


def test_tc_val_003_prose_mutation():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_003"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROSE_MUTATION


def test_tc_val_004_code_block_tampering():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_004"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT


def test_tc_val_005_heading_hierarchy_violation():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_005"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_HEADING_NEST


def test_tc_val_006_metadata_sabotage():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_006"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT


def test_tc_val_007_phantom_heading():
    validator = NormalizationValidator()

    fixture_dir = Path(__file__).parent / "fixtures" / "tc_val_007"

    source = (fixture_dir / "source.md").read_text(encoding="utf-8")
    candidate = (fixture_dir / "candidate.md").read_text(encoding="utf-8")

    result = validator.validate(source, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_UNAUTHORIZED_DELTA


def test_legacy_source_bom_is_normalized_safely():
    result = NormalizationValidator().validate(
        "\ufeff" + VALID_DOCUMENT,
        VALID_DOCUMENT,
    )

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE


def test_candidate_bom_is_quarantined():
    result = NormalizationValidator().validate(
        VALID_DOCUMENT,
        "\ufeff" + VALID_DOCUMENT,
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_FM_SYNTAX


def test_candidate_crlf_is_quarantined():
    result = NormalizationValidator().validate(
        VALID_DOCUMENT,
        VALID_DOCUMENT.replace("\n", "\r\n"),
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_UNAUTHORIZED_DELTA


def test_missing_required_frontmatter_key_is_quarantined():
    candidate = VALID_DOCUMENT.replace("status: Test Fixture\n", "")
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_FM_SYNTAX


def test_malformed_frontmatter_yaml_is_quarantined():
    candidate = VALID_DOCUMENT.replace(
        "status: Test Fixture",
        "status: [unterminated",
    )
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_FM_SYNTAX


def test_multiple_h1_headings_are_quarantined():
    candidate = VALID_DOCUMENT.replace(
        "## Section",
        "# Second Primary Heading",
    )
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_H1_VIOLATION


def test_skipped_heading_depth_is_quarantined():
    candidate = VALID_DOCUMENT.replace("## Section", "### Section")
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_HEADING_NEST


def test_unclosed_fenced_code_block_is_quarantined():
    candidate = VALID_DOCUMENT + "\n```python\nprint('protected')\n"
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT


def test_url_mutation_is_quarantined():
    candidate = VALID_DOCUMENT.replace("example.com", "example.org")
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROSE_MUTATION


def test_citation_mutation_is_quarantined():
    candidate = VALID_DOCUMENT.replace("[REF-001]", "[REF-002]")
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROSE_MUTATION


def test_compliant_result_has_deterministic_classification_log():
    validator = NormalizationValidator()

    first = validator.validate(VALID_DOCUMENT, VALID_DOCUMENT)
    second = validator.validate(VALID_DOCUMENT, VALID_DOCUMENT)

    assert first.classification_log == [
        "DELTA|NONE|prepared_source_and_candidate_identical",
        "FINAL|COMPLIANT|error=NONE",
    ]
    assert second.classification_log == first.classification_log


def test_heading_normalization_log_identifies_authorized_line():
    source = VALID_DOCUMENT.replace("## Section", "**Section**")
    result = NormalizationValidator().validate(source, VALID_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.classification_log == [
        "BODY_LINE|AUTHORIZED|"
        "line=4;class=HEADING_SYNTAX_INJECTION",
        "FINAL|NORMALIZED|error=NONE",
    ]


def test_legacy_preparation_and_metadata_migration_are_logged():
    source = (
        "\ufeff"
        + VALID_DOCUMENT.replace("document_id:", "Document ID:")
        .replace("version:", "Version:")
        .replace("status:", "Status:")
        .replace("last_revised:", "Last Revised:")
    )
    result = NormalizationValidator().validate(source, VALID_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.classification_log == [
        "SOURCE_PREPARATION|AUTHORIZED|"
        "class=LEGACY_INPUT_NORMALIZATION",
        "METADATA|AUTHORIZED|class=KEY_STANDARDIZATION;"
        "source=Document ID;candidate=document_id",
        "METADATA|AUTHORIZED|class=KEY_STANDARDIZATION;"
        "source=Last Revised;candidate=last_revised",
        "METADATA|AUTHORIZED|class=KEY_STANDARDIZATION;"
        "source=Status;candidate=status",
        "METADATA|AUTHORIZED|class=KEY_STANDARDIZATION;"
        "source=Version;candidate=version",
        "BODY|NONE|no_body_delta",
        "FINAL|NORMALIZED|error=NONE",
    ]


def test_quarantine_log_identifies_rejected_line_and_final_error():
    candidate = VALID_DOCUMENT.replace("example.com", "example.org")
    result = NormalizationValidator().validate(VALID_DOCUMENT, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.classification_log == [
        "BODY_LINE|REJECTED|line=6;error=ERR_PROSE_MUTATION",
        "FINAL|QUARANTINE|error=ERR_PROSE_MUTATION",
    ]


def test_parse_failure_log_identifies_error_and_final_outcome():
    result = NormalizationValidator().validate(
        VALID_DOCUMENT,
        "\ufeff" + VALID_DOCUMENT,
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.classification_log == [
        "PARSE|REJECTED|error=ERR_FM_SYNTAX",
        "FINAL|QUARANTINE|error=ERR_FM_SYNTAX",
    ]
