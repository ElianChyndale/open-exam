from __future__ import annotations

from pathlib import Path

import pytest

from app.question_banks import (
    generate_practice_session,
    import_questions,
    load_favorites,
    get_practice_question_display,
    load_practice_attempts,
    load_practice_sessions,
    load_question_notes,
    load_questions,
    load_wrongbook,
    review_question,
    submit_practice_answer,
)
from app.storage import Repository
from app.feature_flags import FeatureFlags


def _verified_question(**overrides: object) -> dict:
    payload: dict[str, object] = {
        "page": 10,
        "prompt": "Which duration measure should be used for a callable bond?",
        "choices": ["A. Macaulay duration", "B. Effective duration", "C. Money duration"],
        "answer": "B",
        "explanation": "Effective duration is used when cash flows can change.",
        "topic": "Fixed Income",
        "module": "M01",
        "los": "FI.1",
        "verification_status": "verified",
    }
    payload.update(overrides)
    return payload


def test_import_report_separates_accepted_rejected_and_duplicates(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    first = import_questions(
        repo,
        "bank.csv",
        [
            _verified_question(),
            {
                "page": 11,
                "prompt": "Broken answer question",
                "choices": ["A. One", "B. Two"],
                "answer": "C",
                "topic": "Fixed Income",
                "module": "M01",
                "los": "FI.2",
            },
        ],
    )
    second = import_questions(repo, "bank.csv", [_verified_question()])

    assert first["accepted_count"] == 1
    assert first["verified_count"] == 1
    assert first["rejected_count"] == 1
    assert "answer must match" in first["rejected"][0]["errors"][0]
    assert second["duplicate_count"] == 1
    assert second["accepted_count"] == 0


def test_published_question_import_is_locked_by_source_identity(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    import_questions(repo, "bank.csv", [_verified_question(page=22)])

    locked = import_questions(
        repo,
        "bank.csv",
        [
            _verified_question(
                page=22,
                prompt="Changed prompt should not replace the published question.",
                answer="A",
                explanation="Changed explanation.",
            )
        ],
    )

    stored = load_questions(repo)
    assert locked["locked_count"] == 1
    assert locked["locked"][0]["changed_fields"] == ["prompt", "answer", "explanation"]
    assert stored[0]["prompt"] == "Which duration measure should be used for a callable bond?"
    assert stored[0]["explanation"] == "Effective duration is used when cash flows can change."


def test_review_locked_question_requires_explicit_override(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    imported = import_questions(repo, "bank.csv", [_verified_question()])
    question_id = imported["questions"][0]["question_id"]

    with pytest.raises(PermissionError, match="Published question fields are locked"):
        review_question(repo, question_id, "approve", {"explanation": "Silently changed."})

    reviewed = review_question(
        repo,
        question_id,
        "override",
        {"explanation": "Admin-approved correction.", "allow_locked_update": True},
    )

    assert reviewed["verification_status"] == "verified"
    assert reviewed["explanation"] == "Admin-approved correction."
    assert reviewed["override_reviewed_at"]


def test_quarantined_question_can_be_completed_during_review(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    imported = import_questions(
        repo,
        "bank.csv",
        [
            {
                "page": 33,
                "prompt": "Incomplete OCR question",
                "topic": "Fixed Income",
            }
        ],
    )
    question_id = imported["questions"][0]["question_id"]

    reviewed = review_question(
        repo,
        question_id,
        "approve",
        {
            "choices": ["A", "B", "C"],
            "answer": "A",
            "explanation": "A is correct.",
            "module": "M01",
            "los": "FI.3",
        },
    )

    assert reviewed["verification_status"] == "verified"
    assert reviewed["chapter"] == "M01"
    assert reviewed["knowledge_tags"] == ["FI.3"]


def test_practice_generation_is_seeded_and_reference_only(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    import_questions(
        repo,
        "bank.csv",
        [
            _verified_question(page=1, los="FI.1", knowledge_tags=["duration", "callable"]),
            _verified_question(page=2, los="FI.2", knowledge_tags=["duration", "putable"]),
            _verified_question(page=3, los="FI.3", knowledge_tags=["credit", "spread"]),
        ],
    )
    before = load_questions(repo)

    first = generate_practice_session(
        repo,
        {
            "topic": "Fixed Income",
            "count": 2,
            "tags": ["duration"],
            "tag_mode": "or",
            "seed": 7,
        },
    )
    second = generate_practice_session(
        repo,
        {
            "topic": "Fixed Income",
            "count": 2,
            "tags": ["duration"],
            "tag_mode": "or",
            "seed": 7,
        },
    )

    assert first["question_ids"] == second["question_ids"]
    assert first["question_count"] == 2
    assert "prompt" not in first["question_refs"][0]
    assert "answer" not in first["question_refs"][0]
    assert load_questions(repo) == before
    assert len(load_practice_sessions(repo)) == 1


def test_practice_tag_and_filter_narrows_results(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    import_questions(
        repo,
        "bank.csv",
        [
            _verified_question(page=1, los="FI.1", knowledge_tags=["duration", "callable"]),
            _verified_question(page=2, los="FI.2", knowledge_tags=["duration", "putable"]),
            _verified_question(page=3, los="FI.3", knowledge_tags=["credit", "callable"]),
        ],
    )

    narrowed = generate_practice_session(
        repo,
        {
            "topic": "Fixed Income",
            "count": 10,
            "tags": ["duration", "callable"],
            "tag_mode": "and",
            "seed": 0,
        },
    )
    broadened = generate_practice_session(
        repo,
        {
            "topic": "Fixed Income",
            "count": 10,
            "tags": ["duration", "callable"],
            "tag_mode": "or",
            "seed": 0,
        },
    )

    assert narrowed["question_count"] == 1
    assert broadened["question_count"] == 3
    assert set(narrowed["question_ids"]).issubset(set(broadened["question_ids"]))


def test_answer_submission_updates_wrongbook_notes_and_favorites_idempotently(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    import_questions(repo, "bank.csv", [_verified_question(page=44)])
    session = generate_practice_session(repo, {"topic": "Fixed Income", "count": 1, "seed": 0})
    question_id = session["question_ids"][0]

    first_wrong = submit_practice_answer(
        repo,
        {
            "session_id": session["session_id"],
            "question_id": question_id,
            "selected_answer": "A",
            "time_spent": 30,
            "confidence": 3,
            "note": "I confused callable duration.",
            "favorite": True,
        },
    )
    second_wrong = submit_practice_answer(
        repo,
        {
            "session_id": session["session_id"],
            "question_id": question_id,
            "selected_answer": "A",
            "time_spent": 25,
            "confidence": 2,
        },
    )
    correct_retry = submit_practice_answer(
        repo,
        {
            "session_id": session["session_id"],
            "question_id": question_id,
            "selected_answer": "B",
            "time_spent": 20,
            "confidence": 3,
        },
    )

    wrongbook = load_wrongbook(repo)
    assert len(wrongbook) == 1
    assert wrongbook[question_id]["wrong_count"] == 2
    assert wrongbook[question_id]["correct_retry_count"] == 1
    assert wrongbook[question_id]["last_is_correct"] is True
    assert wrongbook[question_id]["priority"] < second_wrong["wrongbook_record"]["priority"]
    assert len(load_practice_attempts(repo)) == 3
    assert first_wrong["attempt"]["is_correct"] is False
    assert correct_retry["attempt"]["is_correct"] is True
    assert load_question_notes(repo)[question_id][0]["note"] == "I confused callable duration."
    assert load_favorites(repo)[question_id]["favorite"] is True


def test_core_practice_works_when_question_bank_extensions_are_disabled(tmp_path: Path) -> None:
    config = tmp_path / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "question_bank_recommendations_enabled: false\n"
        "question_bank_adaptive_practice_enabled: false\n",
        encoding="utf-8",
    )
    repo = Repository(tmp_path)
    flags = FeatureFlags.load(tmp_path)
    assert flags.enabled("question_bank_recommendations_enabled") is False
    assert flags.enabled("question_bank_adaptive_practice_enabled") is False

    import_questions(repo, "bank.csv", [_verified_question(page=55)])
    session = generate_practice_session(repo, {"topic": "Fixed Income", "count": 1, "seed": 0})
    answered = submit_practice_answer(
        repo,
        {
            "session_id": session["session_id"],
            "question_id": session["question_ids"][0],
            "selected_answer": "B",
        },
    )

    assert session["question_count"] == 1
    assert answered["attempt"]["is_correct"] is True
    assert load_questions(repo)[0]["answer"] == "B"


def test_practice_question_display_hides_answers_and_reflects_state(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    import_questions(repo, "bank.csv", [_verified_question(page=66)])
    session = generate_practice_session(repo, {"topic": "Fixed Income", "count": 1, "seed": 0})
    question_id = session["question_ids"][0]

    before = get_practice_question_display(repo, session["session_id"], question_id)
    submit_practice_answer(
        repo,
        {
            "session_id": session["session_id"],
            "question_id": question_id,
            "selected_answer": "B",
            "note": "Display state should show this note count.",
            "favorite": True,
        },
    )
    after = get_practice_question_display(repo, session["session_id"], question_id)

    forbidden = {"answer", "correct_answer", "explanation", "rationale"}
    assert forbidden.isdisjoint(before)
    assert forbidden.isdisjoint(after)
    assert before["state"] == "unanswered"
    assert before["prompt"]
    assert before["choices"]
    assert after["state"] == "answered"
    assert after["note_count"] == 1
    assert after["favorite"] is True
    assert after["latest_attempt"]["selected_answer"] == "B"
