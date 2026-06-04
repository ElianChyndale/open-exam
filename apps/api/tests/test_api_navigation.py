from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_navigation_features(repo.root)
    _seed_goal(repo.root)
    _seed_attempt_event(repo.root, wrong_phrase="UNIQUE_WRONG_NAV_COCKPIT")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_navigation_summary_tiers_primary_and_advanced_surfaces(client: TestClient) -> None:
    response = client.get("/api/navigation/summary")

    assert response.status_code == 200
    payload = response.json()
    surfaces = payload["surfaces"]
    by_route = {surface["route"]: surface for surface in surfaces}

    assert by_route["/review"]["tier"] == "primary"
    assert by_route["/review"]["visible_on_main"] is True
    assert by_route["/review/study-planner"]["product_role"] == "plan"
    assert by_route["/review/data"]["tier"] == "advanced"
    assert by_route["/review/interop"]["tier"] == "advanced"
    assert by_route["/review/data"]["visible_on_main"] is False
    assert by_route["/review/interop"]["more_group"] == "System & Portability"
    primary_routes = {surface["route"] for surface in surfaces if surface["visible_on_main"]}
    assert primary_routes == {"/review", "/review/focus", "/review/study-planner", "/review/tutor"}
    assert not primary_routes.intersection({"/review/data", "/review/interop", "/review/knowledge-map", "/review/search", "/review/tools"})
    assert by_route["/review/mission-control#route-registry"]["tier"] == "advanced"
    assert by_route["/review/mission-control#route-registry"]["visible_on_main"] is False
    assert payload["main_visible_count"] <= 4


def test_tools_grouping_contains_advanced_routes_without_wrong_answer_fields(client: TestClient) -> None:
    response = client.get("/api/navigation/tools")

    assert response.status_code == 200
    payload = response.json()
    grouped = {group["group_id"]: group for group in payload["groups"]}
    portability_routes = {item["route"] for item in grouped["system_portability"]["items"]}
    intelligence_routes = {item["route"] for item in grouped["intelligence"]["items"]}

    assert "/review/data" in portability_routes
    assert "/review/interop" in portability_routes
    assert "/review/knowledge-map" in intelligence_routes
    assert "/review/search" in intelligence_routes
    assert "UNIQUE_WRONG_NAV_COCKPIT" not in json.dumps(payload, ensure_ascii=False)
    assert "wrong_choice_or_output" not in json.dumps(payload, ensure_ascii=False)


def test_cockpit_summary_uses_active_goal_for_next_action_and_stays_safe(client: TestClient) -> None:
    response = client.get("/api/navigation/cockpit?profile_id=p1")

    assert response.status_code == 200
    payload = response.json()

    assert payload["active_goal"]["title"] == "CFA Premium Cockpit"
    assert payload["primary_action"]["label"]
    assert payload["primary_action"]["href"].startswith("/")
    assert len(payload["supporting_actions"]) <= 4
    assert all(action["href"] != "/review/data" for action in payload["supporting_actions"])
    assert all(action["href"] != "/review/interop" for action in payload["supporting_actions"])
    assert len(payload["today_plan_preview"]) <= 3
    assert "UNIQUE_WRONG_NAV_COCKPIT" not in json.dumps(payload, ensure_ascii=False)
    assert "wrong_choice_or_output" not in json.dumps(payload, ensure_ascii=False)


def _enable_navigation_features(root: Path) -> None:
    config_root = root / ".system" / "config"
    config_root.mkdir(parents=True, exist_ok=True)
    flags = {
        name: True
        for name in [
            "premium_cockpit_enabled",
            "progressive_disclosure_enabled",
            "advanced_tools_hub_enabled",
        "simplified_mission_control_enabled",
        "premium_visual_system_enabled",
        "goals_enabled",
        "onboarding_enabled",
        "study_planner_enabled",
        "adaptive_session_orchestrator_enabled",
        "energy_aware_planning_enabled",
        "learning_analytics_enabled",
        "knowledge_graph_enabled",
        "global_search_enabled",
            "data_governance_enabled",
            "interop_enabled",
        ]
    }
    (config_root / "features.yaml").write_text(
        "\n".join(f"{name}: {str(enabled).lower()}" for name, enabled in flags.items()) + "\n",
        encoding="utf-8",
    )


def _seed_goal(root: Path) -> None:
    goal_root = root / ".system" / "memory" / "goals" / "profiles"
    goal_root.mkdir(parents=True, exist_ok=True)
    (goal_root / "goal-premium.json").write_text(
        json.dumps(
            {
                "goal_id": "goal-premium",
                "profile_id": "p1",
                "title": "CFA Premium Cockpit",
                "goal_type": "exam",
                "target_exam": "CFA Level I",
                "weekly_minutes": 420,
                "default_energy_mode": "normal",
                "enabled_modules": ["Review Lab", "Tutor", "Study Planner"],
                "preferred_review_modes": ["recall"],
                "status": "active",
                "onboarding_status": {"readiness_score": 0.55, "readiness_status": "ready_for_first_plan"},
                "pack_id": "cfa_finance",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _seed_attempt_event(root: Path, *, wrong_phrase: str) -> None:
    event_root = root / ".system" / "events" / "attempt"
    event_root.mkdir(parents=True, exist_ok=True)
    (event_root / "attempt-events.jsonl").write_text(
        json.dumps(
            {
                "event_id": "attempt-nav-1",
                "profile_id": "p1",
                "topic": "Corporate Issuers",
                "wrong_choice_or_output": wrong_phrase,
                "correct_resolution": "Use after-tax debt cost in WACC.",
                "is_correct": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )
