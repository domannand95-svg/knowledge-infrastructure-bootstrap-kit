"""Fail-closed metadata translation for ``bki.sovereign.profile.v1``."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import yaml


PROFILE_VERSION = "bki.sovereign.profile.v1"
SOURCE_FORMATS = {
    "bki.md001.v1": {
        "document_id": "document_id",
        "version": "version",
        "status": "status",
        "last_revised": "last_revised",
        "namespace": "bki",
        "forbidden": {"ID", "Version", "Status", "Last Updated"},
    },
    "sovereign.document.v1": {
        "document_id": "ID",
        "version": "Version",
        "status": "Status",
        "last_revised": "Last Updated",
        "namespace": "sovereign",
        "forbidden": {"document_id", "version", "status", "last_revised"},
    },
}
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
FULL_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class ProfileTranslationError(ValueError):
    """Raised when metadata cannot be translated without ambiguity."""


class _UniqueKeyLoader(yaml.BaseLoader):
    pass


def _construct_unique_mapping(loader, node, deep=False):
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ProfileTranslationError(f"Duplicate metadata key: {key}.")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _load_frontmatter(markdown: str) -> dict[str, Any]:
    match = FRONTMATTER.match(markdown)
    if match is None:
        raise ProfileTranslationError("Missing or malformed YAML frontmatter.")

    try:
        loaded = yaml.load(match.group(1), Loader=_UniqueKeyLoader)
    except ProfileTranslationError:
        raise
    except yaml.YAMLError as exc:
        raise ProfileTranslationError("Invalid YAML frontmatter.") from exc

    if not isinstance(loaded, dict):
        raise ProfileTranslationError("Frontmatter must be a mapping.")
    if not all(isinstance(key, str) for key in loaded):
        raise ProfileTranslationError("Frontmatter keys must be strings.")
    return loaded


def _required_scalar(metadata: dict[str, Any], key: str) -> str:
    if key not in metadata:
        raise ProfileTranslationError(f"Missing required metadata key: {key}.")
    value = metadata[key]
    if not isinstance(value, str) or not value.strip():
        raise ProfileTranslationError(
            f"Metadata key {key} must contain one non-empty scalar value."
        )
    return value


def translate_frontmatter(
    markdown: str,
    *,
    source_format: str,
    profile_version: str = PROFILE_VERSION,
) -> dict[str, Any]:
    """Translate one explicitly identified vocabulary into the shared profile."""
    if profile_version != PROFILE_VERSION:
        raise ProfileTranslationError(
            f"Unsupported compatibility profile: {profile_version}."
        )
    if source_format not in SOURCE_FORMATS:
        raise ProfileTranslationError(f"Unsupported source format: {source_format}.")

    metadata = _load_frontmatter(markdown)
    mapping = SOURCE_FORMATS[source_format]
    collisions = sorted(mapping["forbidden"].intersection(metadata))
    if collisions:
        raise ProfileTranslationError(
            "Mixed metadata vocabularies are forbidden: " + ", ".join(collisions)
        )

    document_id = _required_scalar(metadata, mapping["document_id"])
    version = _required_scalar(metadata, mapping["version"])
    status = _required_scalar(metadata, mapping["status"])
    last_revised = _required_scalar(metadata, mapping["last_revised"])

    if not FULL_DATE.fullmatch(last_revised):
        raise ProfileTranslationError("Revision date must use YYYY-MM-DD.")
    try:
        date.fromisoformat(last_revised)
    except ValueError as exc:
        raise ProfileTranslationError("Revision date is not a real date.") from exc

    return {
        "profile_version": PROFILE_VERSION,
        "document_id": document_id,
        "version": version,
        "status": {
            "namespace": mapping["namespace"],
            "value": status,
        },
        "last_revised": last_revised,
    }
