from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class SkillRegistryEntry:
    skill_id: str
    name: str
    owned_paths: list[str]
    role_boundary: str
    enabled: bool = True
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> SkillRegistryEntry:
        return cls(
            skill_id=str(payload.get("skill_id") or ""),
            name=str(payload.get("name") or ""),
            owned_paths=list(payload.get("owned_paths") or []),
            role_boundary=str(payload.get("role_boundary") or ""),
            enabled=bool(payload.get("enabled", True)),
            created_at=str(payload.get("created_at") or _now()),
            updated_at=str(payload.get("updated_at") or _now()),
            notes=str(payload.get("notes") or ""),
        )


@dataclass(slots=True)
class SkillReflectionEvent:
    reflection_id: str
    skill_id: str
    analysis_id: str
    mistake_event_id: str
    validator_name: str
    failure_codes: list[str]
    failure_message: str
    source_refs: list[str]
    severity: str = "medium"
    status: str = "open"
    created_at: str = field(default_factory=_now)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> SkillReflectionEvent:
        return cls(
            reflection_id=str(payload.get("reflection_id") or ""),
            skill_id=str(payload.get("skill_id") or ""),
            analysis_id=str(payload.get("analysis_id") or ""),
            mistake_event_id=str(payload.get("mistake_event_id") or ""),
            validator_name=str(payload.get("validator_name") or "validate_tutor_analysis"),
            failure_codes=list(payload.get("failure_codes") or []),
            failure_message=str(payload.get("failure_message") or ""),
            source_refs=list(payload.get("source_refs") or []),
            severity=str(payload.get("severity") or "medium"),
            status=str(payload.get("status") or "open"),
            created_at=str(payload.get("created_at") or _now()),
        )


@dataclass(slots=True)
class SkillUpgradeProposal:
    proposal_id: str
    skill_id: str
    title: str
    problem_statement: str
    evidence_summary: str
    requested_changes: list[str]
    acceptance_criteria: list[str]
    limits: list[str]
    reflection_ids: list[str]
    created_at: str = field(default_factory=_now)
    status: str = "proposed"
    codex_task_path: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> SkillUpgradeProposal:
        return cls(
            proposal_id=str(payload.get("proposal_id") or ""),
            skill_id=str(payload.get("skill_id") or ""),
            title=str(payload.get("title") or ""),
            problem_statement=str(payload.get("problem_statement") or ""),
            evidence_summary=str(payload.get("evidence_summary") or ""),
            requested_changes=list(payload.get("requested_changes") or []),
            acceptance_criteria=list(payload.get("acceptance_criteria") or []),
            limits=list(payload.get("limits") or []),
            reflection_ids=list(payload.get("reflection_ids") or []),
            created_at=str(payload.get("created_at") or _now()),
            status=str(payload.get("status") or "proposed"),
            codex_task_path=str(payload.get("codex_task_path") or ""),
        )


@dataclass(slots=True)
class SkillHealthScore:
    skill_id: str
    score: int
    status: str
    reflection_count: int
    recent_failures: int
    proposal_count: int
    last_reflection_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
