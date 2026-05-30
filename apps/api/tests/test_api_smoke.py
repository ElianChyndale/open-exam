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


def test_health_route_returns_ok(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_wrong_attempt_creates_traceable_event_and_card(client: TestClient, tmp_path: Path) -> None:
    response = client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.1",
            "prompt_or_question": "Bond valuation question",
            "wrong_choice_or_output": "A",
            "correct_resolution": "B because the cash flows must be discounted.",
            "error_type": "concept_confusion",
            "confidence": 2,
            "time_spent": 60,
            "evidence_refs": ["api-smoke"],
            "is_correct": False,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["event_id"].startswith("evt-")
    assert payload["card_id"].startswith("card-")
    assert payload["fix_rule"]
    assert payload["next_drill"]
    assert payload["review_due_at"]

    card_path = tmp_path / ".system" / "memory" / "question-errors" / f"{payload['card_id']}.md"
    assert card_path.exists()
    assert "source_layer: question" in card_path.read_text(encoding="utf-8")


def test_correct_attempt_is_stored_without_mistake_card(client: TestClient, tmp_path: Path) -> None:
    response = client.post(
        "/api/attempts",
        json={
            "topic": "Equity",
            "los": "EQ.1",
            "prompt_or_question": "Market efficiency question",
            "wrong_choice_or_output": "",
            "correct_resolution": "Correct.",
            "error_type": "",
            "confidence": 3,
            "time_spent": 45,
            "evidence_refs": ["api-correct"],
            "is_correct": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["attempt_id"].startswith("attempt-")
    assert payload["event_id"] == ""
    assert payload["card_id"] == ""
    assert list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md")) == []
    assert (tmp_path / ".system" / "events" / "attempt" / "attempt-events.jsonl").exists()


def test_energy_check_in_does_not_poison_mistake_event_loading(client: TestClient) -> None:
    energy = client.post(
        "/api/energy/check-in",
        json={
            "energy_level": 2,
            "mental_clarity": 6,
            "physical_fatigue": 4,
            "motivation": 6,
        },
    )
    assert energy.status_code == 200

    for path in ("/api/attempts/recent", "/api/dashboard/summary"):
        response = client.get(path)
        assert response.status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "/api/review-pack/today",
        "/api/study-plan/today",
        "/api/dashboard/summary",
        "/api/diagnose/patterns",
        "/api/mock/smoke/brief",
        "/api/institution/cohorts",
    ],
)
def test_core_get_endpoints_return_200_on_clean_repo(client: TestClient, path: str) -> None:
    response = client.get(path)

    assert response.status_code == 200
