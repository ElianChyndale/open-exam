from language_science.extraction import extract_candidate_terms, extract_phrases, full_extract, COMMON_WORDS, CFA_DOMAIN_MARKERS


def test_common_words_filtered():
    result = extract_candidate_terms("the and of to in it", max_terms=10)
    assert len(result) == 0, "Common words should be filtered out"


def test_extract_cfa_term():
    text = "The bond duration measures convexity and yield spread relationships in fixed income portfolios."
    result = extract_candidate_terms(text, max_terms=10)
    terms = [r["canonical_form"] for r in result]
    assert any("duration" in t for t in terms), "Should extract 'duration'"


def test_extract_phrases():
    text = "yield to maturity yield to maturity convexity duration measure convexity duration measure"
    result = extract_phrases(text, max_phrases=5)
    assert len(result) > 0


def test_full_extract():
    text = "The yield to maturity and modified duration are key fixed income concepts. " * 10
    result = full_extract(text, max_terms=5, max_phrases=3)
    assert len(result) >= 1


def test_confidence_scoring():
    result = extract_candidate_terms("duration duration duration duration yield yield", max_terms=5)
    for r in result:
        assert 0 < r["confidence"] <= 1.0


def test_cfa_domain_detection():
    result = extract_candidate_terms("convexity duration yield spread portfolio", max_terms=10)
    for r in result:
        assert r["domain"] == "cfa", f"Finance terms should be cfa domain: {r['canonical_form']}"
