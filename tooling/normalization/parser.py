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
    def __init__(self):
        self.md = MarkdownIt("commonmark")
        self.required_keys = {
            "document_id",
            "version",
            "status",
            "last_revised",
        }

    def _prepare_source(self, text: str) -> str:
        # Legacy source tolerance:
        # - accept and strip UTF-8 BOM
        # - normalize CRLF/CR to LF for structural parsing
        if text.startswith("\ufeff"):
            text = text[1:]

        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _prepare_candidate(self, text: str) -> str:
        # MD-001 candidate compliance is strict.
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

    def parse(self, text: str, is_candidate: bool) -> DocumentParse:
        if is_candidate:
            parsed_text = self._prepare_candidate(text)
            self._validate_fenced_code_blocks(parsed_text)
        else:
            parsed_text = self._prepare_source(text)

        # Stage 1: Frontmatter parse
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

        # Candidate compliance is strict.
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

               # Stage 2: AST extraction
        tokens = self.md.parse(body_raw)
        protected_elements = []

        for token in tokens:
            if token.type == "fence":
                protected_elements.append(
                    ProtectedElement(
                        element_type="CODE_BLOCK",
                        content=token.content,
                        original_offset=token.map[0] if token.map else 0,
                    )
                )

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

        # Structural compliance applies to candidate only.
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
            body_raw=body_raw,
            headings=headings,
            protected_elements=protected_elements,
        )
