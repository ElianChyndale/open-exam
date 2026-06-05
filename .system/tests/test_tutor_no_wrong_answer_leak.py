from __future__ import annotations

import json
from pathlib import Path

from app.models import MistakeEvent
from app.storage import Repository
from app.tutor_workflows import tutor_analysis_from_mistake_event


def _enable_flags(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("tutor_analysis_enabled: true\nskill_reflection_enabled: true\n", encoding="utf-8")


def test_tutor_analysis_and_review_seeds_do_not_leak_wrong_output(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_flags(tmp_path)
    wrong = "LEAK_ME_WRONG_CHOICE"
    event = MistakeEvent.from_payload(
        {
            "source_layer": "question",
            "topic": "Corporate Issuers",
            "los": "WACC",
            "prompt_or_question": "Explain WACC.",
            "wrong_choice_or_output": wrong,
            "correct_resolution": "Correct answer: Use after-tax cost of debt and target capital weights.",
            "error_type": "formula_misuse",
            "confidence": 2,
            "time_spent": 45,
            "evidence_refs": ["session-1"],
        }
    )
    repo.append_event(event)
    analysis = tutor_analysis_from_mistake_event(repo, event)
    body = json.dumps(analysis.as_dict(), ensure_ascii=False)
    assert wrong not in body
    assert "wrong_choice_or_output" not in body

    asset_body = (tmp_path / ".system" / "memory" / "tutor" / "correct-asset-seeds" / f"{analysis.correct_asset_seed_id}.json").read_text(encoding="utf-8")
    unit_body = (tmp_path / ".system" / "memory" / "tutor" / "daily-review-unit-seeds" / f"{analysis.daily_review_unit_seed_id}.json").read_text(encoding="utf-8")
    assert wrong not in asset_body
    assert wrong not in unit_body
    assert "wrong_choice_or_output" not in asset_body
    assert "wrong_choice_or_output" not in unit_body
