from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class TutorAnalysisResult:
    analysis_id: str
    event_id: str
    source_layer: str
    topic: str
    los: str
    skill_id: str
    tested_concept: str
    correct_principle: str
    correct_decision_rule: str
    correct_solution_path: list[str]
    boundary: str
    tutor_hint: str
    next_micro_drill: str
    source_refs: list[str]
    created_at: str = field(default_factory=_now)
    validation_status: str = "derived"
    confirmed_at: str = ""
    correct_asset_seed_id: str = ""
    daily_review_unit_seed_id: str = ""
    reflection_event_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> TutorAnalysisResult:
        return cls(
            analysis_id=str(payload.get("analysis_id") or ""),
            event_id=str(payload.get("event_id") or ""),
            source_layer=str(payload.get("source_layer") or ""),
            topic=str(payload.get("topic") or ""),
            los=str(payload.get("los") or ""),
            skill_id=str(payload.get("skill_id") or ""),
            tested_concept=str(payload.get("tested_concept") or ""),
            correct_principle=str(payload.get("correct_principle") or ""),
            correct_decision_rule=str(payload.get("correct_decision_rule") or ""),
            correct_solution_path=list(payload.get("correct_solution_path") or []),
            boundary=str(payload.get("boundary") or ""),
            tutor_hint=str(payload.get("tutor_hint") or ""),
            next_micro_drill=str(payload.get("next_micro_drill") or ""),
            source_refs=list(payload.get("source_refs") or []),
            created_at=str(payload.get("created_at") or _now()),
            validation_status=str(payload.get("validation_status") or "derived"),
            confirmed_at=str(payload.get("confirmed_at") or ""),
            correct_asset_seed_id=str(payload.get("correct_asset_seed_id") or ""),
            daily_review_unit_seed_id=str(payload.get("daily_review_unit_seed_id") or ""),
            reflection_event_id=str(payload.get("reflection_event_id") or ""),
        )


@dataclass(slots=True)
class TutorValidationResult:
    is_valid: bool
    failure_codes: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    reflection_event_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
