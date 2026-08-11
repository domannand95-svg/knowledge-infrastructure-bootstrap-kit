"""Read-only command-line boundary for the deterministic BKI validator."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from .models import ValidationOutcome
from .validator import NormalizationValidator


CONTRACT_VERSION = "bki.validation.v1"
EXIT_PASS = 0
EXIT_QUARANTINE = 2
EXIT_INVOCATION_FAILURE = 3


class InvocationError(ValueError):
    """Raised when input cannot safely cross the CLI boundary."""


def _looks_like_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and (parsed.netloc or parsed.scheme == "file"))


def _contains_link_or_junction(path: Path) -> bool:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)

    for part in absolute.parts[1:]:
        current /= part
        if not current.exists():
            continue
        if current.is_symlink():
            return True
        if hasattr(current, "is_junction") and current.is_junction():
            return True

    return False


def _read_input(value: str, label: str) -> str:
    if _looks_like_url(value):
        raise InvocationError(f"{label} must be a local file path, not a URL.")

    path = Path(value)
    if _contains_link_or_junction(path):
        raise InvocationError(f"{label} must not traverse a link or junction.")
    if not path.exists():
        raise InvocationError(f"{label} does not exist.")
    if not path.is_file():
        raise InvocationError(f"{label} must be a regular file.")

    try:
        return path.read_bytes().decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise InvocationError(f"{label} must be valid UTF-8.") from exc
    except OSError as exc:
        raise InvocationError(f"{label} could not be read.") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate two local Markdown files without modifying them."
    )
    parser.add_argument("--source", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--format", required=True, dest="contract_format")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return EXIT_PASS if exc.code == 0 else EXIT_INVOCATION_FAILURE

    try:
        if args.contract_format != CONTRACT_VERSION:
            raise InvocationError(
                f"Unsupported result format: {args.contract_format}."
            )

        source_text = _read_input(args.source, "source")
        candidate_text = _read_input(args.candidate, "candidate")
        result = NormalizationValidator().validate(source_text, candidate_text)
        sys.stdout.buffer.write(
            (result.to_contract_json() + "\n").encode("utf-8")
        )
        return (
            EXIT_QUARANTINE
            if result.outcome is ValidationOutcome.QUARANTINE
            else EXIT_PASS
        )
    except InvocationError as exc:
        sys.stderr.write(f"BKI invocation failure: {exc}\n")
        return EXIT_INVOCATION_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
