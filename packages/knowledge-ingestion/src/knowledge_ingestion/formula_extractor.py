from __future__ import annotations

import re
from typing import Any

from knowledge_ingestion.models import ParsedBlock


class FormulaExtractor:
    """Detect and normalize mathematical formulas in text blocks."""

    LATEX_PATTERN = re.compile(
        r"(\$\$.*?\$\$|\$[^\$]+\$|\\\[.*?\\\]|\\\(.*?\\\))",
        re.DOTALL,
    )
    FORMULA_KEYWORDS = re.compile(
        r"\b(NPV|IRR|PV|FV|WACC|CAPM| Sharpe|Beta|Alpha|Duration|Convexity|VAR|ES|"
        r"σ|μ|Σ|∫|∂|√|≈|≠|≤|≥|±|∞|∑|∏|∆|∇)\b",
        re.IGNORECASE,
    )

    def extract_from_block(self, block: ParsedBlock) -> dict[str, Any] | None:
        """Attempt to extract a formula from a text block.

        Returns dict with latex, raw_text, confidence or None if no formula detected.
        """
        text = block.text

        latex_matches = self.LATEX_PATTERN.findall(text)
        if latex_matches:
            return {
                "latex": " ".join(latex_matches),
                "raw_text": text,
                "confidence": 0.95,
                "block_id": block.block_id,
            }

        if self.FORMULA_KEYWORDS.search(text):
            normalized = self._normalize_inline_math(text)
            return {
                "latex": normalized,
                "raw_text": text,
                "confidence": 0.7,
                "block_id": block.block_id,
            }

        if block.block_type == "formula":
            normalized = self._normalize_inline_math(text)
            return {
                "latex": normalized,
                "raw_text": text,
                "confidence": 0.9,
                "block_id": block.block_id,
            }

        return None

    def _normalize_inline_math(self, text: str) -> str:
        """Convert common math notation to approximate LaTeX."""
        replacements = [
            (r"σ", r"\\sigma"),
            (r"μ", r"\\mu"),
            (r"Σ", r"\\sum"),
            (r"√", r"\\sqrt"),
            (r"≈", r"\\approx"),
            (r"≠", r"\\neq"),
            (r"≤", r"\\leq"),
            (r"≥", r"\\geq"),
            (r"±", r"\\pm"),
            (r"∞", r"\\infty"),
            (r"∫", r"\\int"),
            (r"∂", r"\\partial"),
            (r"∆", r"\\Delta"),
            (r"∑", r"\\sum"),
            (r"∏", r"\\prod"),
            (r"^2", r"^{2}"),
            (r"^3", r"^{3}"),
            (r"_t", r"_{t}"),
            (r"_0", r"_{0}"),
            (r"_1", r"_{1}"),
        ]
        result = text
        for old, new in replacements:
            result = result.replace(old, new)
        return f"${result}$"
