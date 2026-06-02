"""Spacing Scheduler — optimal review intervals.

Based on spaced practice research (Dunlosky 2013, Nature Reviews Psych 2022).
Schedules review based on confidence, correctness, time spent, exam date,
and personalized calibration history (dynamic expansion factors).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from enum import IntEnum
from pathlib import Path

import math


class ConfidenceLevel(IntEnum):
    GUESS = 0
    UNSURE = 1
    MODERATE = 2
    CONFIDENT = 3
    VERY_CONFIDENT = 4


@dataclass(slots=True)
class SpacingInput:
    """Input data for spacing calculation."""
    topic: str
    los: str
    error_type: str
    confidence: int = 1                    # 0-4
    is_correct: bool = False
    time_spent_seconds: int = 60
    previous_reviews: int = 0              # how many times already reviewed
    last_reviewed_at: str = ""             # ISO date
    exam_date: str = ""                    # ISO date, for urgency scaling
    calibration_adjustment: float = 1.0    # 0.5-1.5, personalized from calibration history


@dataclass(slots=True)
class SpacingDecision:
    """Output of spacing calculation."""
    next_review_date: str = ""             # ISO date
    interval_days: int = 1
    priority: int = 50                     # 0-100
    urgency_multiplier: float = 1.0
    stability: float = 1.0                 # estimated half-life in days
    retrievability: float = 0.9            # predicted recall probability at next review
    reasoning: str = ""


def compute_interval(stability_days: float, retrievability_target: float = 0.9) -> float:
    """Compute review interval from half-life model: R = 2^(-t/H) -> t = -H * log2(R)"""
    if stability_days <= 0:
        stability_days = 1.0
    t = -stability_days * math.log2(retrievability_target)
    return max(1.0, t)


def compute_stability_update(previous_stability: float, correct: bool, confidence: int) -> float:
    """Update stability (half-life) based on recall outcome."""
    if not correct:
        return max(0.5, previous_stability * 0.4)
    # Correct answer: stability grows based on confidence
    growth_multipliers = {0: 1.0, 1: 1.3, 2: 1.8, 3: 2.5, 4: 3.5}
    multiplier = growth_multipliers.get(confidence, 1.0)
    return previous_stability * multiplier


class SpacingScheduler:
    """Calculate optimal review intervals and priorities using exponential forgetting curves."""

    @classmethod
    def predicted_retrievability(cls, stability: float, elapsed_days: float) -> float:
        """R(t) = 2^(-t/stability) — probability of recall at time t."""
        if stability <= 0 or elapsed_days <= 0:
            return 1.0
        return 2.0 ** (-elapsed_days / stability)

    @classmethod
    def compute_calibration_adjustment(cls, calibration_warnings_path: str | Path) -> float:
        """Compute personalized expansion adjustment from calibration history.

        Reads the calibration-warnings.jsonl file and computes an adjustment factor:
        - Few/no warnings → ~1.2 (faster expansion, trust self-assessment)
        - Moderate warnings → ~1.0 (default)
        - Many warnings → ~0.6 (slower expansion, need more reviews)

        Returns a float in [0.5, 1.5].
        """
        path = Path(calibration_warnings_path)
        if not path.exists():
            return 1.0

        warnings = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    warnings.append(json.loads(line))
        except (json.JSONDecodeError, OSError):
            return 1.0

        if not warnings:
            return 1.0

        # Look at recent warnings (last 50)
        recent = warnings[-50:]
        high_conf_errors = sum(
            1 for w in recent if w.get("confidence", 0) >= 3
        )
        total = len(recent)
        error_rate = high_conf_errors / total if total > 0 else 0

        # Map error rate to adjustment: 0% errors → 1.2, 50% errors → 0.8, 100% → 0.5
        adj = 1.2 - (error_rate * 0.7)
        return round(max(0.5, min(1.5, adj)), 2)

    @classmethod
    def schedule(cls, input_: SpacingInput) -> SpacingDecision:
        """Compute optimal next review date and priority using exponential forgetting curve."""
        # Initial stability estimate based on previous reviews
        # Each prior review increased stability via the exponential model
        if input_.previous_reviews == 0:
            stability = 1.0
        else:
            stability = 1.0
            # Simulate prior review history — assume correct at moderate confidence
            for _ in range(input_.previous_reviews):
                stability = compute_stability_update(stability, True, 2)

        # Update stability based on this review's outcome
        stability = compute_stability_update(stability, input_.is_correct, input_.confidence)

        # Apply calibration adjustment
        adj = max(0.5, min(1.5, input_.calibration_adjustment))
        stability *= adj

        # Compute interval from stability
        interval = max(1, int(compute_interval(stability)))

        # Compute retrievability at the scheduled review time
        retrievability = cls.predicted_retrievability(stability, interval)

        # Urgency: compress if exam is approaching
        urgency = 1.0
        if input_.exam_date:
            try:
                exam_date = date.fromisoformat(input_.exam_date[:10])
                days_until_exam = max((exam_date - date.today()).days, 1)
                if days_until_exam < 7:
                    urgency = 0.5
                elif days_until_exam < 14:
                    urgency = 0.6
                elif days_until_exam < 30:
                    urgency = 0.8
                elif days_until_exam < 60:
                    urgency = 0.9
                interval = max(1, int(interval * urgency))
            except (ValueError, TypeError):
                pass

        # Priority: high-confidence errors get highest priority
        priority = 50
        if not input_.is_correct:
            if input_.confidence >= 3:
                priority = 95   # calibration failure — most dangerous
            elif input_.confidence >= 2:
                priority = 80
            else:
                priority = 70
        else:
            if input_.confidence <= 1:
                priority = 65   # lucky guess — needs review
            else:
                priority = 40

        # Time spent penalty: very fast wrong answers may be careless
        if not input_.is_correct and input_.time_spent_seconds < 30:
            priority = min(100, priority + 10)

        next_date = (date.today() + timedelta(days=interval)).isoformat()

        return SpacingDecision(
            next_review_date=next_date,
            interval_days=interval,
            priority=priority,
            urgency_multiplier=urgency,
            stability=round(stability, 2),
            retrievability=round(retrievability, 4),
            reasoning=(
                f"Stability={stability:.1f}d, interval={interval}d, "
                f"urgency={urgency}, priority={priority}"
            ),
        )
