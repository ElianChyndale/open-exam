from __future__ import annotations

from typing import Any

from knowledge_ingestion.models import ParsedBlock


class TableExtractor:
    """Extract table structures from text blocks."""

    def extract_from_block(self, block: ParsedBlock) -> dict[str, Any] | None:
        """Attempt to extract a table from a markdown-formatted block."""
        text = block.text
        lines = text.splitlines()

        table_lines = [ln for ln in lines if ln.strip().startswith("|")]
        if len(table_lines) < 2:
            return None

        header = table_lines[0]
        separator = table_lines[1] if len(table_lines) > 1 else ""
        rows = table_lines[2:] if len(table_lines) > 2 else []

        if not self._is_valid_separator(separator):
            return None

        headers = [cell.strip() for cell in header.split("|") if cell.strip()]
        data_rows: list[list[str]] = []
        for row in rows:
            cells = [cell.strip() for cell in row.split("|") if cell.strip()]
            if cells:
                data_rows.append(cells)

        markdown_table = self._to_markdown_table(headers, data_rows)
        return {
            "headers": headers,
            "rows": data_rows,
            "markdown": markdown_table,
            "confidence": 0.85,
            "block_id": block.block_id,
        }

    def _is_valid_separator(self, line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("|") and "-" in stripped and "|" in stripped[1:]

    def _to_markdown_table(self, headers: list[str], rows: list[list[str]]) -> str:
        header_line = "| " + " | ".join(headers) + " |"
        separator = "|" + "|".join([" --- " for _ in headers]) + "|"
        row_lines = ["| " + " | ".join(row) + " |" for row in rows]
        return "\n".join([header_line, separator] + row_lines)
