from __future__ import annotations

from pathlib import Path
import base64
import hashlib
import hmac
import json
import time

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


def test_local_mode_is_default_and_does_not_require_supabase(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENEXAM_MODE", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_PUBLISHABLE_KEY", raising=False)
    get_repo.cache_clear()

    repo = get_repo()

    assert isinstance(repo, LocalRepository)
    get_repo.cache_clear()


def test_supabase_repository_requires_remote_configuration(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from app.supabase_repository import SupabaseRepository

    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_PUBLISHABLE_KEY", raising=False)

    with pytest.raises(ValueError, match="SUPABASE_URL"):
        SupabaseRepository(tmp_path)


def test_saas_mode_requires_bearer_jwt_but_health_stays_public(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENEXAM_MODE", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", "publishable-test-key")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "test-secret")
    get_repo.cache_clear()
    try:
        with TestClient(app) as client:
            assert client.get("/api/health").status_code == 200
            assert client.get("/api/profile").status_code == 401
            assert client.get("/api/profile", headers={"Authorization": "Bearer malformed"}).status_code == 401
            assert client.get("/api/profile", headers={"Authorization": f"Bearer {_signed_token('test-secret')}"}).status_code == 200
    finally:
        monkeypatch.delenv("OPENEXAM_MODE", raising=False)
        monkeypatch.delenv("SUPABASE_URL", raising=False)
        monkeypatch.delenv("SUPABASE_PUBLISHABLE_KEY", raising=False)
        monkeypatch.delenv("SUPABASE_JWT_SECRET", raising=False)
        get_repo.cache_clear()


def _signed_token(secret: str) -> str:
    def segment(payload: dict) -> str:
        return base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8")).decode("ascii").rstrip("=")

    header = segment({"alg": "HS256", "typ": "JWT"})
    payload = segment({"sub": "test-user", "aud": "authenticated", "exp": time.time() + 60})
    signature = base64.urlsafe_b64encode(hmac.new(secret.encode("utf-8"), f"{header}.{payload}".encode("ascii"), hashlib.sha256).digest()).decode("ascii").rstrip("=")
    return f"{header}.{payload}.{signature}"


def test_transfer_dry_run_checks_schema_and_detects_duplicates(client: TestClient, repo: LocalRepository) -> None:
    envelope = {
        "schema_version": 1,
        "event_id": "source-profile-event",
        "event_type": "profile.updated",
        "learner_id": "source-user",
        "occurred_at": "2026-05-31T00:00:00+00:00",
        "source_refs": [],
        "payload": {"exam_date": "2026-11-15", "current_phase": "review"},
    }
    bundle = {"schema_version": 1, "streams": {"profile": [envelope]}, "questions": []}

    dry_run = client.post("/api/import", json={"bundle": bundle, "dry_run": True})
    assert dry_run.status_code == 200
    assert dry_run.json()["summary"]["importable_event_count"] == 1
    assert repo.load_stream_events("profile") == []

    imported = client.post("/api/import", json={"bundle": bundle, "dry_run": False})
    assert imported.status_code == 200
    assert imported.json()["summary"]["imported_event_count"] == 1

    duplicate = client.post("/api/import", json={"bundle": bundle, "dry_run": True})
    assert duplicate.json()["summary"]["duplicate_event_count"] == 1

    invalid = client.post("/api/import", json={"bundle": {"schema_version": 999, "streams": {}}, "dry_run": True})
    assert invalid.status_code == 409


def test_export_includes_append_only_streams_and_provenance(client: TestClient, repo: LocalRepository) -> None:
    repo.append_stream_event("coach", "coach.session-retro", {"brief": {"evidence_refs": ["card-1"]}}, source_refs=["card-1"])

    response = client.get("/api/export")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == 1
    assert payload["streams"]["coach"][0]["source_refs"] == ["card-1"]
    assert "questions" in payload


def test_institution_intervention_queue_and_delivery_proof(client: TestClient) -> None:
    created = client.post(
        "/api/institution/interventions",
        json={"learner_id": "learner-1", "reason": "Inactive for seven days", "owner_id": "instructor-1"},
    )
    assert created.status_code == 200
    assert created.json()["intervention"]["status"] == "open"

    queue = client.get("/api/institution/interventions")
    assert queue.status_code == 200
    assert queue.json()["interventions"][0]["learner_id"] == "learner-1"

    proof = client.get("/api/institution/delivery-proof")
    assert proof.status_code == 200
    assert proof.json()["intervention_count"] == 1


def test_supabase_migration_enables_rls_and_private_question_storage() -> None:
    migration = Path("supabase/migrations/202605310001_openexam_core.sql").read_text(encoding="utf-8")

    for table in ("organizations", "organization_memberships", "profiles", "learning_events", "questions", "mock_runs", "coach_artifacts", "graph_overlays", "cohorts", "interventions"):
        assert f"alter table public.{table} enable row level security;" in migration
    assert "private.is_org_member" in migration
    assert "auth.uid()" in migration
    assert "'openexam-private-question-banks'" in migration
    assert "insert into storage.buckets" in migration
