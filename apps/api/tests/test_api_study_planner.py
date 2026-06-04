from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app
from study_science.study_planner import StudyPlannerService


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_planner_features(repo.root)
    _write_daily_review_snapshot(repo.root, review_id="daily-review-planner")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_study_planner_fresh_state_returns_safe_default_plan(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_planner_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        with TestClient(app) as fresh_client:
            response = fresh_client.post(
                "/api/study-planner/generate",
                json={"profile_id": "fresh", "energy_mode": "normal", "available_minutes": 60},
            )
            assert response.status_code == 200
            payload = response.json()
            assert payload["profile_id"] == "fresh"
            assert payload["energy_mode"] == "normal"
            assert payload["available_minutes"] == 60
            assert payload["status"] == "draft"
            assert payload["blocks"]
            assert sum(block["target_minutes"] for block in payload["blocks"]) <= 60
            assert {block["block_type"] for block in payload["blocks"]}.issubset(
                {"mission_control_review", "reflection"}
            )
            assert payload["recommended_next_actions"]

            today = fresh_client.get("/api/study-planner/today?profile_id=fresh")
            assert today.status_code == 200
            assert today.json()["plan_id"] == payload["plan_id"]
    finally:
        app.dependency_overrides.clear()


def test_study_planner_is_energy_aware_and_correct_only(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_STUDY_PLAN"
    _seed_cross_system_signals(client, wrong_phrase=wrong_phrase)

    low = client.post(
        "/api/study-planner/generate",
        json={"profile_id": "default", "energy_mode": "low", "available_minutes": 40, "goal": "WACC and transfer"},
    )
    high = client.post(
        "/api/study-planner/generate",
        json={"profile_id": "default", "energy_mode": "high", "available_minutes": 150, "goal": "WACC and transfer"},
    )

    assert low.status_code == 200
    assert high.status_code == 200
    low_payload = low.json()
    high_payload = high.json()
    assert low_payload["blocks"]
    assert high_payload["blocks"]
    assert sum(block["target_minutes"] for block in low_payload["blocks"]) <= 40
    assert sum(block["target_minutes"] for block in high_payload["blocks"]) <= 150
    assert len(high_payload["blocks"]) >= len(low_payload["blocks"])

    low_types = [block["block_type"] for block in low_payload["blocks"]]
    high_types = [block["block_type"] for block in high_payload["blocks"]]
    assert low_types != high_types
    assert "review_lab" in high_types
    assert "formula_lab" in high_types
    assert "lexical_review" in high_types
    assert "coverage_gap" in high_types
    assert "mock_transfer_drill" in high_types
    assert "file_ingestion_cleanup" in high_types

    payload = json.dumps(high_payload, ensure_ascii=False)
    assert "wrong_choice_or_output" not in payload
    assert "wrong_formula" not in payload
    assert "wrong_reasoning" not in payload
    assert wrong_phrase not in payload


def test_study_planner_prefers_actionable_confirmation_before_blocked_work(tmp_path: Path) -> None:
    service = StudyPlannerService(tmp_path)
    blocked = service._candidate(
        plan_id="plan-actionability",
        block_type="resource_confirmation",
        title="Blocked resource gate",
        description="Cannot run until quality gate is resolved.",
        launch_route="/review/resources",
        due_reason="Unscored resources are blocked.",
        priority=99,
        blocked_reason="Resource quality gate must pass first.",
    )
    actionable = service._candidate(
        plan_id="plan-actionability",
        block_type="asset_confirmation",
        title="Confirm source-backed draft",
        description="Manual confirmation can be done now.",
        launch_route="/review/assets",
        due_reason="Draft assets need confirmation.",
        priority=10,
    )

    blocks = service._compose_blocks(
        plan_id="plan-actionability",
        candidates=[blocked, actionable],
        energy_mode="normal",
        available_minutes=30,
    )

    assert blocks
    assert blocks[0].status == "pending"
    assert blocks[0].title == "Confirm source-backed draft"


def test_study_planner_keeps_draft_assets_out_of_review_blocks(client: TestClient) -> None:
    imported = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "profile_id": "default",
            "title": "Draft Planner Asset Note",
            "text": "\n".join(
                [
                    "LOS: CI-PLAN-DRAFT",
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use WACC when valuing a firm with a target capital structure.",
                ]
            ),
            "source_type": "text_note",
        },
    )
    assert imported.status_code == 200
    extracted = client.post(f"/api/review-lab/sources/{imported.json()['source']['source_id']}/extract-assets")
    assert extracted.status_code == 200
    draft_ids = {asset["asset_id"] for asset in extracted.json()["assets"]}
    assert draft_ids

    plan = client.post(
        "/api/study-planner/generate",
        json={"profile_id": "default", "energy_mode": "normal", "available_minutes": 90},
    )
    assert plan.status_code == 200
    blocks = plan.json()["blocks"]
    review_linked_ids = {
        asset_id
        for block in blocks
        if block["block_type"] == "review_lab"
        for asset_id in block["linked_asset_ids"]
    }
    assert not (draft_ids & review_linked_ids)
    confirmation = [block for block in blocks if block["block_type"] == "asset_confirmation"]
    assert confirmation
    assert any(draft_ids & set(block["linked_asset_ids"]) for block in confirmation)
    assert any("not used as review content" in block["due_reason"] for block in confirmation)


def test_study_planner_block_lifecycle_and_retro(client: TestClient) -> None:
    _seed_cross_system_signals(client, wrong_phrase="UNIQUE_WRONG_LIFECYCLE")
    generated = client.post(
        "/api/study-planner/generate",
        json={"energy_mode": "normal", "available_minutes": 90, "goal": "finish today's highest-value review"},
    )
    assert generated.status_code == 200
    plan_id = generated.json()["plan_id"]
    first = next(block for block in generated.json()["blocks"] if block["status"] == "pending")
    second = next(block for block in generated.json()["blocks"] if block["block_id"] != first["block_id"])

    activated = client.post(f"/api/study-planner/plans/{plan_id}/activate")
    assert activated.status_code == 200
    assert activated.json()["status"] == "active"

    started = client.post(f"/api/study-planner/blocks/{first['block_id']}/start")
    assert started.status_code == 200
    assert started.json()["block"]["status"] == "in_progress"

    completed = client.post(
        f"/api/study-planner/blocks/{first['block_id']}/complete",
        json={"outcome": "completed recall block", "actual_minutes": first["target_minutes"]},
    )
    assert completed.status_code == 200
    assert completed.json()["block"]["status"] == "completed"

    skipped = client.post(
        f"/api/study-planner/blocks/{second['block_id']}/skip",
        json={"reason": "defer until evening"},
    )
    assert skipped.status_code == 200
    assert skipped.json()["block"]["status"] == "skipped"
    assert "defer until evening" in skipped.json()["block"]["completion_outcome"]

    finished = client.post(f"/api/study-planner/plans/{plan_id}/complete")
    assert finished.status_code == 200
    summary = finished.json()["summary"]
    assert finished.json()["status"] == "completed"
    assert summary["completed_blocks"] >= 1
    assert summary["skipped_blocks"] >= 1
    assert summary["completed_minutes"] >= first["target_minutes"]
    assert finished.json()["recommended_next_actions"]

    history = client.get("/api/study-planner/history")
    assert history.status_code == 200
    assert any(plan["plan_id"] == plan_id for plan in history.json()["plans"])


def test_mission_control_registry_includes_study_planner(client: TestClient) -> None:
    summary = client.get("/api/review-lab/mission-control")
    assert summary.status_code == 200
    assert any(action["action_id"] == "generate_study_plan" for action in summary.json()["recommended_actions"])

    registry = client.get("/api/review-lab/route-registry")
    assert registry.status_code == 200
    payload = registry.json()
    pages = {item["path"]: item["implemented"] for item in payload["expected_pages"]}
    routes = {item["path"]: item["mounted"] for item in payload["expected_api_routes"]}
    assert pages["/review/study-planner"]
    assert routes["/api/study-planner/generate"]
    assert routes["/api/study-planner/today"]
    assert payload["feature_groups"]["study_planner"]["enabled"]


def _seed_cross_system_signals(client: TestClient, *, wrong_phrase: str) -> None:
    assert client.post("/api/review-lab/syllabus/seed-demo").status_code == 200
    assert client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "topics": [
                {
                    "topic_id": "topic-planner-missing",
                    "subject": "Corporate Issuers",
                    "module": "Planner Coverage",
                    "los": "CI-PLAN-MISS",
                    "title": "Explain marginal cost of capital schedule breakpoints",
                    "exam_weight": 0.9,
                    "expected_asset_types": ["definition", "formula"],
                    "formula_expected": True,
                }
            ]
        },
    ).status_code == 200

    formula = client.post(
        "/api/review-lab/formulas/import-text",
        json={
            "profile_id": "default",
            "title": "Planner WACC Formula",
            "text": "\n".join(
                [
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use after-tax cost of debt with target capital structure weights.",
                    "BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.",
                ]
            ),
        },
    )
    assert formula.status_code == 200
    formula_asset_id = next(asset["asset_id"] for asset in formula.json()["assets"] if asset["asset_type"] == "formula")
    assert client.post(f"/api/review-lab/formulas/{formula_asset_id}/confirm").status_code == 200

    mock = client.post(
        "/api/review-lab/mock-retro/import-text",
        json={
            "title": "Planner Mock Retro",
            "text": "\n".join(
                [
                    "Q1 Corporate Issuers WACC",
                    "LOS: CI-PLAN-MOCK",
                    "Result: incorrect",
                    "Confidence: high",
                    f"Wrong Output: {wrong_phrase}",
                    "Correct Rule: WACC uses after-tax cost of debt.",
                    "Tested Formula: WACC",
                ]
            ),
        },
    )
    assert mock.status_code == 200
    assert client.post(f"/api/review-lab/mock-retro/sessions/{mock.json()['session']['mock_id']}/analyze").status_code == 200

    dictionary = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "Planner Spanish Dictionary",
            "dictionary_type": "spanish_english",
            "entries": [
                {
                    "headword": "aprovechar",
                    "language": "es",
                    "target_language": "en",
                    "part_of_speech": "verb",
                    "definition": "to take advantage of; to make use of",
                    "translation": "take advantage of",
                    "example_sentence": "Debemos aprovechar esta oportunidad.",
                }
            ],
        },
    )
    assert dictionary.status_code == 201
    dictionary_payload = dictionary.json()
    assert client.post(
        f"/api/language-os/dictionaries/{dictionary_payload['dictionary']['dictionary_id']}/confirm"
    ).status_code == 200
    assert client.post(
        f"/api/language-os/lexical-assets/{dictionary_payload['lexical_assets'][0]['lexical_id']}/confirm"
    ).status_code == 200

    resource = client.post(
        "/api/review-lab/resources/import-text",
        json={
            "title": "Planner Low Quality Candidate",
            "text": "WACC reminder only.",
            "resource_type": "manual",
        },
    )
    assert resource.status_code == 200

    unsupported = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Unsupported Planner File"},
        files={"file": ("planner.bin", b"binary", "application/octet-stream")},
    )
    assert unsupported.status_code == 200


def _enable_planner_features(repo_root: Path) -> None:
    config_path = repo_root / ".system" / "config" / "features.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "\n".join(
            [
                "daily_review_lab: true",
                "daily_review_lab_enabled: true",
                "daily_review_correct_only_mode: true",
                "daily_review_asset_scoring: true",
                "daily_review_unit_scoring: true",
                "review_asset_ingestion_enabled: true",
                "review_asset_manual_confirm_required: true",
                "review_asset_draft_preview_enabled: false",
                "formula_lab: true",
                "formula_lab_enabled: true",
                "formula_asset_enrichment_enabled: true",
                "formula_review_units_enabled: true",
                "formula_ba_ii_plus_steps_enabled: true",
                "syllabus_coverage_enabled: true",
                "syllabus_demo_seed_enabled: true",
                "syllabus_asset_mapping_enabled: true",
                "coverage_guided_review_selection_enabled: true",
                "mock_retro_enabled: true",
                "transfer_gap_priority_enabled: true",
                "mock_retro_correct_only_mode: true",
                "mock_retro_review_generation_enabled: true",
                "resource_quality_gate_enabled: true",
                "resource_evidence_extraction_enabled: true",
                "resource_asset_promotion_enabled: true",
                "resource_quality_guided_review_enabled: true",
                "resource_conflict_detection_enabled: true",
                "dictionary_kernel_enabled: true",
                "lexical_review_enabled: true",
                "dictionary_quality_gate_enabled: true",
                "spanish_english_dictionary_enabled: true",
                "english_english_dictionary_enabled: true",
                "language_os_enabled: true",
                "mission_control_enabled: true",
                "integration_health_checks_enabled: true",
                "green_test_gate_enabled: true",
                "file_ingestion_enabled: true",
                "pdf_text_extraction_enabled: true",
                "dictionary_file_import_enabled: true",
                "resource_file_import_enabled: true",
                "file_duplicate_detection_enabled: true",
                "ocr_extraction_enabled: false",
                "study_planner_enabled: true",
                "adaptive_session_orchestrator_enabled: true",
                "energy_aware_planning_enabled: true",
                "study_plan_retro_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_daily_review_snapshot(repo_root: Path, review_id: str) -> None:
    snapshot_root = repo_root / ".system" / "memory" / "review" / "daily"
    snapshot_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "review_id": review_id,
        "knowledge_points": [
            {
                "knowledge_id": "planner-kp-1",
                "subject": "Corporate Issuers",
                "heading": "Cost of Capital",
                "trigger": "Recall WACC component weights.",
                "decision": "Use market-value weights and after-tax debt cost for WACC.",
                "priority": 92,
                "reason": "Due today",
                "state": "Learning",
                "source_refs": ["planner/corporate-issuers#wacc"],
            },
            {
                "knowledge_id": "planner-kp-2",
                "subject": "Fixed Income",
                "heading": "Duration",
                "trigger": "Recall effective duration use case.",
                "decision": "Use effective duration when cash flows may change with rates.",
                "priority": 84,
                "reason": "Spacing pressure",
                "state": "New",
                "source_refs": ["planner/fixed-income#duration"],
            },
        ],
        "mistake_cards": [],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    (snapshot_root / f"{review_id}.json").write_text(text, encoding="utf-8")
    (snapshot_root / "latest.json").write_text(text, encoding="utf-8")
