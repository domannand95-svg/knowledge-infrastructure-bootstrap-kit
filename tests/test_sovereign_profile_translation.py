import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from tooling.integration import ProfileTranslationError, translate_frontmatter


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (
    ROOT / "tests" / "fixtures" / "integration" / "sovereign-document.md"
).read_text(encoding="utf-8")
SCHEMA = json.loads(
    (
        ROOT
        / "docs"
        / "integration"
        / "bki-sovereign-profile-v1.schema.json"
    ).read_text(encoding="utf-8")
)


def test_sovereign_frontmatter_translates_to_schema_valid_profile():
    translated = translate_frontmatter(
        FIXTURE,
        source_format="sovereign.document.v1",
    )

    Draft202012Validator(
        SCHEMA,
        format_checker=FormatChecker(),
    ).validate(translated)
    assert translated == {
        "profile_version": "bki.sovereign.profile.v1",
        "document_id": "SPEC-EV-001",
        "version": "0.1",
        "status": {"namespace": "sovereign", "value": "Proposed"},
        "last_revised": "2026-08-11",
    }


def test_bki_frontmatter_preserves_literal_values_and_namespace():
    markdown = """---
document_id: BKI-SOS-BETA-001
version: 1.0
status: Proposed Beta Contract
last_revised: 2026-08-11
---

# Contract
"""

    translated = translate_frontmatter(markdown, source_format="bki.md001.v1")

    assert translated["version"] == "1.0"
    assert translated["status"] == {
        "namespace": "bki",
        "value": "Proposed Beta Contract",
    }


@pytest.mark.parametrize(
    "source_format",
    ["", "sovereign.document.v2", "automatic"],
)
def test_unknown_or_implicit_source_format_fails_closed(source_format):
    with pytest.raises(ProfileTranslationError, match="source format"):
        translate_frontmatter(FIXTURE, source_format=source_format)


def test_unknown_profile_version_fails_closed():
    with pytest.raises(ProfileTranslationError, match="profile"):
        translate_frontmatter(
            FIXTURE,
            source_format="sovereign.document.v1",
            profile_version="bki.sovereign.profile.v2",
        )


@pytest.mark.parametrize("canonical_key", ["document_id", "version", "status", "last_revised"])
def test_mixed_vocabularies_fail_even_when_values_match(canonical_key):
    value = {
        "document_id": "SPEC-EV-001",
        "version": "0.1",
        "status": "Proposed",
        "last_revised": "2026-08-11",
    }[canonical_key]
    mixed = FIXTURE.replace("---\n\n#", f"{canonical_key}: {value}\n---\n\n#")

    with pytest.raises(ProfileTranslationError, match="Mixed"):
        translate_frontmatter(mixed, source_format="sovereign.document.v1")


def test_duplicate_source_key_fails_closed():
    duplicate = FIXTURE.replace("ID: SPEC-EV-001", "ID: SPEC-EV-001\nID: OTHER")

    with pytest.raises(ProfileTranslationError, match="Duplicate"):
        translate_frontmatter(duplicate, source_format="sovereign.document.v1")


@pytest.mark.parametrize(
    "replacement",
    [
        "Last Updated: 11/08/2026",
        "Last Updated: 2026-02-30",
        "Last Updated:",
        "Last Updated:\n  - 2026-08-11",
    ],
)
def test_invalid_revision_values_fail_closed(replacement):
    invalid = FIXTURE.replace("Last Updated: 2026-08-11", replacement)

    with pytest.raises(ProfileTranslationError):
        translate_frontmatter(invalid, source_format="sovereign.document.v1")


def test_missing_identity_fails_closed():
    missing = FIXTURE.replace("ID: SPEC-EV-001\n", "")

    with pytest.raises(ProfileTranslationError, match="Missing"):
        translate_frontmatter(missing, source_format="sovereign.document.v1")
