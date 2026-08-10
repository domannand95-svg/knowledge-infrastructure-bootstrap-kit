from pathlib import Path

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.validator import NormalizationValidator


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
