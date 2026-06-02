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
    reasoning: str = ""


class SpacingScheduler:
    """Calculate optimal review intervals and priorities.

    Core rules:
    - Low confidence + wrong → review tomorrow (interval = 1)
    - Medium confidence + wrong → review in 3 days
    - High confidence + wrong → review in 7 days (highest priority — calibration failure)
    - Correct + any confidence → increasing intervals (1→3→7→14→30)
    - Closer to exam date → compress intervals
    """

    # Base intervals by confidence and correctness
    BASE_INTERVALS = {
        # (is_correct, confidence): days
        (False, 0): 1,    # guess + wrong → tomorrow
        (False, 1): 1,    # unsure + wrong → tomorrow
        (False, 2): 2,    # moderate + wrong → 2 days
        (False, 3): 5,    # confident + wrong → 5 days (calibration danger)
        (False, 4): 7,    # very confident + wrong → 7 days (worst calibration)
        (True, 0): 1,     # guess + right → still review soon (lucky guess)
        (True, 1): 3,     # unsure + right → 3 days
        (True, 2): 7,     # moderate + right → 7 days
        (True, 3): 14,    # confident + right → 14 days
        (True, 4): 30,    # very confident + right → 30 days
    }

    # Successive review multipliers — expands interval each successful review
    EXPANSION_FACTORS = [1.0, 2.0, 3.5, 5.0, 7.0]  # review #0, #1, #2, #3, #4+

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
        """Compute optimal next review date and priority."""
        # Base interval
        key = (input_.is_correct, min(input_.confidence, 4))
        base_days = cls.BASE_INTERVALS.get(key, 7)

        # Expansion for repeated reviews (adjusted by calibration)
        review_idx = min(input_.previous_reviews, len(cls.EXPANSION_FACTORS) - 1)
        base_expansion = cls.EXPANSION_FACTORS[review_idx]
        # Calibration adjustment: poor calibration → slower expansion (more reviews)
        adj = max(0.5, min(1.5, input_.calibration_adjustment))
        expansion = base_expansion * adj
        interval = max(1, int(base_days * expansion))

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
            reasoning=(
                f"Base={base_days}d, expansion={expansion}x, "
                f"urgency={urgency}, priority={priority}"
            ),
        )
