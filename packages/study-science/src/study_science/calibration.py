"""Confidence Calibration — detect and prioritize confidence errors.

Based on metacognitive calibration research (Dunlosky 2013, MIT LSA).
High-confidence errors are the most dangerous: they represent things the
learner firmly believes but are wrong. These get highest priority.

The engine:
1. Detects calibration mismatches (high confidence + wrong answer)
2. Prioritizes these above all other review items
3. Tracks calibration trends over time
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CalibrationState(str, Enum):
    """Confidence vs correctness alignment."""
    CALIBRATED_HIGH = "calibrated_high"       # confident + correct
    CALIBRATED_LOW = "calibrated_low"         # unsure + wrong
    UNDER_CONFIDENT = "under_confident"       # unsure + correct (lucky or humble)
    OVER_CONFIDENT = "over_confident"         # confident + wrong (DANGER)
    SEVERE_MISCALIBRATION = "severe_miscalibration"  # very confident + wrong


@dataclass(slots=True)
class CalibrationRecord:
    """A single calibration measurement."""
    attempt_id: str
    topic: str
    los: str
    confidence: int               # 0-4
    is_correct: bool
    state: CalibrationState = CalibrationState.CALIBRATED_LOW
    created_at: str = ""


@dataclass(slots=True)
class CalibrationSummary:
    """Aggregate calibration statistics."""
    total_attempts: int = 0
    over_confident_count: int = 0            # high confidence + wrong
    severe_miscalibration_count: int = 0     # very confident + wrong
    calibration_error_rate: float = 0.0      # (over_confident) / total
    topic_miscalibrations: dict[str, int] = field(default_factory=dict)
    trend: str = "stable"                    # "improving", "stable", "worsening"


class ConfidenceCalibration:
    """Detect and track confidence calibration."""

    # Confidence threshold for "high" confidence
    HIGH_CONFIDENCE_THRESHOLD = 3
    VERY_HIGH_CONFIDENCE_THRESHOLD = 4

    @classmethod
    def classify(cls, confidence: int, is_correct: bool) -> CalibrationState:
        """Classify a single attempt's calibration state."""
        if is_correct:
            if confidence >= cls.HIGH_CONFIDENCE_THRESHOLD:
                return CalibrationState.CALIBRATED_HIGH
            return CalibrationState.UNDER_CONFIDENT
        else:
            if confidence >= cls.VERY_HIGH_CONFIDENCE_THRESHOLD:
                return CalibrationState.SEVERE_MISCALIBRATION
            if confidence >= cls.HIGH_CONFIDENCE_THRESHOLD:
                return CalibrationState.OVER_CONFIDENT
            return CalibrationState.CALIBRATED_LOW

    @classmethod
    def is_dangerous(cls, confidence: int, is_correct: bool) -> bool:
        """Check if this attempt represents a dangerous calibration error."""
        return not is_correct and confidence >= cls.HIGH_CONFIDENCE_THRESHOLD

    @classmethod
    def priority_bump(cls, confidence: int, is_correct: bool) -> int:
        """Return additional priority points for calibration errors."""
        if not is_correct:
            if confidence >= cls.VERY_HIGH_CONFIDENCE_THRESHOLD:
                return 40  # highest bump — severe miscalibration
            if confidence >= cls.HIGH_CONFIDENCE_THRESHOLD:
                return 30  # high bump — overconfident
            if confidence <= 1:
                return 5   # small bump — unsure and wrong (expected)
        return 0

    @classmethod
    def summarize(cls, records: list[CalibrationRecord]) -> CalibrationSummary:
        """Generate aggregate calibration statistics."""
        total = len(records)
        if total == 0:
            return CalibrationSummary()

        over_confident = sum(
            1 for r in records
            if r.state in {CalibrationState.OVER_CONFIDENT, CalibrationState.SEVERE_MISCALIBRATION}
        )
        severe = sum(
            1 for r in records
            if r.state == CalibrationState.SEVERE_MISCALIBRATION
        )
        error_rate = over_confident / total

        # Topic breakdown
        topic_miscal: dict[str, int] = {}
        for r in records:
            if r.state in {CalibrationState.OVER_CONFIDENT, CalibrationState.SEVERE_MISCALIBRATION}:
                topic_miscal[r.topic] = topic_miscal.get(r.topic, 0) + 1

        # Trend detection (simple: compare first half vs second half)
        mid = total // 2
        first_half_err = sum(
            1 for r in records[:mid]
            if r.state in {CalibrationState.OVER_CONFIDENT, CalibrationState.SEVERE_MISCALIBRATION}
        ) / max(mid, 1)
        second_half_err = sum(
            1 for r in records[mid:]
            if r.state in {CalibrationState.OVER_CONFIDENT, CalibrationState.SEVERE_MISCALIBRATION}
        ) / max(total - mid, 1)

        if second_half_err < first_half_err * 0.8:
            trend = "improving"
        elif second_half_err > first_half_err * 1.2:
            trend = "worsening"
        else:
            trend = "stable"

        return CalibrationSummary(
            total_attempts=total,
            over_confident_count=over_confident,
            severe_miscalibration_count=severe,
            calibration_error_rate=round(error_rate, 3),
            topic_miscalibrations=topic_miscal,
            trend=trend,
        )

    @classmethod
    def generate_warning(cls, topic: str, los: str, error_count: int) -> str | None:
        """Generate a warning message for a consistently miscalibrated topic."""
        if error_count >= 5:
            return f"⚠️ {topic} / {los}: 连续 {error_count} 次高信心错误——你的知识模型可能有严重误解，建议从头重学概念。"
        if error_count >= 3:
            return f"⚡ {topic} / {los}: {error_count} 次高信心错误，下次做题前先写下你确定的地方，再对答案。"
        if error_count >= 1:
            return f"📌 {topic} / {los}: 检测到信心校准偏差，注意区分'熟悉感'和'真正掌握'。"
        return None
