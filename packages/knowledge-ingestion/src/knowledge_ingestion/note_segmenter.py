from __future__ import annotations

from typing import Any

from knowledge_ingestion.models import ParsedBlock


class NoteSegmenter:
    """Detect and extract sidebar notes, callout boxes, and highlighted sections."""

    NOTE_INDICATORS = [
        "note:",
        "important:",
        "warning:",
        "tip:",
        "remember:",
        "caution:",
        "key takeaway",
        "key concept",
        "callout",
        ":::",
        "!!!",
        "> ",
    ]
    EXAMPLE_INDICATORS = [
        "example:",
        "e.g.,",
        "for example",
        "illustration:",
        "case study",
        "worked example",
    ]

    def segment_notes(self, blocks: list[ParsedBlock]) -> list[dict[str, Any]]:
        """Identify note/callout blocks within a page."""
        notes: list[dict[str, Any]] = []
        for block in blocks:
            note_type = self._detect_note_type(block)
            if note_type:
                notes.append(
                    {
                        "block_id": block.block_id,
                        "note_type": note_type,
                        "text": block.text,
                        "confidence": 0.85,
                    }
                )
        return notes

    def _detect_note_type(self, block: ParsedBlock) -> str | None:
        """Detect if a block is a note, example, or callout."""
        text_lower = block.text.lower()

        if block.block_type == "note":
            return "callout"

        for indicator in self.NOTE_INDICATORS:
            if text_lower.startswith(indicator):
                return "note"

        for indicator in self.EXAMPLE_INDICATORS:
            if indicator in text_lower[:60]:
                return "example"

        return None
