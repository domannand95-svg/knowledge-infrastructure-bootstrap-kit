import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).parents[1]
MANIFEST = json.loads((ROOT / "docs/integration/sovereign-plugin-manifest-v1.schema.json").read_text())
RESULT = json.loads((ROOT / "docs/integration/sovereign-plugin-result-v1.schema.json").read_text())


def valid_manifest():
    return {"plugin_id":"privacy.detect","version":"1.0.0","description":"Local detection","accepted_suffixes":[".md"],"deterministic":True,"network":"denied","requested_capabilities":["filesystem.read"]}


def valid_result():
    return {"contract_version":"sovereign.plugin.result.v1","authority":"none","plugin_id":"privacy.detect","plugin_version":"1.0.0","input_sha256":"a"*64,"status":"candidate","findings":[],"artifacts":[],"requested_actions":[],"errors":[]}


def test_valid_plugin_contracts_are_compatible():
    Draft202012Validator(MANIFEST).validate(valid_manifest())
    Draft202012Validator(RESULT).validate(valid_result())


@pytest.mark.parametrize("field,value", [("network","open"),("plugin_id","shell"),("requested_capabilities",["admin"])])
def test_manifest_authority_confusion_fails_closed(field, value):
    payload = valid_manifest(); payload[field] = value
    with pytest.raises(ValidationError): Draft202012Validator(MANIFEST).validate(payload)


@pytest.mark.parametrize("field,value", [("authority","granted"),("status","authorized"),("contract_version","sovereign.plugin.result.v2"),("input_sha256","0"*63)])
def test_result_authority_or_identity_confusion_fails_closed(field, value):
    payload = valid_result(); payload[field] = value
    with pytest.raises(ValidationError): Draft202012Validator(RESULT).validate(payload)
