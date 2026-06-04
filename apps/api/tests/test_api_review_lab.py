from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app
from study_science.review_lab import ReviewLabEngine
from study_science.review_lab_models import CorrectKnowledgeAsset


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_review_lab(repo.root)
    _write_daily_review_snapshot(repo.root, review_id="daily-review-test")

    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_review_lab_history_includes_active_paused_and_completed_sessions(client: TestClient) -> None:
    created = client.post(
        "/api/review-lab/sessions",
        json={"review_id": "daily-review-test", "energy_level": 2, "focus_topic": "Corporate Issuers", "max_units": 5},
    )
    assert created.status_code == 200
    session_id = created.json()["session_id"]

    history = client.get("/api/review-lab/history?limit=10")
    assert history.status_code == 200
    assert _history_status(history.json()["sessions"], session_id) == "active"

    paused = client.post(f"/api/review-lab/sessions/{session_id}/pause")
    assert paused.status_code == 200
    assert paused.json()["status"] == "paused"

    history = client.get("/api/review-lab/history?limit=10")
    assert history.status_code == 200
    assert _history_status(history.json()["sessions"], session_id) == "paused"

    resumed = client.post(f"/api/review-lab/sessions/{session_id}/resume")
    assert resumed.status_code == 200
    assert resumed.json()["status"] == "active"
    unit_id = resumed.json()["current_unit"]["unit_id"]

    history = client.get("/api/review-lab/history?limit=10")
    assert history.status_code == 200
    assert _history_status(history.json()["sessions"], session_id) == "active"

    outcome = client.post(
        f"/api/review-lab/sessions/{session_id}/units/{unit_id}/outcome",
        json={
            "confidence_before": 2,
            "time_spent_seconds": 18,
            "needed_hint": False,
            "outcome": "recalled",
            "confidence_after": 3,
            "answer_quality": "perfect",
            "next_action": "advance",
        },
    )
    assert outcome.status_code == 200

    completed = client.post(f"/api/review-lab/sessions/{session_id}/complete")
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"

    history = client.get("/api/review-lab/history?limit=10")
    assert history.status_code == 200
    assert _history_status(history.json()["sessions"], session_id) == "completed"

    report = client.get(f"/api/review-lab/sessions/{session_id}/report")
    assert report.status_code == 200
    assert report.json()["session_id"] == session_id
    assert report.json()["status"] == "completed"


def test_review_lab_today_generates_structured_core_units(client: TestClient) -> None:
    response = client.get("/api/review-lab/today?max_units=6")

    assert response.status_code == 200
    payload = response.json()
    units = payload["units"]
    assert payload["review_id"] == "daily-review-test"
    assert units
    assert all("unit_id" in unit for unit in units)
    assert all("asset_id" in unit for unit in units)
    assert all("front_prompt" in unit for unit in units)
    assert all("correct_answer" in unit for unit in units)
    assert all("memory_state_before" in unit for unit in units)
    core_count = sum(1 for unit in units if unit["asset_type"] == "syllabus_core")
    assert core_count >= len(units) / 2


def test_review_lab_asset_priority_characterization_for_release_freeze(tmp_path: Path) -> None:
    engine = ReviewLabEngine(tmp_path)
    high_value_formula = CorrectKnowledgeAsset(
        asset_id="asset-priority-high",
        asset_type="formula",
        title="High-value WACC formula",
        formula_latex="WACC = w_d r_d (1 - t) + w_e r_e",
        source_refs=["priority#wacc"],
        source_quality=0.95,
        exam_weight=0.9,
        mistake_link_count=3,
        decay_risk=0.85,
        mastery_state="Learning",
        validation_status="confirmed",
    )
    low_value_definition = CorrectKnowledgeAsset(
        asset_id="asset-priority-low",
        asset_type="definition",
        title="Low-risk definition",
        source_refs=["priority#definition"],
        source_quality=0.2,
        exam_weight=0.1,
        mistake_link_count=0,
        decay_risk=0.1,
        mastery_state="Mastered",
        validation_status="confirmed",
    )

    high_score = engine._asset_priority(high_value_formula)
    low_score = engine._asset_priority(low_value_definition)

    assert high_score > low_score
    assert high_score - low_score > 0.5


def test_mistake_derived_unit_does_not_expose_wrong_answer(client: TestClient, tmp_path: Path) -> None:
    wrong_answer_text = "Macaulay duration"
    correct_rule = "Use effective duration when cash flows can change."
    _write_mistake_card(
        tmp_path,
        card_id="card-leak-test",
        wrong_answer=wrong_answer_text,
        correct_resolution=correct_rule,
    )
    _write_daily_review_snapshot(
        tmp_path,
        review_id="daily-review-test",
        mistake_cards=[
            {
                "card_id": "card-leak-test",
                "topic": "Fixed Income",
                "los": "FI.Duration",
                "source_refs": ["leak-test"],
            }
        ],
    )

    response = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-test", "energy_level": 2, "focus_topic": "Fixed Income", "max_units": 8},
    )

    assert response.status_code == 200
    payload = response.json()
    body = json.dumps(payload, ensure_ascii=False)
    assert "wrong_choice_or_output" not in body
    assert "wrong_formula" not in body
    assert "wrong_reasoning" not in body
    assert wrong_answer_text not in body
    assert correct_rule in body
    mistake_units = [unit for unit in payload["units"] if unit["asset_type"] == "mistake_corrected"]
    assert mistake_units
    assert mistake_units[0]["correct_answer"] == correct_rule


def test_required_compat_endpoints_complete_unit_and_update_memory(client: TestClient, tmp_path: Path) -> None:
    created = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-test", "energy_level": 2, "focus_topic": "Corporate Issuers", "max_units": 4},
    )
    assert created.status_code == 200
    session = created.json()
    unit = session["current_unit"]

    assets = client.get("/api/review-lab/assets?review_id=daily-review-test")
    assert assets.status_code == 200
    assert assets.json()["count"] >= 4

    explanation = client.get(f"/api/review-lab/explain/{unit['unit_id']}?review_id=daily-review-test")
    assert explanation.status_code == 200
    assert "priority_formula" in explanation.json()

    completed = client.post(
        f"/api/review-lab/units/{unit['unit_id']}/complete",
        json={
            "session_id": session["session_id"],
            "confidence_before": 2,
            "time_spent_seconds": 25,
            "needed_hint": False,
            "outcome": "recalled",
            "confidence_after": 3,
            "answer_quality": "perfect",
            "next_action": "advance",
        },
    )

    assert completed.status_code == 200
    result = completed.json()
    assert result["unit_id"] == unit["unit_id"]
    assert result["km_decision"]["next_review_at"]
    overlay_path = tmp_path / ".system" / "memory" / "review" / "knowledge-status.json"
    assert unit["asset_id"] in overlay_path.read_text(encoding="utf-8")


def test_draft_pdf_note_assets_do_not_enter_review_until_confirmed(client: TestClient, tmp_path: Path) -> None:
    note_text = "\n".join(
        [
            "Gordon growth model is a dividend discount model for stable perpetual dividend growth.",
            "Intrinsic value = D1 / (r - g).",
            "Use Gordon growth only if dividends grow at a stable rate and required return is greater than growth.",
        ]
    )

    imported = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "profile_id": "default",
            "title": "CFA Notes",
            "text": note_text,
            "source_type": "pdf_note",
        },
    )
    assert imported.status_code == 200
    source = imported.json()["source"]
    assert source["extraction_status"] == "extracted"
    assert source["source_refs"]
    assert imported.json()["segments"]
    assert all(segment["source_ref"] for segment in imported.json()["segments"])

    extracted = client.post(f"/api/review-lab/sources/{source['source_id']}/extract-assets")
    assert extracted.status_code == 200
    candidates = extracted.json()["assets"]
    assert len(candidates) >= 3
    assert all(asset["source_refs"] for asset in candidates)
    assert all(asset["validation_status"] in {"draft", "needs_review"} for asset in candidates)

    draft_list = client.get("/api/review-lab/assets?validation_status=draft")
    assert draft_list.status_code == 200
    assert draft_list.json()["assets"]

    candidate_ids = {asset["asset_id"] for asset in candidates}
    review_before = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-test", "energy_level": 2, "max_units": 10},
    )
    assert review_before.status_code == 200
    assert not any(unit["asset_id"] in candidate_ids for unit in review_before.json()["units"])

    confirmed_id = candidates[0]["asset_id"]
    confirmed = client.post(f"/api/review-lab/assets/{confirmed_id}/confirm")
    assert confirmed.status_code == 200
    assert confirmed.json()["asset"]["validation_status"] == "confirmed"

    rejected_id = candidates[1]["asset_id"]
    rejected = client.post(f"/api/review-lab/assets/{rejected_id}/reject")
    assert rejected.status_code == 200
    assert rejected.json()["asset"]["validation_status"] == "rejected"

    review_after = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-test", "energy_level": 2, "max_units": 10},
    )
    assert review_after.status_code == 200
    unit_ids = {unit["asset_id"] for unit in review_after.json()["units"]}
    assert confirmed_id in unit_ids
    assert rejected_id not in unit_ids

    empty_asset = CorrectKnowledgeAsset(
        asset_id="asset-empty-source-refs",
        asset_type="definition",
        profile_id="default",
        title="No source asset",
        correct_rule="This must not be confirmable.",
        source_refs=[],
        created_from="manual",
        validation_status="draft",
    )
    asset_root = tmp_path / ".system" / "memory" / "review" / "asset-candidates"
    asset_root.mkdir(parents=True, exist_ok=True)
    (asset_root / f"{empty_asset.asset_id}.json").write_text(
        json.dumps(empty_asset.as_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    invalid_confirm = client.post(f"/api/review-lab/assets/{empty_asset.asset_id}/confirm")
    assert invalid_confirm.status_code == 400


def test_formula_candidate_requires_source_refs_and_confirmation(client: TestClient, tmp_path: Path) -> None:
    formula_text = "\n".join(
        [
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "w_d = debt weight; r_d = pre-tax cost of debt; t = tax rate; w_e = equity weight; r_e = cost of equity.",
            "Use when valuing the firm with a target capital structure.",
            "BA II Plus: enter cash flows, press NPV, enter WACC as I/Y, then CPT NPV.",
        ]
    )

    imported = client.post(
        "/api/review-lab/formulas/import-text",
        json={"profile_id": "default", "title": "CFA Formula Notes", "text": formula_text},
    )
    assert imported.status_code == 200
    formulas = [asset for asset in imported.json()["assets"] if asset["asset_type"] == "formula"]
    assert formulas
    assert all(asset["source_refs"] for asset in formulas)
    assert all(asset["validation_status"] in {"draft", "needs_review"} for asset in formulas)
    assert formulas[0]["variables"]
    assert formulas[0]["ba_ii_plus_steps"]

    formula_ids = {asset["asset_id"] for asset in formulas}
    session_before = client.post(
        "/api/review-lab/formulas/generate-session",
        json={"profile_id": "default", "max_units": 8},
    )
    assert session_before.status_code == 200
    assert not any(unit["asset_id"] in formula_ids for unit in session_before.json()["units"])

    enriched = client.post(f"/api/review-lab/formulas/{formulas[0]['asset_id']}/enrich")
    assert enriched.status_code == 200
    assert enriched.json()["asset"]["formula_family"] == "cost_of_capital"

    confirmed = client.post(f"/api/review-lab/formulas/{formulas[0]['asset_id']}/confirm")
    assert confirmed.status_code == 200
    assert confirmed.json()["asset"]["validation_status"] == "confirmed"

    if len(formulas) > 1:
        rejected = client.post(f"/api/review-lab/formulas/{formulas[1]['asset_id']}/reject")
        assert rejected.status_code == 200
        assert rejected.json()["asset"]["validation_status"] == "rejected"

    listed = client.get("/api/review-lab/formulas?validation_status=confirmed")
    assert listed.status_code == 200
    assert any(asset["asset_id"] == formulas[0]["asset_id"] for asset in listed.json()["assets"])

    session_after = client.post(
        "/api/review-lab/formulas/generate-session",
        json={"profile_id": "default", "max_units": 8},
    )
    assert session_after.status_code == 200
    payload = session_after.json()
    formula_unit = next(unit for unit in payload["units"] if unit["asset_id"] == formulas[0]["asset_id"])
    assert formula_unit["display_mode"] in {"recall_formula", "ba_ii_plus_procedure"}
    assert formula_unit["formula_latex"]
    assert formula_unit["variables"]
    assert formula_unit["ba_ii_plus_steps"]
    assert formula_unit["source_refs"]

    explanation = client.get(
        f"/api/review-lab/formulas/explain/{formula_unit['unit_id']}?session_id={payload['session_id']}"
    )
    assert explanation.status_code == 200
    assert "priority_formula" in explanation.json()

    completed = client.post(
        f"/api/review-lab/formulas/units/{formula_unit['unit_id']}/complete",
        json={
            "session_id": payload["session_id"],
            "confidence_before": 2,
            "time_spent_seconds": 30,
            "needed_hint": False,
            "outcome": "partial",
            "confidence_after": 2,
            "answer_quality": "minor_gap",
            "next_action": "drill",
        },
    )
    assert completed.status_code == 200
    update = completed.json()["formula_update"]
    assert update["next_review_at"]
    assert "calculator_procedure_gap" in update["weakness_tags"]
    formula_status = tmp_path / ".system" / "memory" / "review" / "formula-status.json"
    assert formulas[0]["asset_id"] in formula_status.read_text(encoding="utf-8")


def test_syllabus_seed_import_and_coverage_statuses(client: TestClient, tmp_path: Path) -> None:
    seeded = client.post("/api/review-lab/syllabus/seed-demo")
    assert seeded.status_code == 200
    assert any(topic["topic_id"] == "demo-ci-wacc" for topic in seeded.json()["topics"])

    imported_text = client.post(
        "/api/review-lab/syllabus/import-text",
        json={
            "profile_id": "default",
            "text": "CI-TEXT-001 | Corporate Issuers | Coverage Text | Calculate text-import WACC | formula | 0.7",
        },
    )
    assert imported_text.status_code == 200
    assert imported_text.json()["topics"][0]["los"] == "CI-TEXT-001"

    topic_id = "topic-coverage-wacc"
    imported = client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "profile_id": "default",
            "topics": [
                {
                    "topic_id": topic_id,
                    "subject": "Corporate Issuers",
                    "module": "Coverage Cost of Capital",
                    "los": "CI-COV-001",
                    "title": "Calculate and interpret WACC coverage",
                    "exam_weight": 0.8,
                    "expected_asset_types": ["formula"],
                    "formula_expected": True,
                }
            ],
        },
    )
    assert imported.status_code == 200

    missing = _coverage_record(client, topic_id)
    assert missing["coverage_status"] == "missing"
    assert "import notes for this topic" in missing["recommended_actions"]

    draft = CorrectKnowledgeAsset(
        asset_id="asset-coverage-wacc",
        asset_type="formula",
        profile_id="default",
        subject="Corporate Issuers",
        module="Coverage Cost of Capital",
        los="CI-COV-001",
        title="WACC coverage formula",
        correct_rule="WACC = wd rd (1 - t) + we re.",
        formula_latex="WACC = wd rd (1 - t) + we re",
        source_refs=["coverage-note#seg-1"],
        source_quality=0.8,
        mastery_state="Mastered",
        created_from="text_note",
        validation_status="draft",
    )
    _write_asset(tmp_path, draft)

    draft_only = _coverage_record(client, topic_id)
    assert draft_only["coverage_status"] == "draft_only"
    assert draft_only["confirmed_asset_count"] == 0
    assert draft_only["draft_asset_count"] == 1
    assert "confirm draft assets" in draft_only["recommended_actions"]

    confirmed = client.post(f"/api/review-lab/assets/{draft.asset_id}/confirm")
    assert confirmed.status_code == 200
    covered = _coverage_record(client, topic_id)
    assert covered["coverage_status"] == "covered"
    assert covered["confirmed_asset_count"] == 1
    assert covered["formula_asset_count"] == 1
    assert covered["links"][0]["created_by"] == "exact_los"
    assert covered["coverage_score"] > 0.65


def test_syllabus_coverage_partial_weak_stale_and_keyword_mapping(client: TestClient, tmp_path: Path) -> None:
    topic_payload = [
        {
            "topic_id": "topic-partial-boundary",
            "subject": "Equity",
            "module": "Coverage Equity",
            "title": "Apply valuation boundary rules",
            "expected_asset_types": ["definition", "formula", "decision_rule"],
            "formula_expected": True,
            "decision_rule_expected": True,
            "exam_weight": 0.75,
        },
        {
            "topic_id": "topic-weak-wacc",
            "subject": "Corporate Issuers",
            "module": "Keyword Match Module",
            "title": "Calculate WACC from component costs",
            "expected_asset_types": ["formula"],
            "formula_expected": True,
            "exam_weight": 0.95,
        },
        {
            "topic_id": "topic-stale-duration",
            "subject": "Fixed Income",
            "module": "Duration Coverage",
            "title": "Calculate effective duration",
            "expected_asset_types": ["formula"],
            "formula_expected": True,
            "exam_weight": 0.85,
        },
    ]
    imported = client.post("/api/review-lab/syllabus/import-json", json={"topics": topic_payload})
    assert imported.status_code == 200

    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-partial-definition",
            asset_type="definition",
            profile_id="default",
            subject="Equity",
            module="Coverage Equity",
            title="Valuation boundary definition",
            correct_rule="A valuation model boundary states when a model is appropriate.",
            source_refs=["coverage-equity#seg-1"],
            mastery_state="Mastered",
            created_from="text_note",
            validation_status="confirmed",
        ),
    )
    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-weak-keyword-wacc",
            asset_type="formula",
            profile_id="default",
            subject="Imported note",
            module="Imported note",
            title="Weighted average cost of capital WACC formula",
            correct_rule="WACC = wd rd (1 - t) + we re.",
            formula_latex="WACC = wd rd (1 - t) + we re",
            source_refs=["coverage-wacc#seg-1"],
            formula_family="cost_of_capital",
            mistake_link_count=2,
            mastery_state="Learning",
            created_from="text_note",
            validation_status="confirmed",
        ),
    )
    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-stale-duration",
            asset_type="formula",
            profile_id="default",
            subject="Fixed Income",
            module="Duration Coverage",
            title="Effective duration formula",
            correct_rule="Effective duration uses price changes for an interest-rate shock.",
            formula_latex="Effective duration = (PV- - PV+) / (2 x Delta curve x PV0)",
            source_refs=["coverage-duration#seg-1"],
            mastery_state="Mastered",
            next_review_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            created_from="text_note",
            validation_status="confirmed",
        ),
    )

    partial = _coverage_record(client, "topic-partial-boundary")
    assert partial["coverage_status"] == "partial"
    assert "create formula asset" in partial["recommended_actions"]
    assert "create decision boundary asset" in partial["recommended_actions"]

    weak = _coverage_record(client, "topic-weak-wacc")
    assert weak["coverage_status"] == "weak"
    assert weak["links"][0]["created_by"] == "keyword_match"
    assert "review weak confirmed assets" in weak["recommended_actions"]
    assert "run Formula Lab" in weak["recommended_actions"]

    stale = _coverage_record(client, "topic-stale-duration")
    assert stale["coverage_status"] == "stale"
    assert stale["decision_rule_asset_count"] == 0
    assert "review stale covered assets" in stale["recommended_actions"]


def test_coverage_guided_review_selection_prioritizes_weak_confirmed_assets(client: TestClient, tmp_path: Path) -> None:
    topic_id = "topic-guided-selection"
    imported = client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "topics": [
                {
                    "topic_id": topic_id,
                    "subject": "Corporate Issuers",
                    "module": "Guided Selection",
                    "los": "CI-GUIDE-001",
                    "title": "Recall weak WACC selection",
                    "expected_asset_types": ["formula"],
                    "formula_expected": True,
                    "exam_weight": 1.0,
                }
            ]
        },
    )
    assert imported.status_code == 200

    weak_asset = CorrectKnowledgeAsset(
        asset_id="asset-guided-weak",
        asset_type="formula",
        profile_id="default",
        subject="Corporate Issuers",
        module="Guided Selection",
        los="CI-GUIDE-001",
        title="Weak WACC formula",
        correct_rule="WACC = wd rd (1 - t) + we re.",
        formula_latex="WACC = wd rd (1 - t) + we re",
        source_refs=["guided-note#seg-1"],
        source_quality=0.9,
        exam_weight=1.0,
        decay_risk=0.95,
        mistake_link_count=3,
        mastery_state="Learning",
        created_from="text_note",
        validation_status="confirmed",
    )
    _write_asset(tmp_path, weak_asset)

    coverage = client.post("/api/review-lab/syllabus/recompute-coverage")
    assert coverage.status_code == 200
    assert _coverage_record(client, topic_id)["coverage_status"] in {"weak", "stale"}

    session = client.post(
        "/api/review-lab/generate",
        json={"review_id": "daily-review-test", "energy_level": 2, "focus_topic": "Guided Selection", "max_units": 1},
    )
    assert session.status_code == 200
    assert session.json()["units"][0]["asset_id"] == weak_asset.asset_id


def test_mock_retro_transfer_gap_generates_correct_only_review_unit(client: TestClient, tmp_path: Path) -> None:
    topic_id = "topic-mock-wacc"
    imported_topic = client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "topics": [
                {
                    "topic_id": topic_id,
                    "subject": "Corporate Issuers",
                    "module": "Mock WACC",
                    "los": "CI-MOCK-001",
                    "title": "Calculate and interpret WACC after-tax debt cost",
                    "expected_asset_types": ["formula"],
                    "formula_expected": True,
                    "exam_weight": 0.95,
                }
            ]
        },
    )
    assert imported_topic.status_code == 200
    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-mock-wacc",
            asset_type="formula",
            profile_id="default",
            subject="Corporate Issuers",
            module="Mock WACC",
            los="CI-MOCK-001",
            title="WACC after-tax debt formula",
            correct_rule="WACC uses after-tax cost of debt: w_d * r_d * (1 - t) + w_e * r_e.",
            formula_latex="WACC = w_d r_d (1 - t) + w_e r_e",
            source_refs=["mock-wacc-note#seg-1"],
            formula_family="cost_of_capital",
            mastery_state="Mastered",
            created_from="text_note",
            validation_status="confirmed",
        ),
    )

    wrong_text = "used pretax cost of debt"
    mock_text = f"""
    Q1 Corporate Issuers WACC
    LOS: CI-MOCK-001
    Result: incorrect
    Confidence: high
    Time: 240s
    Wrong Output: {wrong_text}
    Correct Rule: WACC uses after-tax cost of debt: w_d * r_d * (1 - t) + w_e * r_e.
    Tested Formula: WACC
    BA II Plus: store weights and component costs, calculate weighted sum.
    """
    imported = client.post(
        "/api/review-lab/mock-retro/import-text",
        json={"profile_id": "default", "title": "Mock Retro 1", "text": mock_text},
    )
    assert imported.status_code == 200
    imported_payload = imported.json()
    mock_id = imported_payload["session"]["mock_id"]
    assert imported_payload["evidence_count"] == 1
    assert wrong_text not in json.dumps(imported_payload, ensure_ascii=False)

    analyzed = client.post(f"/api/review-lab/mock-retro/sessions/{mock_id}/analyze")
    assert analyzed.status_code == 200
    gap_types = {gap["gap_type"] for gap in analyzed.json()["gaps"]}
    assert "confidence_mismatch" in gap_types
    assert {"formula_recall_gap", "variable_confusion"}.intersection(gap_types)
    assert "calculator_procedure_gap" in gap_types

    review = client.post("/api/review-lab/mock-retro/generate-review", json={"profile_id": "default", "max_units": 5})
    assert review.status_code == 200
    payload = json.dumps(review.json(), ensure_ascii=False)
    assert "wrong_choice_or_output" not in payload
    assert "wrong_formula" not in payload
    assert "wrong_reasoning" not in payload
    assert wrong_text not in payload
    assert "after-tax cost of debt" in payload
    assert "Recent mock transfer gap:" in payload


def test_transfer_gaps_mark_coverage_weak_and_resolve_removes_signal(client: TestClient, tmp_path: Path) -> None:
    topic_id = "topic-mock-coverage-weak"
    client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "topics": [
                {
                    "topic_id": topic_id,
                    "subject": "Fixed Income",
                    "module": "Mock Duration",
                    "los": "FI-MOCK-001",
                    "title": "Choose the effective duration boundary",
                    "expected_asset_types": ["formula"],
                    "formula_expected": True,
                    "exam_weight": 0.85,
                }
            ]
        },
    )
    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-mock-duration",
            asset_type="formula",
            profile_id="default",
            subject="Fixed Income",
            module="Mock Duration",
            los="FI-MOCK-001",
            title="Effective duration",
            correct_rule="Use effective duration when cash flows can change.",
            formula_latex="Effective duration = (PV- - PV+) / (2 x Delta curve x PV0)",
            source_refs=["mock-duration-note#seg-1"],
            formula_family="fixed_income",
            mastery_state="Mastered",
            created_from="text_note",
            validation_status="confirmed",
        ),
    )
    mock_text = """
    Q1 Fixed Income Duration
    LOS: FI-MOCK-001
    Result: incorrect
    Confidence: high
    Boundary Rule: Use effective duration when cash flows can change.
    Wrong Reasoning: selected Macaulay duration for a callable bond
    Correct Rule: Use effective duration when cash flows can change.
    Tested Formula: Effective duration
    """
    imported = client.post("/api/review-lab/mock-retro/import-text", json={"title": "Mock Duration Retro", "text": mock_text})
    mock_id = imported.json()["session"]["mock_id"]
    analyzed = client.post(f"/api/review-lab/mock-retro/sessions/{mock_id}/analyze")
    assert analyzed.status_code == 200

    weak = _coverage_record(client, topic_id)
    assert weak["coverage_status"] == "weak"
    assert weak["transfer_gaps"]
    assert "review transfer gap" in weak["recommended_actions"]
    assert "create decision boundary asset" in weak["recommended_actions"]

    for gap in analyzed.json()["gaps"]:
        resolved = client.post(f"/api/review-lab/mock-retro/transfer-gaps/{gap['gap_id']}/resolve")
        assert resolved.status_code == 200
        assert resolved.json()["gap"]["status"] == "resolved"

    recomputed = _coverage_record(client, topic_id)
    assert recomputed["coverage_status"] in {"covered", "partial", "stale"}
    assert recomputed["transfer_gaps"] == []


def test_low_quality_resource_assets_do_not_enter_review_until_resource_confirmed(client: TestClient) -> None:
    resource_text = "\n".join(
        [
            "LOS: CI-RES-001",
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "Use target capital structure and after-tax cost of debt.",
            "Source: local CFA study note.",
        ]
    )
    imported = client.post(
        "/api/review-lab/resources/import-text",
        json={
            "profile_id": "default",
            "title": "Unverified WACC Resource",
            "text": resource_text,
            "resource_type": "text_note",
        },
    )
    assert imported.status_code == 200
    resource = imported.json()["resource"]
    resource_id = resource["resource_id"]
    assert resource["validation_status"] == "draft"
    assert imported.json()["evidence"]

    scored = client.post(f"/api/review-lab/resources/{resource_id}/score")
    assert scored.status_code == 200
    assert scored.json()["resource"]["quality_score"] > 0
    assert scored.json()["quality_gate"]["passes"] is False

    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    assert extracted.status_code == 200
    candidates = extracted.json()["candidate_assets"]
    assert candidates
    assert all(asset["source_refs"] for asset in candidates)
    assert all(asset["resource_id"] == resource_id for asset in candidates)
    assert all(asset["resource_quality_status"] in {"low", "medium", "high", "trusted"} for asset in candidates)
    evidence = client.get(f"/api/review-lab/resources/{resource_id}/evidence")
    assert evidence.status_code == 200
    assert all(segment["source_ref"] for segment in evidence.json()["evidence"])

    candidate_ids = {asset["asset_id"] for asset in candidates}
    review_before = client.post("/api/review-lab/generate", json={"review_id": "daily-review-test", "max_units": 12})
    assert review_before.status_code == 200
    assert not any(unit["asset_id"] in candidate_ids for unit in review_before.json()["units"])

    blocked_promotion = client.post(
        f"/api/review-lab/resources/{resource_id}/promote-assets",
        json={"asset_ids": [candidates[0]["asset_id"]]},
    )
    assert blocked_promotion.status_code == 200
    assert blocked_promotion.json()["promoted_count"] == 0
    assert blocked_promotion.json()["quality_gate"]["reason"] == "resource_not_confirmed"

    confirmed_resource = client.post(f"/api/review-lab/resources/{resource_id}/confirm")
    assert confirmed_resource.status_code == 200
    assert confirmed_resource.json()["resource"]["validation_status"] == "confirmed"
    assert confirmed_resource.json()["resource"]["quality_status"] in {"medium", "high", "trusted"}

    promoted = client.post(
        f"/api/review-lab/resources/{resource_id}/promote-assets",
        json={"asset_ids": [candidates[0]["asset_id"]]},
    )
    assert promoted.status_code == 200
    assert promoted.json()["promoted_count"] == 1
    promoted_asset = promoted.json()["assets"][0]
    assert promoted_asset["validation_status"] == "confirmed"
    assert "manual" in promoted_asset["resource_match_reasons"]

    confirm_asset = client.post(f"/api/review-lab/assets/{promoted_asset['asset_id']}/confirm")
    assert confirm_asset.status_code == 200

    review_after = client.post("/api/review-lab/generate", json={"review_id": "daily-review-test", "max_units": 12})
    assert review_after.status_code == 200
    resource_units = [unit for unit in review_after.json()["units"] if unit["asset_id"] == promoted_asset["asset_id"]]
    assert resource_units
    assert "resource" in resource_units[0]["due_reason"].lower()


def test_resource_promotion_links_coverage_and_quality_report(client: TestClient) -> None:
    topic_id = "topic-resource-wacc"
    imported_topic = client.post(
        "/api/review-lab/syllabus/import-json",
        json={
            "topics": [
                {
                    "topic_id": topic_id,
                    "subject": "Corporate Issuers",
                    "module": "ResourceOS WACC",
                    "los": "CI-RES-001",
                    "title": "Calculate WACC with after-tax debt cost",
                    "expected_asset_types": ["formula"],
                    "formula_expected": True,
                    "exam_weight": 0.92,
                }
            ]
        },
    )
    assert imported_topic.status_code == 200

    resource_text = "\n".join(
        [
            "# ResourceOS WACC",
            "LOS: CI-RES-001",
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "Use when valuing the firm with a target capital structure.",
            "Source: curriculum reading note.",
        ]
    )
    imported = client.post(
        "/api/review-lab/resources/import-text",
        json={"title": "ResourceOS WACC Note", "text": resource_text, "resource_type": "lecture_slide"},
    )
    resource_id = imported.json()["resource"]["resource_id"]
    client.post(f"/api/review-lab/resources/{resource_id}/confirm")
    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    asset = extracted.json()["candidate_assets"][0]
    assert {"exact_los", "manual", "source_ref_shared"}.intersection(asset["resource_match_reasons"])

    promoted = client.post(
        f"/api/review-lab/resources/{resource_id}/promote-assets",
        json={"asset_ids": [asset["asset_id"]]},
    )
    assert promoted.status_code == 200
    assert promoted.json()["assets"][0]["source_quality"] >= 0.5

    coverage = _coverage_record(client, topic_id)
    assert coverage["confirmed_asset_count"] >= 1
    assert coverage["coverage_status"] in {"covered", "weak", "stale"}
    assert any(link["asset_id"] == asset["asset_id"] for link in coverage["links"])

    report = client.get("/api/review-lab/resources/quality-report")
    assert report.status_code == 200
    assert report.json()["resource_count"] >= 1
    assert report.json()["promoted_asset_count"] >= 1


def test_resource_duplicate_hash_and_formula_conflict_are_flagged(client: TestClient, tmp_path: Path) -> None:
    _write_asset(
        tmp_path,
        CorrectKnowledgeAsset(
            asset_id="asset-existing-wacc-conflict",
            asset_type="formula",
            profile_id="default",
            subject="Corporate Issuers",
            module="Conflict WACC",
            title="WACC conflicting formula",
            correct_rule="WACC = wd rd (1 - t) + we re.",
            formula_latex="WACC = wd rd (1 - t) + we re",
            source_refs=["existing-wacc#seg-1"],
            formula_family="cost_of_capital",
            created_from="text_note",
            validation_status="confirmed",
        ),
    )
    text = "\n".join(
        [
            "WACC = w_d r_d + w_e r_e.",
            "Use target capital structure.",
            "Source: learner note.",
        ]
    )
    first = client.post("/api/review-lab/resources/import-text", json={"title": "Conflict WACC Note", "text": text})
    assert first.status_code == 200
    resource_id = first.json()["resource"]["resource_id"]
    client.post(f"/api/review-lab/resources/{resource_id}/score")
    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    assert extracted.status_code == 200
    conflicts = " ".join(extracted.json()["conflicts"])
    assert "conflicting_formula_candidate" in conflicts
    assert any(asset["validation_status"] == "needs_review" for asset in extracted.json()["candidate_assets"])

    duplicate = client.post("/api/review-lab/resources/import-text", json={"title": "Same Hash Different Title", "text": text})
    assert duplicate.status_code == 200
    assert duplicate.json()["duplicate"] is True
    assert duplicate.json()["resource"]["duplicate_of"] == resource_id


def test_rejected_resource_excludes_candidate_assets(client: TestClient) -> None:
    text = "\n".join(
        [
            "Effective duration = (PV- - PV+) / (2 x Delta curve x PV0).",
            "Use effective duration when cash flows can change.",
            "Source: local notes.",
        ]
    )
    imported = client.post("/api/review-lab/resources/import-text", json={"title": "Rejectable Duration Note", "text": text})
    resource_id = imported.json()["resource"]["resource_id"]
    client.post(f"/api/review-lab/resources/{resource_id}/confirm")
    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    asset_id = extracted.json()["candidate_assets"][0]["asset_id"]
    client.post(f"/api/review-lab/resources/{resource_id}/promote-assets", json={"asset_ids": [asset_id]})

    rejected = client.post(f"/api/review-lab/resources/{resource_id}/reject")
    assert rejected.status_code == 200
    assert rejected.json()["resource"]["quality_status"] == "rejected"
    assert all(asset["validation_status"] == "rejected" for asset in rejected.json()["rejected_assets"])

    review = client.post("/api/review-lab/generate", json={"review_id": "daily-review-test", "max_units": 12})
    assert review.status_code == 200
    assert not any(unit["asset_id"] == asset_id for unit in review.json()["units"])


def test_mission_control_works_on_fresh_state_and_registry(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_review_lab(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        with TestClient(app) as fresh_client:
            response = fresh_client.get("/api/review-lab/mission-control")
            assert response.status_code == 200
            payload = response.json()
            assert payload["profile_id"] == "default"
            for key in ("review_lab", "assets", "formulas", "coverage", "mock_retro", "resources", "language", "data_governance", "system_health"):
                assert key in payload
            assert payload["data_governance"]["backup_health"]
            assert payload["recommended_actions"]

            registry = fresh_client.get("/api/review-lab/route-registry")
            assert registry.status_code == 200
            registry_payload = registry.json()
            assert registry_payload["feature_groups"]["mission_control"]["exists"]
            assert registry_payload["feature_groups"]["language_os"]["exists"]
            assert registry_payload["feature_groups"]["ux_accessibility"]["exists"]
            assert registry_payload["feature_groups"]["ux_accessibility"]["enabled"]
            assert registry_payload["feature_groups"]["data_governance"]["exists"]
            assert registry_payload["feature_groups"]["data_governance"]["enabled"]
            pages = {item["path"]: item["implemented"] for item in registry_payload["expected_pages"]}
            for page in (
                "/review/lab",
                "/review/formulas",
                "/language/review",
                "/review/assessments",
                "/review/search",
                "/review/knowledge-map",
                "/review/data",
            ):
                assert pages[page]
            mounted = {item["path"]: item["mounted"] for item in registry_payload["expected_api_routes"]}
            assert mounted["/api/review-lab/mission-control"]
            assert mounted["/api/review-lab/route-registry"]
            assert mounted["/api/data-governance/inventory"]
            assert mounted["/api/data-governance/export"]
    finally:
        app.dependency_overrides.clear()


def test_mission_control_summary_is_correct_only_and_cross_system(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_PHRASE_TASK008"
    seed = client.post("/api/review-lab/syllabus/seed-demo")
    assert seed.status_code == 200

    resource_text = "\n".join(
        [
            "LOS: CI-PLAY-MISSION",
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "Use after-tax cost of debt when valuing a firm with target capital structure.",
            "Source: local mission-control note.",
        ]
    )
    imported_resource = client.post(
        "/api/review-lab/resources/import-text",
        json={"title": "Mission Control WACC Resource", "text": resource_text, "resource_type": "text_note"},
    )
    assert imported_resource.status_code == 200
    resource_id = imported_resource.json()["resource"]["resource_id"]
    assert client.post(f"/api/review-lab/resources/{resource_id}/score").status_code == 200
    extracted = client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence")
    assert extracted.status_code == 200
    assert client.post(f"/api/review-lab/resources/{resource_id}/confirm").status_code == 200
    promoted = client.post(f"/api/review-lab/resources/{resource_id}/promote-assets", json={"asset_ids": []})
    assert promoted.status_code == 200

    assert client.post("/api/review-lab/syllabus/recompute-coverage").status_code == 200

    mock_text = "\n".join(
        [
            "Q1 Corporate Issuers WACC",
            "LOS: CI-PLAY-MISSION",
            "Result: incorrect",
            "Confidence: high",
            f"Wrong Output: {wrong_phrase}",
            "Correct Rule: WACC uses after-tax cost of debt.",
            "Tested Formula: WACC",
        ]
    )
    imported_mock = client.post("/api/review-lab/mock-retro/import-text", json={"title": "Mission Control Mock Retro", "text": mock_text})
    assert imported_mock.status_code == 200
    mock_id = imported_mock.json()["session"]["mock_id"]
    analyzed = client.post(f"/api/review-lab/mock-retro/sessions/{mock_id}/analyze")
    assert analyzed.status_code == 200

    review = client.post("/api/review-lab/generate", json={"review_id": "daily-review-test", "max_units": 10})
    assert review.status_code == 200

    imported_dictionary = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "Mission Spanish Dictionary",
            "dictionary_type": "spanish_english",
            "entries": [
                {
                    "headword": "aprovechar",
                    "language": "es",
                    "target_language": "en",
                    "part_of_speech": "verb",
                    "definition": "to take advantage of; to make use of",
                    "translation": "take advantage of, make use of",
                    "example_sentence": "Debemos aprovechar esta oportunidad.",
                    "collocations": ["aprovechar una oportunidad"],
                }
            ],
        },
    )
    assert imported_dictionary.status_code == 201
    dictionary = imported_dictionary.json()["dictionary"]
    lexical_asset = imported_dictionary.json()["lexical_assets"][0]
    assert client.post(f"/api/language-os/dictionaries/{dictionary['dictionary_id']}/confirm").status_code == 200
    assert client.post(f"/api/language-os/lexical-assets/{lexical_asset['lexical_id']}/confirm").status_code == 200
    lexical_review = client.post("/api/language-os/review/generate-session", json={"max_units": 5})
    assert lexical_review.status_code == 200
    assert lexical_review.json()["units"]

    summary = client.get("/api/review-lab/mission-control")
    assert summary.status_code == 200
    payload = summary.json()
    assert payload["review_lab"]["due_count"] >= 1
    assert payload["resources"]["resource_count"] >= 1
    assert payload["mock_retro"]["open_transfer_gap_count"] >= 1
    assert payload["language"]["confirmed_lexical_count"] >= 1
    action_ids = {action["action_id"] for action in payload["recommended_actions"]}
    assert {"review_today", "resolve_transfer_gaps", "lexical_review"}.intersection(action_ids)

    body = json.dumps(payload, ensure_ascii=False)
    assert "wrong_choice_or_output" not in body
    assert "wrong_formula" not in body
    assert "wrong_reasoning" not in body
    assert wrong_phrase not in body


def test_source_file_import_extracts_segments_candidates_and_duplicates(client: TestClient) -> None:
    text = "\n".join(
        [
            "# File WACC Note",
            "LOS: CI-FILE-001",
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "Use WACC when valuing a firm with a target capital structure.",
            "Source: local uploaded note.",
        ]
    )
    uploaded = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Uploaded WACC Note", "source_type": "text_note"},
        files={"file": ("wacc-note.txt", text.encode("utf-8"), "text/plain")},
    )
    assert uploaded.status_code == 200
    payload = uploaded.json()
    file_payload = payload["file"]
    assert payload["duplicate"] is False
    assert file_payload["extraction_status"] == "extracted"
    assert file_payload["storage_path"]
    assert not Path(file_payload["storage_path"]).is_absolute()
    assert payload["segments"]
    assert payload["segments"][0]["source_ref"].startswith(f"file:{file_payload['file_id']}:page:1:seg:")
    assert payload["assets"]
    assert all(asset["validation_status"] in {"draft", "needs_review"} for asset in payload["assets"])
    assert all(any(ref.startswith("file:") for ref in asset["source_refs"]) for asset in payload["assets"])

    file_id = file_payload["file_id"]
    listed = client.get("/api/review-lab/files")
    assert listed.status_code == 200
    assert any(item["file_id"] == file_id for item in listed.json()["files"])

    segments = client.get(f"/api/review-lab/files/{file_id}/segments")
    assert segments.status_code == 200
    assert segments.json()["count"] == len(payload["segments"])

    candidates = client.get(f"/api/review-lab/files/{file_id}/candidate-assets")
    assert candidates.status_code == 200
    assert candidates.json()["count"] == len(payload["assets"])

    duplicate = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Uploaded WACC Note", "source_type": "text_note"},
        files={"file": ("wacc-note.txt", text.encode("utf-8"), "text/plain")},
    )
    assert duplicate.status_code == 200
    duplicate_payload = duplicate.json()
    assert duplicate_payload["duplicate"] is True
    assert duplicate_payload["file"]["extraction_status"] == "duplicate"
    assert duplicate_payload["file"]["duplicate_of"] == file_id
    assert duplicate_payload["count"] == len(payload["assets"])


def test_markdown_and_pdf_file_import_preserve_page_and_heading_metadata(client: TestClient) -> None:
    md_text = "\n\n".join(
        [
            "# Duration Heading",
            "Effective duration = (PV- - PV+) / (2 x Delta curve x PV0).",
            "Use effective duration when cash flows can change.",
        ]
    )
    markdown = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Markdown Duration"},
        files={"file": ("duration.md", md_text.encode("utf-8"), "text/markdown")},
    )
    assert markdown.status_code == 200
    md_segments = markdown.json()["segments"]
    assert md_segments
    assert md_segments[0]["heading"] == "Duration Heading"
    assert md_segments[0]["page"] == 1

    pdf_bytes = _make_pdf_bytes(
        [
            "PDF Duration Note",
            "Effective duration = (PV- - PV+) / (2 x Delta curve x PV0).",
            "Use effective duration for option-sensitive bonds.",
        ]
    )
    pdf = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "PDF Duration"},
        files={"file": ("duration.pdf", pdf_bytes, "application/pdf")},
    )
    assert pdf.status_code == 200
    pdf_payload = pdf.json()
    assert pdf_payload["file"]["extraction_status"] == "extracted"
    assert pdf_payload["file"]["page_count"] == 1
    assert any(segment["page"] == 1 for segment in pdf_payload["segments"])
    assert any(ref.startswith(f"file:{pdf_payload['file']['file_id']}:page:1:seg:") for ref in pdf_payload["source"]["source_refs"])

    blank_pdf = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Blank PDF"},
        files={"file": ("blank.pdf", _make_pdf_bytes([]), "application/pdf")},
    )
    assert blank_pdf.status_code == 200
    assert blank_pdf.json()["file"]["extraction_status"] == "extracted_no_text"
    assert "OCR is disabled" in " ".join(blank_pdf.json()["warnings"])


def test_resource_file_import_scores_extracts_and_keeps_assets_draft(client: TestClient) -> None:
    text = "\n".join(
        [
            "# Resource File WACC",
            "LOS: CI-FILE-RES",
            "WACC = w_d r_d (1 - t) + w_e r_e.",
            "Use when valuing a firm with target capital structure.",
            "Source: local uploaded lecture note.",
        ]
    )
    uploaded = client.post(
        "/api/review-lab/resources/import-file",
        data={"title": "Uploaded Resource WACC", "resource_type": "lecture_slide"},
        files={"file": ("resource-wacc.txt", text.encode("utf-8"), "text/plain")},
    )
    assert uploaded.status_code == 200
    payload = uploaded.json()
    assert payload["file"]["extraction_status"] == "extracted"
    assert payload["resource"]["origin"] == "file"
    assert payload["resource"]["validation_status"] == "draft"
    assert payload["resource"]["quality_status"] in {"low", "medium", "high", "trusted"}
    assert payload["evidence_count"] >= 1
    assert payload["candidate_count"] >= 1
    assert all(any(ref.startswith("file:") for ref in asset["source_refs"]) for asset in payload["candidate_assets"])


def test_unsupported_file_import_returns_safe_status(client: TestClient) -> None:
    uploaded = client.post(
        "/api/review-lab/sources/import-file",
        data={"title": "Unsupported"},
        files={"file": ("macro.exe", b"not executable here", "application/octet-stream")},
    )
    assert uploaded.status_code == 200
    payload = uploaded.json()
    assert payload["file"]["extraction_status"] == "unsupported"
    assert payload["assets"] == []
    assert payload["warnings"]


def _history_status(sessions: list[dict], session_id: str) -> str:
    match = next((session for session in sessions if session["session_id"] == session_id), None)
    assert match is not None
    return match["status"]


def _enable_review_lab(repo_root: Path) -> None:
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
                "mission_control_enabled: true",
                "integration_health_checks_enabled: true",
                "green_test_gate_enabled: true",
                "file_ingestion_enabled: true",
                "pdf_text_extraction_enabled: true",
                "dictionary_file_import_enabled: true",
                "resource_file_import_enabled: true",
                "file_duplicate_detection_enabled: true",
                "ocr_extraction_enabled: false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_daily_review_snapshot(
    repo_root: Path,
    review_id: str,
    mistake_cards: list[dict] | None = None,
) -> None:
    snapshot_root = repo_root / ".system" / "memory" / "review" / "daily"
    snapshot_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "review_id": review_id,
        "knowledge_points": [
            {
                "knowledge_id": "kp-1",
                "subject": "Corporate Issuers",
                "heading": "Capital Structure",
                "trigger": "Recall the trade-off theory intuition.",
                "decision": "Tax shields are balanced against expected distress costs.",
                "priority": 90,
                "reason": "Due today",
                "state": "Learning",
                "source_refs": ["curriculum/corporate-issuers"],
            },
            {
                "knowledge_id": "kp-2",
                "subject": "Corporate Issuers",
                "heading": "Working Capital",
                "trigger": "Recall cash conversion cycle components.",
                "decision": "Cash conversion cycle is days inventory plus days receivables minus days payables.",
                "priority": 85,
                "reason": "Core syllabus coverage",
                "state": "New",
                "source_refs": ["curriculum/corporate-issuers"],
            },
            {
                "knowledge_id": "kp-3",
                "subject": "Equity",
                "heading": "Dividend Discount Model",
                "trigger": "Recall when the Gordon growth model applies.",
                "decision": "Use Gordon growth only for stable perpetual dividend growth where required return exceeds growth.",
                "priority": 80,
                "reason": "Core syllabus coverage",
                "state": "New",
                "source_refs": ["curriculum/equity"],
            },
            {
                "knowledge_id": "kp-4",
                "subject": "Economics",
                "heading": "Business Cycles",
                "trigger": "Recall leading versus lagging indicators.",
                "decision": "Leading indicators move before the cycle; lagging indicators confirm after the turn.",
                "priority": 75,
                "reason": "Core syllabus coverage",
                "state": "New",
                "source_refs": ["curriculum/economics"],
            },
        ],
        "mistake_cards": mistake_cards or [],
    }
    snapshot_text = json.dumps(payload, ensure_ascii=False, indent=2)
    (snapshot_root / f"{review_id}.json").write_text(snapshot_text, encoding="utf-8")
    (snapshot_root / "latest.json").write_text(snapshot_text, encoding="utf-8")


def _write_mistake_card(repo_root: Path, card_id: str, wrong_answer: str, correct_resolution: str) -> None:
    card_root = repo_root / ".system" / "memory" / "question-errors"
    card_root.mkdir(parents=True, exist_ok=True)
    (card_root / f"{card_id}.md").write_text(
        "\n".join(
            [
                "---",
                f"card_id: {card_id}",
                "topic: Fixed Income",
                "los: FI.Duration",
                "fix_rule: Use effective duration for option-sensitive bonds.",
                "next_drill: Practice one callable bond duration question.",
                f"correct_resolution: {correct_resolution}",
                "---",
                "",
                "## Prompt",
                "Which duration measure fits callable bonds?",
                "",
                "## Wrong Output",
                wrong_answer,
            ]
        ),
        encoding="utf-8",
    )


def _make_pdf_bytes(lines: list[str]) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    _, height = letter
    y = height - 72
    for line in lines:
        pdf.drawString(72, y, line)
        y -= 18
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _write_asset(repo_root: Path, asset: CorrectKnowledgeAsset) -> None:
    asset_root = repo_root / ".system" / "memory" / "review" / "asset-candidates"
    asset_root.mkdir(parents=True, exist_ok=True)
    (asset_root / f"{asset.asset_id}.json").write_text(
        json.dumps(asset.as_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _coverage_record(client: TestClient, topic_id: str) -> dict:
    response = client.get(f"/api/review-lab/syllabus/coverage/{topic_id}")
    assert response.status_code == 200
    return response.json()
