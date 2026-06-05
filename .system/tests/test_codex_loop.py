from __future__ import annotations

import json
from pathlib import Path

from app.codex_loop import complete_codex_loop_candidate, plan_codex_loop
from app.models import MistakeEvent
from app.skill_reflection import skill_reflection_from_validator_failure
from app.storage import Repository
from app.tutor_models import TutorAnalysisResult, TutorValidationResult


def _enable_loop(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "\n".join(
            [
                "codex_self_loop_enabled: true",
                "skill_reflection_enabled: true",
                "skill_upgrade_proposals_enabled: true",
                "skill_codex_task_generator_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_codex_loop_plan_writes_traceable_bootstrap_task(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)

    plan = plan_codex_loop(repo)

    assert plan.selected is not None
    assert plan.selected.candidate_id == "self-cycle-skill-governance"
    assert plan.task_path.startswith("docs/codex_tasks/TASK-")
    assert (tmp_path / plan.task_path).exists()
    assert (tmp_path / plan.plan_json_path).exists()
    assert (tmp_path / plan.plan_markdown_path).exists()
    events = repo.load_jsonl_events("codex_loop")
    assert events[-1]["event_type"] == "codex.loop.planned"
    assert events[-1]["candidate_id"] == "self-cycle-skill-governance"


def test_completed_candidate_is_skipped_on_next_plan(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)

    complete_codex_loop_candidate(
        repo,
        candidate_id="self-cycle-skill-governance",
        summary="Bootstrap workflow implemented.",
        artifacts=[".system/app/codex_loop.py"],
        verification="pytest -q .system/tests/test_codex_loop.py",
    )
    plan = plan_codex_loop(repo)

    assert plan.selected is not None
    assert plan.selected.candidate_id == "gap-admin-auth-boundary"


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


def test_skill_upgrade_proposal_can_be_selected_after_bootstrap(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)
    for index in range(3):
        _reflection(repo, index)

    from app.skill_upgrade import proposal_from_repeated_reflections

    proposal_from_repeated_reflections(repo, threshold=3)
    complete_codex_loop_candidate(
        repo,
        candidate_id="self-cycle-skill-governance",
        summary="Bootstrap workflow implemented.",
        artifacts=[".system/app/codex_loop.py"],
        verification="pytest -q .system/tests/test_codex_loop.py",
    )

    plan = plan_codex_loop(repo)

    assert plan.selected is not None
    assert plan.selected.candidate_id.startswith("proposal-")
    plan_payload = json.loads((tmp_path / plan.plan_json_path).read_text(encoding="utf-8"))
    assert plan_payload["selected"]["source"] == "skill_upgrade_proposal"


def test_frontend_auth_gap_candidate_is_selected_when_backend_auth_exists_without_ui_binding(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)
    complete_codex_loop_candidate(
        repo,
        candidate_id="self-cycle-skill-governance",
        summary="Bootstrap workflow implemented.",
        artifacts=[".system/app/codex_loop.py"],
        verification="pytest -q .system/tests/test_codex_loop.py",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-1-import-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-2-practice-generation",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-2-answer-wrongbook-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-3-practice-ui-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-3-safe-question-display-endpoint",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-4-analytics-extension-boundary",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )

    auth_router = tmp_path / "apps" / "api" / "routers"
    auth_router.mkdir(parents=True, exist_ok=True)
    (auth_router / "auth.py").write_text("@router.post('/login')\n", encoding="utf-8")
    frontend_lib = tmp_path / "apps" / "web" / "src" / "lib"
    frontend_lib.mkdir(parents=True, exist_ok=True)
    (frontend_lib / "api.ts").write_text("export const questionBanksApi = {};\n", encoding="utf-8")

    plan = plan_codex_loop(repo)

    assert plan.selected is not None
    assert plan.selected.candidate_id == "gap-auth-ui-session-integration"
