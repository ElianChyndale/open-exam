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
    _enable_tutor_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_tutor_empty_state_returns_missing_evidence(client: TestClient) -> None:
    response = client.post(
        "/api/tutor/ask",
        json={"profile_id": "fresh", "mode": "explain", "query": "Explain WACC"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["missing_evidence"] is True
    assert payload["source_context"] == []
    assert "evidence is missing" in payload["answer"].lower()
    assert {action["launch_route"] for action in payload["recommended_actions"]}.intersection(
        {"/review/assets", "/review/resources", "/review/search"}
    )


def test_tutor_grounded_answer_is_correct_only_and_cited(client: TestClient, tmp_path: Path) -> None:
    wrong_phrase = "UNIQUE_WRONG_TUTOR_PHRASE"
    _seed_tutor_fixture(tmp_path, wrong_phrase=wrong_phrase)

    response = client.post(
        "/api/tutor/ask",
        json={
            "profile_id": "default",
            "mode": "formula_help",
            "query": "Explain WACC and the calculator steps",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    body = json.dumps(payload, ensure_ascii=False)
    assert payload["answer"]
    assert payload["missing_evidence"] is False
    assert payload["source_context"]
    assert "source_refs" in body or "cited_source_refs" in body
    assert "tutor-wacc#seg-1" in body
    assert "WACC = w_d r_d (1 - t) + w_e r_e" in body
    assert "BA II Plus" in body
    assert any(action["launch_route"] == "/review/formulas" for action in payload["recommended_actions"])

    for forbidden in [
        "wrong_choice_or_output",
        "wrong_formula",
        "wrong_reasoning",
        "answer_text",
        "selected_choice",
        "internal_secret",
        wrong_phrase,
        "DRAFT_UNCONFIRMED_TUTOR_PHRASE",
    ]:
        assert forbidden not in body


def test_tutor_hint_mode_uses_progressive_hints_without_final_answer(client: TestClient, tmp_path: Path) -> None:
    _seed_tutor_fixture(tmp_path, wrong_phrase="UNIQUE_WRONG_TUTOR_HINT")

    response = client.post(
        "/api/tutor/ask",
        json={"profile_id": "default", "mode": "hint", "query": "Give me a hint for WACC"},
    )

    assert response.status_code == 200
    payload = response.json()
    answer = payload["answer"]
    assert "Hint 1" in answer
    assert "Final answer" not in answer
    assert "w_d r_d (1 - t)" not in answer
    assert payload["source_context"]


def test_tutor_language_strategy_and_trace_modes(client: TestClient, tmp_path: Path) -> None:
    wrong_phrase = "UNIQUE_WRONG_TUTOR_MODE"
    _seed_tutor_fixture(tmp_path, wrong_phrase=wrong_phrase)

    language = client.post(
        "/api/tutor/ask",
        json={"profile_id": "default", "mode": "language_help", "query": "Explain repasar in context"},
    )
    assert language.status_code == 200
    language_payload = language.json()
    assert "repasar" in json.dumps(language_payload, ensure_ascii=False)
    assert any(ctx["context_type"] == "lexical_asset" for ctx in language_payload["source_context"])
    assert any(action["launch_route"] == "/language/review" for action in language_payload["recommended_actions"])

    strategy = client.post(
        "/api/tutor/ask",
        json={
            "profile_id": "default",
            "mode": "study_strategy",
            "query": "What should I do next if I only have 20 minutes?",
        },
    )
    assert strategy.status_code == 200
    strategy_payload = strategy.json()
    strategy_body = json.dumps(strategy_payload, ensure_ascii=False)
    assert "20" in strategy_body or "minute" in strategy_body.lower()
    assert any(action["launch_route"] in {"/review/study-planner", "/review/analytics"} for action in strategy_payload["recommended_actions"])

    trace = client.post(
        "/api/tutor/ask",
        json={"profile_id": "default", "mode": "trace_source", "query": "Show me the source for WACC"},
    )
    assert trace.status_code == 200
    trace_payload = trace.json()
    trace_body = json.dumps(trace_payload, ensure_ascii=False)
    assert "upstream" in trace_body.lower() or "source" in trace_body.lower()
    assert "tutor-wacc#seg-1" in trace_body
    assert wrong_phrase not in trace_body


def test_tutor_search_context_suggestions_and_conversation_memory(client: TestClient, tmp_path: Path) -> None:
    _seed_tutor_fixture(tmp_path, wrong_phrase="UNIQUE_WRONG_TUTOR_MEMORY")

    contexts = client.get("/api/tutor/search-context?profile_id=default&q=WACC&mode=formula_help")
    assert contexts.status_code == 200
    context_payload = contexts.json()
    assert context_payload["source_context"]
    assert context_payload["source_context"][0]["relevance_score"] >= context_payload["source_context"][-1]["relevance_score"]

    suggestions = client.get("/api/tutor/suggestions?profile_id=default")
    assert suggestions.status_code == 200
    suggestion_payload = suggestions.json()
    assert any(item["mode"] == "formula_help" for item in suggestion_payload["suggestions"])
    assert any(item["launch_route"] == "/review/tutor" for item in suggestion_payload["suggestions"])

    created = client.post(
        "/api/tutor/conversations",
        json={"profile_id": "default", "mode": "formula_help", "title": "WACC tutor"},
    )
    assert created.status_code == 200
    conversation_id = created.json()["conversation"]["conversation_id"]

    message = client.post(
        f"/api/tutor/conversations/{conversation_id}/message",
        json={"content": "Explain WACC and calculator steps"},
    )
    assert message.status_code == 200
    updated = message.json()["conversation"]
    assert len(updated["messages"]) == 2
    assert updated["messages"][1]["role"] == "assistant"
    assert updated["messages"][1]["cited_source_refs"]

    fetched = client.get(f"/api/tutor/conversations/{conversation_id}")
    assert fetched.status_code == 200
    assert fetched.json()["conversation_id"] == conversation_id

    listed = client.get("/api/tutor/conversations?profile_id=default")
    assert listed.status_code == 200
    assert any(item["conversation_id"] == conversation_id for item in listed.json()["conversations"])

    archived = client.post(f"/api/tutor/conversations/{conversation_id}/archive")
    assert archived.status_code == 200
    assert archived.json()["conversation"]["status"] == "archived"


def test_tutor_ranking_prefers_confirmed_source_backed_context_over_generated_noise(client: TestClient, tmp_path: Path) -> None:
    _seed_tutor_fixture(tmp_path, wrong_phrase="UNIQUE_WRONG_TUTOR_RANKING")
    _write_json(
        tmp_path / ".system" / "memory" / "review" / "asset-candidates" / "asset-generated-no-source.json",
        {
            "asset_id": "asset-generated-no-source",
            "asset_type": "formula",
            "profile_id": "default",
            "title": "Explain WACC and the calculator steps",
            "correct_rule": "Generated summary without cited evidence.",
            "plain_formula": "WACC placeholder",
            "validation_status": "generated",
            "quality_score": 1.0,
            "source_refs": [],
        },
    )

    contexts = client.get(
        "/api/tutor/search-context?profile_id=default&q=Explain%20WACC%20and%20the%20calculator%20steps&mode=formula_help"
    )

    assert contexts.status_code == 200
    payload = contexts.json()
    assert payload["source_context"]
    top = payload["source_context"][0]
    assert top["validation_status"] in {"confirmed", "validated", "derived"}
    assert top["source_refs"]
    assert top["context_type"] in {"formula", "asset", "source_segment"}


def test_tutor_data_governance_inventory_and_safe_export(client: TestClient, tmp_path: Path) -> None:
    _seed_tutor_fixture(tmp_path, wrong_phrase="UNIQUE_WRONG_TUTOR_GOVERNANCE")
    created = client.post(
        "/api/tutor/conversations",
        json={"profile_id": "default", "mode": "explain", "title": "Governed tutor"},
    )
    assert created.status_code == 200
    assert client.post(
        f"/api/tutor/conversations/{created.json()['conversation']['conversation_id']}/message",
        json={"content": "Explain WACC"},
    ).status_code == 200

    inventory = client.get("/api/data-governance/inventory")
    assert inventory.status_code == 200
    categories = {item["category"]: item for item in inventory.json()["items"]}
    assert "tutor_conversations" in categories
    assert categories["tutor_conversations"]["record_count"] >= 1

    export = client.post("/api/data-governance/export", json={"mode": "safe"})
    assert export.status_code == 200
    export_path = tmp_path / export.json()["snapshot"]["file_path"]
    assert export_path.exists()
    archive_bytes = export_path.read_bytes()
    assert b"data/tutor_conversations.json" in archive_bytes
    assert b"UNIQUE_WRONG_TUTOR_GOVERNANCE" not in archive_bytes
    for forbidden in [b"wrong_choice_or_output", b"wrong_formula", b"wrong_reasoning", b"answer_text", b"selected_choice"]:
        assert forbidden not in archive_bytes


def _seed_tutor_fixture(repo_root: Path, *, wrong_phrase: str) -> None:
    _write_json(
        repo_root / ".system" / "memory" / "review" / "asset-sources" / "source-tutor-wacc.json",
        {
            "source_id": "source-tutor-wacc",
            "profile_id": "default",
            "title": "Tutor WACC Source",
            "source_type": "text_note",
            "content_hash": "source-hash",
            "imported_at": "2026-06-03T00:00:00+00:00",
            "extraction_status": "extracted",
            "source_refs": ["tutor-wacc#source"],
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "asset-segments" / "source-tutor-wacc.json",
        [
            {
                "segment_id": "seg-tutor-wacc",
                "source_id": "source-tutor-wacc",
                "page": 1,
                "heading": "Weighted average cost of capital",
                "text": "WACC = w_d r_d (1 - t) + w_e r_e. Use after-tax cost of debt and target market weights.",
                "source_ref": "tutor-wacc#seg-1",
                "evidence_type": "formula",
                "confidence": 0.96,
            }
        ],
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "asset-candidates" / "asset-wacc-tutor.json",
        {
            "asset_id": "asset-wacc-tutor",
            "asset_type": "formula",
            "profile_id": "default",
            "subject": "Corporate Issuers",
            "module": "Cost of Capital",
            "los": "CI-TUTOR-WACC",
            "title": "WACC formula and calculator procedure",
            "correct_rule": "Use after-tax cost of debt with target capital weights.",
            "formula_latex": "WACC = w_d r_d (1 - t) + w_e r_e",
            "plain_formula": "WACC = w_d r_d (1 - t) + w_e r_e",
            "variables": [
                {"symbol": "w_d", "meaning": "target debt weight"},
                {"symbol": "r_d", "meaning": "pre-tax cost of debt"},
                {"symbol": "t", "meaning": "tax rate"},
                {"symbol": "w_e", "meaning": "target equity weight"},
                {"symbol": "r_e", "meaning": "cost of equity"},
            ],
            "applies_when": ["valuing a firm with target capital structure"],
            "common_correct_boundary_rules": ["Use after-tax debt cost; weights should be target market weights."],
            "ba_ii_plus_steps": ["Enter cash flows", "Set I/Y to WACC", "Press NPV, then CPT"],
            "formula_family": "cost_of_capital",
            "syllabus_topic_id": "topic-wacc-tutor",
            "source_refs": ["tutor-wacc#seg-1"],
            "source_quality": 0.92,
            "validation_status": "confirmed",
            "mastery_state": "Learning",
            "wrong_choice_or_output": wrong_phrase,
            "wrong_formula": wrong_phrase,
            "wrong_reasoning": wrong_phrase,
            "answer_text": wrong_phrase,
            "selected_choice": wrong_phrase,
            "internal_secret": wrong_phrase,
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "asset-candidates" / "asset-draft-wacc-tutor.json",
        {
            "asset_id": "asset-draft-wacc-tutor",
            "asset_type": "formula",
            "profile_id": "default",
            "title": "Draft WACC unsafe note",
            "correct_rule": "DRAFT_UNCONFIRMED_TUTOR_PHRASE",
            "plain_formula": "DRAFT_UNCONFIRMED_TUTOR_PHRASE",
            "source_refs": ["draft-wacc#seg-1"],
            "validation_status": "draft",
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "syllabus" / "topics.json",
        [
            {
                "topic_id": "topic-wacc-tutor",
                "profile_id": "default",
                "subject": "Corporate Issuers",
                "module": "Cost of Capital",
                "los": "CI-TUTOR-WACC",
                "title": "Calculate and interpret WACC",
                "description": "Weighted average cost of capital with target weights.",
                "exam_weight": 0.8,
                "importance": 0.9,
                "expected_asset_types": ["formula"],
                "formula_expected": True,
                "source_refs": ["tutor-wacc#seg-1"],
            }
        ],
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "syllabus" / "coverage-default.json",
        {
            "profile_id": "default",
            "records": [
                {
                    "record_id": "coverage-wacc-tutor",
                    "profile_id": "default",
                    "topic_id": "topic-wacc-tutor",
                    "coverage_status": "weak",
                    "coverage_score": 0.61,
                    "confirmed_asset_count": 1,
                    "missing_asset_types": [],
                    "topic": {
                        "topic_id": "topic-wacc-tutor",
                        "profile_id": "default",
                        "title": "Calculate and interpret WACC",
                        "subject": "Corporate Issuers",
                        "module": "Cost of Capital",
                        "exam_weight": 0.8,
                        "source_refs": ["tutor-wacc#seg-1"],
                    },
                    "links": [{"asset_id": "asset-wacc-tutor", "confidence": 0.9, "match_reason": "exact LOS"}],
                }
            ],
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "review" / "mock-retro" / "transfer-gaps" / "transfer-gap-wacc-tutor.json",
        {
            "gap_id": "transfer-gap-wacc-tutor",
            "profile_id": "default",
            "topic_id": "topic-wacc-tutor",
            "asset_id": "asset-wacc-tutor",
            "formula_family": "cost_of_capital",
            "gap_type": "calculator_procedure_gap",
            "severity": 0.86,
            "evidence_count": 2,
            "source_refs": ["tutor-wacc#seg-1"],
            "status": "open",
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "language" / "dictionary-kernel" / "dictionaries" / "dict-tutor.json",
        {
            "dictionary_id": "dict-tutor",
            "profile_id": "default",
            "title": "Tutor Spanish Dictionary",
            "dictionary_type": "spanish_english",
            "validation_status": "confirmed",
            "quality_score": 0.9,
            "source_refs": ["dict-tutor#entry-repasar"],
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "language" / "dictionary-kernel" / "lexical-assets" / "lex-repasar.json",
        {
            "lexical_id": "lex-repasar",
            "profile_id": "default",
            "dictionary_id": "dict-tutor",
            "headword": "repasar",
            "language": "es",
            "target_language": "en",
            "part_of_speech": "verb",
            "definition": "to review or go over again",
            "translation": "review",
            "example_sentence": "Voy a repasar la formula WACC.",
            "collocations": ["repasar una formula"],
            "validation_status": "confirmed",
            "quality_score": 0.88,
            "source_refs": ["dict-tutor#entry-repasar"],
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "study-planner" / "plans" / "study-plan-tutor.json",
        {
            "plan_id": "study-plan-tutor",
            "profile_id": "default",
            "plan_date": "2026-06-03",
            "energy_mode": "normal",
            "available_minutes": 20,
            "goal": "WACC repair",
            "status": "active",
            "blocks": [
                {
                    "block_id": "block-wacc-tutor",
                    "block_type": "formula_lab",
                    "title": "Repair WACC calculator procedure",
                    "status": "pending",
                    "priority": 96,
                    "target_minutes": 20,
                    "launch_route": "/review/formulas",
                    "due_reason": "Open calculator procedure gap in WACC.",
                    "linked_asset_ids": ["asset-wacc-tutor"],
                    "linked_topic_ids": ["topic-wacc-tutor"],
                    "linked_gap_ids": ["transfer-gap-wacc-tutor"],
                    "linked_lexical_ids": [],
                }
            ],
        },
    )
    _write_json(
        repo_root / ".system" / "memory" / "assessments" / "sessions" / "assessment-tutor.json",
        {
            "assessment_id": "assessment-tutor",
            "profile_id": "default",
            "title": "Tutor WACC Assessment",
            "mode": "formula_drill",
            "status": "completed",
            "summary": {"score": 0.5, "transfer_gaps_created": 1},
            "questions": [
                {
                    "question_id": "question-wacc-tutor",
                    "profile_id": "default",
                    "question_type": "calculator_steps",
                    "prompt": "Which calculator setup supports WACC valuation?",
                    "correct_rule": "Use WACC as I/Y for NPV valuation.",
                    "validation_status": "confirmed",
                    "source_refs": ["tutor-wacc#seg-1"],
                    "linked_asset_ids": ["asset-wacc-tutor"],
                    "linked_topic_ids": ["topic-wacc-tutor"],
                    "linked_gap_ids": ["transfer-gap-wacc-tutor"],
                }
            ],
            "responses": [{"question_id": "question-wacc-tutor", "answer_text": wrong_phrase, "selected_choice": wrong_phrase}],
        },
    )


def _enable_tutor_features(repo_root: Path) -> None:
    config_path = repo_root / ".system" / "config" / "features.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "\n".join(
            [
                "daily_review_lab: true",
                "daily_review_lab_enabled: true",
                "daily_review_correct_only_mode: true",
                "review_asset_ingestion_enabled: true",
                "formula_lab_enabled: true",
                "formula_ba_ii_plus_steps_enabled: true",
                "syllabus_coverage_enabled: true",
                "mock_retro_enabled: true",
                "transfer_gap_priority_enabled: true",
                "dictionary_kernel_enabled: true",
                "lexical_review_enabled: true",
                "language_os_enabled: true",
                "mission_control_enabled: true",
                "study_planner_enabled: true",
                "learning_analytics_enabled: true",
                "adaptive_assessment_enabled: true",
                "knowledge_graph_enabled: true",
                "global_search_enabled: true",
                "traceability_map_enabled: true",
                "impact_analysis_enabled: true",
                "correct_only_graph_enabled: true",
                "data_governance_enabled: true",
                "safe_export_enabled: true",
                "backup_restore_enabled: true",
                "privacy_redaction_enabled: true",
                "tutor_copilot_enabled: true",
                "grounded_tutor_retrieval_enabled: true",
                "tutor_source_citations_enabled: true",
                "tutor_correct_only_enabled: true",
                "tutor_llm_provider_enabled: false",
                "tutor_conversation_memory_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
