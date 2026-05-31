"""Pass probability prediction engine.

Multi-factor model incorporating:
- Topic completion rate
- Error recurrence by topic
- Calibration trend
- Review completion rate
- Mock scores (when available)
- Days until exam (urgency)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(slots=True)
class PredictionInput:
    """Input data for pass probability calculation."""
    total_events: int = 0
    topics_attempted: int = 0
    total_topics: int = 10
    high_conf_errors: int = 0
    pattern_recurrence_rate: float = 0.0
    review_completion_rate: float = 0.0
    calibration_error_rate: float = 0.0
    calibration_trend: str = "stable"
    mock_score: float | None = None
    days_until_exam: int = 365


@dataclass(slots=True)
class PredictionResult:
    """Pass probability prediction with breakdown."""
    pass_probability: float = 0.5
    confidence_band_low: float = 0.4
    confidence_band_high: float = 0.6
    factors: dict[str, float] = field(default_factory=dict)
    top_actions: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class PassPredictor:
    """Predict pass probability based on study behavior patterns."""

    @classmethod
    def predict(cls, input_: PredictionInput) -> PredictionResult:
        """Compute pass probability from multi-factor input.

        Core formula:
        pass_prob = base_rate
          + topic_coverage_bonus
          - recurrence_penalty
          - calibration_penalty
          + review_bonus
          + mock_bonus (if available)
          + urgency_bonus (compression effect)
        """
        base_rate = 0.65

        # Topic coverage: how many of 10 topics have been attempted
        coverage_ratio = input_.topics_attempted / max(input_.total_topics, 1)
        topic_coverage_bonus = min(0.10, coverage_ratio * 0.10)

        # Error recurrence: high recurrence → lower probability
        recurrence_penalty = min(0.15, input_.pattern_recurrence_rate * 0.25)

        # Calibration: overconfidence is dangerous
        calibration_penalty = min(0.20, input_.calibration_error_rate * 0.50)
        if input_.calibration_trend == "worsening":
            calibration_penalty += 0.05
        elif input_.calibration_trend == "improving":
            calibration_penalty = max(0, calibration_penalty - 0.03)

        # Review completion: actually reviewing mistakes helps
        review_bonus = min(0.10, input_.review_completion_rate * 0.12)

        # Mock score bonus (when available)
        mock_bonus = 0.0
        if input_.mock_score is not None:
            mock_bonus = max(0, (input_.mock_score - 0.5) * 0.20)

        # Urgency: close to exam creates focus
        urgency_bonus = 0.0
        if input_.days_until_exam < 30:
            urgency_bonus = 0.05
        elif input_.days_until_exam < 7:
            urgency_bonus = 0.08

        # High-confidence error penalty (additional)
        high_conf_penalty = min(0.10, input_.high_conf_errors * 0.02)

        pass_prob = (
            base_rate
            + topic_coverage_bonus
            - recurrence_penalty
            - calibration_penalty
            + review_bonus
            + mock_bonus
            + urgency_bonus
            - high_conf_penalty
        )
        pass_prob = max(0.15, min(0.95, pass_prob))

        # Top 3 actions that would most improve the score
        actions = []
        if recurrence_penalty > 0.05:
            actions.append({
                "action": "减少同类错误复发",
                "impact": "中",
                "detail": f"当前复发率 {input_.pattern_recurrence_rate:.0%}，目标 < 20%",
            })
        if calibration_penalty > 0.08:
            actions.append({
                "action": "改善信心校准",
                "impact": "高",
                "detail": f"校准错误率 {input_.calibration_error_rate:.0%}，高信心错误 {input_.high_conf_errors} 次",
            })
        if review_bonus < 0.05:
            actions.append({
                "action": "提高复习完成率",
                "impact": "中",
                "detail": f"当前完成率 {input_.review_completion_rate:.0%}，目标 > 70%",
            })
        if topic_coverage_bonus < 0.05:
            remaining = input_.total_topics - input_.topics_attempted
            if remaining > 0:
                actions.append({
                    "action": "覆盖更多 Topic",
                    "impact": "中",
                    "detail": f"还有 {remaining} 个 Topic 未覆盖",
                })
        if input_.mock_score is None:
            actions.append({
                "action": "做一次模拟考试",
                "impact": "高",
                "detail": "模拟考成绩可以显著提升预测准确度",
            })

        warnings = []
        if input_.calibration_trend == "worsening" and input_.calibration_error_rate > 0.3:
            warnings.append("⚠️ 信心校准持续恶化——你可能越来越自信，但正确率没有同步上升")
        if input_.pattern_recurrence_rate > 0.4:
            warnings.append("⚠️ 同类错误复发率很高——纠偏规则可能需要重新审视")
        if input_.review_completion_rate < 0.3:
            warnings.append("⚠️ 复习完成率偏低——记录的错题如果不复习，等于白记")

        return PredictionResult(
            pass_probability=round(pass_prob, 3),
            confidence_band_low=round(max(0.10, pass_prob - 0.10), 3),
            confidence_band_high=round(min(0.99, pass_prob + 0.10), 3),
            factors={
                "base_rate": base_rate,
                "topic_coverage_bonus": round(topic_coverage_bonus, 3),
                "recurrence_penalty": round(recurrence_penalty, 3),
                "calibration_penalty": round(calibration_penalty, 3),
                "review_bonus": round(review_bonus, 3),
                "mock_bonus": round(mock_bonus, 3),
                "urgency_bonus": round(urgency_bonus, 3),
                "high_conf_penalty": round(high_conf_penalty, 3),
            },
            top_actions=actions[:3],
            warnings=warnings,
        )

    @classmethod
    def what_if(cls, input_: PredictionInput, adjustments: dict[str, float]) -> PredictionResult:
        """Recalculate pass probability with hypothetical adjustments.

        adjustments can include:
        - recurrence_rate_reduction: reduce recurrence by this factor (0-1)
        - calibration_improvement: reduce calibration error by this factor (0-1)
        - review_boost: increase review completion rate by this amount (0-1)
        - new_topics: additional topics covered
        """
        adj = {**adjustments}

        if "recurrence_rate_reduction" in adj:
            input_.pattern_recurrence_rate *= (1 - adj["recurrence_rate_reduction"])
        if "calibration_improvement" in adj:
            input_.calibration_error_rate *= (1 - adj["calibration_improvement"])
            if input_.calibration_trend == "worsening":
                input_.calibration_trend = "stable"
        if "review_boost" in adj:
            input_.review_completion_rate = min(1.0, input_.review_completion_rate + adj["review_boost"])
        if "new_topics" in adj:
            input_.topics_attempted = min(input_.total_topics, input_.topics_attempted + int(adj["new_topics"]))

        return cls.predict(input_)
