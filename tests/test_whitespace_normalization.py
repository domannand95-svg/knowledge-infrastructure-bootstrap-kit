import pytest

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.validator import NormalizationValidator


CANONICAL_DOCUMENT = (
    """---
document_id: WS-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-10
---

# Whitespace Fixture

## Section

Stable prose with `inline_code`, https://example.com and [REF-001].

| Field | Value |
| --- | --- |
| mode | stable |

```text
"""
    + "protected trailing spaces  \n"
    + """
protected blank line above
```
"""
)


def test_source_trailing_whitespace_is_authorized_outside_protection():
    source = CANONICAL_DOCUMENT.replace(
        "and [REF-001].",
        "and [REF-001].   ",
    )
    result = NormalizationValidator().validate(source, CANONICAL_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert "BODY|AUTHORIZED|class=TRAILING_WHITESPACE_REMOVAL" in (
        result.classification_log
    )


def test_source_repeated_blank_lines_are_collapsed():
    source = CANONICAL_DOCUMENT.replace(
        "## Section\n\nStable",
        "## Section\n\n\n\nStable",
    )
    result = NormalizationValidator().validate(source, CANONICAL_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert "BODY|AUTHORIZED|class=BLANK_LINE_COLLAPSE" in (
        result.classification_log
    )


def test_offset_shift_preserves_typed_protected_elements():
    source = CANONICAL_DOCUMENT.replace(
        "| Field | Value |",
        "\n\n| Field | Value |",
    )
    result = NormalizationValidator().validate(source, CANONICAL_DOCUMENT)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert any(
        event.startswith("PROTECTED_CONTENT|PRESERVED|")
        for event in result.classification_log
    )


@pytest.mark.parametrize(
    "candidate",
    [
        CANONICAL_DOCUMENT.replace(
            "and [REF-001].",
            "and [REF-001].  ",
        ),
        CANONICAL_DOCUMENT.replace(
            "## Section\n\nStable",
            "## Section\n\n\nStable",
        ),
    ],
)
def test_noncanonical_candidate_whitespace_is_quarantined(candidate):
    result = NormalizationValidator().validate(candidate, candidate)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_UNAUTHORIZED_DELTA


def test_fenced_code_whitespace_remains_protected():
    candidate = CANONICAL_DOCUMENT.replace(
        "protected trailing spaces  ",
        "protected trailing spaces",
    )
    result = NormalizationValidator().validate(
        CANONICAL_DOCUMENT,
        candidate,
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT


def test_table_whitespace_remains_protected():
    candidate = CANONICAL_DOCUMENT.replace(
        "| mode | stable |",
        "| mode  | stable |",
    )
    result = NormalizationValidator().validate(
        CANONICAL_DOCUMENT,
        candidate,
    )

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code == ErrorCode.ERR_PROTECTED_CONTENT
