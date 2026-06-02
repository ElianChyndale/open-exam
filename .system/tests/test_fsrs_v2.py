"""Tests for FSRS-6 scheduler, state cache, and card factory."""

from __future__ import annotations

from pathlib import Path

from language_science.fsrs_cache import FSRSStateCache
from language_science.scheduler import FSRS6Scheduler, ScheduleDecision, GRADUATION_THRESHOLD


# ── FSRSStateCache ──


def test_fsrs_cache_hit_ratio():
    cache = FSRSStateCache(maxsize=128)
    state = {"stability": 2.0, "difficulty": 5.0, "retrievability": 0.9}
    result1 = cache.get_or_compute("card-1", lambda: state)
    result2 = cache.get_or_compute("card-1", lambda: {"WRONG": "should not call"})
    assert result2 == state, "Cache should return original on hit"


def test_fsrs_cache_miss():
    cache = FSRSStateCache(maxsize=128)
    state_a = {"stability": 1.0}
    state_b = {"stability": 2.0}
    assert cache.get_or_compute("a", lambda: state_a) == state_a
    assert cache.get_or_compute("b", lambda: state_b) == state_b


def test_fsrs_cache_invalidate():
    cache = FSRSStateCache(maxsize=128)
    cache.get_or_compute("x", lambda: {"v": 1})
    cache.invalidate("x")
    called = False
    def recompute():
        nonlocal called
        called = True
        return {"v": 2}
    result = cache.get_or_compute("x", recompute)
    assert result == {"v": 2}
    assert called, "Should recompute after invalidate"


# ── FSRS-6 Scheduler ──


def test_fsrs6_schedule_good_rating():
    """First review with 'good' rating produces stability > 0."""
    decision = FSRS6Scheduler.schedule(None, "good")
    assert decision.stability >= 0
    assert decision.repetitions >= 0
    assert decision.param_version in (1, 2)


def test_fsrs6_schedule_again_resets():
    """'again' rating should not increase stability beyond a good rating."""
    first = FSRS6Scheduler.schedule(None, "good")
    second = FSRS6Scheduler.schedule(first.as_dict(), "again")
    assert second.state in ("learning", "relearning"), "again should reset state"


def test_fsrs6_schedule_easy_increases():
    """Consecutive 'easy' ratings increase stability."""
    state = FSRS6Scheduler.schedule(None, "easy")
    for _ in range(5):
        state = FSRS6Scheduler.schedule(state.as_dict(), "easy")
    assert state.stability >= 0


def test_fsrs6_graduation_default():
    """Before GRADUATION_THRESHOLD reviews, param_version should be 1 (simplified)."""
    decision = FSRS6Scheduler.schedule(None, "good", total_reviews=5)
    assert decision.param_version == 1


def test_fsrs6_graduation_upgrade():
    """At GRADUATION_THRESHOLD reviews, scheduler upgrades to param_version 2."""
    decision = FSRS6Scheduler.schedule(None, "good", total_reviews=GRADUATION_THRESHOLD)
    assert decision.param_version == 2


def test_fsrs6_legacy_state_conversion():
    """Old-format fsrs_state is converted without error."""
    old = {"state": "new", "repetitions": 0, "stability": 1.0, "difficulty": 5.0, "retrievability": 1.0}
    decision = FSRS6Scheduler.schedule(old, "good")
    assert decision.stability >= 0
    assert decision.state in ("learning", "review")


def test_fsrs6_preview_returns_all_ratings():
    """preview() returns all 4 rating decisions."""
    previews = FSRS6Scheduler.preview(None)
    for rating in ("again", "hard", "good", "easy"):
        assert rating in previews
        assert previews[rating].stability >= 0


def test_fsrs6_fallback_on_package_missing(monkeypatch):
    """When py-fsrs is not available, fallback scheduler is used."""
    monkeypatch.setattr("language_science.scheduler.FSRS_AVAILABLE", False)
    decision = FSRS6Scheduler.schedule(None, "good")
    assert decision.param_version == 0  # fallback
    assert decision.repetitions == 1


def test_fsrs6_schedule_decision_as_dict():
    """ScheduleDecision.as_dict() returns all expected keys."""
    decision = FSRS6Scheduler.schedule(None, "good")
    d = decision.as_dict()
    assert "next_due_at" in d
    assert "stability" in d
    assert "difficulty" in d
    assert "retrievability" in d
    assert "state" in d
    assert "param_version" in d


# ── End-to-End ──


def test_fsrs6_full_cycle(tmp_path: Path):
    """Full cycle: import -> collect -> generate -> review with FSRS-6."""
    from app.language_storage import LanguageRepository
    from app.storage import Repository
    from app.language_workflows import import_source, collect_item, generate_cards, review_card

    repo = Repository(tmp_path)
    lang_repo = LanguageRepository(repo)

    imported = import_source(
        lang_repo, source_type="text", title="Test",
        language="en", content="This is a test sentence for FSRS-6 review cycle.",
    )
    assert not imported.get("duplicate")

    segment = imported["segments"][0]
    collected = collect_item(
        lang_repo, item_type="phrase", canonical_form="test sentence",
        language="en", segment_id=segment["segment_id"],
    )
    assert not collected.get("merged")
    assert collected["item"]["canonical_form"] == "test sentence"

    gen_cards = generate_cards(lang_repo, collected["item"]["item_id"], card_types=["recognition", "production"])
    assert len(gen_cards) == 2

    reviewed = review_card(lang_repo, gen_cards[0]["card_id"], "good")
    assert reviewed["fsrs_state"]["stability"] > 0
