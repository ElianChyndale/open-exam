from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app
from study_science.knowledge_graph import KnowledgeGraphNode, KnowledgeGraphService


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_graph_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_knowledge_graph_empty_state_is_safe(client: TestClient) -> None:
    recompute = client.post("/api/knowledge-graph/recompute", json={"profile_id": "fresh"})
    assert recompute.status_code == 200
    payload = recompute.json()
    assert payload["profile_id"] == "fresh"
    assert payload["summary"]["node_count"] >= 0
    assert "nodes_by_type" in payload["summary"]
    assert "edges_by_type" in payload["summary"]

    summary = client.get("/api/knowledge-graph/summary?profile_id=fresh")
    assert summary.status_code == 200
    assert summary.json()["profile_id"] == "fresh"

    search = client.get("/api/knowledge-graph/search?profile_id=fresh&q=wacc")
    assert search.status_code == 200
    assert search.json()["results"] == []


def test_knowledge_graph_rank_boosts_exact_structured_fields_over_generic_metadata() -> None:
    formula_query = "WACC = w_d r_d (1 - t) + w_e r_e"
    structured_formula = KnowledgeGraphNode(
        node_id="formula:structured",
        profile_id="default",
        node_type="formula",
        title="Cost of capital setup",
        validation_status="confirmed",
        source_refs=["rank#formula"],
        metadata={"plain_formula": formula_query},
    )
    generic_formula = KnowledgeGraphNode(
        node_id="formula:generic",
        profile_id="default",
        node_type="formula",
        title="Cost of capital metadata",
        validation_status="confirmed",
        source_refs=["rank#formula"],
        metadata={"notes": f"Remember {formula_query}"},
    )
    assert KnowledgeGraphService._rank(structured_formula, query=formula_query, source_ref=None) > KnowledgeGraphService._rank(
        generic_formula,
        query=formula_query,
        source_ref=None,
    )

    structured_headword = KnowledgeGraphNode(
        node_id="lexical:repasar",
        profile_id="default",
        node_type="lexical_asset",
        title="Spanish review verb",
        validation_status="confirmed",
        source_refs=["rank#lexical"],
        metadata={"headword": "repasar"},
    )
    generic_headword = KnowledgeGraphNode(
        node_id="lexical:generic",
        profile_id="default",
        node_type="lexical_asset",
        title="Spanish vocabulary note",
        validation_status="confirmed",
        source_refs=["rank#lexical"],
        metadata={"notes": "repasar appears in this note"},
    )
    assert KnowledgeGraphService._rank(structured_headword, query="repasar", source_ref=None) > KnowledgeGraphService._rank(
        generic_headword,
        query="repasar",
        source_ref=None,
    )


def test_knowledge_graph_learner_content_beats_system_node_for_formula_query() -> None:
    formula_query = "WACC = w_d r_d (1 - t) + w_e r_e"
    formula = KnowledgeGraphNode(
        node_id="formula:wacc",
        profile_id="default",
        node_type="formula",
        title="Cost of capital setup",
        validation_status="confirmed",
        source_refs=["rank#wacc"],
        metadata={"plain_formula": formula_query},
    )
    system_action = KnowledgeGraphNode(
        node_id="mission_action:wacc",
        profile_id="default",
        node_type="mission_action",
        title=formula_query,
        status="open",
        quality_score=1.0,
        source_refs=[],
        metadata={"reason": "System action mentioning the formula exactly."},
    )

    assert KnowledgeGraphService._rank(formula, query=formula_query, source_ref=None) > KnowledgeGraphService._rank(
        system_action,
        query=formula_query,
        source_ref=None,
    )


def test_knowledge_graph_trace_search_and_impact_are_correct_only(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_GRAPH_PHRASE"
    fixture = _seed_cross_system_graph_fixture(client, wrong_phrase=wrong_phrase)

    recompute = client.post("/api/knowledge-graph/recompute", json={"profile_id": "default"})
    assert recompute.status_code == 200
    payload = recompute.json()
    counts = payload["summary"]["nodes_by_type"]
    assert counts["source_document"] >= 1
    assert counts["source_segment"] >= 1
    assert counts["asset"] >= 1
    assert counts["formula"] >= 1
    assert counts["syllabus_topic"] >= 1
    assert counts["coverage_record"] >= 1
    assert counts["transfer_gap"] >= 1
    assert counts["assessment"] >= 1
    assert counts["assessment_question"] >= 1
    assert counts["lexical_asset"] >= 1
    assert counts["study_plan"] >= 1
    assert counts["study_plan_block"] >= 1
    assert counts["analytics_record"] >= 1

    formula_search = client.get("/api/knowledge-graph/search?profile_id=default&q=WACC&node_type=formula")
    assert formula_search.status_code == 200
    formula_results = formula_search.json()["results"]
    assert formula_results
    assert formula_results[0]["node"]["node_type"] == "formula"
    assert formula_results[0]["connected_nodes"]

    lexical_search = client.get("/api/knowledge-graph/search?profile_id=default&q=repasar&node_type=lexical_asset")
    assert lexical_search.status_code == 200
    assert lexical_search.json()["results"]

    confirmed_assets = client.get("/api/knowledge-graph/nodes?profile_id=default&node_type=asset&validation_status=confirmed")
    assert confirmed_assets.status_code == 200
    asset_nodes = confirmed_assets.json()["nodes"]
    assert any(node["metadata"].get("asset_id") == fixture["review_asset_id"] for node in asset_nodes)

    source_search = client.get("/api/knowledge-graph/search?profile_id=default&q=Assessment Graph Review Source&node_type=source_document")
    assert source_search.status_code == 200
    source_node_id = source_search.json()["results"][0]["node"]["node_id"]
    source_impact = client.get(f"/api/knowledge-graph/impact/{source_node_id}?profile_id=default")
    assert source_impact.status_code == 200
    impacted = source_impact.json()["affected_nodes"]
    assert any(node["node_type"] in {"asset", "source_segment"} for node in impacted)

    formula_node_id = formula_results[0]["node"]["node_id"]
    trace = client.get(f"/api/knowledge-graph/nodes/{formula_node_id}/trace?profile_id=default")
    assert trace.status_code == 200
    trace_payload = trace.json()
    assert trace_payload["node"]["node_type"] == "formula"
    downstream_types = {node["node_type"] for node in trace_payload["downstream_usage"]}
    related_types = {node["node_type"] for node in trace_payload["related_nodes"]}
    assert "assessment_question" in downstream_types
    assert "transfer_gap" in downstream_types or "transfer_gap" in related_types
    assert trace_payload["source_refs"]

    related = client.get(f"/api/knowledge-graph/related/{formula_node_id}?profile_id=default")
    assert related.status_code == 200
    assert related.json()["nodes"]

    body = json.dumps(
        {
            "recompute": payload,
            "formula_search": formula_search.json(),
            "lexical_search": lexical_search.json(),
            "trace": trace_payload,
            "impact": source_impact.json(),
            "related": related.json(),
        },
        ensure_ascii=False,
    )
    assert "wrong_choice_or_output" not in body
    assert "wrong_formula" not in body
    assert "wrong_reasoning" not in body
    assert "internal_answer" not in body
    assert wrong_phrase not in body


def _seed_cross_system_graph_fixture(client: TestClient, *, wrong_phrase: str) -> dict[str, str]:
    review_source = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "title": "Assessment Graph Review Source",
            "text": "\n".join(
                [
                    "LOS: CI-GRAPH-REVIEW",
                    "Use after-tax cost of debt in WACC.",
                    "Target capital weights belong in WACC.",
                ]
            ),
            "source_type": "text_note",
        },
    )
    assert review_source.status_code == 200
    source_id = review_source.json()["source"]["source_id"]
    extracted = client.post(f"/api/review-lab/sources/{source_id}/extract-assets")
    assert extracted.status_code == 200
    review_asset = extracted.json()["assets"][0]
    assert client.post(f"/api/review-lab/assets/{review_asset['asset_id']}/confirm").status_code == 200

    resource = client.post(
        "/api/review-lab/resources/import-text",
        json={
            "title": "Assessment Graph Resource",
            "resource_type": "lecture_slide",
            "text": "\n".join(
                [
                    "LOS: CI-GRAPH-RESOURCE",
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use after-tax cost of debt with target capital structure.",
                ]
            ),
        },
    )
    assert resource.status_code == 200
    resource_id = resource.json()["resource"]["resource_id"]
    assert client.post(f"/api/review-lab/resources/{resource_id}/score").status_code == 200
    assert client.post(f"/api/review-lab/resources/{resource_id}/confirm").status_code == 200
    assert client.post(f"/api/review-lab/resources/{resource_id}/extract-evidence").status_code == 200
    assert client.post(f"/api/review-lab/resources/{resource_id}/promote-assets", json={"asset_ids": []}).status_code == 200

    formula = client.post(
        "/api/review-lab/formulas/import-text",
        json={
            "title": "Assessment Graph WACC Formula",
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
            "title": "Assessment Graph Spanish Dictionary",
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
    lexical_id = dictionary_payload["lexical_assets"][0]["lexical_id"]
    assert client.post(f"/api/language-os/dictionaries/{dictionary_payload['dictionary']['dictionary_id']}/confirm").status_code == 200
    assert client.post(f"/api/language-os/lexical-assets/{lexical_id}/confirm").status_code == 200

    retro = client.post(
        "/api/review-lab/mock-retro/import-text",
        json={
            "title": "Assessment Graph Mock Retro",
            "text": "\n".join(
                [
                    "Q1 Corporate Issuers WACC",
                    "LOS: CI-GRAPH-MOCK",
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

    assessment = client.post(
        "/api/assessments/generate",
        json={"mode": "formula_drill", "target_minutes": 20, "question_count": 4, "focus": "formula"},
    )
    assert assessment.status_code == 200
    session = assessment.json()
    formula_question = next(question for question in session["questions"] if question["question_type"] in {"formula_setup", "calculator_steps"})
    assert client.post(f"/api/assessments/{session['assessment_id']}/start").status_code == 200
    answer = client.post(
        f"/api/assessments/questions/{formula_question['question_id']}/answer",
        json={"answer_text": wrong_phrase, "confidence_before": 0.9, "time_spent_seconds": 30},
    )
    assert answer.status_code == 200
    assert client.post(
        f"/api/assessments/questions/{formula_question['question_id']}/self-grade",
        json={"grade": "partial", "confidence_after": 0.4},
    ).status_code == 200
    assert client.post(f"/api/assessments/{session['assessment_id']}/complete").status_code == 200

    plan = client.post(
        "/api/study-planner/generate",
        json={"energy_mode": "normal", "available_minutes": 90, "goal": "trace WACC"},
    )
    assert plan.status_code == 200
    plan_payload = plan.json()
    pending = next(block for block in plan_payload["blocks"] if block["status"] == "pending")
    assert client.post(f"/api/study-planner/blocks/{pending['block_id']}/start").status_code == 200
    assert client.post(
        f"/api/study-planner/blocks/{pending['block_id']}/complete",
        json={"outcome": "graph trace complete", "actual_minutes": pending["target_minutes"]},
    ).status_code == 200
    assert client.post(f"/api/study-planner/plans/{plan_payload['plan_id']}/complete").status_code == 200

    analytics = client.post("/api/learning-analytics/recompute", json={"profile_id": "default", "range": "30d"})
    assert analytics.status_code == 200
    return {
        "source_id": source_id,
        "review_asset_id": review_asset["asset_id"],
        "formula_asset_id": formula_asset["asset_id"],
        "lexical_id": lexical_id,
        "assessment_id": session["assessment_id"],
    }


def _enable_graph_features(repo_root: Path) -> None:
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
                "knowledge_graph_enabled: true",
                "global_search_enabled: true",
                "traceability_map_enabled: true",
                "impact_analysis_enabled: true",
                "correct_only_graph_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
