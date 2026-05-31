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


def test_profile_update_is_persisted_as_versioned_event(client: TestClient, repo: LocalRepository) -> None:
    response = client.put(
        "/api/profile",
        json={
            "exam_date": "2026-11-15",
            "current_phase": "review",
            "target_score_percentile": 75,
            "daily_minutes_available": 150,
            "weekly_study_days": 6,
            "preferred_session_minutes": 50,
            "peak_energy_window": "08:00-11:00",
            "moderate_energy_window": "14:00-18:00",
            "low_energy_window": "20:00-22:00",
        },
    )

    assert response.status_code == 200
    assert response.json()["profile"]["exam_date"] == "2026-11-15"
    events = repo.load_stream_events("profile")
    assert events[-1]["schema_version"] == 1
    assert events[-1]["event_type"] == "profile.updated"
    assert client.get("/api/profile").json()["profile"]["daily_minutes_available"] == 150


def test_curriculum_exposes_official_2026_registry(client: TestClient) -> None:
    response = client.get("/api/curriculum")

    assert response.status_code == 200
    payload = response.json()
    assert payload["subject_count"] == 10
    assert payload["module_count"] == 93
    assert payload["subjects"][0]["modules"]


def test_today_tasks_persist_allowed_status_transition(client: TestClient, repo: LocalRepository) -> None:
    tasks_response = client.get("/api/tasks/today?focus_topic=Fixed%20Income")

    assert tasks_response.status_code == 200
    tasks = tasks_response.json()["tasks"]
    assert tasks
    task_id = tasks[0]["task_id"]

    status_response = client.post(f"/api/tasks/{task_id}/status", json={"status": "completed"})

    assert status_response.status_code == 200
    assert status_response.json()["task"]["status"] == "completed"
    events = repo.load_stream_events("task")
    assert any(event["event_type"] == "task.completed" for event in events)


def test_task_status_rejects_unknown_transition(client: TestClient) -> None:
    tasks = client.get("/api/tasks/today").json()["tasks"]

    response = client.post(f"/api/tasks/{tasks[0]['task_id']}/status", json={"status": "invented"})

    assert response.status_code == 422


def test_retrieval_session_scores_response_and_updates_spacing(client: TestClient, repo: LocalRepository) -> None:
    attempt = client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "When should effective duration be used?",
            "wrong_choice_or_output": "Only for straight bonds.",
            "correct_resolution": "Use effective duration when cash flows may change as yields change.",
            "error_type": "concept_confusion",
            "confidence": 1,
            "time_spent": 70,
            "evidence_refs": ["daily-loop-test"],
        },
    )
    assert attempt.status_code == 200

    session = client.post("/api/review-sessions", json={"max_items": 5}).json()

    assert session["items"]
    item = session["items"][0]
    assert item["answer_text"]
    response = client.post(
        f"/api/review-sessions/{session['session_id']}/responses",
        json={
            "prompt_id": item["prompt_id"],
            "score": 3,
            "self_explanation": "Cash flows can change because embedded options alter the expected path.",
        },
    )

    assert response.status_code == 200
    assert response.json()["next_review_date"]
    assert repo.load_stream_events("review")[-1]["event_type"] == "review.responded"


def test_notifications_include_open_tasks(client: TestClient) -> None:
    client.get("/api/tasks/today?focus_topic=Economics")

    response = client.get("/api/notifications")

    assert response.status_code == 200
    assert any(item["kind"] == "task.pending" for item in response.json()["notifications"])
