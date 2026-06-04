from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app
from study_science.focus_session import FocusStep, _balance_step_sequence
from test_api_study_planner import (
    _enable_planner_features,
    _seed_cross_system_signals,
    _write_daily_review_snapshot,
)


FOCUS_FLAGS = [
    "focus_session_enabled",
    "unified_study_flow_enabled",
    "focus_embedded_review_enabled",
    "focus_embedded_formula_enabled",
    "focus_embedded_language_enabled",
    "focus_embedded_assessment_enabled",
    "focus_tutor_hint_enabled",
    "focus_polish_enabled",
    "focus_local_reveal_contract_enabled",
    "validation_resource_cleanup_enabled",
    "playwright_state_isolation_enabled",
]


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_focus_features(repo.root)
    _write_daily_review_snapshot(repo.root, review_id="daily-review-focus")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_focus_start_uses_today_plan_and_embeds_safe_adapters(client: TestClient) -> None:
    wrong_phrase = "UNIQUE_WRONG_FOCUS_SESSION"
    _seed_cross_system_signals(client, wrong_phrase=wrong_phrase)
    generated = client.post(
        "/api/study-planner/generate",
        json={
            "profile_id": "default",
            "energy_mode": "high",
            "available_minutes": 120,
            "goal": "WACC lexical transfer",
        },
    )
    assert generated.status_code == 200

    started = client.post("/api/focus/start", json={"profile_id": "default"})

    assert started.status_code == 200
    session = started.json()
    assert session["status"] == "active"
    assert session["plan_id"] == generated.json()["plan_id"]
    assert session["current_step_id"]
    assert session["total_target_minutes"] <= 120

    step_types = [step["step_type"] for step in session["steps"]]
    assert "review_lab" in step_types
    assert "formula_lab" in step_types
    assert "lexical_review" in step_types
    assert "reflection" in step_types

    review = _step(session, "review_lab")
    assert review["launch_route"] == "/review/lab"
    assert review["embedded_payload"]["adapter"] == "review_lab"
    assert review["embedded_payload"]["prompt"]
    assert review["correct_only_warning"]

    formula = _step(session, "formula_lab")
    assert formula["embedded_payload"]["adapter"] == "formula_lab"
    assert formula["embedded_payload"]["prompt"]
    assert formula["source_refs"]

    lexical = _step(session, "lexical_review")
    assert lexical["embedded_payload"]["adapter"] == "lexical_review"
    assert lexical["linked_lexical_ids"]

    payload_text = json.dumps(session, ensure_ascii=False)
    assert "wrong_choice_or_output" not in payload_text
    assert "wrong_formula" not in payload_text
    assert "wrong_reasoning" not in payload_text
    assert wrong_phrase not in payload_text


def test_focus_reveal_payload_uses_explicit_local_only_contract(client: TestClient) -> None:
    _seed_cross_system_signals(client, wrong_phrase="UNIQUE_WRONG_FOCUS_REVEAL_CONTRACT")
    generated = client.post(
        "/api/study-planner/generate",
        json={"profile_id": "default", "energy_mode": "high", "available_minutes": 90},
    )
    assert generated.status_code == 200

    started = client.post("/api/focus/start", json={"profile_id": "default"})

    assert started.status_code == 200
    session = started.json()
    reveal_steps = [
        _step(session, "review_lab"),
        _step(session, "formula_lab"),
        _step(session, "lexical_review"),
    ]
    for step in reveal_steps:
        payload = step["embedded_payload"]
        assert payload["local_reveal_available"] is True
        assert payload["answer_hidden_until_reveal"] is True
        assert "correct_answer" not in payload
        assert "correct_reasoning" not in payload
        assert payload["reveal_payload"]["correct_answer"]
        assert payload["reveal_payload"]["correct_reasoning"]
        body = json.dumps(payload["reveal_payload"], ensure_ascii=False)
        assert "wrong_choice_or_output" not in body
        assert "wrong_formula" not in body
        assert "wrong_reasoning" not in body


def test_focus_step_balancer_avoids_three_same_type_steps_in_a_row() -> None:
    steps = [
        _focus_step("review-1", "review_lab"),
        _focus_step("review-2", "review_lab"),
        _focus_step("review-3", "review_lab"),
        _focus_step("formula-1", "formula_lab"),
        _focus_step("lexical-1", "lexical_review"),
    ]

    balanced = _balance_step_sequence(steps)

    assert {step.step_id for step in balanced} == {step.step_id for step in steps}
    for index in range(len(balanced) - 2):
        assert len({balanced[index].step_type, balanced[index + 1].step_type, balanced[index + 2].step_type}) > 1


def test_focus_public_payload_redacts_local_paths_and_nested_forbidden_values() -> None:
    wrong_phrase = "UNIQUE_WRONG_FOCUS_PUBLIC_BOUNDARY"
    step = FocusStep(
        step_id="focus-public-boundary",
        focus_id="focus-boundary",
        step_type="review_lab",
        title="Safe public focus payload",
        description="Boundary test",
        target_minutes=8,
        embedded_payload={
            "prompt": "Recall WACC before reveal.",
            "source_refs": [r"C:\Users\Administrator\private\wacc-note.md#L7"],
            "wrong_choice_or_output": wrong_phrase,
            "notes": f"Nested diagnostic value must be scrubbed: {wrong_phrase}",
            "nested": {"selected_answer": wrong_phrase},
        },
        source_refs=[r"D:\private\sources\wacc.pdf#page=1"],
        correct_only_warning="Recall first.",
    )

    payload = step.as_dict()
    body = json.dumps(payload, ensure_ascii=False)

    assert "[local-path]" in body
    assert "C:\\Users\\Administrator" not in body
    assert "D:\\private" not in body
    assert "wacc-note.md" not in body
    assert "wrong_choice_or_output" not in body
    assert "selected_answer" not in body
    assert wrong_phrase not in body


def test_focus_keeps_draft_assets_as_confirmation_work_not_review_content(client: TestClient) -> None:
    imported = client.post(
        "/api/review-lab/sources/import-text",
        json={
            "profile_id": "default",
            "title": "Draft Focus Asset Note",
            "text": "\n".join(
                [
                    "LOS: FOCUS-DRAFT",
                    "WACC = w_d r_d (1 - t) + w_e r_e.",
                    "Use WACC when valuing a firm with a target capital structure.",
                ]
            ),
            "source_type": "text_note",
        },
    )
    assert imported.status_code == 200
    extracted = client.post(f"/api/review-lab/sources/{imported.json()['source']['source_id']}/extract-assets")
    assert extracted.status_code == 200
    draft_ids = {asset["asset_id"] for asset in extracted.json()["assets"]}
    assert draft_ids

    _seed_cross_system_signals(client, wrong_phrase="UNIQUE_WRONG_FOCUS_DRAFT")
    assert client.post(
        "/api/study-planner/generate",
        json={"profile_id": "default", "energy_mode": "normal", "available_minutes": 90},
    ).status_code == 200

    started = client.post("/api/focus/start", json={"profile_id": "default"})

    assert started.status_code == 200
    session = started.json()
    review_like = [step for step in session["steps"] if step["step_type"] in {"review_lab", "formula_lab", "lexical_review"}]
    assert review_like
    for step in review_like:
        linked_ids = set(step["linked_asset_ids"])
        payload_ids = set(json.dumps(step["embedded_payload"], ensure_ascii=False).split())
        assert not (draft_ids & linked_ids)
        assert not (draft_ids & payload_ids)

    confirmation_steps = [
        step
        for step in session["steps"]
        if step["step_type"] in {"coverage_confirmation", "resource_confirmation"}
    ]
    assert confirmation_steps
    assert any(draft_ids & set(step["linked_asset_ids"]) for step in confirmation_steps)
    assert any(step["blocked_reason"] or "confirm" in step["description"].lower() for step in confirmation_steps)


def test_focus_safe_fallback_and_step_lifecycle(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_focus_features(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        with TestClient(app) as fresh_client:
            started = fresh_client.post("/api/focus/start", json={"profile_id": "fresh"})
            assert started.status_code == 200
            session = started.json()
            assert session["profile_id"] == "fresh"
            assert session["status"] == "active"
            assert session["steps"]
            assert "reflection" in {step["step_type"] for step in session["steps"]}
            assert all(
                step["blocked_reason"] or step["embedded_payload"].get("prompt") or step["embedded_payload"].get("next_action")
                for step in session["steps"]
            )

            step_id = session["current_step_id"]
            assert step_id
            started_step = fresh_client.post(f"/api/focus/{session['focus_id']}/steps/{step_id}/start")
            assert started_step.status_code == 200
            assert _find_step(started_step.json(), step_id)["status"] == "in_progress"

            completed = fresh_client.post(
                f"/api/focus/{session['focus_id']}/steps/{step_id}/complete",
                json={"outcome": "recalled", "actual_minutes": 5, "notes": "Completed safely"},
            )
            assert completed.status_code == 200
            completed_session = completed.json()
            assert _find_step(completed_session, step_id)["status"] == "completed"
            assert completed_session["summary"]["completed_steps"] >= 1
            current_after_complete = completed_session["current_step_id"]

            completed_again = fresh_client.post(
                f"/api/focus/{session['focus_id']}/steps/{step_id}/complete",
                json={"outcome": "partial", "actual_minutes": 7, "notes": "Duplicate click"},
            )
            assert completed_again.status_code == 200
            repeated = completed_again.json()
            assert _find_step(repeated, step_id)["status"] == "completed"
            assert repeated["summary"]["completed_steps"] == completed_session["summary"]["completed_steps"]
            assert repeated["current_step_id"] == current_after_complete

            next_step_id = completed_session["current_step_id"]
            if next_step_id:
                skipped = fresh_client.post(
                    f"/api/focus/{session['focus_id']}/steps/{next_step_id}/skip",
                    json={"reason": "Defer until after source confirmation"},
                )
                assert skipped.status_code == 200
                assert _find_step(skipped.json(), next_step_id)["status"] == "skipped"
                skipped_again = fresh_client.post(
                    f"/api/focus/{session['focus_id']}/steps/{next_step_id}/skip",
                    json={"reason": "Duplicate skip"},
                )
                assert skipped_again.status_code == 200
                assert _find_step(skipped_again.json(), next_step_id)["status"] == "skipped"
                assert skipped_again.json()["summary"]["skipped_steps"] == skipped.json()["summary"]["skipped_steps"]

            finished = fresh_client.post(f"/api/focus/{session['focus_id']}/complete")
            assert finished.status_code == 200
            assert finished.json()["status"] == "completed"
            assert finished.json()["completed_at"]
            assert finished.json()["summary"]["completed_steps"] >= 1
    finally:
        app.dependency_overrides.clear()


def test_focus_current_get_and_abandon_contract(client: TestClient) -> None:
    started = client.post("/api/focus/start", json={"profile_id": "default"})
    assert started.status_code == 200
    focus_id = started.json()["focus_id"]

    current = client.get("/api/focus/current?profile_id=default")
    assert current.status_code == 200
    assert current.json()["focus_session"]["focus_id"] == focus_id

    fetched = client.get(f"/api/focus/{focus_id}")
    assert fetched.status_code == 200
    assert fetched.json()["focus_id"] == focus_id

    abandoned = client.post(f"/api/focus/{focus_id}/abandon", json={"reason": "manual reset"})
    assert abandoned.status_code == 200
    assert abandoned.json()["status"] == "abandoned"
    assert "manual reset" in abandoned.json()["summary"]["abandon_reason"]

    current_after = client.get("/api/focus/current?profile_id=default")
    assert current_after.status_code == 200
    assert current_after.json()["focus_session"] is None


def test_focus_feature_flags_gate_api(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_focus_features(repo.root)
    config_path = repo.root / ".system" / "config" / "features.yaml"
    config_path.write_text(config_path.read_text(encoding="utf-8") + "focus_session_enabled: false\n", encoding="utf-8")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        with TestClient(app) as gated_client:
            response = gated_client.post("/api/focus/start", json={"profile_id": "default"})
            assert response.status_code == 403
    finally:
        app.dependency_overrides.clear()


def _enable_focus_features(repo_root: Path) -> None:
    _enable_planner_features(repo_root)
    config_path = repo_root / ".system" / "config" / "features.yaml"
    existing = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        existing + "".join(f"{flag}: true\n" for flag in FOCUS_FLAGS),
        encoding="utf-8",
    )


def _focus_step(step_id: str, step_type: str) -> FocusStep:
    return FocusStep(
        step_id=step_id,
        focus_id="focus-balance",
        step_type=step_type,  # type: ignore[arg-type]
        title=step_id,
        description="Balance test",
        target_minutes=5,
    )


def _step(session: dict[str, object], step_type: str) -> dict[str, object]:
    return next(step for step in session["steps"] if step["step_type"] == step_type)  # type: ignore[index,return-value]


def _find_step(session: dict[str, object], step_id: str) -> dict[str, object]:
    return next(step for step in session["steps"] if step["step_id"] == step_id)  # type: ignore[index,return-value]
