"""Tests for the C+ Content Extraction Pipeline.

Tests cover:
  - ePub section matching and extraction
  - KnowledgeBlock field mapping rules
  - Integration with cfa_c_plus_redesign build_knowledge_block
  - Fallback behavior (PDF, missing cache)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from scripts.cfa_content_extractor import (
    EpubSectionExtractor,
    ExtractedSection,
    extract_core_meaning,
    extract_english_terms,
    extract_formula_rule,
    extract_why_it_matters,
    extract_exam_translation,
    extract_question_triggers,
    extract_trap_fix_rule,
    build_knowledge_block_from_extraction,
    cache_key,
    _is_real_term,
    _serialize_cache_entries,
    _deserialize_cache_entries,
    load_cache,
)
from scripts.cfa_c_plus_redesign import (
    load_textbook_index,
    KnowledgeBlock,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EPUB_PATH = Path(r"D:\BaiduNetdiskDownload\CFA2026一级原版书\cfa-program2026L1V1.ePub")
V1_EXISTS = EPUB_PATH.exists()


# ======================================================================
# Section matching
# ======================================================================


@pytest.mark.skipif(not V1_EXISTS, reason="ePub V1 not available on this machine")
class TestEpubSectionMatching:
    """Test that section titles from the textbook index map correctly to nav entries."""

    @pytest.mark.parametrize(
        "signal,expected_anchor",
        [
            ("2. Interest Rates and Time Value of Money", "CFA2401-R-s02-R-1a"),
            ("2.1. Determinants of Interest Rates", "CFA2401-R-s02-01-01"),
            ("3.1. Holding Period Return", "CFA2401-R-s03-01-01"),
            ("4. Money-Weighted and Time-Weighted Return", "CFA2401-R-s04-R-1a"),
            ("5.3. Continuously Compounded Returns", "CFA2401-R-s05-01-03"),
        ],
    )
    def test_match_section(self, signal: str, expected_anchor: str) -> None:
        with EpubSectionExtractor(EPUB_PATH) as ext:
            matched = ext.match_section(signal)
            assert matched is not None, f"Failed to match: {signal}"
            _fz, anchor, _title = matched
            assert anchor == expected_anchor, f"Expected {expected_anchor}, got {anchor}"


# ======================================================================
# Section content extraction
# ======================================================================


@pytest.mark.skipif(not V1_EXISTS, reason="ePub V1 not available")
class TestEpubSectionExtraction:
    """Test that section content is actually extracted from ePub body."""

    def test_section_2_yields_definitions_and_terms(self) -> None:
        with EpubSectionExtractor(EPUB_PATH) as ext:
            sec = ext.extract_section("2. Interest Rates and Time Value of Money")
        assert len(sec.paragraphs) + len(sec.definition_sentences) >= 5, (
            f"Expected >= 5 content items, got {len(sec.paragraphs)}p + "
            f"{len(sec.definition_sentences)}d"
        )
        assert len(sec.english_terms) >= 3, (
            f"Expected >= 3 glossary terms, got {len(sec.english_terms)}"
        )
        # Verify real textbook terms
        term_text = " ".join(sec.english_terms).lower()
        assert "opportunity cost" in term_text or "interest rate" in term_text, (
            f"Expected finance terms like 'interest rate' in {sec.english_terms}"
        )

    def test_section_3_1_yields_formula(self) -> None:
        with EpubSectionExtractor(EPUB_PATH) as ext:
            sec = ext.extract_section("3.1. Holding Period Return")
        assert len(sec.formula_texts) >= 1, (
            f"Expected >= 1 formula, got {len(sec.formula_texts)}"
        )
        formula_joined = " ".join(sec.formula_texts)
        assert "R" in formula_joined or "P1" in formula_joined or "P0" in formula_joined, (
            f"Expected formula content in {sec.formula_texts}"
        )

    def test_section_5_3_yields_warning_sentences(self) -> None:
        with EpubSectionExtractor(EPUB_PATH) as ext:
            sec = ext.extract_section("5.3. Continuously Compounded Returns")
        assert len(sec.warning_sentences) + len(sec.paragraphs) >= 3, (
            f"Expected content, got {len(sec.warning_sentences)}w + {len(sec.paragraphs)}p"
        )


# ======================================================================
# Rule-based field mapper
# ======================================================================


class TestFieldExtractor:
    """Test that the rule-based mapper produces reasonable fields from ExtractedSection."""

    def make_sec(self, **overrides: Any) -> ExtractedSection:
        defaults: dict[str, Any] = {
            "section_number": "2.1",
            "heading": "Determinants of Interest Rates",
            "paragraphs": [
                "An interest rate can be viewed as the sum of the real risk-free rate and a set of premiums.",
                "The inflation premium compensates for expected inflation.",
            ],
            "english_terms": [
                "real risk-free interest rate",
                "inflation premium",
                "default risk premium",
            ],
            "definition_sentences": [
                "The nominal risk-free interest rate is the sum of the real risk-free rate and the inflation premium."
            ],
            "formula_texts": [
                "r = Real risk-free rate + Inflation premium + Default risk premium"
            ],
            "warning_sentences": [
                "In practice, however, the nominal rate is often approximated as the sum of the real risk-free rate plus an inflation premium."
            ],
            "procedural_sentences": [
                "To calculate the nominal rate, first identify the real risk-free rate."
            ],
        }
        defaults.update(overrides)
        return ExtractedSection(**defaults)

    def test_extract_core_meaning_uses_definitions_first(self) -> None:
        sec = self.make_sec()
        result = extract_core_meaning(sec)
        assert "nominal risk-free" in result
        assert "interest rate" in result or "premium" in result

    def test_extract_core_meaning_falls_back_to_paragraph(self) -> None:
        sec = self.make_sec(definition_sentences=[])
        result = extract_core_meaning(sec)
        assert result and "real risk-free" in result

    def test_extract_core_meaning_empty_fallback(self) -> None:
        sec = self.make_sec(paragraphs=[], definition_sentences=[])
        result = extract_core_meaning(sec)
        assert "Determinants" in result or "讲解" in result or result == ""

    def test_extract_english_terms_from_dfn(self) -> None:
        sec = self.make_sec()
        result = extract_english_terms(sec)
        assert "default risk premium" in result
        assert "inflation premium" in result

    def test_extract_formula_rule_from_formula_texts(self) -> None:
        sec = self.make_sec()
        result = extract_formula_rule(sec)
        assert "Real risk-free" in result
        assert "Inflation premium" in result

    def test_extract_why_it_matters_from_keyword(self) -> None:
        sec = self.make_sec(paragraphs=[
            "The inflation premium is important because it compensates investors for expected inflation."
        ])
        result = extract_why_it_matters(sec)
        assert "inflation premium" in result.lower()

    def test_extract_exam_translation_from_procedural(self) -> None:
        sec = self.make_sec()
        result = extract_exam_translation(sec)
        assert "nominal" in result.lower()

    def test_extract_trap_fix_rule_from_warning(self) -> None:
        sec = self.make_sec()
        result = extract_trap_fix_rule(sec)
        assert "however" in result.lower()

    def test_build_knowledge_block_from_extraction(self) -> None:
        sec = self.make_sec()
        fields = build_knowledge_block_from_extraction(
            sec, "Quant M01 | 2.1 Determinants of Interest Rates"
        )
        assert "core_meaning" in fields
        assert "english_terms" in fields
        assert "formula_rule" in fields
        assert "trap_fix_rule" in fields
        assert len(fields) == 8


# ======================================================================
# _is_real_term
# ======================================================================


class TestIsRealTerm:
    def test_accepts_multiword_finance_terms(self) -> None:
        assert _is_real_term("real risk-free interest rate")
        assert _is_real_term("opportunity cost")

    def test_rejects_sentence_fragments(self) -> None:
        assert not _is_real_term("Suppose we purchased a stock for EUR 100")
        assert not _is_real_term("Using Equation 3, we can compute")

    def test_rejects_short_lowercase_single_words(self) -> None:
        assert not _is_real_term("the")
        assert not _is_real_term("rate")

    def test_accepts_short_uppercase_terms(self) -> None:
        assert _is_real_term("HPR")
        assert _is_real_term("TWRR")


# ======================================================================
# Cache
# ======================================================================


class TestCache:
    def test_cache_key_format(self) -> None:
        assert cache_key("Quantitative Methods", "M01") == "Quantitative Methods::M01"

    def test_serialize_deserialize_roundtrip(self) -> None:
        sec = ExtractedSection(
            section_number="2.1",
            heading="Test",
            paragraphs=["para1", "para2"],
            english_terms=["term1"],
            formula_texts=["formula1"],
        )
        data = _serialize_cache_entries({"signal": sec})
        restored = _deserialize_cache_entries(data)
        assert "signal" in restored
        assert restored["signal"].heading == "Test"
        assert restored["signal"].paragraphs == ["para1", "para2"]
        assert restored["signal"].english_terms == ["term1"]

    def test_load_cache_returns_dict(self) -> None:
        cache = load_cache()
        assert isinstance(cache, dict)


# ======================================================================
# Integration with cfa_c_plus_redesign
# ======================================================================


class TestIntegration:
    @pytest.mark.skipif(not V1_EXISTS, reason="ePub V1 not available")
    def test_build_knowledge_block_uses_extraction(self) -> None:
        """Verify the integration path: cache → KnowledgeBlock with real content."""
        from scripts.cfa_c_plus_redesign import (
            build_knowledge_block,
            FormulaFramework,
        )

        module = {"module": "M01", "official_module": "Module 1: Rates and Returns"}
        formulas: list[FormulaFramework] = []

        # This should hit the extraction cache (populated in setup)
        block = build_knowledge_block(
            subject="Quantitative Methods",
            module=module,
            signal="2. Interest Rates and Time Value of Money",
            formulas=formulas,
        )
        assert isinstance(block, KnowledgeBlock)
        assert block.core_meaning and len(block.core_meaning) > 20
        # Should not be template text
        assert "本节把" not in block.core_meaning
        assert "opportunity cost" in block.core_meaning.lower() or "interest rate" in block.core_meaning.lower()
        # English terms should be populated
        assert len(block.english_terms) > 10

    def test_build_knowledge_block_fallback_on_missing_cache(self) -> None:
        """When cache is missing, fall back to template."""
        from scripts.cfa_c_plus_redesign import (
            build_knowledge_block,
            FormulaFramework,
        )

        module = {"module": "M99", "official_module": "Module 99: Nonexistent"}
        formulas: list[FormulaFramework] = []

        block = build_knowledge_block(
            subject="Nonexistent Subject",
            module=module,
            signal="99. Nonexistent Topic",
            formulas=formulas,
        )
        assert isinstance(block, KnowledgeBlock)
        # Should use template text
        assert "本节把" in block.core_meaning


# ======================================================================
# Textbook index alignment
# ======================================================================


class TestTextbookAlignment:
    """Verify the signal_topics in the textbook index match nav entries."""

    @pytest.mark.skipif(not V1_EXISTS, reason="ePub V1 not available")
    def test_quant_signal_topics_match_nav(self) -> None:
        m01_signals = [
            "2. Interest Rates and Time Value of Money",
            "2.1. Determinants of Interest Rates",
            "3.1. Holding Period Return",
            "5.3. Continuously Compounded Returns",
        ]
        with EpubSectionExtractor(EPUB_PATH) as ext:
            for signal in m01_signals:
                matched = ext.match_section(signal)
                assert matched is not None, f"Signal not found in nav: {signal}"
