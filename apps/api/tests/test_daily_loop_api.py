from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
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


def test_notifications_include_reviews_overdue_tasks_mock_deadlines_and_inactive_streaks(client: TestClient, repo: LocalRepository) -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    repo.append_stream_event("review", "review.responded", {"prompt_id": "due-prompt", "next_review_date": yesterday})
    repo.append_stream_event(
        "task",
        "task.planned",
        {"task": {"task_id": "overdue-task", "title": "Finish deferred drill", "date": yesterday, "deadline": yesterday, "status": "pending", "estimated_minutes": 20, "energy_fit": "moderate", "priority": 80}},
    )
    mock_dir = repo.memory_root / "mock_sessions"
    mock_dir.mkdir(parents=True, exist_ok=True)
    (mock_dir / "deadline-mock.json").write_text('{"session_id":"deadline-mock","session_label":"Deadline mock","scheduled_date":"' + yesterday + '"}', encoding="utf-8")

    kinds = {item["kind"] for item in client.get("/api/notifications").json()["notifications"]}

    assert {"review.due", "task.overdue", "mock.deadline"} <= kinds

    old_repo = LocalRepository(repo.root / "old-profile")
    old_repo.append_jsonl_event(
        "profile",
        {
            "schema_version": 1,
            "event_id": "old-profile",
            "event_type": "profile.updated",
            "learner_id": "local",
            "occurred_at": (datetime.now(UTC) - timedelta(days=8)).isoformat(),
            "source_refs": [],
            "payload": {},
        },
    )
    from services.daily_loop_service import notifications

    assert any(item["kind"] == "streak.inactive" for item in notifications(old_repo))


def test_curriculum_subjects_include_evidence_weakness_overlays(client: TestClient) -> None:
    client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "Which duration measure handles changing cash flows?",
            "wrong_choice_or_output": "Modified duration",
            "correct_resolution": "Effective duration",
            "error_type": "concept_confusion",
            "confidence": 1,
            "time_spent": 20,
            "evidence_refs": ["map-overlay"],
        },
    )

    fixed_income = next(subject for subject in client.get("/api/curriculum").json()["subjects"] if subject["subject"] == "Fixed Income")

    assert fixed_income["weakness_count"] == 1
    assert fixed_income["weakness_los"] == ["FI.Duration"]


def test_energy_check_in_refits_executable_task_order(client: TestClient) -> None:
    initial = client.get("/api/tasks/today?focus_topic=Fixed%20Income").json()["tasks"]
    assert initial[0]["task_type"] == "active_recall"

    response = client.post(
        "/api/energy/check-in",
        json={"energy_level": 0, "mental_clarity": 3, "physical_fatigue": 8, "motivation": 3},
    )

    assert response.status_code == 200
    refitted = client.get("/api/tasks/today").json()["tasks"]
    assert refitted[0]["task_type"] in {"active_recall", "light_review"}
    assert refitted[-1]["task_type"] == "interleaved_set"
