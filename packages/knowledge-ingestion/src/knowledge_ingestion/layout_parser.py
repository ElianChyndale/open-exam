from __future__ import annotations

from pathlib import Path
from typing import Any

from knowledge_ingestion.models import ParsedBlock, ParsedPage


class LayoutParser:
    """Parse PDF pages into structured blocks by font, size, and position."""

    HEADING_FONT_SIZE_THRESHOLD = 14.0
    NOTE_LEFT_MARGIN_THRESHOLD = 50.0

    def parse_pages(self, raw_pages: list[dict[str, Any]]) -> list[ParsedPage]:
        """Convert raw page text into structured ParsedPage objects."""
        parsed_pages: list[ParsedPage] = []
        for page_data in raw_pages:
            page_num = page_data.get("page_number", 0)
            text = page_data.get("text", "")
            blocks = self._parse_text_into_blocks(text, page_num)
            parsed_pages.append(ParsedPage(page_number=page_num, blocks=blocks))
        return parsed_pages

    def _parse_text_into_blocks(self, text: str, page_number: int) -> list[ParsedBlock]:
        """Split page text into logical blocks."""
        blocks: list[ParsedBlock] = []
        lines = text.splitlines()
        current_block_lines: list[str] = []
        current_type = "paragraph"
        block_idx = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current_block_lines:
                    block_id = f"p{page_number}_b{block_idx}"
                    blocks.append(self._create_block(block_id, current_block_lines, current_type))
                    block_idx += 1
                    current_block_lines = []
                    current_type = "paragraph"
                continue

            detected_type = self._detect_block_type(stripped)
            if detected_type != current_type and current_block_lines:
                block_id = f"p{page_number}_b{block_idx}"
                blocks.append(self._create_block(block_id, current_block_lines, current_type))
                block_idx += 1
                current_block_lines = []
                current_type = detected_type

            current_block_lines.append(stripped)

        if current_block_lines:
            block_id = f"p{page_number}_b{block_idx}"
            blocks.append(self._create_block(block_id, current_block_lines, current_type))

        return blocks

    def _detect_block_type(self, line: str) -> str:
        """Heuristic block type detection from text content."""
        stripped = line.strip()
        upper_ratio = sum(1 for c in stripped if c.isupper()) / max(len(stripped), 1)

        if stripped.startswith("#") or stripped.startswith("**"):
            return "heading"
        if stripped.startswith("|") and "|" in stripped[1:]:
            return "table"
        if stripped.startswith("$$") or stripped.startswith("$"):
            return "formula"
        if stripped.startswith(("> ", ":::", "!!!")):
            return "note"
        if stripped.startswith(("- ", "* ", "1. ", "2. ")):
            return "list"
        if len(stripped) < 60 and upper_ratio > 0.5 and not stripped.endswith("."):
            return "heading"
        return "paragraph"

    def _create_block(self, block_id: str, lines: list[str], block_type: str) -> ParsedBlock:
        text = "\n".join(lines)
        markdown = self._to_markdown(lines, block_type)
        confidence = 1.0 if block_type != "paragraph" else 0.8
        return ParsedBlock(
            block_id=block_id,
            block_type=block_type,
            bbox=(0.0, 0.0, 0.0, 0.0),
            text=text,
            markdown=markdown,
            font_size=12.0,
            is_bold=block_type == "heading",
            confidence=confidence,
        )

    def _to_markdown(self, lines: list[str], block_type: str) -> str:
        if block_type == "heading":
            return "# " + " ".join(lines)
        if block_type == "list":
            return "\n".join(lines)
        if block_type == "formula":
            return "\n".join(lines)
        if block_type == "table":
            return "\n".join(lines)
        return "\n\n".join(lines)
