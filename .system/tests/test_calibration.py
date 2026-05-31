"""Tests for ConfidenceCalibration."""
from __future__ import annotations

import pytest
from study_science.calibration import (
    CalibrationRecord,
    CalibrationState,
    ConfidenceCalibration,
)


class TestClassify:
    def test_high_confidence_wrong_is_over_confident(self):
        state = ConfidenceCalibration.classify(confidence=3, is_correct=False)
        assert state == CalibrationState.OVER_CONFIDENT

    def test_very_high_confidence_wrong_is_severe(self):
        state = ConfidenceCalibration.classify(confidence=4, is_correct=False)
        assert state == CalibrationState.SEVERE_MISCALIBRATION

    def test_low_confidence_wrong_is_calibrated_low(self):
        state = ConfidenceCalibration.classify(confidence=1, is_correct=False)
        assert state == CalibrationState.CALIBRATED_LOW

    def test_high_confidence_correct_is_calibrated_high(self):
        state = ConfidenceCalibration.classify(confidence=3, is_correct=True)
        assert state == CalibrationState.CALIBRATED_HIGH

    def test_low_confidence_correct_is_under_confident(self):
        state = ConfidenceCalibration.classify(confidence=1, is_correct=True)
        assert state == CalibrationState.UNDER_CONFIDENT


class TestIsDangerous:
    def test_high_confidence_wrong_is_dangerous(self):
        assert ConfidenceCalibration.is_dangerous(confidence=3, is_correct=False) is True

    def test_low_confidence_wrong_is_not_dangerous(self):
        assert ConfidenceCalibration.is_dangerous(confidence=0, is_correct=False) is False

    def test_high_confidence_correct_is_not_dangerous(self):
        assert ConfidenceCalibration.is_dangerous(confidence=4, is_correct=True) is False


class TestPriorityBump:
    def test_severe_miscalibration_bumps_40(self):
        bump = ConfidenceCalibration.priority_bump(confidence=4, is_correct=False)
        assert bump == 40

    def test_overconfident_bumps_30(self):
        bump = ConfidenceCalibration.priority_bump(confidence=3, is_correct=False)
        assert bump == 30

    def test_correct_no_bump(self):
        bump = ConfidenceCalibration.priority_bump(confidence=4, is_correct=True)
        assert bump == 0


class TestSummarize:
    def test_empty_records_returns_empty_summary(self):
        summary = ConfidenceCalibration.summarize([])
        assert summary.total_attempts == 0
        assert summary.calibration_error_rate == 0.0

    def test_mixed_records_computes_rate(self):
        records = [
            CalibrationRecord(attempt_id="1", topic="A", los="L1", confidence=4, is_correct=False, state=CalibrationState.SEVERE_MISCALIBRATION),
            CalibrationRecord(attempt_id="2", topic="A", los="L1", confidence=4, is_correct=True, state=CalibrationState.CALIBRATED_HIGH),
            CalibrationRecord(attempt_id="3", topic="A", los="L1", confidence=1, is_correct=False, state=CalibrationState.CALIBRATED_LOW),
            CalibrationRecord(attempt_id="4", topic="A", los="L1", confidence=1, is_correct=True, state=CalibrationState.UNDER_CONFIDENT),
        ]
        summary = ConfidenceCalibration.summarize(records)
        assert summary.total_attempts == 4
        assert summary.over_confident_count == 1
        assert summary.calibration_error_rate == 0.25
