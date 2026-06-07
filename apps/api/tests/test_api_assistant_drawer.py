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


def test_assistant_router_creates_capture_follow_up_when_question_text_is_missing(client: TestClient) -> None:
    response = client.post(
        "/api/assistant/messages",
        json={
            "conversation_id": "",
            "page_context": {"route": "/review", "label": "Daily Review"},
            "message": "I got this FSA common-size question wrong.",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"]["workflow"] == "record-mistake"
    assert payload["assistant_reply"]["kind"] == "follow_up"
    assert payload["assistant_reply"]["question"] == "Paste the question or upload the screenshot."
    assert payload["action"] is None


def test_assistant_router_records_capture_when_required_fields_are_present(client: TestClient) -> None:
    response = client.post(
        "/api/assistant/messages",
        json={
            "conversation_id": "",
            "page_context": {"route": "/review", "label": "Daily Review"},
            "message": "I got this wrong. Topic: Financial Statement Analysis. LOS: FSA.2.2. Question: cash common-size balance sheet. Wrong answer: 20%. Correct answer: 25%. Confidence: 3.",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"]["workflow"] == "record-mistake"
    assert payload["assistant_reply"]["kind"] == "action_result"
    assert payload["action"]["action_type"] == "record_mistake"
    assert payload["action"]["status"] == "completed"
    assert payload["action"]["summary"].startswith("Recorded")


def test_assistant_router_routes_tutor_request_to_grounded_answer(client: TestClient) -> None:
    response = client.post(
        "/api/assistant/messages",
        json={
            "conversation_id": "",
            "page_context": {"route": "/today", "label": "Today"},
            "message": "Explain WACC step by step and tell me the BA II Plus steps.",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"]["workflow"] == "tutor"
    assert payload["assistant_reply"]["kind"] == "tutor_answer"
    assert payload["action"]["action_type"] == "tutor_answer"


def test_assistant_router_routes_quick_command_without_new_capture_record(client: TestClient) -> None:
    response = client.post(
        "/api/assistant/messages",
        json={
            "conversation_id": "",
            "page_context": {"route": "/today", "label": "Today"},
            "message": "Open Review Lab",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"]["workflow"] == "quick-command"
    assert payload["action"]["action_type"] == "open_route"
    assert payload["action"]["launch_route"] == "/review/lab"
