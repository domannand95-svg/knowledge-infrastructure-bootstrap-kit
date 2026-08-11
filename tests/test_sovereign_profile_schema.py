import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (
        ROOT
        / "docs"
        / "integration"
        / "bki-sovereign-profile-v1.schema.json"
    ).read_text(encoding="utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
FIXTURES = ROOT / "tests" / "fixtures" / "integration"


@pytest.mark.parametrize(
    "fixture_name",
    ["profile-v1-bki.json", "profile-v1-sovereign.json"],
)
def test_profile_accepts_namespaced_repository_metadata(fixture_name):
    record = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))

    VALIDATOR.validate(record)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("profile_version", "bki.sovereign.profile.v2"),
        ("document_id", ""),
        ("version", ""),
        ("last_revised", "11/08/2026"),
    ],
)
def test_profile_rejects_unknown_or_ambiguous_core_values(field, value):
    record = json.loads(
        (FIXTURES / "profile-v1-sovereign.json").read_text(encoding="utf-8")
    )
    record[field] = value

    assert list(VALIDATOR.iter_errors(record))


def test_profile_rejects_unknown_status_namespace():
    record = json.loads(
        (FIXTURES / "profile-v1-sovereign.json").read_text(encoding="utf-8")
    )
    record["status"]["namespace"] = "shared"

    assert list(VALIDATOR.iter_errors(record))


def test_profile_rejects_fields_that_could_smuggle_authority():
    record = json.loads(
        (FIXTURES / "profile-v1-sovereign.json").read_text(encoding="utf-8")
    )
    record["promotion_authorized"] = True

    assert list(VALIDATOR.iter_errors(record))
