from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import LocalRepository
from deps import get_repo
from main import app


@pytest.fixture()
def repo(tmp_path: Path) -> LocalRepository:
    return LocalRepository(tmp_path)


@pytest.fixture()
def client(repo: LocalRepository) -> TestClient:
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_timed_mock_run_tracks_checkpoints_pause_resume_and_mistake_capture(client: TestClient, repo: LocalRepository) -> None:
    created = client.post(
        "/api/mock/runs",
        json={"session_label": "Mock AM", "total_minutes": 135, "total_questions": 90},
    )

    assert created.status_code == 200
    run = created.json()["run"]
    assert len(run["checkpoints"]) == 3

    paused = client.post(
        f"/api/mock/runs/{run['run_id']}/state",
        json={"action": "pause", "elapsed_seconds": 900},
    )
    assert paused.status_code == 200
    assert paused.json()["run"]["status"] == "paused"

    resumed = client.post(
        f"/api/mock/runs/{run['run_id']}/state",
        json={"action": "resume", "elapsed_seconds": 900},
    )
    assert resumed.json()["run"]["status"] == "active"

    answer = client.post(
        f"/api/mock/runs/{run['run_id']}/answers",
        json={
            "question_id": "mock-q-18",
            "prompt": "Which duration measure handles changing expected cash flows?",
            "answer": "A",
            "correct_answer": "B",
            "explanation": "Effective duration handles changing expected cash flows.",
            "is_correct": False,
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "elapsed_seconds": 110,
            "confidence": 4,
        },
    )

    assert answer.status_code == 200
    assert answer.json()["mistake_event_id"]
    assert repo.load_stream_events("mock-run")[-1]["event_type"] == "mock-run.answered"
    assert repo.load_events()[-1].question_source == "mock_run"


def test_external_mock_result_import_is_append_only(client: TestClient, repo: LocalRepository) -> None:
    response = client.post(
        "/api/mock/import-results",
        json={
            "source_name": "provider-export.csv",
            "session_label": "External Mock 2",
            "total_questions": 2,
            "answers": [
                {"question_id": "q1", "is_correct": True, "topic": "Ethics", "los": "ETH.I"},
                {"question_id": "q2", "is_correct": False, "topic": "Economics", "los": "ECO.FX"},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["run"]["source_kind"] == "external_import"
    assert response.json()["run"]["correct_count"] == 1
    assert repo.load_stream_events("mock-run")[-1]["event_type"] == "mock-run.imported"


def test_coach_rejects_unsupported_claims_and_persists_evidence_linked_briefs(client: TestClient, repo: LocalRepository) -> None:
    rejected = client.post(
        "/api/coach/session-retro",
        json={"summary": "Spend more time on Fixed Income.", "source_refs": []},
    )
    assert rejected.status_code == 422

    accepted = client.post(
        "/api/coach/session-retro",
        json={
            "summary": "Slow down on duration comparisons.",
            "source_refs": ["mock-q-18", "card-duration"],
            "biases": ["high-confidence guessing"],
        },
    )

    assert accepted.status_code == 200
    brief = accepted.json()["brief"]
    assert brief["evidence_refs"] == ["mock-q-18", "card-duration"]
    assert brief["recommendations"]
    assert client.get("/api/coach/briefs").json()["briefs"][0]["brief_id"] == brief["brief_id"]
    assert repo.load_stream_events("coach")[-1]["event_type"] == "coach.session-retro"


def test_search_indexes_curriculum_and_evidence_assets(client: TestClient) -> None:
    client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "When should effective duration be used?",
            "wrong_choice_or_output": "Never.",
            "correct_resolution": "Use effective duration when expected cash flows can change.",
            "error_type": "concept_confusion",
            "confidence": 1,
            "time_spent": 30,
            "evidence_refs": ["search-evidence"],
        },
    )

    response = client.get("/api/search?q=duration")

    assert response.status_code == 200
    assert response.json()["results"]
    assert any(result["kind"] in {"curriculum", "mistake-card"} for result in response.json()["results"])


def test_graph_locks_official_records_and_persists_personal_overlay(client: TestClient, repo: LocalRepository) -> None:
    graph = client.get("/api/knowledge-graph").json()
    official = next(node for node in graph["nodes"] if node["source_kind"] == "official")
    assert official["locked"] is True

    rejected = client.put(
        "/api/knowledge-graph/overlay",
        json={"nodes": [{**official, "label": "Tampered"}], "edges": []},
    )
    assert rejected.status_code == 409

    accepted = client.put(
        "/api/knowledge-graph/overlay",
        json={
            "nodes": [
                {
                    "id": "personal-duration-note",
                    "label": "Duration comparison drill",
                    "source_kind": "personal",
                    "node_type": "note",
                    "x": 120,
                    "y": 240,
                    "notes": "Contrast effective and modified duration.",
                }
            ],
            "edges": [],
        },
    )

    assert accepted.status_code == 200
    assert repo.load_stream_events("graph-overlay")[-1]["event_type"] == "graph-overlay.updated"
    refreshed = client.get("/api/knowledge-graph").json()
    assert any(node["id"] == "personal-duration-note" for node in refreshed["nodes"])


def test_weekly_report_is_exportable_and_evidence_linked(client: TestClient) -> None:
    client.post(
        "/api/coach/session-retro",
        json={"summary": "Practice curve interpretation.", "source_refs": ["week-source"]},
    )

    response = client.get("/api/reports/weekly")

    assert response.status_code == 200
    payload = response.json()
    assert payload["report_id"]
    assert payload["evidence_refs"] == ["week-source"]
    assert "# OpenExam weekly learner report" in payload["markdown_content"]

    markdown = client.get("/api/reports/weekly?format=markdown")
    assert markdown.status_code == 200
    assert "attachment;" in markdown.headers["content-disposition"]
