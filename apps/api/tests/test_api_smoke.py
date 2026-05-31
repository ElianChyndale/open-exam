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


def test_local_development_ports_are_allowed_by_cors(client: TestClient) -> None:
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://127.0.0.1:3001",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:3001"


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
        "/api/daily-review/today",
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


def test_daily_review_api_completes_snapshot_idempotently(client: TestClient, tmp_path: Path) -> None:
    attempt = client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "Which duration measure fits callable bonds?",
            "wrong_choice_or_output": "Macaulay duration",
            "correct_resolution": "Use effective duration when cash flows can change.",
            "error_type": "concept_confusion",
            "confidence": 1,
            "time_spent": 60,
            "evidence_refs": ["api-daily-review"],
            "is_correct": False,
        },
    )
    assert attempt.status_code == 200

    review = client.get("/api/daily-review/today")
    assert review.status_code == 200
    review_id = review.json()["review_id"]
    assert review_id.startswith("daily-review-")

    first = client.post(f"/api/daily-review/{review_id}/complete")
    second = client.post(f"/api/daily-review/{review_id}/complete")
    assert first.status_code == 200
    assert first.json()["completed"] is True
    assert first.json()["newly_reviewed_items"] == 1
    assert second.status_code == 200
    assert second.json() == {
        "review_id": review_id,
        "completed": False,
        "newly_reviewed_items": 0,
    }

    card_path = tmp_path / ".system" / "memory" / "question-errors" / f"{attempt.json()['card_id']}.md"
    assert "review_status: Reviewed once" in card_path.read_text(encoding="utf-8")


def test_batch_import_records_correct_attempts_without_creating_cards(client: TestClient, tmp_path: Path) -> None:
    response = client.post(
        "/api/attempts/batch-import",
        json=[
            {
                "topic": "Equity",
                "los": "EQ.1",
                "prompt_or_question": "Correct import",
                "correct_resolution": "Correct.",
                "confidence": 3,
                "is_correct": True,
            },
            {
                "topic": "Equity",
                "los": "EQ.2",
                "prompt_or_question": "Wrong import",
                "wrong_choice_or_output": "A",
                "correct_resolution": "B",
                "confidence": 2,
                "is_correct": False,
            },
        ],
    )

    assert response.status_code == 200
    assert response.json()["attempt_count"] == 2
    assert response.json()["mistake_count"] == 1
    assert len(list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))) == 1
    attempts = (tmp_path / ".system" / "events" / "attempt" / "attempt-events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(attempts) == 2


def test_card_review_and_fix_rule_feedback_persist_spacing_metadata(client: TestClient, tmp_path: Path) -> None:
    attempt = client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Convexity",
            "prompt_or_question": "When does convexity matter?",
            "wrong_choice_or_output": "Never",
            "correct_resolution": "Include convexity for larger yield changes.",
            "error_type": "formula_misuse",
            "confidence": 1,
            "time_spent": 50,
            "is_correct": False,
        },
    ).json()

    reviewed = client.post(
        f"/api/cards/{attempt['card_id']}/review",
        json={"outcome": "struggled", "confidence_after": 2},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["confidence_delta"] == 1

    feedback = client.post(
        f"/api/cards/{attempt['card_id']}/fix-rule-feedback",
        json={"helpful": True, "note": "The yield-change trigger is actionable."},
    )
    assert feedback.status_code == 200

    card_path = tmp_path / ".system" / "memory" / "question-errors" / f"{attempt['card_id']}.md"
    card_text = card_path.read_text(encoding="utf-8")
    assert "last_reviewed_at:" in card_text
    assert "spacing_reasoning:" in card_text
    feedback_log = tmp_path / ".system" / "events" / "review" / "review-events.jsonl"
    assert "card.fix_rule.feedback" in feedback_log.read_text(encoding="utf-8")


def test_study_plan_uses_latest_saved_energy_and_returns_interleaving_mix(client: TestClient) -> None:
    energy = client.post(
        "/api/energy/check-in",
        json={
            "energy_level": 0,
            "mental_clarity": 4,
            "physical_fatigue": 8,
            "motivation": 4,
        },
    )
    assert energy.status_code == 200

    response = client.get("/api/study-plan/today")
    assert response.status_code == 200
    assert response.json()["energy_level"] == 0
    assert "interleaving_composition" in response.json()


def test_dashboard_uses_attempt_correctness_and_calendar_keeps_day_keys(client: TestClient, tmp_path: Path) -> None:
    from app.storage import Repository
    from app.workflows import record_question_attempt

    repo = Repository(tmp_path)
    record_question_attempt(
        repo,
        {
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "Wrong duration attempt",
            "wrong_choice_or_output": "A",
            "correct_resolution": "B",
            "confidence": 3,
            "is_correct": False,
            "created_at": "2026-05-20T10:00:00+00:00",
        },
    )
    record_question_attempt(
        repo,
        {
            "topic": "Equity",
            "los": "EQ.DDM",
            "prompt_or_question": "Correct DDM attempt",
            "correct_resolution": "Correct.",
            "confidence": 3,
            "is_correct": True,
            "created_at": "2026-05-21T10:00:00+00:00",
        },
    )

    summary = client.get("/api/dashboard/summary")
    calendar = client.get("/api/dashboard/calendar?month=2026-05")
    effectiveness = client.get("/api/dashboard/effectiveness?days=30")

    assert summary.status_code == 200
    assert summary.json()["total_attempts"] == 2
    assert summary.json()["accuracy"] == 0.5
    assert calendar.status_code == 200
    assert calendar.json()["daily_errors"]["2026-05-20"] == 1
    assert effectiveness.status_code == 200
    assert effectiveness.json()["interleaving_accuracy"] == 1.0


def test_private_question_import_quarantines_incomplete_records_until_reviewed(client: TestClient) -> None:
    imported = client.post(
        "/api/question-banks/import",
        json={
            "source_file": "private-bank.pdf",
            "questions": [
                {
                    "page": 12,
                    "prompt": "Incomplete OCR question",
                    "topic": "Fixed Income",
                },
                {
                    "page": 13,
                    "prompt": "Verified question",
                    "choices": ["A", "B", "C"],
                    "answer": "B",
                    "explanation": "B is correct.",
                    "topic": "Fixed Income",
                    "module": "M01",
                    "los": "FI.1",
                    "verification_status": "verified",
                },
            ],
        },
    )

    assert imported.status_code == 200
    assert imported.json()["verified_count"] == 1
    assert imported.json()["quarantined_count"] == 1

    quarantine = client.get("/api/question-banks/quarantine")
    assert quarantine.status_code == 200
    question = quarantine.json()["questions"][0]
    assert question["verification_status"] == "quarantined"

    reviewed = client.post(
        f"/api/question-banks/{question['question_id']}/review",
        json={
            "action": "approve",
            "patch": {
                "choices": ["A", "B", "C"],
                "answer": "A",
                "explanation": "A is correct.",
                "module": "M01",
                "los": "FI.1",
            },
        },
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["question"]["verification_status"] == "verified"
    assert client.get("/api/question-banks/quarantine").json()["questions"] == []


def test_calendar_settings_and_weekly_markdown_report_are_exportable(client: TestClient) -> None:
    setting = client.put("/api/dashboard/calendar/settings", json={"exam_date": "2026-11-15"})
    assert setting.status_code == 200
    assert setting.json()["exam_date"] == "2026-11-15"

    calendar = client.get("/api/dashboard/calendar")
    assert calendar.status_code == 200
    assert calendar.json()["exam_date"] == "2026-11-15"

    report = client.get("/api/export/weekly-report.md")
    assert report.status_code == 200
    assert report.headers["content-type"].startswith("text/markdown")
    assert "# OpenExam Weekly Learner Report" in report.text


def test_active_profile_api_persists_and_drives_mastery_topics(client: TestClient) -> None:
    changed = client.put("/api/profiles/active", json={"profile_name": "frm-p1"})
    assert changed.status_code == 200
    assert changed.json()["profile"]["short_name"] == "frm-p1"

    active = client.get("/api/profiles/active")
    mastery = client.get("/api/dashboard/mastery")
    assert active.status_code == 200
    assert active.json()["profile"]["short_name"] == "frm-p1"
    assert [topic["topic"] for topic in mastery.json()["topics"]] == [
        "Foundations of Risk Management",
        "Quantitative Analysis",
        "Financial Markets and Products",
        "Valuation and Risk Models",
    ]


def test_explicit_transfer_supports_duplicate_safe_dry_run(client: TestClient) -> None:
    exported = client.get("/api/export")
    assert exported.status_code == 200
    assert exported.json()["schema_version"] == 1

    dry_run = client.post("/api/import", json={"dry_run": True, "data": exported.json()})
    assert dry_run.status_code == 200
    assert dry_run.json()["dry_run"] is True
    assert "would_import" in dry_run.json()
