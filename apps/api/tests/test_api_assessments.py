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
    _enable_assessment_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_assessment_empty_state_is_safe(client: TestClient) -> None:
    generated = client.post(
        "/api/assessments/generate",
        json={"profile_id": "fresh", "mode": "quick_check", "target_minutes": 15, "question_count": 3},
    )
    assert generated.status_code == 200
    payload = generated.json()
    assert payload["profile_id"] == "fresh"
    assert payload["status"] == "draft"
    assert payload["question_ids"] == []
    assert payload["summary"]["available_question_count"] == 0

    listing = client.get("/api/assessments?profile_id=fresh")
    assert listing.status_code == 200
    assert listing.json()["assessments"]


def test_assessment_generation_uses_confirmed_assets_only(client: TestClient) -> None:
    source = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "title": "Assessment confirmed only source",
            "text": "\n".join(
                [
                    "LOS: CI-ASSESS-CONFIRMED",
                    "Use after-tax cost of debt in WACC.",
                    "Apply target capital weights when valuing a firm.",
                ]
            ),
        },
    )
    assert source.status_code == 200
    extracted = client.post(f"/api/review-lab/sources/{source.json()['source']['source_id']}/extract-assets")
    assert extracted.status_code == 200
    assets = extracted.json()["assets"]
    assert len(assets) >= 2
    confirmed_asset_id = assets[0]["asset_id"]
    rejected_asset_id = assets[1]["asset_id"]
    assert client.post(f"/api/review-lab/assets/{confirmed_asset_id}/confirm").status_code == 200
    assert client.post(f"/api/review-lab/assets/{rejected_asset_id}/reject").status_code == 200

    generated = client.post(
        "/api/assessments/generate",
        json={"mode": "quick_check", "target_minutes": 20, "question_count": 5},
    )
    assert generated.status_code == 200
    questions = generated.json()["questions"]
    linked_assets = {asset_id for question in questions for asset_id in question["linked_asset_ids"]}
    assert confirmed_asset_id in linked_assets
    assert rejected_asset_id not in linked_assets
    assert all(question["validation_status"] == "generated" for question in questions)


def test_assessment_interleaving_correct_only_and_updates_transfer_gap(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_ASSESSMENT_PHRASE"
    _seed_assessment_cross_system_fixture(client, wrong_phrase=wrong_phrase)

    generated = client.post(
        "/api/assessments/generate",
        json={
            "profile_id": "default",
            "mode": "interleaving_drill",
            "target_minutes": 30,
            "question_count": 8,
            "difficulty": "medium",
            "focus": "mixed",
        },
    )
    assert generated.status_code == 200
    session = generated.json()
    assert session["question_ids"]
    question_types = {question["question_type"] for question in session["questions"]}
    assert question_types.intersection({"formula_setup", "calculator_steps"})
    assert question_types.intersection({"lexical_production", "cloze", "collocation"})
    assert question_types.intersection({"mini_case", "boundary_choice"})
    assert len(question_types) >= 3

    start = client.post(f"/api/assessments/{session['assessment_id']}/start")
    assert start.status_code == 200
    question = session["questions"][0]
    answer = client.post(
        f"/api/assessments/questions/{question['question_id']}/answer",
        json={
            "answer_text": wrong_phrase,
            "selected_choice": "incorrect option if present",
            "confidence_before": 0.9,
            "time_spent_seconds": 35,
        },
    )
    assert answer.status_code == 200
    feedback = answer.json()["feedback"]
    assert "correct_rule" in feedback
    assert "correct_answer" in feedback
    assert "recommended_review_asset_ids" in feedback
    assert wrong_phrase not in json.dumps(feedback, ensure_ascii=False)

    grade = client.post(
        f"/api/assessments/questions/{question['question_id']}/self-grade",
        json={"grade": "partial", "confidence_after": 0.4},
    )
    assert grade.status_code == 200
    assert grade.json()["score"] == 0.5

    completed = client.post(f"/api/assessments/{session['assessment_id']}/complete")
    assert completed.status_code == 200
    retro = client.get(f"/api/assessments/{session['assessment_id']}/retro")
    assert retro.status_code == 200
    retro_payload = retro.json()
    body = json.dumps(retro_payload, ensure_ascii=False)
    assert "correct_rules_to_review" in retro_payload
    assert "wrong_choice_or_output" not in body
    assert "wrong_formula" not in body
    assert "wrong_reasoning" not in body
    assert wrong_phrase not in body
    assert retro_payload["transfer_gaps_created"] >= 1

    gaps = client.get("/api/review-lab/mock-retro/transfer-gaps?profile_id=default&status=open")
    assert gaps.status_code == 200
    assert any(gap["source_refs"] and "assessment:" in gap["source_refs"][0] for gap in gaps.json()["gaps"])

    analytics = client.get("/api/learning-analytics/events?profile_id=default&range=30d")
    assert analytics.status_code == 200
    events_body = json.dumps(analytics.json(), ensure_ascii=False)
    assert "assessment" in events_body
    assert wrong_phrase not in events_body


def test_assessment_recommendations_and_mode_specific_generation(client: TestClient) -> None:
    _seed_assessment_cross_system_fixture(client, wrong_phrase="UNIQUE_WRONG_ASSESSMENT_MODE")

    formula = client.post(
        "/api/assessments/generate",
        json={"mode": "formula_drill", "target_minutes": 20, "question_count": 4, "focus": "formula"},
    )
    assert formula.status_code == 200
    assert formula.json()["questions"]
    assert all(question["question_type"] in {"formula_setup", "calculator_steps", "mini_case", "boundary_choice"} for question in formula.json()["questions"])

    lexical = client.post(
        "/api/assessments/generate",
        json={"mode": "lexical_drill", "target_minutes": 20, "question_count": 4, "focus": "lexical"},
    )
    assert lexical.status_code == 200
    assert lexical.json()["questions"]
    assert all(question["question_type"] in {"lexical_production", "cloze", "collocation", "short_answer"} for question in lexical.json()["questions"])

    recs = client.get("/api/assessments/recommendations?profile_id=default")
    assert recs.status_code == 200
    payload = recs.json()
    assert payload["recommended_modes"]
    assert payload["recommended_actions"]


def _seed_assessment_cross_system_fixture(client: TestClient, *, wrong_phrase: str) -> None:
    review_source = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "title": "Assessment Review Source",
            "text": "\n".join(
                [
                    "LOS: CI-ASSESS-REVIEW",
                    "Use after-tax cost of debt in WACC.",
                    "Target capital weights belong in WACC.",
                ]
            ),
        },
    )
    assert review_source.status_code == 200
    review_assets = client.post(f"/api/review-lab/sources/{review_source.json()['source']['source_id']}/extract-assets")
    assert review_assets.status_code == 200
    for asset in review_assets.json()["assets"][:2]:
        assert client.post(f"/api/review-lab/assets/{asset['asset_id']}/confirm").status_code == 200

    formula = client.post(
        "/api/review-lab/formulas/import-text",
        json={
            "title": "Assessment WACC Formula",
            "text": "\n".join(
                [
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use after-tax cost of debt with target market value weights.",
                    "BA II Plus: enter cash flows, set I/Y to WACC, then CPT NPV.",
                ]
            ),
        },
    )
    assert formula.status_code == 200
    formula_asset = next(asset for asset in formula.json()["assets"] if asset["asset_type"] == "formula")
    assert client.post(f"/api/review-lab/formulas/{formula_asset['asset_id']}/confirm").status_code == 200

    dictionary = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "Assessment Spanish Dictionary",
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
    assert client.post(f"/api/language-os/lexical-assets/{dictionary_payload['lexical_assets'][0]['lexical_id']}/confirm").status_code == 200

    retro = client.post(
        "/api/review-lab/mock-retro/import-text",
        json={
            "title": "Assessment Mock Retro",
            "text": "\n".join(
                [
                    "Q1 Corporate Issuers WACC",
                    "LOS: CI-ASSESS-MOCK",
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
    assert client.post("/api/review-lab/syllabus/seed-demo").status_code == 200
    assert client.post("/api/review-lab/syllabus/recompute-coverage").status_code == 200


def _enable_assessment_features(repo_root: Path) -> None:
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
                "adaptive_assessment_enabled: true",
                "interleaving_drill_enabled: true",
                "assessment_feedback_correct_only_enabled: true",
                "assessment_transfer_gap_integration_enabled: true",
                "assessment_analytics_integration_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
