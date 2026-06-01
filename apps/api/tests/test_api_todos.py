from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_todo_api_crud_and_revision_conflict(client: TestClient) -> None:
    initial = client.get("/api/todos/today?date=2026-06-02")
    assert initial.status_code == 200
    revision = initial.json()["revision"]

    created = client.post(
        "/api/todos/tasks",
        json={"text": "Implement Todo API", "deadline": "18:00", "expected_revision": revision, "date": "2026-06-02"},
    )
    assert created.status_code == 201
    state = created.json()
    task = next(item for item in state["tasks"] if item["text"] == "Implement Todo API")

    stale = client.patch(
        f"/api/todos/tasks/{task['task_id']}",
        json={"progress": 50, "expected_revision": revision},
    )
    assert stale.status_code == 409

    toggled = client.post(
        f"/api/todos/tasks/{task['task_id']}/toggle",
        json={"expected_revision": state["revision"]},
    )
    assert toggled.status_code == 200
    assert next(item for item in toggled.json()["tasks"] if item["task_id"] == task["task_id"])["status"] == "completed"


def test_todo_api_import_requires_explicit_confirmation(client: TestClient) -> None:
    blocked = client.post(
        "/api/todos/import-study-plan",
        json={"confirmed": False, "plan": {"plan_id": "sp-1", "high_energy_tasks": [{"description": "Practice"}]}},
    )
    assert blocked.status_code == 422

    imported = client.post(
        "/api/todos/import-study-plan",
        json={"confirmed": True, "plan": {"plan_id": "sp-1", "high_energy_tasks": [{"description": "Practice"}]}},
    )
    assert imported.status_code == 200
    assert any(item["text"] == "Practice" for item in imported.json()["tasks"])
