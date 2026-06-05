from __future__ import annotations

import json
from pathlib import Path

from app.feature_flags import FeatureFlags
from app.models import stable_id
from app.skill_models import SkillReflectionEvent
from app.tutor_models import TutorAnalysisResult, TutorValidationResult


def _reflection_path(repo_root: Path, reflection_id: str) -> Path:
    return repo_root / ".system" / "memory" / "skills" / "reflections" / f"{reflection_id}.json"


def load_reflections(repo_root: Path) -> list[SkillReflectionEvent]:
    root = repo_root / ".system" / "memory" / "skills" / "reflections"
    rows: list[SkillReflectionEvent] = []
    for path in sorted(root.glob("*.json")):
        rows.append(SkillReflectionEvent.from_dict(json.loads(path.read_text(encoding="utf-8"))))
    return rows


def save_reflection(repo_root: Path, reflection: SkillReflectionEvent) -> Path:
    path = _reflection_path(repo_root, reflection.reflection_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reflection.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def skill_reflection_from_validator_failure(
    repo,
    *,
    analysis: TutorAnalysisResult,
    validation: TutorValidationResult,
    validator_name: str = "validate_tutor_analysis",
) -> SkillReflectionEvent | None:
    if validation.is_valid:
        return None
    if not FeatureFlags.load(repo.root).enabled("skill_reflection_enabled"):
        return None
    message = "; ".join(validation.messages or validation.failure_codes) or "Tutor analysis validation failed."
    reflection = SkillReflectionEvent(
        reflection_id=stable_id("reflection", analysis.skill_id, analysis.analysis_id, ",".join(validation.failure_codes)),
        skill_id=analysis.skill_id,
        analysis_id=analysis.analysis_id,
        mistake_event_id=analysis.event_id,
        validator_name=validator_name,
        failure_codes=list(validation.failure_codes),
        failure_message=message,
        source_refs=list(dict.fromkeys([analysis.analysis_id, analysis.event_id, *analysis.source_refs])),
        severity="high" if "wrong_answer_leakage" in validation.failure_codes else "medium",
    )
    save_reflection(repo.root, reflection)
    repo.append_jsonl_event("skill_reflection", reflection.as_dict())
    return reflection
