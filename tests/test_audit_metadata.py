from datetime import datetime, timezone

import pytest

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.validator import NormalizationValidator


VALID_DOCUMENT = """---
document_id: AUDIT-TEST-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-10
---

# Audit Metadata Fixture
"""


FIXED_TIME = datetime(2026, 8, 10, 14, 30, tzinfo=timezone.utc)


def test_compliant_result_contains_governed_audit_metadata():
    validator = NormalizationValidator(clock=lambda: FIXED_TIME)

    result = validator.validate(VALID_DOCUMENT, VALID_DOCUMENT)

    assert result.audit_metadata is not None
    assert result.audit_metadata.executed_at_utc == "2026-08-10T14:30:00Z"
    assert result.audit_metadata.validator_version == "VAL-001 v1.0-pilot"
    assert result.audit_metadata.source_document_id == "AUDIT-TEST-001"
    assert result.audit_metadata.candidate_document_id == "AUDIT-TEST-001"
    assert result.audit_metadata.outcome == ValidationOutcome.COMPLIANT
    assert result.audit_metadata.error_code == ErrorCode.NONE


def test_legacy_source_identifier_is_preserved_in_audit_metadata():
    validator = NormalizationValidator(clock=lambda: FIXED_TIME)
    source = VALID_DOCUMENT.replace("document_id:", "Document ID:")

    result = validator.validate(source, VALID_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.audit_metadata is not None
    assert result.audit_metadata.source_document_id == "AUDIT-TEST-001"
    assert result.audit_metadata.candidate_document_id == "AUDIT-TEST-001"


def test_parse_failure_audit_metadata_records_partial_identity():
    validator = NormalizationValidator(clock=lambda: FIXED_TIME)

    result = validator.validate(VALID_DOCUMENT, "\ufeff" + VALID_DOCUMENT)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.audit_metadata is not None
    assert result.audit_metadata.source_document_id == "AUDIT-TEST-001"
    assert result.audit_metadata.candidate_document_id is None
    assert result.audit_metadata.outcome == ValidationOutcome.QUARANTINE
    assert result.audit_metadata.error_code == ErrorCode.ERR_FM_SYNTAX


def test_naive_audit_clock_is_rejected():
    validator = NormalizationValidator(
        clock=lambda: datetime(2026, 8, 10, 14, 30),
    )

    with pytest.raises(
        ValueError,
        match="Audit clock must return a timezone-aware datetime",
    ):
        validator.validate(VALID_DOCUMENT, VALID_DOCUMENT)
