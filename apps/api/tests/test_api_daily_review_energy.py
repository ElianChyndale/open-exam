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


def test_daily_review_today_accepts_energy_level_override(client: TestClient) -> None:
    response = client.get("/api/daily-review/today?energy_level=0")

    assert response.status_code == 200
    payload = response.json()
    assert payload["generated_for"]
    assert "当前精力偏低" in payload["markdown_content"] or "精力耗尽" in payload["markdown_content"]


def test_daily_review_today_uses_latest_energy_when_override_missing(client: TestClient) -> None:
    energy = client.post(
        "/api/energy/check-in",
        json={
            "energy_level": 4,
            "mental_clarity": 8,
            "physical_fatigue": 2,
            "motivation": 8,
        },
    )
    assert energy.status_code == 200

    response = client.get("/api/daily-review/today")

    assert response.status_code == 200
    assert "精力充沛" in response.json()["markdown_content"]
