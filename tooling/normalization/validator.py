import difflib

from .models import (
    ValidationResult,
    ValidationOutcome,
    ErrorCode,
    ValidatorError,
)
from .parser import DeterministicParser
from .classifier import DeltaClassifier


class NormalizationValidator:
    def __init__(self):
        self.parser = DeterministicParser()
        self.classifier = DeltaClassifier()

    def validate(
        self,
        source_text: str,
        candidate_text: str,
    ) -> ValidationResult:
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

            error_code = self.classifier.classify(
                source_parse,
                candidate_parse,
            )

            if error_code != ErrorCode.NONE:
                return ValidationResult(
                    ValidationOutcome.QUARANTINE,
                    error_code,
                    diff,
                )

            if source_text == candidate_text:
                return ValidationResult(
                    ValidationOutcome.COMPLIANT,
                    ErrorCode.NONE,
                    diff,
                )

            return ValidationResult(
                ValidationOutcome.NORMALIZED,
                ErrorCode.NONE,
                diff,
            )

        except ValidatorError as exc:
            return ValidationResult(
                ValidationOutcome.QUARANTINE,
                exc.code,
                diff,
            )
