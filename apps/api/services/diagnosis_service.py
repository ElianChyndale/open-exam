"""Diagnosis service — integrates error diagnosis with cognitive science engines."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure packages are importable
for pkg in ["exam-core", "study-science", "agent-runtime"]:
    pkg_path = Path(__file__).resolve().parents[3] / "packages" / pkg / "src"
    if str(pkg_path) not in sys.path:
        sys.path.insert(0, str(pkg_path))


def diagnose_with_engines(
    topic: str,
    los: str,
    error_type: str,
    correct_resolution: str,
    user_answer: str = "",
    confidence: int = 1,
    time_spent: int = 60,
) -> dict:
    """Run the full diagnosis pipeline using all cognitive science engines.

    Returns a complete diagnosis with fix rule, next drill, spacing,
    retrieval prompts, and self-explanation prompt.
    """
    from study_science.spacing import SpacingInput, SpacingScheduler
    from study_science.retrieval import RetrievalEngine
    from study_science.self_explanation import SelfExplanationPrompt
    from study_science.calibration import ConfidenceCalibration

    # Spacing
    spacing_input = SpacingInput(
        topic=topic,
        los=los,
        error_type=error_type,
        confidence=confidence,
        is_correct=False,
        time_spent_seconds=time_spent,
    )
    spacing = SpacingScheduler.schedule(spacing_input)

    # Retrieval prompts
    retrieval_prompts = RetrievalEngine.build_prompts(
        topic=topic,
        los=los,
        error_type=error_type,
        correct_resolution=correct_resolution,
        count=3,
    )

    # Self-explanation
    self_explanation = SelfExplanationPrompt.generate(
        error_type=error_type,
        topic=topic,
        los=los,
        correct_answer=correct_resolution,
        user_answer=user_answer,
    )

    # Calibration check
    is_dangerous = ConfidenceCalibration.is_dangerous(confidence, is_correct=False)
    priority_bump = ConfidenceCalibration.priority_bump(confidence, is_correct=False)

    return {
        "error_type": error_type,
        "spacing": {
            "next_review_date": spacing.next_review_date,
            "interval_days": spacing.interval_days,
            "priority": spacing.priority + priority_bump,
            "reasoning": spacing.reasoning,
        },
        "retrieval_prompts": [
            {"text": p.prompt_text, "type": p.retrieval_type}
            for p in retrieval_prompts
        ],
        "self_explanation_prompt": self_explanation,
        "calibration_danger": is_dangerous,
        "calibration_priority_bump": priority_bump,
    }
