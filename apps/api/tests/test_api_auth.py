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


def _bootstrap_admin(client: TestClient) -> dict[str, str]:
    created = client.post(
        "/api/auth/bootstrap-admin",
        json={"username": "admin", "password": "s3cret-passphrase"},
    )
    assert created.status_code == 200

    logged_in = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "s3cret-passphrase"},
    )
    assert logged_in.status_code == 200
    token = logged_in.json()["session_token"]
    return {"Authorization": f"Bearer {token}"}


def test_bootstrap_login_and_session_round_trip(client: TestClient, tmp_path: Path) -> None:
    headers = _bootstrap_admin(client)

    session = client.get("/api/auth/session", headers=headers)
    assert session.status_code == 200
    payload = session.json()
    assert payload["authenticated"] is True
    assert payload["user"]["username"] == "admin"
    assert payload["user"]["role"] == "admin"

    users_path = tmp_path / ".system" / "private" / "security" / "users.json"
    assert users_path.exists()


def test_question_bank_import_requires_admin_auth(client: TestClient) -> None:
    denied = client.post(
        "/api/question-banks/import",
        json={"source_file": "private-bank.csv", "questions": []},
    )

    assert denied.status_code == 401
    assert denied.json()["detail"] == "Authentication required"


def test_question_bank_import_allows_admin_session(client: TestClient) -> None:
    headers = _bootstrap_admin(client)

    imported = client.post(
        "/api/question-banks/import",
        headers=headers,
        json={
            "source_file": "private-bank.csv",
            "questions": [
                {
                    "page": 1,
                    "prompt": "Verified question",
                    "choices": ["A", "B", "C"],
                    "answer": "B",
                    "explanation": "B is correct.",
                    "topic": "Fixed Income",
                    "module": "M01",
                    "los": "FI.1",
                    "verification_status": "verified",
                }
            ],
        },
    )

    assert imported.status_code == 200
    assert imported.json()["verified_count"] == 1


def test_security_events_require_admin_and_return_recent_audit_log(client: TestClient) -> None:
    denied = client.get("/api/security/events")
    assert denied.status_code == 401

    headers = _bootstrap_admin(client)
    events = client.get("/api/security/events", headers=headers)

    assert events.status_code == 200
    payload = events.json()
    assert payload["count"] >= 2
    assert any(item["event_type"] == "auth.bootstrap_admin" for item in payload["events"])
    assert any(item["event_type"] == "auth.login_succeeded" for item in payload["events"])
