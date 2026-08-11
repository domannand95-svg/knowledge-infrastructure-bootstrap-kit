import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from tooling.normalization.models import (
    AuditMetadata,
    ErrorCode,
    ValidationOutcome,
    ValidationResult,
)
from tooling.normalization.validator import NormalizationValidator


FIXED_TIME = datetime(2026, 8, 11, 9, 15, tzinfo=timezone.utc)
VALID_DOCUMENT = """---
document_id: SERIALIZATION-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-11
---

# Serialization Fixture

Stable prose with https://example.com/reference.
"""


@pytest.fixture(scope="module")
def result_schema():
    schema_path = (
        Path(__file__).parents[1]
        / "docs"
        / "integration"
        / "bki-validation-result-v1.schema.json"
    )
    return json.loads(schema_path.read_text(encoding="utf-8"))


def assert_schema_valid(payload, schema):
    Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    ).validate(payload)


def fixed_validator():
    return NormalizationValidator(clock=lambda: FIXED_TIME)


def test_compliant_result_serializes_to_frozen_schema(result_schema):
    result = fixed_validator().validate(VALID_DOCUMENT, VALID_DOCUMENT)
    payload = result.to_contract_dict()

    assert_schema_valid(payload, result_schema)
    assert payload == {
        "contract_version": "bki.validation.v1",
        "validator_version": "VAL-001 v1.0-pilot",
        "executed_at_utc": "2026-08-11T09:15:00Z",
        "source_sha256": hashlib.sha256(
            VALID_DOCUMENT.encode("utf-8")
        ).hexdigest(),
        "candidate_sha256": hashlib.sha256(
            VALID_DOCUMENT.encode("utf-8")
        ).hexdigest(),
        "source_document_id": "SERIALIZATION-001",
        "candidate_document_id": "SERIALIZATION-001",
        "outcome": "PASS — COMPLIANT",
        "error_code": None,
        "classification_log": [
            "DELTA|NONE|prepared_source_and_candidate_identical",
            "FINAL|COMPLIANT|error=NONE",
        ],
        "diff": "",
    }


def test_contract_json_is_canonical_and_repeatable(result_schema):
    first = fixed_validator().validate(VALID_DOCUMENT, VALID_DOCUMENT)
    second = fixed_validator().validate(VALID_DOCUMENT, VALID_DOCUMENT)

    first_json = first.to_contract_json()
    second_json = second.to_contract_json()

    assert first_json == second_json
    assert first_json == json.dumps(
        first.to_contract_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    assert_schema_valid(json.loads(first_json), result_schema)


def test_normalized_result_serializes_with_exact_input_hashes(result_schema):
    source = VALID_DOCUMENT.replace(
        "# Serialization Fixture",
        "**Serialization Fixture**",
    )
    result = fixed_validator().validate(source, VALID_DOCUMENT)
    payload = result.to_contract_dict()

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert payload["source_sha256"] == hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()
    assert payload["candidate_sha256"] == hashlib.sha256(
        VALID_DOCUMENT.encode("utf-8")
    ).hexdigest()
    assert_schema_valid(payload, result_schema)


def test_quarantine_result_serializes_with_error_code(result_schema):
    candidate = VALID_DOCUMENT.replace("example.com", "example.org")
    result = fixed_validator().validate(VALID_DOCUMENT, candidate)
    payload = result.to_contract_dict()

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert payload["error_code"] == "ERR_PROTECTED_CONTENT"
    assert_schema_valid(payload, result_schema)


def test_parse_failure_preserves_hashes_and_partial_identity(result_schema):
    candidate = "\ufeff" + VALID_DOCUMENT
    result = fixed_validator().validate(VALID_DOCUMENT, candidate)
    payload = result.to_contract_dict()

    assert payload["source_document_id"] == "SERIALIZATION-001"
    assert payload["candidate_document_id"] is None
    assert payload["candidate_sha256"] == hashlib.sha256(
        candidate.encode("utf-8")
    ).hexdigest()
    assert_schema_valid(payload, result_schema)


def test_serialization_rejects_result_without_audit_metadata():
    result = ValidationResult(
        outcome=ValidationOutcome.COMPLIANT,
        error_code=ErrorCode.NONE,
        diff="",
    )

    with pytest.raises(
        ValueError,
        match="Audit metadata is required",
    ):
        result.to_contract_dict()


def test_serialization_rejects_inconsistent_audit_metadata():
    result = ValidationResult(
        outcome=ValidationOutcome.COMPLIANT,
        error_code=ErrorCode.NONE,
        diff="",
        audit_metadata=AuditMetadata(
            executed_at_utc="2026-08-11T09:15:00Z",
            validator_version="VAL-001 v1.0-pilot",
            source_sha256="0" * 64,
            candidate_sha256="0" * 64,
            source_document_id="SERIALIZATION-001",
            candidate_document_id="SERIALIZATION-001",
            outcome=ValidationOutcome.QUARANTINE,
            error_code=ErrorCode.ERR_PROSE_MUTATION,
        ),
    )

    with pytest.raises(
        ValueError,
        match="must match the validation outcome and error code",
    ):
        result.to_contract_dict()
