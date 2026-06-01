from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SkillState:
    skill_id: str
    mastery: float
    confidence_bias: float
    attempt_count: int
    transfer_score: float = 0.0
    half_life_days: float = 1.0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LearnerTwin:
    learner_id: str = "local-default"
    skills: dict[str, SkillState] = field(default_factory=dict)

    @classmethod
    def from_attempts(cls, attempts: list[dict[str, Any]], learner_id: str = "local-default") -> LearnerTwin:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for attempt in attempts:
            grouped.setdefault(str(attempt.get("topic") or "unknown"), []).append(attempt)
        skills: dict[str, SkillState] = {}
        for topic, rows in grouped.items():
            correct = sum(1 for row in rows if row.get("is_correct"))
            overconfident_errors = sum(
                1 for row in rows if not row.get("is_correct") and int(row.get("confidence", 0)) >= 3
            )
            skills[topic] = SkillState(
                skill_id=topic,
                mastery=round(correct / len(rows), 4),
                confidence_bias=round(overconfident_errors / len(rows), 4),
                attempt_count=len(rows),
                half_life_days=max(1.0, round(1.0 + correct * 1.5, 2)),
            )
        return cls(learner_id=learner_id, skills=skills)

    def as_dict(self) -> dict[str, Any]:
        return {"learner_id": self.learner_id, "skills": {key: value.as_dict() for key, value in self.skills.items()}}


__all__ = ["LearnerTwin", "SkillState"]
