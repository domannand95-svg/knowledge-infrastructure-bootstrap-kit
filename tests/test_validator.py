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
