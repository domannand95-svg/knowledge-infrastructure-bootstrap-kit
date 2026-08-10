import re

from .models import DocumentParse, ErrorCode


class DeltaClassifier:
    LEGACY_METADATA_MAP = {
        "Document ID": "document_id",
        "Version": "version",
        "Status": "status",
        "Last Revised": "last_revised",
    }

    TERMINAL_PUNCTUATION = (".", ",", ";", ":", "?", "!")

    def classify(
        self,
        source: DocumentParse,
        candidate: DocumentParse,
        classification_log: list[str],
    ) -> ErrorCode:
        # No transformation.
        if source.raw_text == candidate.raw_text:
            classification_log.append(
                "DELTA|NONE|prepared_source_and_candidate_identical"
            )
            return ErrorCode.NONE

        metadata_result = self._verify_metadata(
            source,
            candidate,
            classification_log,
        )

        if metadata_result != ErrorCode.NONE:
            return metadata_result

        if source.protected_elements != candidate.protected_elements:
            classification_log.append(
                "PROTECTED_CONTENT|REJECTED|"
                "error=ERR_PROTECTED_CONTENT"
            )
            return ErrorCode.ERR_PROTECTED_CONTENT

        if source.protected_elements:
            classification_log.append(
                "PROTECTED_CONTENT|PRESERVED|"
                f"count={len(source.protected_elements)}"
            )

        return self._verify_body_transformations(
            source.body_raw,
            candidate.body_raw,
            classification_log,
        )

    def _verify_metadata(
        self,
        source: DocumentParse,
        candidate: DocumentParse,
        classification_log: list[str],
    ) -> ErrorCode:
        migrated_source = {}
        migrated_keys = []

        for key, value in source.frontmatter_data.items():
            if key in self.LEGACY_METADATA_MAP:
                normalized_key = self.LEGACY_METADATA_MAP[key]
                migrated_keys.append((key, normalized_key))
            else:
                normalized_key = key

            migrated_source[normalized_key] = value

        if migrated_source != candidate.frontmatter_data:
            classification_log.append(
                "METADATA|REJECTED|error=ERR_PROTECTED_CONTENT"
            )
            return ErrorCode.ERR_PROTECTED_CONTENT

        for source_key, candidate_key in sorted(migrated_keys):
            classification_log.append(
                "METADATA|AUTHORIZED|"
                f"class=KEY_STANDARDIZATION;source={source_key};"
                f"candidate={candidate_key}"
            )

        return ErrorCode.NONE

    def _verify_body_transformations(
        self,
        source_body: str,
        candidate_body: str,
        classification_log: list[str],
    ) -> ErrorCode:
        if source_body == candidate_body:
            classification_log.append("BODY|NONE|no_body_delta")
            return ErrorCode.NONE

        source_lines = source_body.splitlines()
        candidate_lines = candidate_body.splitlines()

        if len(source_lines) != len(candidate_lines):
            classification_log.append(
                "BODY|REJECTED|error=ERR_UNAUTHORIZED_DELTA;"
                f"source_lines={len(source_lines)};"
                f"candidate_lines={len(candidate_lines)}"
            )
            return ErrorCode.ERR_UNAUTHORIZED_DELTA

        for index, (source_line, candidate_line) in enumerate(
            zip(source_lines, candidate_lines)
        ):
            if source_line == candidate_line:
                continue

            if self._is_running_prose_mutation(
                source_line,
                candidate_line,
            ):
                classification_log.append(
                    "BODY_LINE|REJECTED|"
                    f"line={index + 1};error=ERR_PROSE_MUTATION"
                )
                return ErrorCode.ERR_PROSE_MUTATION

            result = self._verify_heading_conversion(
                source_lines,
                candidate_lines,
                index,
                source_line,
                candidate_line,
            )

            if result != ErrorCode.NONE:
                classification_log.append(
                    "BODY_LINE|REJECTED|"
                    f"line={index + 1};error={result.value}"
                )
                return result

            classification_log.append(
                "BODY_LINE|AUTHORIZED|"
                f"line={index + 1};class=HEADING_SYNTAX_INJECTION"
            )

        return ErrorCode.NONE

    def _is_running_prose_mutation(
        self,
        source_line: str,
        candidate_line: str,
    ) -> bool:
        source_text = source_line.strip()
        candidate_text = candidate_line.strip()

        if not source_text or not candidate_text:
            return False

        # Exclude the authorized visual-heading pathway.
        if re.fullmatch(r"\*\*(.+?)\*\*", source_text):
            return False

        if re.fullmatch(r"(#{1,6})[ \t]+(.+)", candidate_text):
            return False

        # Explicit heading syntax changes are structural, not prose.
        if source_text.startswith("#") or candidate_text.startswith("#"):
            return False

        return True
    def _verify_heading_conversion(
        self,
        source_lines: list[str],
        candidate_lines: list[str],
        index: int,
        source_line: str,
        candidate_line: str,
    ) -> ErrorCode:
        bold_match = re.fullmatch(
            r"\*\*(.+?)\*\*",
            source_line.strip(),
        )

        heading_match = re.fullmatch(
            r"(#{1,6})[ \t]+(.+)",
            candidate_line.strip(),
        )

        if not bold_match or not heading_match:
            return ErrorCode.ERR_UNAUTHORIZED_DELTA

        source_content = bold_match.group(1)
        candidate_content = heading_match.group(2)

        # Underlying heading text must be identical.
        if source_content != candidate_content:
            return ErrorCode.ERR_PROSE_MUTATION

        # Running-prose punctuation is not eligible.
        if source_content.endswith(self.TERMINAL_PUNCTUATION):
            return ErrorCode.ERR_UNAUTHORIZED_DELTA

        # Source heading candidate must be surrounded by blank lines.
        previous_blank = (
            index > 0
            and source_lines[index - 1].strip() == ""
        )

        next_blank = (
            index + 1 < len(source_lines)
            and source_lines[index + 1].strip() == ""
        )

        if not previous_blank or not next_blank:
            return ErrorCode.ERR_UNAUTHORIZED_DELTA

        # Candidate conversion may change only the heading syntax.
        # Surrounding lines themselves must remain unchanged.
        if index > 0:
            if source_lines[index - 1] != candidate_lines[index - 1]:
                return ErrorCode.ERR_UNAUTHORIZED_DELTA

        if index + 1 < len(source_lines):
            if source_lines[index + 1] != candidate_lines[index + 1]:
                return ErrorCode.ERR_UNAUTHORIZED_DELTA

        return ErrorCode.NONE
