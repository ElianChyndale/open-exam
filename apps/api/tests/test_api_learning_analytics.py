from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_analytics_features(repo.root)
    _write_daily_review_snapshot(repo.root, review_id="daily-review-analytics")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_learning_analytics_empty_state_is_safe(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_analytics_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        with TestClient(app) as fresh_client:
            summary = fresh_client.get("/api/learning-analytics/summary?profile_id=fresh&range=30d")
            assert summary.status_code == 200
            payload = summary.json()
            for key in (
                "overall",
                "review_lab",
                "formula_lab",
                "language_os",
                "study_planner",
                "coverage",
                "mock_retro",
                "resource_os",
                "file_ingestion",
                "calibration",
            ):
                assert key in payload
            assert payload["overall"]["event_count"] == 0
            assert payload["recommended_strategy_adjustments"]

            events = fresh_client.get("/api/learning-analytics/events?profile_id=fresh")
            assert events.status_code == 200
            assert events.json()["events"] == []
    finally:
        app.dependency_overrides.clear()


def test_learning_analytics_correct_only_and_cross_system(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_ANALYTICS_PHRASE"
    _seed_cross_system_analytics_fixture(client, wrong_phrase=wrong_phrase)

    recompute = client.post("/api/learning-analytics/recompute", json={"profile_id": "default", "range": "30d"})
    assert recompute.status_code == 200
    assert recompute.json()["event_count"] >= 8

    summary = client.get("/api/learning-analytics/summary?profile_id=default&range=30d")
    assert summary.status_code == 200
    payload = summary.json()
    for key in (
        "overall",
        "review_lab",
        "formula_lab",
        "language_os",
        "study_planner",
        "coverage",
        "mock_retro",
        "resource_os",
        "file_ingestion",
        "calibration",
    ):
        assert key in payload
    assert payload["review_lab"]["attempts"] >= 2
    assert payload["formula_lab"]["attempts"] >= 1
    assert payload["language_os"]["attempts"] >= 1
    assert payload["study_planner"]["plan_count"] >= 1
    assert payload["study_planner"]["completed_blocks"] >= 1
    assert payload["coverage"]["topic_count"] >= 1
    assert payload["mock_retro"]["open_transfer_gap_count"] >= 1
    assert payload["resource_os"]["promoted_assets"] >= 1
    assert payload["calibration"]["overconfidence_count"] >= 1
    assert payload["calibration"]["underconfidence_count"] >= 1
    assert payload["recommended_strategy_adjustments"]
    priorities = [item["priority"] for item in payload["recommended_strategy_adjustments"]]
    assert priorities == sorted(priorities, reverse=True)

    events = client.get("/api/learning-analytics/events?profile_id=default&range=30d")
    assert events.status_code == 200
    event_payload = events.json()
    subsystems = {event["subsystem"] for event in event_payload["events"]}
    assert {"review_lab", "formula_lab", "language_os", "study_planner", "coverage", "mock_retro", "resource_os", "file_ingestion", "assets"}.intersection(subsystems)

    body = json.dumps({"summary": payload, "events": event_payload}, ensure_ascii=False)
    assert "wrong_choice_or_output" not in body
    assert "wrong_formula" not in body
    assert "wrong_reasoning" not in body
    assert wrong_phrase not in body


def test_learning_analytics_endpoint_breakouts(client: TestClient) -> None:
    _seed_cross_system_analytics_fixture(client, wrong_phrase="UNIQUE_WRONG_BREAKOUT_ANALYTICS")

    calibration = client.get("/api/learning-analytics/calibration")
    assert calibration.status_code == 200
    records = calibration.json()["records"]
    assert any(record["scope_type"] == "global" for record in records)
    assert any(record["overconfidence_count"] for record in records)

    mastery = client.get("/api/learning-analytics/mastery-trends")
    assert mastery.status_code == 200
    assert mastery.json()["records"]

    plan = client.get("/api/learning-analytics/plan-effectiveness")
    assert plan.status_code == 200
    assert plan.json()["block_completion_by_type"]

    resources = client.get("/api/learning-analytics/resource-usefulness")
    assert resources.status_code == 200
    assert resources.json()["resources"]

    coverage = client.get("/api/learning-analytics/coverage-momentum")
    assert coverage.status_code == 200
    assert coverage.json()["topic_count"] >= 1

    formulas = client.get("/api/learning-analytics/formula-outcomes")
    assert formulas.status_code == 200
    assert formulas.json()["attempts"] >= 1

    language = client.get("/api/learning-analytics/language-outcomes")
    assert language.status_code == 200
    assert language.json()["attempts"] >= 1


def _seed_cross_system_analytics_fixture(client: TestClient, *, wrong_phrase: str) -> None:
    assert client.post("/api/review-lab/syllabus/seed-demo").status_code == 200

    review = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-analytics", "energy_level": 2, "max_units": 5},
    )
    assert review.status_code == 200
    units = review.json()["units"]
    session_id = review.json()["session_id"]
    assert len(units) >= 2
    assert client.post(
        f"/api/review-lab/sessions/{session_id}/units/{units[0]['unit_id']}/outcome",
        json={
            "confidence_before": 4,
            "time_spent_seconds": 35,
            "needed_hint": False,
            "outcome": "forgot",
            "confidence_after": 1,
            "answer_quality": "blank",
            "next_action": "drill",
        },
    ).status_code == 200
    assert client.post(
        f"/api/review-lab/sessions/{session_id}/units/{units[1]['unit_id']}/outcome",
        json={
            "confidence_before": 0,
            "time_spent_seconds": 22,
            "needed_hint": False,
            "outcome": "recalled",
            "confidence_after": 3,
            "answer_quality": "perfect",
            "next_action": "advance",
        },
    ).status_code == 200

    formula = client.post(
        "/api/review-lab/formulas/import-text",
        json={
            "title": "Analytics WACC Formula",
            "text": "\n".join(
                [
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use after-tax cost of debt with target weights.",
                    "BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.",
                ]
            ),
        },
    )
    assert formula.status_code == 200
    formula_asset = next(asset for asset in formula.json()["assets"] if asset["asset_type"] == "formula")
    assert client.post(f"/api/review-lab/formulas/{formula_asset['asset_id']}/confirm").status_code == 200
    formula_session = client.post("/api/review-lab/formulas/generate-session", json={"max_units": 5})
    assert formula_session.status_code == 200
    formula_unit = formula_session.json()["units"][0]
    assert client.post(
        f"/api/review-lab/formulas/units/{formula_unit['unit_id']}/complete",
        json={
            "session_id": formula_session.json()["session_id"],
            "confidence_before": 3,
            "time_spent_seconds": 40,
            "needed_hint": True,
            "outcome": "partial",
            "confidence_after": 2,
            "answer_quality": "minor_gap",
            "next_action": "drill",
        },
    ).status_code == 200

    dictionary = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "Analytics Spanish Dictionary",
            "dictionary_type": "spanish_english",
            "entries": [
                {
                    "headword": "repasar",
                    "language": "es",
                    "target_language": "en",
                    "part_of_speech": "verb",
                    "definition": "to review or go over again",
                    "translation": "review",
                    "example_sentence": "Voy a repasar la formula.",
                    "collocations": ["repasar una formula"],
                }
            ],
        },
    )
    assert dictionary.status_code == 201
    dictionary_payload = dictionary.json()
    assert client.post(f"/api/language-os/dictionaries/{dictionary_payload['dictionary']['dictionary_id']}/confirm").status_code == 200
    lexical_id = dictionary_payload["lexical_assets"][0]["lexical_id"]
    assert client.post(f"/api/language-os/lexical-assets/{lexical_id}/confirm").status_code == 200
    lexical_session = client.post("/api/language-os/review/generate-session", json={"max_units": 5})
    assert lexical_session.status_code == 200
    lexical_unit = lexical_session.json()["units"][0]
    assert client.post(
        f"/api/language-os/review/units/{lexical_unit['unit_id']}/complete",
        json={"session_id": lexical_session.json()["session_id"], "outcome": "forgot", "time_spent_seconds": 18},
    ).status_code == 200

    retro = client.post(
        "/api/review-lab/mock-retro/import-text",
        json={
            "title": "Analytics Mock Retro",
            "text": "\n".join(
                [
                    "Q1 Corporate Issuers WACC",
                    "LOS: CI-ANALYTICS-MOCK",
                    "Result: incorrect",
                    "Confidence: high",
                    f"Wrong Output: {wrong_phrase}",
                    "Correct Rule: WACC uses after-tax cost of debt.",
                    "Tested Formula: WACC",
                ]
            ),
        },
    )
    assert retro.status_code == 200
    assert client.post(f"/api/review-lab/mock-retro/sessions/{retro.json()['session']['mock_id']}/analyze").status_code == 200

    resource = client.post(
        "/api/review-lab/resources/import-text",
        json={
            "title": "Analytics Resource WACC",
            "resource_type": "lecture_slide",
            "text": "\n".join(
                [
                    "LOS: CI-ANALYTICS-RESOURCE",
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use after-tax cost of debt with target capital structure.",
                    "Source: curriculum reading note.",
                ]
            ),
        },
    )
    assert resource.status_code == 200
    resource_id = resource.json()["resource"]["resource_id"]
    assert client.post(f"/api/review-lab/resources/{resource_id}/score").status_code == 200
    assert client.post(f"/api/review-lab/resources/{resource_id}/confirm").status_code == 200
    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    assert extracted.status_code == 200
    promote = client.post(f"/api/review-lab/resources/{resource_id}/promote-assets", json={"asset_ids": []})
    assert promote.status_code == 200

    unsupported = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Analytics Unsupported File"},
        files={"file": ("analytics.bin", b"binary", "application/octet-stream")},
    )
    assert unsupported.status_code == 200

    plan = client.post(
        "/api/study-planner/generate",
        json={"energy_mode": "normal", "available_minutes": 90, "goal": "analytics WACC"},
    )
    assert plan.status_code == 200
    blocks = plan.json()["blocks"]
    pending = [block for block in blocks if block["status"] == "pending"]
    assert pending
    assert client.post(f"/api/study-planner/blocks/{pending[0]['block_id']}/start").status_code == 200
    assert client.post(
        f"/api/study-planner/blocks/{pending[0]['block_id']}/complete",
        json={"outcome": "analytics completed block", "actual_minutes": pending[0]["target_minutes"]},
    ).status_code == 200
    if len(pending) > 1:
        assert client.post(
            f"/api/study-planner/blocks/{pending[1]['block_id']}/skip",
            json={"reason": "analytics skipped block"},
        ).status_code == 200
    assert client.post(f"/api/study-planner/plans/{plan.json()['plan_id']}/complete").status_code == 200
    assert client.post("/api/review-lab/syllabus/recompute-coverage").status_code == 200


def _enable_analytics_features(repo_root: Path) -> None:
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
                "study_planner_enabled: true",
                "adaptive_session_orchestrator_enabled: true",
                "energy_aware_planning_enabled: true",
                "study_plan_retro_enabled: true",
                "learning_analytics_enabled: true",
                "mastery_calibration_enabled: true",
                "plan_effectiveness_enabled: true",
                "resource_usefulness_enabled: true",
                "coverage_momentum_enabled: true",
                "correct_only_analytics_enabled: true",
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
                "knowledge_id": "analytics-kp-1",
                "subject": "Corporate Issuers",
                "heading": "Cost of Capital",
                "trigger": "Recall WACC debt cost.",
                "decision": "Use after-tax cost of debt in WACC.",
                "priority": 92,
                "reason": "Due today",
                "state": "Learning",
                "source_refs": ["analytics/corporate-issuers#wacc"],
            },
            {
                "knowledge_id": "analytics-kp-2",
                "subject": "Fixed Income",
                "heading": "Duration",
                "trigger": "Recall effective duration boundary.",
                "decision": "Use effective duration when cash flows can change.",
                "priority": 84,
                "reason": "Spacing pressure",
                "state": "New",
                "source_refs": ["analytics/fixed-income#duration"],
            },
        ],
        "mistake_cards": [],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    (snapshot_root / f"{review_id}.json").write_text(text, encoding="utf-8")
    (snapshot_root / "latest.json").write_text(text, encoding="utf-8")
