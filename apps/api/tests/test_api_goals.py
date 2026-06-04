from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_goal_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_course_packs_list_safe_local_starters_on_fresh_state(client: TestClient) -> None:
    response = client.get("/api/goals/packs")

    assert response.status_code == 200
    payload = response.json()
    pack_ids = {pack["pack_id"] for pack in payload["packs"]}
    assert {
        "custom_exam_course",
        "language_learning",
        "cfa_finance",
        "spanish_english_vocabulary",
        "academic_english_vocabulary",
    }.issubset(pack_ids)

    cfa = next(pack for pack in payload["packs"] if pack["pack_id"] == "cfa_finance")
    assert cfa["pack_type"] == "exam"
    assert "Review Lab" in cfa["default_modules"]
    assert "Formula Lab" in cfa["default_modules"]
    assert "Assessments" in cfa["default_modules"]
    assert all("proprietary" not in json.dumps(topic).lower() for topic in cfa["syllabus_seed"])

    spanish = next(pack for pack in payload["packs"] if pack["pack_id"] == "spanish_english_vocabulary")
    assert spanish["pack_type"] == "language"
    assert "LanguageOS" in spanish["default_modules"]
    assert any(item["import_type"] == "dictionary" for item in spanish["suggested_imports"])


def test_goal_profile_create_activate_patch_archive_lifecycle(client: TestClient) -> None:
    created = client.post(
        "/api/goals",
        json={
            "profile_id": "p1",
            "title": "CFA Level I",
            "goal_type": "exam",
            "target_exam": "CFA Level I",
            "pack_id": "cfa_finance",
            "weekly_minutes": 600,
            "default_energy_mode": "normal",
            "wrong_choice_or_output": "UNIQUE_WRONG_GOAL_CREATE",
        },
    )

    assert created.status_code == 200
    goal = created.json()["goal"]
    assert goal["goal_id"]
    assert goal["profile_id"] == "p1"
    assert goal["status"] == "draft"
    assert goal["weekly_minutes"] == 600
    assert "Formula Lab" in goal["enabled_modules"]
    assert "wrong_choice_or_output" not in json.dumps(goal, ensure_ascii=False)

    activated = client.post(f"/api/goals/{goal['goal_id']}/activate")
    assert activated.status_code == 200
    assert activated.json()["goal"]["status"] == "active"

    listed = client.get("/api/goals")
    assert listed.status_code == 200
    assert listed.json()["active_goal"]["goal_id"] == goal["goal_id"]
    assert any(item["goal_id"] == goal["goal_id"] for item in listed.json()["goals"])

    patched = client.patch(
        f"/api/goals/{goal['goal_id']}",
        json={"weekly_minutes": 720, "default_energy_mode": "high", "enabled_modules": ["Review Lab", "Tutor"]},
    )
    assert patched.status_code == 200
    assert patched.json()["goal"]["weekly_minutes"] == 720
    assert patched.json()["goal"]["default_energy_mode"] == "high"
    assert patched.json()["goal"]["enabled_modules"] == ["Review Lab", "Tutor"]

    archived = client.post(f"/api/goals/{goal['goal_id']}/archive")
    assert archived.status_code == 200
    assert archived.json()["goal"]["status"] == "archived"
    assert client.get("/api/goals").json()["active_goal"] is None


def test_onboarding_fresh_state_readiness_day1_plan_is_safe_and_quality_gated(
    client: TestClient,
    tmp_path: Path,
) -> None:
    fresh = client.get("/api/onboarding/state")
    assert fresh.status_code == 200
    assert fresh.json()["readiness_score"] == 0
    assert fresh.json()["readiness_status"] == "not_started"
    assert fresh.json()["current_step"] == "choose_goal"

    goal = _create_and_activate_goal(client, pack_id="cfa_finance")
    after_goal = client.get("/api/onboarding/readiness?profile_id=p1")
    assert after_goal.status_code == 200
    assert after_goal.json()["readiness_score"] >= 0.2
    assert after_goal.json()["readiness_score"] < 1
    assert after_goal.json()["readiness_status"] in {"needs_import", "needs_confirmation", "ready_for_first_plan"}

    wrong_phrase = "UNIQUE_WRONG_ONBOARDING_DAY1"
    _seed_onboarding_fixture(tmp_path, wrong_phrase=wrong_phrase, confirmed=False)
    day1 = client.post("/api/onboarding/generate-day1-plan", json={"profile_id": "p1"})
    assert day1.status_code == 200
    day1_payload = day1.json()
    payload_text = json.dumps(day1_payload, ensure_ascii=False)

    assert day1_payload["goal"]["goal_id"] == goal["goal_id"]
    assert day1_payload["blocks"]
    assert any(block["block_type"] in {"import", "confirmation"} for block in day1_payload["blocks"])
    assert any(block["launch_route"] == "/review/data" for block in day1_payload["blocks"])
    assert "wrong_choice_or_output" not in payload_text
    assert "wrong_formula" not in payload_text
    assert "wrong_reasoning" not in payload_text
    assert wrong_phrase not in payload_text

    state = client.get("/api/onboarding/state?profile_id=p1")
    assert state.status_code == 200
    assert "generate_first_plan" in state.json()["completed_steps"]
    assert state.json()["readiness_score"] > after_goal.json()["readiness_score"]


def test_readiness_improves_after_confirmed_assets_and_plan(client: TestClient, tmp_path: Path) -> None:
    _create_and_activate_goal(client, pack_id="cfa_finance")
    initial_score = client.get("/api/onboarding/readiness?profile_id=p1").json()["readiness_score"]

    _seed_onboarding_fixture(tmp_path, wrong_phrase="UNIQUE_WRONG_READY_CONFIRMED", confirmed=True)
    ready = client.get("/api/onboarding/readiness?profile_id=p1")
    assert ready.status_code == 200
    ready_payload = ready.json()
    assert ready_payload["readiness_score"] > initial_score
    assert ready_payload["components"]["confirmed_assets_or_lexical_items"]["earned"] is True
    assert ready_payload["components"]["source_refs_present"]["earned"] is True

    day1 = client.post("/api/onboarding/generate-day1-plan", json={"profile_id": "p1"})
    assert day1.status_code == 200
    block_types = {block["block_type"] for block in day1.json()["blocks"]}
    assert "review_lab" in block_types
    assert "formula_lab" in block_types
    assert "mission_control_review" in block_types

    after_plan = client.get("/api/onboarding/readiness?profile_id=p1").json()
    assert after_plan["components"]["plan_generated"]["earned"] is True
    assert after_plan["readiness_score"] >= ready_payload["readiness_score"]


def test_language_and_exam_packs_recommend_different_modules_and_steps(client: TestClient) -> None:
    language = client.post(
        "/api/goals",
        json={
            "profile_id": "lang",
            "title": "Spanish Vocabulary",
            "goal_type": "language",
            "pack_id": "spanish_english_vocabulary",
            "target_language": "es",
            "source_language": "en",
            "weekly_minutes": 210,
            "default_energy_mode": "low",
        },
    )
    assert language.status_code == 200
    language_goal = language.json()["goal"]
    assert "LanguageOS" in language_goal["enabled_modules"]
    assert "Lexical Review" in language_goal["enabled_modules"]
    assert "Formula Lab" not in language_goal["enabled_modules"]

    client.post(f"/api/goals/{language_goal['goal_id']}/activate")
    language_day1 = client.post("/api/onboarding/generate-day1-plan", json={"profile_id": "lang"})
    assert language_day1.status_code == 200
    assert any(block["block_type"] == "dictionary_import" for block in language_day1.json()["blocks"])

    exam = client.post(
        "/api/goals",
        json={
            "profile_id": "exam",
            "title": "Finance Exam",
            "goal_type": "exam",
            "pack_id": "cfa_finance",
            "weekly_minutes": 480,
            "default_energy_mode": "normal",
        },
    )
    assert exam.status_code == 200
    exam_goal = exam.json()["goal"]
    assert "Review Lab" in exam_goal["enabled_modules"]
    assert "Coverage" in exam_goal["enabled_modules"]
    assert "Assessments" in exam_goal["enabled_modules"]
    assert "Formula Lab" in exam_goal["enabled_modules"]


def test_onboarding_steps_skip_reset_and_mission_control_integration(client: TestClient) -> None:
    mission_empty = client.get("/api/review-lab/mission-control")
    assert mission_empty.status_code == 200
    assert mission_empty.json()["onboarding"]["readiness_status"] == "not_started"
    assert any(action["action_id"] == "start_onboarding" for action in mission_empty.json()["recommended_actions"])

    goal = _create_and_activate_goal(client, pack_id="custom_exam_course")
    completed = client.post("/api/onboarding/step", json={"profile_id": "p1", "step_id": "set_time_budget"})
    assert completed.status_code == 200
    assert "set_time_budget" in completed.json()["completed_steps"]

    skipped = client.post("/api/onboarding/skip-step", json={"profile_id": "p1", "step_id": "import_resources_or_files"})
    assert skipped.status_code == 200
    assert "import_resources_or_files" in skipped.json()["skipped_steps"]

    mission_active = client.get("/api/review-lab/mission-control")
    assert mission_active.status_code == 200
    assert mission_active.json()["active_goal"]["goal_id"] == goal["goal_id"]
    assert mission_active.json()["onboarding"]["active_goal_id"] == goal["goal_id"]

    reset = client.post("/api/onboarding/reset", json={"profile_id": "p1"})
    assert reset.status_code == 200
    assert reset.json()["completed_steps"] == []
    assert reset.json()["current_step"] == "choose_goal"


def test_goal_and_onboarding_data_governance_inventory_and_safe_export(
    client: TestClient,
    tmp_path: Path,
) -> None:
    _create_and_activate_goal(client, pack_id="cfa_finance")
    assert client.post("/api/onboarding/step", json={"profile_id": "p1", "step_id": "choose_goal"}).status_code == 200

    inventory = client.get("/api/data-governance/inventory")
    assert inventory.status_code == 200
    categories = {item["category"]: item for item in inventory.json()["items"]}
    assert "goal_profiles" in categories
    assert "onboarding_state" in categories
    assert categories["goal_profiles"]["record_count"] >= 1
    assert categories["onboarding_state"]["record_count"] >= 1

    export = client.post("/api/data-governance/export", json={"mode": "safe"})
    assert export.status_code == 200
    export_path = tmp_path / export.json()["snapshot"]["file_path"]
    assert export_path.exists()
    with zipfile.ZipFile(export_path) as archive:
        names = set(archive.namelist())
    assert "data/goal_profiles.json" in names
    assert "data/onboarding_state.json" in names
    archive_bytes = export_path.read_bytes()
    for forbidden in [b"wrong_choice_or_output", b"wrong_formula", b"wrong_reasoning", b"answer_text", b"selected_choice"]:
        assert forbidden not in archive_bytes


def _create_and_activate_goal(client: TestClient, *, pack_id: str) -> dict:
    created = client.post(
        "/api/goals",
        json={
            "profile_id": "p1",
            "title": "CFA Level I",
            "goal_type": "exam",
            "target_exam": "CFA Level I",
            "pack_id": pack_id,
            "weekly_minutes": 600,
            "default_energy_mode": "normal",
        },
    )
    assert created.status_code == 200
    goal = created.json()["goal"]
    activated = client.post(f"/api/goals/{goal['goal_id']}/activate")
    assert activated.status_code == 200
    return activated.json()["goal"]


def _seed_onboarding_fixture(repo_root: Path, *, wrong_phrase: str, confirmed: bool) -> None:
    validation_status = "confirmed" if confirmed else "draft"
    review_root = repo_root / ".system" / "memory" / "review"
    _write_json(
        review_root / "syllabus" / "topics.json",
        [
            {
                "topic_id": "topic-onboarding-wacc",
                "profile_id": "p1",
                "subject": "Corporate Issuers",
                "module": "Cost of Capital",
                "los": "GOAL-WACC",
                "title": "Generic WACC overview",
                "description": "Generic placeholder topic for a finance exam pack.",
                "source_refs": ["onboarding-wacc#seg-1"],
                "formula_expected": True,
            }
        ],
    )
    _write_json(
        review_root / "asset-candidates" / "asset-onboarding-wacc.json",
        {
            "asset_id": "asset-onboarding-wacc",
            "profile_id": "p1",
            "asset_type": "formula",
            "title": "Generic WACC formula",
            "correct_rule": "Use after-tax debt cost and target capital weights.",
            "plain_formula": "WACC = w_d r_d (1 - t) + w_e r_e",
            "ba_ii_plus_steps": ["Use WACC as I/Y for NPV valuation"],
            "source_refs": ["onboarding-wacc#seg-1"],
            "validation_status": validation_status,
            "source_quality": 0.9,
            "wrong_choice_or_output": wrong_phrase,
            "wrong_formula": wrong_phrase,
            "wrong_reasoning": wrong_phrase,
            "answer_text": wrong_phrase,
            "selected_choice": wrong_phrase,
        },
    )


def _enable_goal_features(repo_root: Path) -> None:
    config_path = repo_root / ".system" / "config" / "features.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "\n".join(
            [
                "daily_review_lab: true",
                "daily_review_lab_enabled: true",
                "review_asset_ingestion_enabled: true",
                "review_asset_manual_confirm_required: true",
                "review_asset_draft_preview_enabled: false",
                "formula_lab_enabled: true",
                "formula_ba_ii_plus_steps_enabled: true",
                "syllabus_coverage_enabled: true",
                "syllabus_demo_seed_enabled: true",
                "mock_retro_enabled: true",
                "resource_quality_gate_enabled: true",
                "dictionary_kernel_enabled: true",
                "lexical_review_enabled: true",
                "language_os_enabled: true",
                "mission_control_enabled: true",
                "integration_health_checks_enabled: true",
                "green_test_gate_enabled: true",
                "study_planner_enabled: true",
                "adaptive_session_orchestrator_enabled: true",
                "energy_aware_planning_enabled: true",
                "learning_analytics_enabled: true",
                "adaptive_assessment_enabled: true",
                "knowledge_graph_enabled: true",
                "global_search_enabled: true",
                "data_governance_enabled: true",
                "safe_export_enabled: true",
                "backup_restore_enabled: true",
                "privacy_redaction_enabled: true",
                "tutor_copilot_enabled: true",
                "grounded_tutor_retrieval_enabled: true",
                "tutor_correct_only_enabled: true",
                "goal_profiles_enabled: true",
                "course_packs_enabled: true",
                "first_run_onboarding_enabled: true",
                "day1_plan_enabled: true",
                "onboarding_readiness_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
