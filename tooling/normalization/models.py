from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any


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
    original_offset: int


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


@dataclass(frozen=True)
class AuditMetadata:
    executed_at_utc: str
    validator_version: str
    source_document_id: str | None
    candidate_document_id: str | None
    outcome: ValidationOutcome
    error_code: ErrorCode


@dataclass
class ValidationResult:
    outcome: ValidationOutcome
    error_code: ErrorCode
    diff: str
    classification_log: List[str] = field(default_factory=list)
    audit_metadata: AuditMetadata | None = None
