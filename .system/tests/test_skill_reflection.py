from __future__ import annotations

from pathlib import Path

from app.models import MistakeEvent
from app.storage import Repository
from app.tutor_models import TutorAnalysisResult, TutorValidationResult
from app.skill_reflection import load_reflections, skill_reflection_from_validator_failure


def _enable_flags(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("skill_reflection_enabled: true\n", encoding="utf-8")


def test_validator_failure_creates_skill_reflection_event(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_flags(tmp_path)
    event = MistakeEvent.from_payload(
        {
            "source_layer": "question",
            "topic": "FSA",
            "los": "LOS",
            "prompt_or_question": "Prompt",
            "wrong_choice_or_output": "Wrong",
            "correct_resolution": "Correct resolution",
            "error_type": "formula_misuse",
            "confidence": 1,
            "time_spent": 10,
            "evidence_refs": ["mock-1"],
        }
    )
    analysis = TutorAnalysisResult(
        analysis_id="analysis-x",
        event_id=event.event_id or "",
        source_layer="question",
        topic=event.topic,
        los=event.los,
        skill_id="cfa-question-captor",
        tested_concept="",
        correct_principle="",
        correct_decision_rule="",
        correct_solution_path=[],
        boundary="",
        tutor_hint="",
        next_micro_drill="",
        source_refs=[],
    )
    validation = TutorValidationResult(
        is_valid=False,
        failure_codes=["missing_source_refs"],
        messages=["Missing source_refs."],
    )
    reflection = skill_reflection_from_validator_failure(repo, analysis=analysis, validation=validation)
    assert reflection is not None
    loaded = load_reflections(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].skill_id == "cfa-question-captor"
