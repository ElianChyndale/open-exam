from __future__ import annotations

import json

from app.models import MistakeEvent
from app.tutor_models import TutorAnalysisResult, TutorValidationResult
from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS


def validate_tutor_analysis(
    analysis: TutorAnalysisResult,
    *,
    source_event: MistakeEvent | None = None,
) -> TutorValidationResult:
    failures: list[str] = []
    messages: list[str] = []

    required_scalars = [
        ("tested_concept", analysis.tested_concept, "missing_tested_concept"),
        ("correct_principle", analysis.correct_principle, "missing_correct_principle"),
        ("correct_decision_rule", analysis.correct_decision_rule, "missing_correct_rule"),
        ("boundary", analysis.boundary, "missing_boundary"),
        ("tutor_hint", analysis.tutor_hint, "missing_tutor_hint"),
        ("next_micro_drill", analysis.next_micro_drill, "missing_next_micro_drill"),
    ]
    for field_name, value, failure_code in required_scalars:
        if not str(value or "").strip():
            failures.append(failure_code)
            messages.append(f"Missing required tutor analysis field: {field_name}.")

    if not analysis.correct_solution_path:
        failures.append("missing_correct_solution_path")
        messages.append("Missing correct_solution_path.")
    if not analysis.source_refs:
        failures.append("missing_source_refs")
        messages.append("Missing source_refs.")

    body = json.dumps(analysis.as_dict(), ensure_ascii=False).lower()
    for forbidden in FORBIDDEN_SAFE_PAYLOAD_KEYS:
        if forbidden.lower() in body:
            failures.append("wrong_answer_leakage")
            messages.append(f"Forbidden wrong-answer field leaked into tutor analysis: {forbidden}.")
            break

    if source_event is not None:
        leaked_values = [
            str(source_event.wrong_choice_or_output or "").strip(),
        ]
        for leaked in leaked_values:
            if leaked and leaked.lower() in body:
                failures.append("wrong_answer_leakage")
                messages.append("Tutor analysis leaked source wrong output.")
                break

    return TutorValidationResult(
        is_valid=not failures,
        failure_codes=list(dict.fromkeys(failures)),
        messages=messages,
    )
