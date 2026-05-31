from __future__ import annotations

from pathlib import Path

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


def question_payload(**overrides):
    payload = {
        "source_file": "private-pack.pdf",
        "source_page": 12,
        "prompt": "Which duration measure is appropriate when cash flows can change as yields change?",
        "choices": ["A. Macaulay duration", "B. Effective duration", "C. Modified duration"],
        "correct_answer": "B",
        "explanation": "Effective duration accounts for changes in expected cash flows.",
        "topic": "Fixed Income",
        "module": "M10",
        "los": "FI.Duration",
        "error_type": "formula_misuse",
    }
    payload.update(overrides)
    return payload


def test_import_quarantines_incomplete_questions_and_stores_private_records(client: TestClient, repo: LocalRepository) -> None:
    response = client.post(
        "/api/question-banks/import",
        json={
            "source_name": "private-pack",
            "questions": [
                question_payload(),
                question_payload(source_page=13, correct_answer="", explanation=""),
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["verified_count"] == 1
    assert response.json()["quarantined_count"] == 1
    assert (repo.private_root / "question-bank" / "questions.jsonl").exists()
    quarantine = client.get("/api/question-banks/quarantine").json()["questions"]
    assert len(quarantine) == 1
    assert quarantine[0]["verification_status"] == "quarantined"


def test_review_console_can_correct_and_approve_quarantined_record(client: TestClient) -> None:
    imported = client.post(
        "/api/question-banks/import",
        json={"source_name": "private-pack", "questions": [question_payload(correct_answer="", explanation="")]},
    ).json()
    question_id = imported["questions"][0]["question_id"]

    response = client.post(
        f"/api/question-banks/{question_id}/review",
        json={"action": "approve", "corrections": {"correct_answer": "B", "explanation": "Effective duration handles changing cash flows."}},
    )

    assert response.status_code == 200
    assert response.json()["question"]["verification_status"] == "verified"


def test_practice_sessions_only_include_verified_questions(client: TestClient) -> None:
    client.post(
        "/api/question-banks/import",
        json={
            "source_name": "private-pack",
            "questions": [question_payload(), question_payload(source_page=13, correct_answer="")],
        },
    )

    response = client.post("/api/practice-sessions", json={"max_items": 10})

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["verification_status"] == "verified"
    assert "correct_answer" not in items[0]


def test_practice_answer_persists_attempt_and_returns_calibration_remediation(client: TestClient, repo: LocalRepository) -> None:
    client.post("/api/question-banks/import", json={"source_name": "private-pack", "questions": [question_payload()]})
    session = client.post("/api/practice-sessions", json={"max_items": 5}).json()
    question_id = session["items"][0]["question_id"]

    response = client.post(
        f"/api/practice-sessions/{session['session_id']}/answers",
        json={
            "question_id": question_id,
            "answer": "A",
            "confidence": 4,
            "elapsed_seconds": 75,
            "self_explanation": "I used the wrong formula because I ignored the embedded option.",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["is_correct"] is False
    assert payload["calibration_state"] == "severe_miscalibration"
    assert payload["explanation_quality"] == 3
    assert payload["self_explanation_prompt"]
    assert repo.load_attempt_records()
    assert repo.load_stream_events("practice")[-1]["event_type"] == "practice.answered"


def test_practice_answer_rejects_quarantined_question_even_if_session_is_tampered(client: TestClient, repo: LocalRepository) -> None:
    imported = client.post(
        "/api/question-banks/import",
        json={"source_name": "private-pack", "questions": [question_payload(correct_answer="")]},
    ).json()
    question_id = imported["questions"][0]["question_id"]
    repo.append_stream_event(
        "practice",
        "practice.started",
        {"session_id": "tampered", "items": [{"question_id": question_id}]},
    )

    response = client.post(
        "/api/practice-sessions/tampered/answers",
        json={"question_id": question_id, "answer": "B", "confidence": 2, "elapsed_seconds": 30},
    )

    assert response.status_code == 409


def test_practice_session_includes_personalized_mistake_card_drills(client: TestClient) -> None:
    attempt = client.post(
        "/api/attempts",
        json={
            "topic": "Economics",
            "los": "ECO.FX",
            "prompt_or_question": "How should an A/B FX quote be read?",
            "wrong_choice_or_output": "Read it backwards.",
            "correct_resolution": "A/B is units of B required for one unit of A.",
            "error_type": "careless_reading",
            "confidence": 1,
            "time_spent": 20,
            "evidence_refs": ["practice-drill-test"],
        },
    )
    assert attempt.status_code == 200

    session = client.post("/api/practice-sessions", json={"max_items": 5}).json()

    assert session["drills"]
    assert session["drills"][0]["source_kind"] == "mistake_card"


def test_practice_session_composes_formula_concept_and_maintenance_drills(client: TestClient) -> None:
    client.post("/api/question-banks/import", json={"source_name": "private-pack", "questions": [question_payload()]})
    client.post(
        "/api/attempts",
        json={
            "topic": "Fixed Income",
            "los": "FI.Duration",
            "prompt_or_question": "Choose the duration formula.",
            "wrong_choice_or_output": "Macaulay duration.",
            "correct_resolution": "Use effective duration when expected cash flows change.",
            "error_type": "formula_misuse",
            "confidence": 1,
            "time_spent": 30,
            "evidence_refs": ["formula-drill"],
        },
    )
    client.post(
        "/api/attempts",
        json={
            "topic": "Economics",
            "los": "ECO.FX",
            "prompt_or_question": "Read the A/B quote.",
            "wrong_choice_or_output": "Read backwards.",
            "correct_resolution": "A/B is units of B for one unit of A.",
            "error_type": "concept_confusion",
            "confidence": 1,
            "time_spent": 30,
            "evidence_refs": ["concept-drill"],
        },
    )

    session = client.post("/api/practice-sessions", json={"max_items": 10}).json()
    source_kinds = {drill["source_kind"] for drill in session["drills"]}

    assert {"mistake_card", "weak_los", "adjacent_concept", "formula_recall", "concept_discrimination", "maintenance"} <= source_kinds


def test_worked_example_remediation_fades_after_repeated_failure(client: TestClient) -> None:
    client.post("/api/question-banks/import", json={"source_name": "private-pack", "questions": [question_payload()]})
    session = client.post("/api/practice-sessions", json={"max_items": 5}).json()
    question_id = session["items"][0]["question_id"]

    stages = []
    for answer in ("A", "A", "A", "B"):
        response = client.post(
            f"/api/practice-sessions/{session['session_id']}/answers",
            json={"question_id": question_id, "answer": answer, "confidence": 2, "elapsed_seconds": 30},
        )
        stages.append(response.json()["worked_example_stage"])

    assert stages[-2:] == ["full_solution", "hidden_step_completion"]
