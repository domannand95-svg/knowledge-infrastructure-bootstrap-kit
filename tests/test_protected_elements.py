import pytest

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.parser import DeterministicParser
from tooling.normalization.validator import NormalizationValidator


PROTECTED_DOCUMENT = """---
document_id: PROTECTED-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-10
---

# Protected Elements

## Examples

Use `stable_command` with https://example.com/reference and [REF-001].

| Field | Value |
| --- | --- |
| mode | deterministic |
"""


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("stable_command", "changed_command"),
        ("https://example.com/reference", "https://example.org/reference"),
        ("[REF-001]", "[REF-002]"),
        ("| mode | deterministic |", "| mode | heuristic |"),
    ],
)
def test_typed_protected_element_mutation_is_quarantined(before, after):
    candidate = PROTECTED_DOCUMENT.replace(before, after)
    result = NormalizationValidator().validate(
        PROTECTED_DOCUMENT,
        candidate,
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT
    assert result.classification_log[-2:] == [
        "PROTECTED_CONTENT|REJECTED|error=ERR_PROTECTED_CONTENT",
        "FINAL|QUARANTINE|error=ERR_PROTECTED_CONTENT",
    ]


def test_protected_element_types_and_order_are_deterministic():
    parser = DeterministicParser()

    first = parser.parse(PROTECTED_DOCUMENT, is_candidate=True)
    second = parser.parse(PROTECTED_DOCUMENT, is_candidate=True)

    assert first.protected_elements == second.protected_elements
    assert [element.element_type for element in first.protected_elements] == [
        "INLINE_CODE",
        "URL",
        "CITATION_KEY",
        "TABLE",
    ]


def test_authorized_heading_change_preserves_typed_elements():
    source = PROTECTED_DOCUMENT.replace("## Examples", "**Examples**")
    result = NormalizationValidator().validate(source, PROTECTED_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert any(
        event.startswith("PROTECTED_CONTENT|PRESERVED|")
        for event in result.classification_log
    )
