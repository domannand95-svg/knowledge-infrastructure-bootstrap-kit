import re

import yaml
from markdown_it import MarkdownIt

from .models import (
    DocumentParse,
    HeadingNode,
    ProtectedElement,
    ErrorCode,
    ValidatorError,
)


class DeterministicParser:
    URL_PATTERN = re.compile(r"https?://[^\s<>()\[\]{}]+")
    CITATION_PATTERN = re.compile(
        r"\[(?P<key>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\]"
    )

    def __init__(self):
        self.md = MarkdownIt("commonmark").enable("table")
        self.required_keys = {
            "document_id",
            "version",
            "status",
            "last_revised",
        }

    def _prepare_source(self, text: str) -> str:
        if text.startswith("\ufeff"):
            text = text[1:]

        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _prepare_candidate(self, text: str) -> str:
        if text.startswith("\ufeff"):
            raise ValidatorError(
                ErrorCode.ERR_FM_SYNTAX,
                "Candidate contains a UTF-8 BOM.",
            )

        if "\r\n" in text or "\r" in text:
            raise ValidatorError(
                ErrorCode.ERR_UNAUTHORIZED_DELTA,
                "Candidate must use LF line endings.",
            )

        return text

    def _validate_fenced_code_blocks(self, text: str) -> None:
        opening_character = None
        opening_length = 0

        for line in text.splitlines():
            if opening_character is None:
                opening_match = re.match(
                    r"^ {0,3}(`{3,}|~{3,})(.*)$",
                    line,
                )

                if opening_match:
                    fence = opening_match.group(1)
                    opening_character = fence[0]
                    opening_length = len(fence)

                continue

            closing_match = re.match(
                rf"^ {{0,3}}({re.escape(opening_character)}"
                rf"{{{opening_length},}})[ \t]*$",
                line,
            )

            if closing_match:
                opening_character = None
                opening_length = 0

        if opening_character is not None:
            raise ValidatorError(
                ErrorCode.ERR_PROTECTED_CONTENT,
                "Candidate contains an unclosed fenced code block.",
            )

    def _protected_line_numbers(self, tokens) -> set[int]:
        protected = set()

        for token in tokens:
            if token.type not in {
                "fence",
                "code_block",
                "table_open",
                "html_block",
            }:
                continue

            if token.map:
                start, end = token.map
                protected.update(range(start, end))

        return protected

    def _normalize_source_whitespace(
        self,
        body_raw: str,
        tokens,
    ) -> tuple[str, list[str]]:
        protected = self._protected_line_numbers(tokens)
        normalized_lines = []
        previous_blank = False
        removed_trailing_whitespace = False
        collapsed_blank_lines = False

        for index, line in enumerate(body_raw.splitlines()):
            if index in protected:
                normalized_lines.append(line)
                previous_blank = False
                continue

            normalized_line = line.rstrip(" \t")

            if normalized_line != line:
                removed_trailing_whitespace = True

            if normalized_line == "":
                if previous_blank:
                    collapsed_blank_lines = True
                    continue

                previous_blank = True
            else:
                previous_blank = False

            normalized_lines.append(normalized_line)

        normalized_body = "\n".join(normalized_lines)

        if body_raw.endswith("\n"):
            normalized_body += "\n"

        transformations = []

        if removed_trailing_whitespace:
            transformations.append("TRAILING_WHITESPACE_REMOVAL")

        if collapsed_blank_lines:
            transformations.append("BLANK_LINE_COLLAPSE")

        return normalized_body, transformations

    def _validate_candidate_whitespace(self, body_raw: str, tokens) -> None:
        protected = self._protected_line_numbers(tokens)
        previous_blank = False

        for index, line in enumerate(body_raw.splitlines()):
            if index in protected:
                previous_blank = False
                continue

            if line != line.rstrip(" \t"):
                raise ValidatorError(
                    ErrorCode.ERR_UNAUTHORIZED_DELTA,
                    "Candidate contains trailing whitespace.",
                )

            if line == "":
                if previous_blank:
                    raise ValidatorError(
                        ErrorCode.ERR_UNAUTHORIZED_DELTA,
                        "Candidate contains repeated blank lines.",
                    )

                previous_blank = True
            else:
                previous_blank = False

    def _extract_protected_elements(
        self,
        body_raw: str,
        tokens,
    ) -> list[ProtectedElement]:
        body_lines = body_raw.splitlines()
        records = []
        sequence = 0

        def add(element_type, content, line, column=0):
            nonlocal sequence
            records.append(
                (
                    line,
                    column,
                    sequence,
                    ProtectedElement(
                        element_type=element_type,
                        content=content,
                        original_offset=line,
                    ),
                )
            )
            sequence += 1

        for token in tokens:
            if token.type == "fence":
                add(
                    "CODE_BLOCK",
                    token.content,
                    token.map[0] if token.map else 0,
                )

            if token.type == "table_open" and token.map:
                start, end = token.map
                add("TABLE", "\n".join(body_lines[start:end]), start)

            if token.type == "inline" and token.children:
                line = token.map[0] if token.map else 0
                search_offset = 0

                for child in token.children:
                    if child.type != "code_inline":
                        continue

                    column = token.content.find(child.content, search_offset)

                    if column < 0:
                        column = search_offset

                    add("INLINE_CODE", child.content, line, column)
                    search_offset = column + len(child.content)

        for line_number, line in enumerate(body_lines):
            for match in self.URL_PATTERN.finditer(line):
                content = match.group(0).rstrip(".,;:!?\"'")

                if content:
                    add("URL", content, line_number, match.start())

            for match in self.CITATION_PATTERN.finditer(line):
                add(
                    "CITATION_KEY",
                    match.group("key"),
                    line_number,
                    match.start(),
                )

        records.sort(key=lambda record: record[:3])
        return [record[3] for record in records]

    def parse(self, text: str, is_candidate: bool) -> DocumentParse:
        if is_candidate:
            parsed_text = self._prepare_candidate(text)
            self._validate_fenced_code_blocks(parsed_text)
        else:
            parsed_text = self._prepare_source(text)

        fm_match = re.match(
            r"^---\n(.*?)\n---\n(.*)",
            parsed_text,
            re.DOTALL,
        )

        if not fm_match:
            raise ValidatorError(
                ErrorCode.ERR_FM_SYNTAX,
                "Missing or malformed frontmatter delimiters.",
            )

        fm_raw, body_raw = fm_match.groups()

        try:
            fm_data = yaml.safe_load(fm_raw)

            if not isinstance(fm_data, dict):
                raise ValidatorError(
                    ErrorCode.ERR_FM_SYNTAX,
                    "Frontmatter YAML is not a mapping.",
                )

        except yaml.YAMLError as exc:
            raise ValidatorError(
                ErrorCode.ERR_FM_SYNTAX,
                "YAML parsing failed.",
            ) from exc

        if is_candidate:
            if not self.required_keys.issubset(fm_data.keys()):
                raise ValidatorError(
                    ErrorCode.ERR_FM_SYNTAX,
                    "Candidate missing required MD-001 snake_case keys.",
                )

            if not body_raw.startswith("\n# "):
                raise ValidatorError(
                    ErrorCode.ERR_H1_VIOLATION,
                    "Candidate requires exactly one blank line before H1.",
                )

        tokens = self.md.parse(body_raw)

        if is_candidate:
            self._validate_candidate_whitespace(body_raw, tokens)

        protected_elements = self._extract_protected_elements(
            body_raw,
            tokens,
        )
        comparison_body = body_raw
        whitespace_transformations = []

        if not is_candidate:
            (
                comparison_body,
                whitespace_transformations,
            ) = self._normalize_source_whitespace(body_raw, tokens)
        headings = []

        for index, token in enumerate(tokens):
            if token.type == "heading_open":
                level = int(token.tag[1])
                content = (
                    tokens[index + 1].content
                    if index + 1 < len(tokens)
                    else ""
                )

                headings.append(
                    HeadingNode(
                        level=level,
                        content=content,
                        line_number=token.map[0] if token.map else 0,
                    )
                )

        if is_candidate:
            h1_count = sum(
                1 for heading in headings if heading.level == 1
            )

            if h1_count != 1:
                raise ValidatorError(
                    ErrorCode.ERR_H1_VIOLATION,
                    "Candidate must contain exactly one H1 heading.",
                )

            for index in range(1, len(headings)):
                previous = headings[index - 1]
                current = headings[index]

                if current.level > previous.level + 1:
                    raise ValidatorError(
                        ErrorCode.ERR_HEADING_NEST,
                        "Skipped heading level detected in candidate.",
                    )

        return DocumentParse(
            raw_text=parsed_text,
            frontmatter_raw=fm_raw,
            frontmatter_data=fm_data,
            body_raw=comparison_body,
            headings=headings,
            protected_elements=protected_elements,
            whitespace_transformations=whitespace_transformations,
        )
