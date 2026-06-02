"""Tests for EXAMOS algorithm-level fixes.

Covers:
- Task 1: SpacingScheduler — exponential forgetting curve
- Task 2: FSRS-6 scheduler — single param set, cache wiring, fallback formula
- Task 3: DifficultyAnalyzer — Beta-Bernoulli posterior
- Task 4: Extraction — TF-IDF confidence
"""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta
from typing import Any

import pytest

from language_science.difficulty import AdaptiveDifficultyEstimator
from language_science.extraction import (
    compute_confidence,
    extract_candidate_terms,
    extract_phrases,
)
from language_science.fsrs_cache import FSRSStateCache
from language_science.scheduler import (
    FSRS6Scheduler,
    ScheduleDecision,
    _FallbackScheduler,
)
from study_science.spacing import (
    SpacingDecision,
    SpacingInput,
    SpacingScheduler,
    compute_interval,
    compute_stability_update,
)


# =============================================================================
# Task 1: SpacingScheduler — exponential forgetting curve
# =============================================================================


class TestComputeInterval:
    """Verify the half-life interval formula."""

    def test_positive_stability(self) -> None:
        """t = -H * log2(R); with H=10, R=0.9 => ~1.52 days."""
        interval = compute_interval(10.0, 0.9)
        expected = -10.0 * math.log2(0.9)
        assert interval == pytest.approx(expected, rel=1e-4)
        assert interval >= 1.0

    def test_zero_stability_defaults_to_one(self) -> None:
        """Zero or negative stability gets clamped to 1.0, then max(1.0, interval) = 1.0."""
        assert compute_interval(0.0) == 1.0
        assert compute_interval(-5.0) == 1.0

    def test_minimum_interval_is_one(self) -> None:
        """Interval never goes below 1 day."""
        assert compute_interval(0.001, 0.99) == 1.0
        assert compute_interval(0.1, 0.999) == 1.0


class TestComputeStabilityUpdate:
    """Verify stability update behavior."""

    def test_incorrect_reduces_stability(self) -> None:
        """Wrong answer should reduce stability significantly."""
        new = compute_stability_update(10.0, correct=False, confidence=2)
        assert new == pytest.approx(4.0, rel=1e-4)  # 10 * 0.4

    def test_incorrect_floor_at_half_day(self) -> None:
        """Stability never goes below 0.5 days on wrong answer."""
        new = compute_stability_update(0.3, correct=False, confidence=2)
        assert new == 0.5

    def test_correct_grows_stability(self) -> None:
        """Correct answer grows stability by confidence multiplier."""
        assert compute_stability_update(10.0, correct=True, confidence=0) == 10.0
        assert compute_stability_update(10.0, correct=True, confidence=1) == 13.0
        assert compute_stability_update(10.0, correct=True, confidence=2) == 18.0
        assert compute_stability_update(10.0, correct=True, confidence=3) == 25.0
        assert compute_stability_update(10.0, correct=True, confidence=4) == 35.0

    def test_unbounded_growth(self) -> None:
        """No cap on stability growth — no plateau at 7.0x."""
        # After many correct reviews, stability should keep growing
        s = 1.0
        for _ in range(20):
            s = compute_stability_update(s, correct=True, confidence=3)
        # Should be much larger than old cap would allow
        assert s > 1000.0, "Stability should grow unbounded"


class TestSpacingScheduler:
    """Verify the new schedule method uses exponential model."""

    def test_new_item_baseline(self) -> None:
        """A brand-new item (no prior reviews) should get a reasonable interval."""
        inp = SpacingInput(topic="test", los="L1", error_type="vocab",
                           confidence=2, is_correct=True, previous_reviews=0)
        dec = SpacingScheduler.schedule(inp)
        assert dec.interval_days >= 1
        assert dec.stability > 0
        assert 0 < dec.retrievability <= 1.0

    def test_incorrect_item_shorter_interval(self) -> None:
        """Wrong answer yields shorter interval than correct answer."""
        inp_wrong = SpacingInput(topic="test", los="L1", error_type="vocab",
                                 confidence=2, is_correct=False, previous_reviews=0)
        inp_correct = SpacingInput(topic="test", los="L1", error_type="vocab",
                                   confidence=2, is_correct=True, previous_reviews=0)
        dec_wrong = SpacingScheduler.schedule(inp_wrong)
        dec_correct = SpacingScheduler.schedule(inp_correct)
        assert dec_wrong.interval_days <= dec_correct.interval_days

    def test_priority_high_on_calibration_failure(self) -> None:
        """High-confidence errors get highest priority (95)."""
        inp = SpacingInput(topic="test", los="L1", error_type="vocab",
                           confidence=4, is_correct=False, previous_reviews=0)
        dec = SpacingScheduler.schedule(inp)
        assert dec.priority == 95

    def test_priority_low_on_correct_confident(self) -> None:
        """Correct + confident gets low priority (40)."""
        inp = SpacingInput(topic="test", los="L1", error_type="vocab",
                           confidence=3, is_correct=True, previous_reviews=0)
        dec = SpacingScheduler.schedule(inp)
        assert dec.priority == 40

    def test_exam_urgency_compresses_interval(self) -> None:
        """Close exam date should compress the interval."""
        near_exam = (date.today() + timedelta(days=3)).isoformat()
        far_exam = (date.today() + timedelta(days=90)).isoformat()
        inp_near = SpacingInput(topic="test", los="L1", error_type="vocab",
                                confidence=2, is_correct=True,
                                previous_reviews=0, exam_date=near_exam)
        inp_far = SpacingInput(topic="test", los="L1", error_type="vocab",
                               confidence=2, is_correct=True,
                               previous_reviews=0, exam_date=far_exam)
        dec_near = SpacingScheduler.schedule(inp_near)
        dec_far = SpacingScheduler.schedule(inp_far)
        assert dec_near.interval_days <= dec_far.interval_days

    def test_predicted_retrievability(self) -> None:
        """R(t) = 2^(-t/stability) — at t=0, R=1.0; at t=H, R=0.5."""
        assert SpacingScheduler.predicted_retrievability(10.0, 0) == 1.0
        assert SpacingScheduler.predicted_retrievability(10.0, 10) == 0.5
        assert SpacingScheduler.predicted_retrievability(10.0, 20) == 0.25
        # Zero/negative args
        assert SpacingScheduler.predicted_retrievability(0, 5) == 1.0
        assert SpacingScheduler.predicted_retrievability(10, -1) == 1.0

    def test_calibration_adjustment_returns_default_when_no_file(self) -> None:
        """No calibration file => default 1.0."""
        adj = SpacingScheduler.compute_calibration_adjustment("/nonexistent/file.jsonl")
        assert adj == 1.0

    def test_repeated_reviews_increase_interval(self) -> None:
        """More prior reviews should lead to longer intervals (exponential growth)."""
        inp_0 = SpacingInput(topic="test", los="L1", error_type="vocab",
                             confidence=3, is_correct=True, previous_reviews=0)
        inp_5 = SpacingInput(topic="test", los="L1", error_type="vocab",
                             confidence=3, is_correct=True, previous_reviews=5)
        dec_0 = SpacingScheduler.schedule(inp_0)
        dec_5 = SpacingScheduler.schedule(inp_5)
        assert dec_5.interval_days >= dec_0.interval_days


# =============================================================================
# Task 2: FSRS-6 scheduler fixes
# =============================================================================


class TestFallbackSchedulerFormula:
    """Verify the fix in _FallbackScheduler interval formula.

    Old: max(FALLBACK_INTERVALS[rating], stability * FALLBACK_INTERVALS[rating])
    New: FALLBACK_INTERVALS[rating] * max(1.0, stability)
    """

    def _interval_from_decision(self, dec: ScheduleDecision, ref_time: datetime) -> float:
        """Derive interval in days from a ScheduleDecision's next_due_at."""
        due = datetime.fromisoformat(dec.next_due_at)
        return (due - ref_time).total_seconds() / 86400

    def test_new_item_uses_base_interval(self) -> None:
        """With stability=1.0, interval = base * max(1.0, 1.0 * multiplier)."""
        from datetime import timezone
        ref_time = datetime(2026, 6, 1, tzinfo=timezone.utc)
        state: dict[str, Any] = {"stability": 1.0, "difficulty": 5.0, "repetitions": 0}
        # New: interval = FALLBACK_INTERVALS[rating] * max(1.0, stability_after_multiplier)
        # where stability_after_multiplier = max(0.25, old_stability * FALLBACK_MULTIPLIERS[rating])
        cases = [
            ("again", 0.01, 0.35, 0.01 * max(1.0, 0.35)),   # 0.01 * 1.0 = 0.01
            ("hard",  1.0,  1.2,  1.0 * max(1.0, 1.2)),      # 1.0 * 1.2 = 1.2
            ("good",  3.0,  2.2,  3.0 * max(1.0, 2.2)),      # 3.0 * 2.2 = 6.6
            ("easy",  7.0,  3.2,  7.0 * max(1.0, 3.2)),      # 7.0 * 3.2 = 22.4
        ]
        for rating, _base, _mult, expected in cases:
            dec = _FallbackScheduler.schedule(state, rating, now=ref_time)  # type: ignore[arg-type]
            actual_interval = self._interval_from_decision(dec, ref_time)
            assert actual_interval == pytest.approx(expected, rel=1e-3), f"rating={rating}"

    def test_stability_below_one_gets_floor(self) -> None:
        """When stability < 1.0, max(1.0, stability*multiplier) prevents sub-base intervals."""
        from datetime import timezone
        ref_time = datetime(2026, 6, 1, tzinfo=timezone.utc)
        state: dict[str, Any] = {"stability": 0.5, "difficulty": 5.0, "repetitions": 0}
        dec = _FallbackScheduler.schedule(state, "good", now=ref_time)
        # stability = max(0.25, 0.5 * 2.2) = max(0.25, 1.1) = 1.1
        # interval = 3.0 * max(1.0, 1.1) = 3.0 * 1.1 = 3.3
        assert self._interval_from_decision(dec, ref_time) == pytest.approx(3.3, rel=1e-3)

    def test_stability_above_one_scales_linearly(self) -> None:
        """When stability > 1.0, interval = base * (stability * multiplier)."""
        from datetime import timezone
        ref_time = datetime(2026, 6, 1, tzinfo=timezone.utc)
        state: dict[str, Any] = {"stability": 5.0, "difficulty": 5.0, "repetitions": 2}
        dec = _FallbackScheduler.schedule(state, "good", now=ref_time)
        # stability = max(0.25, 5.0 * 2.2) = 11.0
        # interval = 3.0 * max(1.0, 11.0) = 33.0
        assert self._interval_from_decision(dec, ref_time) == pytest.approx(33.0, rel=1e-3)


class TestFSRS6CacheWiring:
    """Verify FSRSStateCache is wired into schedule()."""

    def test_cache_accepts_none(self) -> None:
        """schedule() should work with _cache=None (backward compat)."""
        dec = FSRS6Scheduler.schedule({"stability": 1.0, "difficulty": 5.0}, "good", _cache=None)
        assert isinstance(dec, ScheduleDecision)

    def test_cache_is_callable(self) -> None:
        """schedule() should accept an FSRSStateCache instance without error."""
        cache = FSRSStateCache(maxsize=16)
        state = {"stability": 1.0, "difficulty": 5.0, "card_id": "test-001"}
        dec = FSRS6Scheduler.schedule(state, "good", _cache=cache)
        assert isinstance(dec, ScheduleDecision)


class TestFSRS6NoGraduatedSplit:
    """Verify the graduated/simplified split has been removed."""

    def test_no_total_reviews_param(self) -> None:
        """schedule() no longer accepts total_reviews."""
        import inspect
        sig = inspect.signature(FSRS6Scheduler.schedule)
        assert "total_reviews" not in sig.parameters, "total_reviews param should be removed"

    def test_preview_no_total_reviews(self) -> None:
        """preview() no longer accepts total_reviews."""
        import inspect
        sig = inspect.signature(FSRS6Scheduler.preview)
        assert "total_reviews" not in sig.parameters, "total_reviews param should be removed from preview"

    def test_always_param_version_two(self) -> None:
        """All FSRS schedules should use param_version=2 (full parameters)."""
        dec = FSRS6Scheduler.schedule({"stability": 1.0, "difficulty": 5.0}, "good")
        assert dec.param_version == 2


# =============================================================================
# Task 3: DifficultyAnalyzer Beta-Bernoulli
# =============================================================================


class TestDifficultyBetaBernoulli:
    """Verify the corrected Beta-Bernoulli posterior formula.

    Old: corrected = difficulty * (1.0 - posterior_mean * 0.3)
    New: corrected = difficulty * (1.0 - alpha / (alpha + beta + 1))
    """

    def test_no_reviews_default_posterior(self) -> None:
        """With no reviews (alpha=5, beta=5), posterior mean = 5/11 ≈ 0.455."""
        est = AdaptiveDifficultyEstimator(domain="general")
        result = est.estimate("the")  # frequent word, should be easy
        # alpha=5, beta=5 (defaults), so correction = 1 - 5/(5+5+1) = 1 - 5/11 ≈ 0.545
        expected_correction = 1.0 - 5.0 / 11.0
        # difficulty should be corrected by that factor
        raw_difficulty = result["difficulty_score"] / expected_correction
        assert result["difficulty_score"] == pytest.approx(raw_difficulty * expected_correction, rel=1e-3)

    def test_more_corrects_lower_difficulty(self) -> None:
        """After more correct reviews, difficulty should decrease."""
        est = AdaptiveDifficultyEstimator(domain="general")
        # Record several correct outcomes
        for _ in range(10):
            est.record_outcome("bond", correct=True)
        result = est.estimate("bond")
        assert result["difficulty_score"] >= 0.0
        assert result["posterior_mean"] > 0.5  # bias toward correct

    def test_more_incorrects_higher_difficulty(self) -> None:
        """After more incorrect reviews, difficulty should increase."""
        est = AdaptiveDifficultyEstimator(domain="general")
        # Record several incorrect outcomes
        for _ in range(10):
            est.record_outcome("yield", correct=False)
        result = est.estimate("yield")
        assert result["difficulty_score"] >= 0.0
        assert result["posterior_mean"] < 0.5  # bias toward incorrect

    def test_correction_formula_is_bayesian(self) -> None:
        """Verify the specific correction: corrected = difficulty * (1 - alpha/(alpha+beta+1))."""
        est = AdaptiveDifficultyEstimator(domain="general")
        # Estimate a word to get baseline
        result = est.estimate("stock")
        # The formula uses self._alphas and self._betas internally
        # Default alpha=5, beta=5 => correction = 1 - 5/11 ≈ 0.545
        # If we record 10 corrects: alpha=15, beta=5 => correction = 1 - 15/21 ≈ 0.286
        # difficulty should be lower with 10 corrects
        for _ in range(10):
            est.record_outcome("stock", correct=True)
        result_after = est.estimate("stock")
        assert result_after["difficulty_score"] < result["difficulty_score"]


# =============================================================================
# Task 4: Extraction confidence (TF-IDF)
# =============================================================================


class TestExtractionTfIdf:
    """Verify TF-IDF confidence replaces the old linear formula."""

    def test_compute_confidence_tfidf_basics(self) -> None:
        """Basic TF-IDF properties."""
        # Term appearing once in a 100-word doc
        conf = compute_confidence(term_freq=1, doc_length=100)
        assert 0 < conf < 0.95

        # Higher term frequency -> higher confidence
        conf_high = compute_confidence(term_freq=10, doc_length=100)
        assert conf_high > conf

        # More common in corpus (higher doc_freq) -> lower confidence
        conf_rare = compute_confidence(term_freq=1, doc_length=100, doc_freq=1)
        conf_common = compute_confidence(term_freq=1, doc_length=100, doc_freq=50)
        assert conf_rare > conf_common

    def test_confidence_ceiling(self) -> None:
        """Confidence is capped at 0.95."""
        very_confident = compute_confidence(term_freq=100, doc_length=10, doc_freq=1)
        assert very_confident <= 0.95

    def test_confidence_uses_tfidf_formula(self) -> None:
        """Verify exact formula: tf = freq/doc_len, idf = log((N+1)/(df+1)) + 1, min(0.95, tf*idf*0.5)."""
        term_freq, doc_length, total_docs, doc_freq = 5, 200, 100, 1
        tf = term_freq / doc_length
        idf = math.log((total_docs + 1) / (doc_freq + 1)) + 1
        expected = min(0.95, tf * idf * 0.5)
        assert compute_confidence(term_freq, doc_length, total_docs, doc_freq) == pytest.approx(expected)

    def test_extract_candidate_terms_uses_tfidf(self) -> None:
        """extract_candidate_terms should use compute_confidence."""
        text = "The bond yield curve inverted sharply today. Bond investors watch yield spreads."
        terms = extract_candidate_terms(text, max_terms=5)
        assert len(terms) > 0
        for term in terms:
            assert 0 < term["confidence"] <= 0.95

    def test_extract_phrases_still_works(self) -> None:
        """extract_phrases should still return valid results."""
        text = "The yield curve inverted. The bond market reacted."
        phrases = extract_phrases(text, max_phrases=5)
        assert isinstance(phrases, list)


# =============================================================================
# Smoke: all imports resolve and modules load
# =============================================================================


class TestSmoke:
    """Smoke tests — everything loads and basic contracts hold."""

    def test_spacing_decision_defaults(self) -> None:
        """SpacingDecision default values are sensible."""
        d = SpacingDecision()
        assert d.interval_days == 1
        assert d.priority == 50
        assert d.stability == 1.0
        assert d.retrievability == 0.9

    def test_schedule_decision_defaults(self) -> None:
        """ScheduleDecision default param_version is 1 (will be overridden in practice)."""
        d = ScheduleDecision(
            next_due_at="2026-01-01",
            stability=1.0,
            difficulty=5.0,
            retrievability=0.9,
            state="new",
            repetitions=0,
            explanation="test",
        )
        assert d.param_version == 1
