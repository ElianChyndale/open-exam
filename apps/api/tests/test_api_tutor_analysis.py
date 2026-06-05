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
    config = tmp_path / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "\n".join(
            [
                "tutor_analysis_enabled: true",
                "skill_reflection_enabled: true",
                "skill_upgrade_proposals_enabled: true",
                "skill_codex_task_generator_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    from app.models import MistakeEvent

    event = MistakeEvent.from_payload(
        {
            "source_layer": "question",
            "topic": "Financial Statement Analysis",
            "los": "common-size balance sheet",
            "prompt_or_question": "Using vertical common-size balance sheet analysis, cash is what percentage?",
            "wrong_choice_or_output": "32%",
            "correct_resolution": "Correct answer: 25%. For a common-size balance sheet, each line item is divided by total assets.",
            "error_type": "formula_misuse",
            "confidence": 2,
            "time_spent": 30,
            "evidence_refs": ["mock-1"],
        }
    )
    repo.append_event(event)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_api_tutor_analysis_and_skills_routes(client: TestClient) -> None:
    analyzed = client.post("/api/tutor/analyze-event/evt-74c61c67778a")
    if analyzed.status_code == 404:
        # fall back to the single seeded event id if the stable id changes
        from deps import get_repo

        repo = app.dependency_overrides[get_repo]()
        event_id = repo.load_events()[0].event_id
        analyzed = client.post(f"/api/tutor/analyze-event/{event_id}")
    assert analyzed.status_code == 200
    analysis_id = analyzed.json()["analysis"]["analysis_id"]

    fetched = client.get(f"/api/tutor/analysis/{analysis_id}")
    assert fetched.status_code == 200
    assert fetched.json()["analysis"]["analysis_id"] == analysis_id

    confirmed = client.post(f"/api/tutor/analysis/{analysis_id}/confirm")
    assert confirmed.status_code == 200
    assert confirmed.json()["analysis"]["validation_status"] == "confirmed"

    registry = client.get("/api/skills/registry")
    assert registry.status_code == 200
    assert registry.json()["skills"]

    health = client.get("/api/skills/cfa-question-captor/health")
    assert health.status_code == 200
    assert "score" in health.json()["health"]

    proposals = client.get("/api/skills/upgrade-proposals")
    assert proposals.status_code == 200
