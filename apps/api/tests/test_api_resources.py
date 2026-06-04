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


def test_resource_api_import_search_subscription_and_audit(client: TestClient) -> None:
    providers = client.get("/api/resources/providers")
    assert providers.status_code == 200
    assert any(provider["provider_id"] == "generic_web" for provider in providers.json()["providers"])

    subscription = client.post(
        "/api/resources/subscriptions",
        json={"lane": "language", "provider": "rss_atom", "target": "https://example.com/feed.xml"},
    )
    assert subscription.status_code == 201
    subscription_id = subscription.json()["subscription_id"]
    assert client.get("/api/resources/subscriptions").json()["subscriptions"][0]["provider"] == "rss_atom"
    paused = client.patch(f"/api/resources/subscriptions/{subscription_id}", json={"enabled": False, "budget": 10})
    assert paused.status_code == 200
    assert paused.json()["enabled"] is False
    assert paused.json()["budget"] == 10

    imported = client.post(
        "/api/resources/documents/import",
        json={
            "lane": "language",
            "provider": "generic_web",
            "url": "https://example.com/open",
            "title": "Open duration text",
            "text": "Effective duration belongs in a licensed corpus.",
            "license_mode": "fulltext_allowed",
        },
    )
    assert imported.status_code == 201

    searched = client.get("/api/resources/search?q=duration")
    assert searched.status_code == 200
    assert searched.json()["count"] == 1

    audit = client.post("/api/resources/audits/run", json={"scope": "content"})
    assert audit.status_code == 200
    assert audit.json()["scope"] == "content"
    assert client.get("/api/resources/scheduler/status").status_code == 200
    assert client.get("/api/resources/settings").json()["consent"]["openai_web_search"] is False
    consent = client.post(
        "/api/privacy/consent",
        json={"provider": "openai", "purpose": "resource_ai_discovery", "granted": True},
    )
    assert consent.status_code == 201
    assert client.get("/api/resources/settings").json()["consent"]["openai_web_search"] is True


def test_resource_candidate_api_is_flag_gated_and_then_works(client: TestClient) -> None:
    gated = client.get("/api/resources/candidates")
    assert gated.status_code == 403

    config_dir = client.app.dependency_overrides[get_repo]().root / ".system" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "features.yaml").write_text(
        "resource_quality_gate: true\nresource_candidate_queue: true\n",
        encoding="utf-8",
    )

    imported = client.post(
        "/api/resources/documents/import",
        json={
            "lane": "language",
            "provider": "generic_web",
            "url": "https://example.com/spanish",
            "title": "Spanish listening practice",
            "text": "Spanish listening practice with CEFR aligned vocabulary and grammar notes.",
            "license_mode": "fulltext_allowed",
            "language": "es",
            "topic": "listening",
        },
    )
    assert imported.status_code == 201
    document_id = imported.json()["document"]["document_id"]

    enqueued = client.post("/api/resources/candidates/enqueue", json={"document_id": document_id})
    assert enqueued.status_code == 201
    candidate_id = enqueued.json()["candidate_id"]

    listed = client.get("/api/resources/candidates")
    assert listed.status_code == 200
    assert listed.json()["candidates"][0]["document_id"] == document_id

    rescored = client.post(f"/api/resources/candidates/{candidate_id}/rescore")
    assert rescored.status_code == 200
    assert "normalized_score" in rescored.json()["score"]
