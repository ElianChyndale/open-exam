"""Tests for PassPredictor."""
from __future__ import annotations

import pytest
from study_science.prediction import PassPredictor, PredictionInput


def test_default_prediction_is_baseline():
    """No data → should return ~0.65 base rate."""
    input_ = PredictionInput()
    result = PassPredictor.predict(input_)
    assert 0.60 <= result.pass_probability <= 0.70


def test_high_calibration_errors_penalize():
    """High calibration error rate should reduce pass probability."""
    good = PassPredictor.predict(PredictionInput(calibration_error_rate=0.0))
    bad = PassPredictor.predict(PredictionInput(calibration_error_rate=0.8))
    assert bad.pass_probability < good.pass_probability


def test_high_recurrence_penalizes():
    """High recurrence rate should reduce pass probability."""
    good = PassPredictor.predict(PredictionInput(pattern_recurrence_rate=0.0))
    bad = PassPredictor.predict(PredictionInput(pattern_recurrence_rate=0.8))
    assert bad.pass_probability < good.pass_probability


def test_good_review_rate_helps():
    """High review completion should increase pass probability."""
    bad = PassPredictor.predict(PredictionInput(review_completion_rate=0.0))
    good = PassPredictor.predict(PredictionInput(review_completion_rate=0.9))
    assert good.pass_probability > bad.pass_probability


def test_mock_score_boosts():
    """Good mock score should increase pass probability."""
    no_mock = PassPredictor.predict(PredictionInput(mock_score=None))
    good_mock = PassPredictor.predict(PredictionInput(mock_score=0.85))
    assert good_mock.pass_probability >= no_mock.pass_probability


def test_what_if_recurrence_reduction():
    """What-if reduction in recurrence should improve probability."""
    input_ = PredictionInput(pattern_recurrence_rate=0.6)
    result = PassPredictor.what_if(input_, {"recurrence_rate_reduction": 0.5})
    assert result.factors["recurrence_penalty"] < 0.10


def test_top_actions_includes_calibration_when_bad():
    """Bad calibration should appear in top actions."""
    input_ = PredictionInput(calibration_error_rate=0.5, high_conf_errors=5)
    result = PassPredictor.predict(input_)
    actions = [a["action"] for a in result.top_actions]
    assert any("校准" in a for a in actions)


def test_warnings_appear_for_bad_metrics():
    """Warnings should appear when metrics are critically bad."""
    input_ = PredictionInput(
        calibration_error_rate=0.4,
        calibration_trend="worsening",
        pattern_recurrence_rate=0.5,
        review_completion_rate=0.2,
    )
    result = PassPredictor.predict(input_)
    assert len(result.warnings) > 0
