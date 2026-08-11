from enum import Enum
import json
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List


class ValidationOutcome(Enum):
    COMPLIANT = "PASS — COMPLIANT"
    NORMALIZED = "PASS — NORMALIZED"
    QUARANTINE = "FAIL — QUARANTINE"


class ErrorCode(Enum):
    NONE = None
    ERR_FM_SYNTAX = "ERR_FM_SYNTAX"
    ERR_H1_VIOLATION = "ERR_H1_VIOLATION"
    ERR_HEADING_NEST = "ERR_HEADING_NEST"
    ERR_PROTECTED_CONTENT = "ERR_PROTECTED_CONTENT"
    ERR_PROSE_MUTATION = "ERR_PROSE_MUTATION"
    ERR_UNAUTHORIZED_DELTA = "ERR_UNAUTHORIZED_DELTA"


class ValidatorError(Exception):
    def __init__(self, code: ErrorCode, message: str = ""):
        self.code = code
        super().__init__(message or code.value)


@dataclass
class ProtectedElement:
    element_type: str
    content: str
    original_offset: int = field(compare=False)


@dataclass
class HeadingNode:
    level: int
    content: str
    line_number: int


@dataclass
class DocumentParse:
    raw_text: str
    frontmatter_raw: str
    frontmatter_data: Dict[str, Any]
    body_raw: str
    headings: List[HeadingNode] = field(default_factory=list)
    protected_elements: List[ProtectedElement] = field(default_factory=list)
    whitespace_transformations: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AuditMetadata:
    executed_at_utc: str
    validator_version: str
    source_sha256: str
    candidate_sha256: str
    source_document_id: str | None
    candidate_document_id: str | None
    outcome: ValidationOutcome
    error_code: ErrorCode


@dataclass
class ValidationResult:
    CONTRACT_VERSION: ClassVar[str] = "bki.validation.v1"

    outcome: ValidationOutcome
    error_code: ErrorCode
    diff: str
    classification_log: List[str] = field(default_factory=list)
    audit_metadata: AuditMetadata | None = None

    def to_contract_dict(self) -> Dict[str, Any]:
        """Return the frozen ``bki.validation.v1`` result envelope."""
        if self.audit_metadata is None:
            raise ValueError(
                "Audit metadata is required for bki.validation.v1 serialization."
            )

        audit = self.audit_metadata
        if audit.outcome != self.outcome or audit.error_code != self.error_code:
            raise ValueError(
                "Audit metadata must match the validation outcome and error code."
            )

        return {
            "contract_version": self.CONTRACT_VERSION,
            "validator_version": audit.validator_version,
            "executed_at_utc": audit.executed_at_utc,
            "source_sha256": audit.source_sha256,
            "candidate_sha256": audit.candidate_sha256,
            "source_document_id": audit.source_document_id,
            "candidate_document_id": audit.candidate_document_id,
            "outcome": self.outcome.value,
            "error_code": self.error_code.value,
            "classification_log": list(self.classification_log),
            "diff": self.diff,
        }

    def to_contract_json(self) -> str:
        """Serialize the result as deterministic UTF-8-safe JSON text."""
        return json.dumps(
            self.to_contract_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
