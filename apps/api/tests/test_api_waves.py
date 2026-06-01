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


def test_provenance_privacy_xapi_and_trust_routes(client: TestClient) -> None:
    consent = client.post("/api/privacy/consent", json={"provider": "deepseek", "purpose": "grounded_explanations", "granted": True})
    assert consent.status_code == 201

    provenance = client.post(
        "/api/provenance",
        json={"entity_id": "source-1", "activity_type": "source.imported", "evidence_refs": ["manual-1"]},
    )
    assert provenance.status_code == 201
    assert client.get("/api/provenance/source-1").json()["evidence_refs"] == ["manual-1"]

    exported = client.get("/api/privacy/export")
    assert exported.status_code == 200
    assert "consent" in exported.json()["streams"]
    assert client.get("/api/export/xapi.json").json()["statements"] == []
    assert client.get("/api/export/caliper.json").json()["sensor"] == "OpenExam"

    requested = client.post("/api/privacy/purge", json={})
    assert requested.status_code == 200
    blocked = client.post("/api/privacy/purge", json={"confirmation_token": "wrong"})
    assert blocked.status_code == 422
