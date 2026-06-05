from __future__ import annotations

from app.models import MistakeEvent
from app.tutor_models import TutorAnalysisResult
from app.tutor_validator import validate_tutor_analysis


def test_tutor_validator_detects_missing_fields() -> None:
    analysis = TutorAnalysisResult(
        analysis_id="analysis-1",
        event_id="evt-1",
        source_layer="question",
        topic="FSA",
        los="LOS",
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
    result = validate_tutor_analysis(analysis)
    assert result.is_valid is False
    assert "missing_tested_concept" in result.failure_codes
    assert "missing_source_refs" in result.failure_codes


def test_tutor_validator_detects_wrong_answer_leakage() -> None:
    event = MistakeEvent.from_payload(
        {
            "source_layer": "question",
            "topic": "FSA",
            "los": "LOS",
            "prompt_or_question": "Prompt",
            "wrong_choice_or_output": "LEAK_THIS",
            "correct_resolution": "Correct answer only.",
            "error_type": "formula_misuse",
            "confidence": 1,
            "time_spent": 1,
            "evidence_refs": [],
        }
    )
    analysis = TutorAnalysisResult(
        analysis_id="analysis-2",
        event_id=event.event_id or "",
        source_layer="question",
        topic="FSA",
        los="LOS",
        skill_id="cfa-question-captor",
        tested_concept="Concept",
        correct_principle="Principle",
        correct_decision_rule="Rule mentions LEAK_THIS",
        correct_solution_path=["Step"],
        boundary="Boundary",
        tutor_hint="Hint",
        next_micro_drill="Drill",
        source_refs=["evt-1"],
    )
    result = validate_tutor_analysis(analysis, source_event=event)
    assert result.is_valid is False
    assert "wrong_answer_leakage" in result.failure_codes
