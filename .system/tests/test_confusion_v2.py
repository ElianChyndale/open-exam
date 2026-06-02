# .system/tests/test_confusion_v2.py

from language_science.confusion_map import lookup_confusions, CONFUSION_MAP, EXPLICIT_CFA_CONFUSIONS, LANGUAGE_CONFUSIONS
from language_science.confusion import detect_term_confusion
from language_science.difficulty import AdaptiveDifficultyEstimator, _count_syllables, _estimate_frequency


# ── Task 3.1: Confusion Map Tests ──────────────────────────────────────────

def test_confusion_map_has_cfa_pairs():
    """Confusion map must have at least 30 CFA entries."""
    cfa_pairs = [p for p in EXPLICIT_CFA_CONFUSIONS]
    assert len(cfa_pairs) >= 30, "Need at least 30 explicit CFA pairs"


def test_lookup_macaulay_duration():
    """Macaulay duration should find Modified duration confusion."""
    results = lookup_confusions("Macaulay duration", domain="cfa")
    assert any("Modified duration" in r["term_b"] for r in results), "Must detect Macaulay vs Modified"


def test_lookup_type1_type2():
    """Type I error should find Type II error."""
    results = lookup_confusions("Type I error", domain="cfa")
    assert any("Type II" in r["term_b"] for r in results)


def test_lookup_its_vs_its():
    """'its' should find 'it's' in language domain."""
    results = lookup_confusions("its", domain="language")
    assert any("it's" in r["term_b"] for r in results)


def test_lookup_accept_except():
    """'accept' should find 'except'."""
    results = lookup_confusions("accept", domain="language")
    assert any("except" in r["term_b"] for r in results)


def test_confusion_map_no_duplicate_ids():
    """Every pair must have unique pair_id."""
    ids = [p["pair_id"] for p in CONFUSION_MAP.values()]
    assert len(ids) == len(set(ids)), "Duplicate pair_id found"


def test_confusion_map_bidirectional():
    """Lookup should work from either term."""
    results_a = lookup_confusions("NPV", domain="cfa")
    results_b = lookup_confusions("IRR", domain="cfa")
    assert len(results_a) > 0 and len(results_b) > 0


def test_confusion_map_language_has_entries():
    """Language confusion map must have at least 10 entries."""
    assert len(LANGUAGE_CONFUSIONS) >= 10, "Need at least 10 language confusion pairs"


# ── Task 3.2: Semantic Interference Detection Tests ────────────────────────

def test_detect_explicit_cfa_confusion():
    """NPV should detect IRR via explicit confusion map."""
    item = {"canonical_form": "NPV", "item_type": "cfa_formula"}
    existing = [{"canonical_form": "IRR", "item_type": "cfa_formula"}]
    result = detect_term_confusion(item, existing)
    assert result["confusable"] is True
    assert result["strategy"] == "explicit"


def test_detect_explicit_language_confusion():
    """'its' should detect 'it's'."""
    item = {"canonical_form": "its", "item_type": "phrase"}
    existing = [{"canonical_form": "it's", "item_type": "phrase"}]
    result = detect_term_confusion(item, existing)
    assert result["confusable"] is True


def test_detect_no_confusion():
    """Unrelated terms should not be confusable."""
    item = {"canonical_form": "apple", "item_type": "word"}
    existing = [{"canonical_form": "zebra", "item_type": "word"}]
    result = detect_term_confusion(item, existing)
    assert result["confusable"] is False


def test_detect_token_overlap():
    """Terms sharing significant token overlap should be detected."""
    item = {"canonical_form": "Modified duration", "item_type": "cfa_concept"}
    existing = [{"canonical_form": "Effective duration", "item_type": "cfa_concept", "item_id": "test-123"}]
    result = detect_term_confusion(item, existing)
    # Should detect via token overlap (shared: "duration") since explicit lookup
    # for "modified duration" won't find "effective duration" in the map directly
    # (map has "Modified duration" vs "Effective duration" but from "Modified duration"
    #  side, it only matches when the term IS "modified duration" — and it is!)
    assert result["confusable"] is True


# ── Task 3.3: Lexical Difficulty Analyzer Tests ────────────────────────────

def test_syllable_count():
    assert _count_syllables("hello") == 2
    assert _count_syllables("duration") >= 3


def test_frequency_estimate_common():
    assert _estimate_frequency("the") == 0.95, "Common word should score high"
    assert _estimate_frequency("bond") == 0.60, "Finance term should score medium"
    assert _estimate_frequency("xylophone") == 0.25, "Rare word should score low"


def test_difficulty_estimator_basic():
    est = AdaptiveDifficultyEstimator(domain="general")
    result = est.estimate("hello")
    assert 0 <= result["difficulty_score"] <= 10
    assert result["canonical_form"] == "hello"
    assert result["cefr"] in ("A1", "A2", "B1", "B2", "C1", "C2")


def test_difficulty_cfa_term():
    est = AdaptiveDifficultyEstimator(domain="cfa")
    result = est.estimate("duration", context="bond duration CFA")
    assert result["domain"] == "cfa"
    assert result["difficulty_score"] >= 3.0, "CFA term should be medium-hard"


def test_difficulty_l1_bonus():
    est_en = AdaptiveDifficultyEstimator(domain="general", l1_language="en")
    est_zh = AdaptiveDifficultyEstimator(domain="general", l1_language="zh")
    result_en = est_en.estimate("hello")
    result_zh = est_zh.estimate("hello")
    assert result_en["difficulty_score"] <= result_zh["difficulty_score"], "L1 English should score easier"


def test_difficulty_outcome_updates():
    est = AdaptiveDifficultyEstimator()
    d1 = est.estimate("yield")
    est.record_outcome("yield", True)
    est.record_outcome("yield", True)
    est.record_outcome("yield", True)
    d2 = est.estimate("yield")
    assert d2["difficulty_score"] <= d1["difficulty_score"], "Correct reviews should lower difficulty"


def test_difficulty_language_has_entries():
    """Language confusions must have at least 12 entries."""
    assert len(LANGUAGE_CONFUSIONS) >= 12
