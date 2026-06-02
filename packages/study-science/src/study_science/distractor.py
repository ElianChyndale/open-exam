"""CFA Distractor Analysis Engine — classifies why specific wrong answers are wrong."""
from __future__ import annotations

from typing import Any


DISTRACTOR_TYPES = {
    "inverse_relationship": "Confuses direct/inverse relationship (e.g., price-yield)",
    "formula_substitution": "Uses wrong formula (e.g., arithmetic vs geometric mean)",
    "sign_error": "Sign error in calculation (e.g., adds instead of subtracts)",
    "method_confusion": "Confuses two methods (e.g., LIFO vs FIFO effect on COGS)",
    "definition_boundary": "Misapplies definitional boundary (e.g., Type I vs Type II error)",
    "multi_step_omission": "Skips a step in multi-step calculation",
    "unit_error": "Unit/scaling error (e.g., million vs billion)",
    "temporal_confusion": "Time horizon confusion (e.g., spot vs forward rate)",
    "concept_pair": "Confuses two related concepts (e.g., NPV vs IRR decision rule)",
}


def classify_distractor(correct_answer: Any, selected_answer: Any, question_type: str, topic: str) -> dict[str, Any]:
    """Classify why the selected distractor was wrong, based on actual answer comparison."""
    if question_type == "calculation":
        # Check for sign error
        if isinstance(correct_answer, (int, float)) and isinstance(selected_answer, (int, float)):
            if abs(correct_answer) == abs(-selected_answer):
                return {"distractor_type": "sign_error", "topic": topic, "confidence": 0.8}
            if selected_answer == correct_answer * 2 or selected_answer == correct_answer / 2:
                return {"distractor_type": "unit_error", "topic": topic, "confidence": 0.7}
    elif question_type == "concept":
        ca_str = str(correct_answer).lower()
        sa_str = str(selected_answer).lower()
        # Check inverse relationship
        inverse_pairs = [
            ("increase", "decrease"), ("buy", "sell"), ("long", "short"),
            ("call", "put"), ("asset", "liability"), ("revenue", "expense"),
        ]
        for a, b in inverse_pairs:
            if a in ca_str and b in sa_str:
                return {"distractor_type": "inverse_relationship", "topic": topic, "confidence": 0.8}

    return {"distractor_type": "concept_pair", "topic": topic, "confidence": 0.5}


class DistractorAnalyzer:
    def __init__(self) -> None:
        self._log: list[dict[str, Any]] = []

    def record_attempt(self, item_id: str, correct: bool, distractor_type: str = "", topic: str = "") -> dict[str, Any]:
        entry = {
            "item_id": item_id,
            "correct": correct,
            "distractor_type": distractor_type,
            "topic": topic,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }
        self._log.append(entry)
        return entry

    def get_patterns(self, item_id: str | None = None) -> list[dict[str, Any]]:
        if item_id:
            return [e for e in self._log if e["item_id"] == item_id]
        return self._log

    def most_common_distractor(self, topic: str) -> str:
        matches = [e for e in self._log if e["topic"] == topic and not e["correct"]]
        if not matches:
            return ""
        from collections import Counter
        return Counter(e["distractor_type"] for e in matches).most_common(1)[0][0]
