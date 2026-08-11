import difflib
import hashlib
from collections.abc import Callable
from datetime import datetime, timezone

from .models import (
    ValidationResult,
    ValidationOutcome,
    ErrorCode,
    ValidatorError,
    AuditMetadata,
)
from .parser import DeterministicParser
from .classifier import DeltaClassifier


class NormalizationValidator:
    VERSION = "VAL-001 v1.0-pilot"

    def __init__(
        self,
        clock: Callable[[], datetime] | None = None,
    ):
        self.parser = DeterministicParser()
        self.classifier = DeltaClassifier()
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def _document_id(self, document_parse):
        if document_parse is None:
            return None

        value = document_parse.frontmatter_data.get("document_id")

        if value is None:
            value = document_parse.frontmatter_data.get("Document ID")

        return str(value) if value is not None else None

    def _audit_metadata(
        self,
        source_parse,
        candidate_parse,
        source_sha256: str,
        candidate_sha256: str,
        outcome: ValidationOutcome,
        error_code: ErrorCode,
    ) -> AuditMetadata:
        executed_at = self.clock()

        if executed_at.tzinfo is None or executed_at.utcoffset() is None:
            raise ValueError("Audit clock must return a timezone-aware datetime.")

        executed_at_utc = (
            executed_at.astimezone(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

        return AuditMetadata(
            executed_at_utc=executed_at_utc,
            validator_version=self.VERSION,
            source_sha256=source_sha256,
            candidate_sha256=candidate_sha256,
            source_document_id=self._document_id(source_parse),
            candidate_document_id=self._document_id(candidate_parse),
            outcome=outcome,
            error_code=error_code,
        )

    def validate(
        self,
        source_text: str,
        candidate_text: str,
    ) -> ValidationResult:
        classification_log = []
        source_sha256 = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
        candidate_sha256 = hashlib.sha256(
            candidate_text.encode("utf-8")
        ).hexdigest()
        source_parse = None
        candidate_parse = None
        diff = "".join(
            difflib.unified_diff(
                source_text.splitlines(keepends=True),
                candidate_text.splitlines(keepends=True),
                fromfile="source.md",
                tofile="candidate.md",
            )
        )

        try:
            source_parse = self.parser.parse(
                source_text,
                is_candidate=False,
            )

            candidate_parse = self.parser.parse(
                candidate_text,
                is_candidate=True,
            )

            if source_text != source_parse.raw_text:
                classification_log.append(
                    "SOURCE_PREPARATION|AUTHORIZED|"
                    "class=LEGACY_INPUT_NORMALIZATION"
                )

            error_code = self.classifier.classify(
                source_parse,
                candidate_parse,
                classification_log,
            )

            if error_code != ErrorCode.NONE:
                outcome = ValidationOutcome.QUARANTINE
                classification_log.append(
                    "FINAL|QUARANTINE|"
                    f"error={error_code.value}"
                )
                return ValidationResult(
                    outcome,
                    error_code,
                    diff,
                    classification_log,
                    self._audit_metadata(
                        source_parse,
                        candidate_parse,
                        source_sha256,
                        candidate_sha256,
                        outcome,
                        error_code,
                    ),
                )

            if source_text == candidate_text:
                outcome = ValidationOutcome.COMPLIANT
                classification_log.append("FINAL|COMPLIANT|error=NONE")
                return ValidationResult(
                    outcome,
                    ErrorCode.NONE,
                    diff,
                    classification_log,
                    self._audit_metadata(
                        source_parse,
                        candidate_parse,
                        source_sha256,
                        candidate_sha256,
                        outcome,
                        ErrorCode.NONE,
                    ),
                )

            outcome = ValidationOutcome.NORMALIZED
            classification_log.append("FINAL|NORMALIZED|error=NONE")
            return ValidationResult(
                outcome,
                ErrorCode.NONE,
                diff,
                classification_log,
                self._audit_metadata(
                    source_parse,
                    candidate_parse,
                    source_sha256,
                    candidate_sha256,
                    outcome,
                    ErrorCode.NONE,
                ),
            )

        except ValidatorError as exc:
            outcome = ValidationOutcome.QUARANTINE
            classification_log.extend(
                [
                    f"PARSE|REJECTED|error={exc.code.value}",
                    f"FINAL|QUARANTINE|error={exc.code.value}",
                ]
            )
            return ValidationResult(
                outcome,
                exc.code,
                diff,
                classification_log,
                self._audit_metadata(
                    source_parse,
                    candidate_parse,
                    source_sha256,
                    candidate_sha256,
                    outcome,
                    exc.code,
                ),
            )
