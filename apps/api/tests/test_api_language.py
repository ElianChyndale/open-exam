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


def test_language_api_manual_capture_review_grammar_and_graph(client: TestClient) -> None:
    profiles = client.get("/api/language/profiles")
    assert profiles.status_code == 200
    assert len(profiles.json()["profiles"]) == 4

    source = client.post("/api/language/sources", json={
        "source_type": "manual",
        "title": "Finance sentence",
        "language": "en",
        "content": "New shares can have a dilutive effect on EPS.",
    })
    assert source.status_code == 201
    segment_id = source.json()["segments"][0]["segment_id"]
    item = client.post("/api/language/items", json={
        "item_type": "phrase", "canonical_form": "dilutive effect", "language": "en", "segment_id": segment_id,
    })
    assert item.status_code == 201
    item_id = item.json()["item"]["item_id"]

    cards = client.post("/api/language/cards/generate", json={"item_id": item_id, "card_types": ["recognition", "production"]})
    assert cards.status_code == 201
    card_id = cards.json()["cards"][0]["card_id"]
    reviewed = client.post(f"/api/language/cards/{card_id}/review", json={"rating": "good"})
    assert reviewed.status_code == 200
    assert reviewed.json()["fsrs_state"]["repetitions"] == 1

    grammar = client.post("/api/language/grammar/analyze", json={"segment_id": segment_id})
    assert grammar.status_code == 200
    graph = client.post("/api/language/intuition/rebuild")
    assert graph.status_code == 200
    assert client.get("/api/language/stats").status_code == 200
