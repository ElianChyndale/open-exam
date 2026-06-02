"""Full integration test for Plan C — end-to-end pipeline verification."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_full_language_pipeline(tmp_path: Path):
    """Import source -> collect item -> generate multi-dim cards -> FSRS-6 review."""
    from app.language_storage import LanguageRepository
    from app.storage import Repository
    from app.language_workflows import import_source, collect_item, generate_cards, review_card

    repo = Repository(tmp_path)
    lang_repo = LanguageRepository(repo)

    # Import
    imported = import_source(lang_repo, source_type="text", title="Integration Test",
                              language="en", content="This integration test covers the complete pipeline from source to review.")
    assert not imported.get("duplicate")
    source_id = imported["source"]["source_id"]
    assert source_id

    # Collect
    segment = imported["segments"][0]
    collected = collect_item(lang_repo, item_type="phrase", canonical_form="integration test",
                              language="en", segment_id=segment["segment_id"])
    assert not collected.get("merged")
    item_id = collected["item"]["item_id"]

    # Multi-dim generation
    from app.language_workflows import generate_multidim_cards
    cards = generate_multidim_cards(lang_repo, item_id, card_dimensions=["recognition", "production", "cloze"])
    assert len(cards) >= 1

    # FSRS-6 review
    # Enable FSRS v2 features via config yaml
    features_path = repo.root / ".system" / "config" / "features.yaml"
    features_path.parent.mkdir(parents=True, exist_ok=True)
    features_path.write_text("language_fsrs_v2_enabled: true\n", encoding="utf-8")
    reviewed = review_card(lang_repo, cards[0]["card_id"], "good")
    assert reviewed["fsrs_state"]["stability"] > 0
    assert "param_version" in reviewed["fsrs_state"]


def test_cfa_pipeline(tmp_path: Path):
    """Create CFA item -> create card -> FSRS review with exam-weight adjustment."""
    from app.cfa_storage import CfaRepository
    from app.cfa_workflows import create_cfa_item, create_cfa_card, review_cfa_card, due_cfa_cards, EXAM_WEIGHTS
    from app.storage import Repository

    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)

    # Create items across different weight topics
    high_weight = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Ethics Standard",
                                   topic="Ethical_and_Professional_Standards")
    low_weight = create_cfa_item(cfa, item_type="cfa_concept", canonical_form="Option",
                                  topic="Derivatives")
    assert EXAM_WEIGHTS["Ethical_and_Professional_Standards"] > EXAM_WEIGHTS["Derivatives"]

    # Create cards
    high_card = create_cfa_card(cfa, high_weight)
    low_card = create_cfa_card(cfa, low_weight)
    assert high_card["exam_weight"] > low_card["exam_weight"]

    # Due cards should respect weights (before any review)
    due = due_cfa_cards(cfa)
    assert len(due) == 2
    assert due[0]["exam_weight"] >= due[1]["exam_weight"], "Higher weight cards should sort first"

    # Review with FSRS — pushes due_at to the future, so high_weight card won't be due
    reviewed = review_cfa_card(cfa, high_card["card_id"], "easy")
    assert reviewed["fsrs_state"]["difficulty"] > 0

    # After review, only the unreviewed low_weight card remains due
    due_after = due_cfa_cards(cfa)
    assert len(due_after) == 1
    assert due_after[0]["exam_weight"] == EXAM_WEIGHTS["Derivatives"]


def test_semantic_interference_detection():
    """Confusion map detects CFA confusable pairs."""
    from language_science.confusion_map import lookup_confusions, EXPLICIT_CFA_CONFUSIONS
    assert len(EXPLICIT_CFA_CONFUSIONS) >= 30
    results = lookup_confusions("Macaulay duration", domain="cfa")
    assert any("Modified" in r["term_b"] for r in results)


def test_lexical_difficulty_in_pipeline():
    """Difficulty analyzer scores words and updates from outcomes."""
    from language_science.difficulty import AdaptiveDifficultyEstimator
    est = AdaptiveDifficultyEstimator(domain="cfa")
    result = est.estimate("duration", context="bond duration CFA fixed income")
    assert 0 <= result["difficulty_score"] <= 10
    old_score = result["difficulty_score"]
    for _ in range(5):
        est.record_outcome("duration", True)
    new_result = est.estimate("duration")
    assert new_result["difficulty_score"] <= old_score + 0.01, "Correct reviews should not increase difficulty"


def test_mock_exam_complete_flow(tmp_path: Path):
    """Full mock exam: start -> answer all questions -> complete -> evaluate."""
    from app.mock_exam import MockExamManager
    from app.cfa_storage import CfaRepository
    from app.storage import Repository
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)

    session = manager.start_session(question_count=30)
    assert session["status"] == "in_progress"

    subjects = list(session["subject_distribution"].keys())
    for i in range(30):
        subject = subjects[i % len(subjects)]
        manager.record_answer(f"q-{i}", subject, correct=i < 21, time_spent_seconds=60.0)

    result = manager.complete_session()
    assert result["status"] == "completed"
    assert result["score"] == 0.7  # 21/30 = 0.7
    assert result["pass"] is True
    assert len(result["subject_scores"]) > 0
    assert "timing" in result


def test_interleaving_with_mixed_domains():
    """Interleaving V2 works for both CFA and language domains."""
    from language_science.interleaving import InterleavingBuilderV2, InterleavingConfigV2, CFA_ADJACENCY, LANGUAGE_ADJACENCY
    assert len(CFA_ADJACENCY) >= 15
    assert len(LANGUAGE_ADJACENCY) >= 8

    cfa_builder = InterleavingBuilderV2(domain="cfa")
    assert cfa_builder.find_adjacent("NPV")

    lang_builder = InterleavingBuilderV2(domain="language")
    assert lang_builder.find_adjacent("its")


def test_fsrs6_graduation_pipeline(tmp_path: Path):
    """FSRS-6 graduates from simplified to full params via accumulated reviews."""
    from language_science.scheduler import FSRS6Scheduler
    state = None
    for i in range(26):
        decision = FSRS6Scheduler.schedule(state, "good" if i % 3 else "again", total_reviews=i)
        state = decision.as_dict()
    assert decision.param_version == 2, "Should graduate to full params after 25 reviews"


def test_resource_extraction_pipeline():
    """Term extraction produces valid candidates from finance text."""
    from language_science.extraction import full_extract
    text = "The yield to maturity and modified duration are key fixed income concepts. " * 20 + \
           "Portfolio managers use convexity to measure curvature. " * 10
    result = full_extract(text, max_terms=10, max_phrases=5)
    assert len(result) >= 3
    terms = [r["canonical_form"] for r in result]
    assert any("duration" in t for t in terms)
    assert any("yield" in t for t in terms)


def test_distractor_analysis_classification():
    """Distractor analyzer records and retrieves error patterns."""
    from study_science.distractor import DistractorAnalyzer, DISTRACTOR_TYPES
    assert len(DISTRACTOR_TYPES) >= 5
    da = DistractorAnalyzer()
    da.record_attempt("item-1", False, "inverse_relationship", "Fixed_Income")
    da.record_attempt("item-1", False, "inverse_relationship", "Fixed_Income")
    da.record_attempt("item-1", True, "", "Fixed_Income")
    assert da.most_common_distractor("Fixed_Income") == "inverse_relationship"


def test_retrieval_prompts_bridge():
    """RetrievalEngine prompts are generated correctly."""
    from study_science.retrieval import format_retrieval_prompt, score_recall
    # "concept_boundary" template includes both {term} and {related}
    prompt = format_retrieval_prompt("concept_boundary", "Modified Duration", related="Macaulay Duration")
    assert "Modified Duration" in prompt
    assert "Macaulay Duration" in prompt
    result = score_recall("modified duration measures price sensitivity", "modified duration measures price sensitivity")
    assert result["score"] >= 0.5
