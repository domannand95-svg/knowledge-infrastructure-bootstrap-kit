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
        classification_log = []
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
                classification_log.append(
                    "FINAL|QUARANTINE|"
                    f"error={error_code.value}"
                )
                return ValidationResult(
                    ValidationOutcome.QUARANTINE,
                    error_code,
                    diff,
                    classification_log,
                )

            if source_text == candidate_text:
                classification_log.append("FINAL|COMPLIANT|error=NONE")
                return ValidationResult(
                    ValidationOutcome.COMPLIANT,
                    ErrorCode.NONE,
                    diff,
                    classification_log,
                )

            classification_log.append("FINAL|NORMALIZED|error=NONE")
            return ValidationResult(
                ValidationOutcome.NORMALIZED,
                ErrorCode.NONE,
                diff,
                classification_log,
            )

        except ValidatorError as exc:
            classification_log.extend(
                [
                    f"PARSE|REJECTED|error={exc.code.value}",
                    f"FINAL|QUARANTINE|error={exc.code.value}",
                ]
            )
            return ValidationResult(
                ValidationOutcome.QUARANTINE,
                exc.code,
                diff,
                classification_log,
            )
