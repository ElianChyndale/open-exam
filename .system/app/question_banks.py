"""Private question-bank import, quarantine, and review storage."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from app.models import stable_id
from app.storage import Repository

REQUIRED_VERIFIED_FIELDS = ("prompt", "choices", "answer", "explanation", "topic", "module", "los")


def _store_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "questions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_questions(repo: Repository) -> list[dict]:
    path = _store_path(repo)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_questions(repo: Repository, questions: list[dict]) -> None:
    _store_path(repo).write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_complete(question: dict) -> bool:
    return all(question.get(field) for field in REQUIRED_VERIFIED_FIELDS)


def _append_event(repo: Repository, event_type: str, question: dict) -> None:
    repo.append_jsonl_event(
        "practice",
        {
            "schema_version": 1,
            "event_id": stable_id("practice-event", event_type, question["question_id"], datetime.now(UTC).isoformat()),
            "event_type": event_type,
            "learner_id": "local",
            "occurred_at": datetime.now(UTC).isoformat(),
            "source_refs": [question.get("source_file", "")],
            "payload": question,
        },
    )


def import_questions(repo: Repository, source_file: str, questions: list[dict]) -> dict:
    stored = load_questions(repo)
    existing_ids = {question["question_id"] for question in stored}
    imported: list[dict] = []
    for raw in questions:
        question = {
            **raw,
            "source_file": source_file,
            "question_id": stable_id("private-question", source_file, str(raw.get("page", "")), str(raw.get("prompt", ""))),
            "imported_at": datetime.now(UTC).isoformat(),
        }
        if question["question_id"] in existing_ids:
            continue
        requested_status = question.get("verification_status", "")
        question["verification_status"] = "verified" if requested_status == "verified" and _is_complete(question) else "quarantined"
        stored.append(question)
        imported.append(question)
        existing_ids.add(question["question_id"])
        _append_event(repo, "question_bank.imported", question)
    _save_questions(repo, stored)
    return {
        "imported_count": len(imported),
        "verified_count": sum(1 for question in imported if question["verification_status"] == "verified"),
        "quarantined_count": sum(1 for question in imported if question["verification_status"] == "quarantined"),
        "questions": imported,
    }


def review_question(repo: Repository, question_id: str, action: str, patch: dict | None = None) -> dict:
    questions = load_questions(repo)
    for question in questions:
        if question["question_id"] != question_id:
            continue
        question.update(patch or {})
        if action == "reject":
            question["verification_status"] = "rejected"
        elif action == "approve" and _is_complete(question):
            question["verification_status"] = "verified"
        else:
            question["verification_status"] = "quarantined"
        question["reviewed_at"] = datetime.now(UTC).isoformat()
        _save_questions(repo, questions)
        _append_event(repo, "question_bank.reviewed", question)
        return question
    raise FileNotFoundError(f"Question not found: {question_id}")


def load_verified_questions(repo: Repository) -> list[dict]:
    """Return gradeable records only. Quarantined imports never cross this gate."""
    return [question for question in load_questions(repo) if question.get("verification_status") == "verified"]
