import pytest

from tooling.normalization.models import ErrorCode, ValidationOutcome
from tooling.normalization.validator import NormalizationValidator


CANDIDATE = """---
document_id: HEADING-001
version: 1.0
status: Test Fixture
last_revised: 2026-08-10
---

# Heading Fixture

## Governed Section

Stable prose.
"""


@pytest.mark.parametrize(
    "visual_heading",
    ["*Governed Section*", "_Governed Section_"],
)
def test_standalone_italic_heading_conversion_is_authorized(visual_heading):
    source = CANDIDATE.replace("## Governed Section", visual_heading)
    result = NormalizationValidator().validate(source, CANDIDATE)

    assert result.outcome == ValidationOutcome.NORMALIZED
    assert result.error_code == ErrorCode.NONE
    assert "BODY_LINE|AUTHORIZED|line=4;class=VISUAL_STYLING_REMOVAL" in (
        result.classification_log
    )
    assert "BODY_LINE|AUTHORIZED|line=4;class=HEADING_SYNTAX_INJECTION" in (
        result.classification_log
    )


@pytest.mark.parametrize(
    "source_heading",
    [
        "*Governed sentence.*",
        "_Governed sentence._",
        "Prefix *Governed Section* suffix",
        "* Governed Section",
    ],
)
def test_ambiguous_italic_or_list_syntax_is_quarantined(source_heading):
    source = CANDIDATE.replace("## Governed Section", source_heading)
    result = NormalizationValidator().validate(source, CANDIDATE)

    assert result.outcome == ValidationOutcome.QUARANTINE
    assert result.error_code in {
        ErrorCode.ERR_PROSE_MUTATION,
        ErrorCode.ERR_UNAUTHORIZED_DELTA,
    }
