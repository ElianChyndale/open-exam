from __future__ import annotations

from pathlib import Path

from app.models import MistakeEvent
from app.skill_upgrade import load_upgrade_proposals, proposal_from_repeated_reflections
from app.storage import Repository
from app.tutor_models import TutorAnalysisResult, TutorValidationResult
from app.skill_reflection import skill_reflection_from_validator_failure


def _enable_flags(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "skill_reflection_enabled: true\nskill_upgrade_proposals_enabled: true\nskill_codex_task_generator_enabled: true\n",
        encoding="utf-8",
    )


def _reflection(repo: Repository, index: int) -> None:
    event = MistakeEvent.from_payload(
        {
            "source_layer": "question",
            "topic": "FSA",
            "los": f"LOS-{index}",
            "prompt_or_question": "Prompt",
            "wrong_choice_or_output": "Wrong",
            "correct_resolution": "Correct resolution",
            "error_type": "formula_misuse",
            "confidence": 1,
            "time_spent": 10,
            "evidence_refs": [f"mock-{index}"],
        }
    )
    analysis = TutorAnalysisResult(
        analysis_id=f"analysis-{index}",
        event_id=event.event_id or "",
        source_layer="question",
        topic=event.topic,
        los=event.los,
        skill_id="cfa-question-captor",
        tested_concept="Concept",
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
        failure_codes=["missing_correct_rule", "missing_source_refs"],
        messages=["Failure"],
    )
    skill_reflection_from_validator_failure(repo, analysis=analysis, validation=validation)


def test_repeated_reflections_create_upgrade_proposal(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_flags(tmp_path)
    for index in range(3):
        _reflection(repo, index)
    created = proposal_from_repeated_reflections(repo, threshold=3)
    assert len(created) == 1
    assert created[0].reflection_ids
    assert created[0].codex_task_path
    loaded = load_upgrade_proposals(tmp_path)
    assert len(loaded) == 1
