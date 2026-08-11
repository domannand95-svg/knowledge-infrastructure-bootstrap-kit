import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    REPO_ROOT / "docs" / "integration" / "bki-validation-result-v1.schema.json"
)


def _document(title: str = "Title") -> str:
    return (
        "---\n"
        "document_id: TEST-001\n"
        "version: 1.0\n"
        "status: Draft\n"
        "last_revised: 2026-08-11\n"
        "---\n\n"
        f"# {title}\n\n"
        "Stable prose.\n"
    )


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tooling.normalization.cli", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=10,
    )


def test_cli_module_has_no_mutation_network_or_process_capabilities():
    cli_path = REPO_ROOT / "tooling" / "normalization" / "cli.py"
    tree = ast.parse(cli_path.read_text(encoding="utf-8"))
    imported_roots = set()
    attribute_calls = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            attribute_calls.add(node.func.attr)

    assert imported_roots <= {
        "__future__",
        "argparse",
        "os",
        "pathlib",
        "sys",
        "urllib",
        "models",
        "validator",
    }
    assert attribute_calls.isdisjoint(
        {
            "connect",
            "mkdir",
            "open",
            "popen",
            "remove",
            "rename",
            "replace",
            "request",
            "rmdir",
            "run",
            "system",
            "unlink",
            "write_bytes",
            "write_text",
        }
    )


def test_cli_emits_exact_schema_valid_contract_without_writes(tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    source_bytes = _document().encode("utf-8")
    source = tmp_path / "source.md"
    candidate = tmp_path / "candidate.md"
    source.write_bytes(source_bytes)
    candidate.write_bytes(source_bytes)
    before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}

    completed = _run_cli(
        "--source",
        str(source),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout.count("\n") == 1
    payload = json.loads(completed.stdout)
    jsonschema.Draft202012Validator(
        json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        format_checker=jsonschema.FormatChecker(),
    ).validate(payload)
    assert payload["contract_version"] == "bki.validation.v1"
    assert payload["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert payload["candidate_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before


def test_cli_quarantine_is_json_evidence_and_exit_two(tmp_path):
    source = tmp_path / "source.md"
    candidate = tmp_path / "candidate.md"
    source.write_text(_document(), encoding="utf-8")
    candidate.write_text(_document("Changed"), encoding="utf-8")

    completed = _run_cli(
        "--source",
        str(source),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    )

    assert completed.returncode == 2
    assert completed.stderr == ""
    assert json.loads(completed.stdout)["outcome"] == "FAIL — QUARANTINE"


@pytest.mark.parametrize(
    "arguments",
    [
        ("--source", "https://example.invalid/source.md"),
        ("--format", "bki.validation.v2"),
    ],
)
def test_cli_fails_closed_for_url_or_unknown_contract(tmp_path, arguments):
    source = tmp_path / "source.md"
    candidate = tmp_path / "candidate.md"
    source.write_text(_document(), encoding="utf-8")
    candidate.write_text(_document(), encoding="utf-8")
    args = [
        "--source",
        str(source),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    ]
    option, value = arguments
    args[args.index(option) + 1] = value

    completed = _run_cli(*args)

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert completed.stderr.startswith("BKI invocation failure:")


def test_cli_rejects_directory_and_invalid_utf8(tmp_path):
    candidate = tmp_path / "candidate.md"
    candidate.write_bytes(b"\xff")

    directory_result = _run_cli(
        "--source",
        str(tmp_path),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    )
    encoding_result = _run_cli(
        "--source",
        str(candidate),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    )

    assert directory_result.returncode == 3
    assert directory_result.stdout == ""
    assert encoding_result.returncode == 3
    assert encoding_result.stdout == ""


def test_cli_rejects_symbolic_link_when_supported(tmp_path):
    target = tmp_path / "source.md"
    link = tmp_path / "source-link.md"
    candidate = tmp_path / "candidate.md"
    target.write_text(_document(), encoding="utf-8")
    candidate.write_text(_document(), encoding="utf-8")
    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("Symbolic links are unavailable in this environment.")

    completed = _run_cli(
        "--source",
        str(link),
        "--candidate",
        str(candidate),
        "--format",
        "bki.validation.v1",
    )

    assert completed.returncode == 3
    assert completed.stdout == ""
    assert "link or junction" in completed.stderr
