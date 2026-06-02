"""Adaptive instructional system with mastery-based progression."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PedagogyDecision:
    strategy: str
    explanation: str = ""
    prompt_template: str = ""


PEDAGOGY_STRATEGIES = {
    "recall": PedagogyDecision("recall", "Active recall: try to answer before seeing options",
                               "Without looking at any materials, answer: {prompt}"),
    "discrimination": PedagogyDecision("discrimination", "Compare and contrast: identify the key difference",
                                       "What is the key difference between {term_a} and {term_b}?"),
    "worked_example": PedagogyDecision("worked_example", "Study the complete example step-by-step",
                                       "Study this example carefully:\n{example}"),
    "application": PedagogyDecision("application", "Apply the concept to a new scenario",
                                    "Given {scenario}, calculate {target}."),
    "interleaving": PedagogyDecision("interleaving", "Mixed practice across topics",
                                     "This set includes questions from {topics}."),
}


class AdaptivePedagogy:
    """Mastery-based pedagogy selector. Tracks learner history per (topic, los)."""

    def __init__(self) -> None:
        self._history: dict[str, dict[str, Any]] = {}

    def select(self, *, topic: str, los: str = "", error_type: str = "",
               confidence: int = 0, energy_level: int = 2, consecutive_correct: int = 0) -> PedagogyDecision:
        key = f"{topic}:{los}" if los else topic

        if energy_level <= 1:
            return PEDAGOGY_STRATEGIES["recall"]

        if error_type == "concept_confusion" and confidence >= 3:
            return PEDAGOGY_STRATEGIES["discrimination"]

        if error_type == "formula_misuse":
            if consecutive_correct < 2:
                return PEDAGOGY_STRATEGIES["worked_example"]
            return PEDAGOGY_STRATEGIES["application"]

        if consecutive_correct >= 3:
            return PEDAGOGY_STRATEGIES["interleaving"]

        return PEDAGOGY_STRATEGIES["recall"]

    def record_outcome(self, key: str, correct: bool) -> None:
        if key not in self._history:
            self._history[key] = {"consecutive_correct": 0, "total": 0, "correct": 0}
        self._history[key]["total"] += 1
        if correct:
            self._history[key]["consecutive_correct"] += 1
            self._history[key]["correct"] += 1
        else:
            self._history[key]["consecutive_correct"] = 0


# Backward-compatible alias for study_science.__init__ and existing callers
PedagogyPolicy = AdaptivePedagogy
