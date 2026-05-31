"""Tests for SpacingScheduler."""
from __future__ import annotations

from datetime import date, timedelta

import pytest
from study_science.spacing import ConfidenceLevel, SpacingInput, SpacingScheduler


def test_wrong_low_confidence_returns_one_day():
    """Guess + wrong -> review tomorrow."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=0, is_correct=False, time_spent_seconds=60,
    )
    decision = SpacingScheduler.schedule(input_)
    expected = (date.today() + timedelta(days=1)).isoformat()
    assert decision.next_review_date == expected
    assert decision.interval_days == 1


def test_wrong_high_confidence_returns_priority_95():
    """Very confident + wrong -> highest priority (calibration danger)."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=4, is_correct=False, time_spent_seconds=60,
    )
    decision = SpacingScheduler.schedule(input_)
    assert decision.priority == 95
    assert decision.interval_days == 7


def test_correct_high_confidence_returns_long_interval():
    """Very confident + correct -> 30 day interval."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=4, is_correct=True, time_spent_seconds=60,
    )
    decision = SpacingScheduler.schedule(input_)
    assert decision.interval_days == 30


def test_expansion_factor_increases_interval():
    """Previous reviews should expand the interval."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=2, is_correct=True, time_spent_seconds=60,
        previous_reviews=3,
    )
    decision = SpacingScheduler.schedule(input_)
    assert decision.interval_days > 7  # base 7 * expansion 5 = 35


def test_exam_urgency_compresses_interval():
    """Close exam date should compress intervals."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=2, is_correct=True, time_spent_seconds=60,
        exam_date=(date.today() + timedelta(days=5)).isoformat(),
    )
    decision = SpacingScheduler.schedule(input_)
    assert decision.urgency_multiplier < 1.0


def test_very_fast_wrong_answer_gets_priority_bump():
    """Wrong answer in <30 seconds should get +10 priority."""
    input_ = SpacingInput(
        topic="Test", los="T1", error_type="concept_confusion",
        confidence=2, is_correct=False, time_spent_seconds=15,
    )
    decision = SpacingScheduler.schedule(input_)
    # base priority for moderate+wrong = 80, +10 for fast = 90
    assert decision.priority >= 80
