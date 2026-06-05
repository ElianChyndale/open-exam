from __future__ import annotations

import json
from pathlib import Path

from app.storage import Repository
from app.tutor_workflows import load_tutor_analysis, tutor_analysis_from_mistake_event


def _enable_flags(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "\n".join(
            [
                "tutor_analysis_enabled: true",
                "skill_reflection_enabled: true",
                "skill_upgrade_proposals_enabled: true",
                "skill_codex_task_generator_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_tutor_analysis_generates_correct_only_result_and_seeds(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_flags(tmp_path)
    payload = {
        "source_layer": "question",
        "topic": "Financial Statement Analysis",
        "los": "common-size balance sheet",
        "prompt_or_question": "Using vertical common-size balance sheet analysis, cash and cash equivalents are what percentage?",
        "wrong_choice_or_output": "32%",
        "correct_resolution": "Correct answer: 25%. For a common-size balance sheet, each line item is divided by total assets.",
        "error_type": "formula_misuse",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["mock-1"],
    }
    event = repo.load_event_by_id("missing")
    assert event is None
    from app.models import MistakeEvent

    recorded = MistakeEvent.from_payload(payload)
    repo.append_event(recorded)

    analysis = tutor_analysis_from_mistake_event(repo, recorded)
    assert analysis.tested_concept
    assert analysis.correct_principle
    assert analysis.correct_decision_rule == "For a common-size balance sheet, express each line item as a percentage of total assets."
    assert analysis.correct_solution_path
    assert analysis.boundary
    assert analysis.tutor_hint
    assert analysis.next_micro_drill
    assert analysis.source_refs
    assert analysis.correct_asset_seed_id
    assert analysis.daily_review_unit_seed_id

    saved = load_tutor_analysis(tmp_path, analysis.analysis_id)
    assert saved is not None
    assert saved.analysis_id == analysis.analysis_id

    asset_seed = json.loads((tmp_path / ".system" / "memory" / "tutor" / "correct-asset-seeds" / f"{analysis.correct_asset_seed_id}.json").read_text(encoding="utf-8"))
    assert asset_seed["correct_rule"] == analysis.correct_decision_rule
    unit_seed = json.loads((tmp_path / ".system" / "memory" / "tutor" / "daily-review-unit-seeds" / f"{analysis.daily_review_unit_seed_id}.json").read_text(encoding="utf-8"))
    assert unit_seed["correct_answer"] == analysis.correct_decision_rule
