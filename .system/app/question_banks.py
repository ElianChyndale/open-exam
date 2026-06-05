"""Private question-bank import, quarantine, and review storage."""

from __future__ import annotations

import json
import random
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.storage import Repository

REQUIRED_VERIFIED_FIELDS = (
    "exam",
    "subject",
    "chapter",
    "prompt",
    "choices",
    "answer",
    "explanation",
    "topic",
    "module",
    "los",
)
LOCKED_FIELDS = ("prompt", "choices", "answer", "explanation")
LOCKED_STATUSES = {"verified", "published"}
ALLOWED_DIFFICULTIES = {
    "unknown",
    "easy",
    "medium",
    "hard",
    "low",
    "moderate",
    "high",
    "1",
    "2",
    "3",
    "4",
    "5",
}


def _store_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "questions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _practice_session_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "practice-sessions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _practice_attempt_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "practice-attempts.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _wrongbook_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "wrongbook.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _notes_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "notes.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _favorites_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "question-banks" / "favorites.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_questions(repo: Repository) -> list[dict]:
    path = _store_path(repo)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_questions(repo: Repository, questions: list[dict]) -> None:
    _store_path(repo).write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")


def load_practice_sessions(repo: Repository) -> list[dict]:
    path = _practice_session_path(repo)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_practice_sessions(repo: Repository, sessions: list[dict]) -> None:
    _practice_session_path(repo).write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")


def load_practice_attempts(repo: Repository) -> list[dict]:
    path = _practice_attempt_path(repo)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_practice_attempts(repo: Repository, attempts: list[dict]) -> None:
    _practice_attempt_path(repo).write_text(json.dumps(attempts, ensure_ascii=False, indent=2), encoding="utf-8")


def load_wrongbook(repo: Repository) -> dict[str, dict]:
    path = _wrongbook_path(repo)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_wrongbook(repo: Repository, wrongbook: dict[str, dict]) -> None:
    _wrongbook_path(repo).write_text(json.dumps(wrongbook, ensure_ascii=False, indent=2), encoding="utf-8")


def load_question_notes(repo: Repository) -> dict[str, list[dict]]:
    path = _notes_path(repo)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_question_notes(repo: Repository, notes: dict[str, list[dict]]) -> None:
    _notes_path(repo).write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")


def load_favorites(repo: Repository) -> dict[str, dict]:
    path = _favorites_path(repo)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_favorites(repo: Repository, favorites: dict[str, dict]) -> None:
    _favorites_path(repo).write_text(json.dumps(favorites, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_complete(question: dict) -> bool:
    return all(question.get(field) for field in REQUIRED_VERIFIED_FIELDS)


def _hydrate_review_metadata(question: dict) -> None:
    if not question.get("subject") and question.get("topic"):
        question["subject"] = question["topic"]
    if not question.get("chapter") and question.get("module"):
        question["chapter"] = question["module"]
    if not question.get("knowledge_tags") and question.get("los"):
        question["knowledge_tags"] = [question["los"]]
    if not question.get("exam"):
        question["exam"] = "CFA Level I"
    if not question.get("difficulty"):
        question["difficulty"] = "unknown"


def _as_clean_string(value: object) -> str:
    return str(value or "").strip()


def _normalize_list(value: object) -> list[str]:
    if isinstance(value, list):
        raw_items = value
    elif isinstance(value, str):
        raw_items = re.split(r"[\n,;；|]+", value)
    else:
        raw_items = []
    items: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        text = _as_clean_string(item)
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(text)
    return items


def _normalize_choices(value: object) -> tuple[list[str], list[str]]:
    if value in (None, ""):
        return [], []
    if not isinstance(value, list):
        return [], ["choices must be a list of answer options"]
    choices = [_as_clean_string(item) for item in value if _as_clean_string(item)]
    if value and not choices:
        return [], ["choices cannot be empty when provided"]
    if choices and len(choices) < 2:
        return choices, ["choices must include at least two options"]
    return choices, []


def _choice_labels(choices: list[str]) -> set[str]:
    labels: set[str] = set()
    for index, choice in enumerate(choices):
        match = re.match(r"^\s*([A-Z])(?:[.)、:]|\s)", choice.strip(), flags=re.IGNORECASE)
        labels.add(match.group(1).upper() if match else chr(ord("A") + index))
    return labels


def _answer_matches_choices(answer: str, choices: list[str]) -> bool:
    if not answer or not choices:
        return True
    normalized = answer.strip()
    label_match = re.match(r"^\s*([A-Z])(?:[.)、:]|\s|$)", normalized, flags=re.IGNORECASE)
    if label_match and label_match.group(1).upper() in _choice_labels(choices):
        return True
    choice_texts = {choice.strip().lower() for choice in choices}
    return normalized.lower() in choice_texts


def _answer_label(value: str) -> str:
    match = re.match(r"^\s*([A-Z])(?:[.)、:]|\s|$)", value.strip(), flags=re.IGNORECASE)
    return match.group(1).upper() if match else ""


def _answer_is_correct(selected_answer: str, question: dict) -> bool:
    expected = _as_clean_string(question.get("answer"))
    selected = _as_clean_string(selected_answer)
    if not expected or not selected:
        return False
    expected_label = _answer_label(expected)
    selected_label = _answer_label(selected)
    if expected_label and selected_label:
        return expected_label == selected_label
    if selected.lower() == expected.lower():
        return True
    labels = _choice_labels(list(question.get("choices") or []))
    if expected_label and selected_label in labels:
        return expected_label == selected_label
    return False


def _identity_value(raw: dict, question: dict) -> str:
    return (
        _as_clean_string(raw.get("question_id"))
        or _as_clean_string(raw.get("external_id"))
        or _as_clean_string(raw.get("question_number"))
        or _as_clean_string(raw.get("number"))
        or _as_clean_string(raw.get("page"))
        or stable_id("private-question-content", question.get("prompt", ""))
    )


def _question_identity(source_file: str, raw: dict, question: dict) -> str:
    return stable_id("private-question", source_file, _identity_value(raw, question))


def normalize_import_question(source_file: str, raw: dict) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    choices, choice_errors = _normalize_choices(raw.get("choices"))
    errors.extend(choice_errors)

    topic = _as_clean_string(raw.get("topic") or raw.get("subject"))
    module = _as_clean_string(raw.get("module") or raw.get("chapter"))
    los = _as_clean_string(raw.get("los") or raw.get("learning_outcome"))
    subject = _as_clean_string(raw.get("subject") or topic)
    chapter = _as_clean_string(raw.get("chapter") or module)
    difficulty = _as_clean_string(raw.get("difficulty") or "unknown").lower()
    if difficulty not in ALLOWED_DIFFICULTIES:
        errors.append(f"difficulty must be one of: {', '.join(sorted(ALLOWED_DIFFICULTIES))}")

    answer = _as_clean_string(raw.get("answer") or raw.get("correct_answer"))
    if not _answer_matches_choices(answer, choices):
        errors.append("answer must match one of the provided choice labels or choice texts")

    knowledge_tags = _normalize_list(raw.get("knowledge_tags") or raw.get("tags") or raw.get("knowledge_point"))
    if not knowledge_tags and los:
        knowledge_tags = [los]
    if not knowledge_tags:
        warnings.append("knowledge_tags is empty; record will remain quarantined until tagged")

    question: dict[str, Any] = {
        **raw,
        "source_file": source_file,
        "exam": _as_clean_string(raw.get("exam") or raw.get("exam_project") or "CFA Level I"),
        "subject": subject,
        "chapter": chapter,
        "knowledge_tags": knowledge_tags,
        "difficulty": difficulty,
        "prompt": _as_clean_string(raw.get("prompt") or raw.get("stem") or raw.get("question")),
        "choices": choices,
        "answer": answer,
        "explanation": _as_clean_string(raw.get("explanation") or raw.get("rationale") or raw.get("solution")),
        "topic": topic,
        "module": module,
        "los": los,
    }
    question["question_id"] = _question_identity(source_file, raw, question)
    question["import_key"] = question["question_id"]
    question["imported_at"] = datetime.now(UTC).isoformat()
    if not question["prompt"]:
        errors.append("prompt is required")
    return question, errors, warnings


def _locked_field_changes(existing: dict, incoming: dict) -> list[str]:
    changed = []
    for field in LOCKED_FIELDS:
        if existing.get(field) != incoming.get(field):
            changed.append(field)
    return changed


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
    existing_by_id = {question["question_id"]: question for question in stored}
    accepted: list[dict] = []
    rejected: list[dict] = []
    duplicates: list[dict] = []
    locked: list[dict] = []
    for raw in questions:
        question, errors, warnings = normalize_import_question(source_file, raw)
        existing = existing_by_id.get(question["question_id"])
        if existing:
            changed_locked_fields = _locked_field_changes(existing, question)
            if existing.get("verification_status") in LOCKED_STATUSES and changed_locked_fields:
                locked.append(
                    {
                        "question_id": question["question_id"],
                        "changed_fields": changed_locked_fields,
                        "message": "published question content is locked; use explicit review override",
                    }
                )
                _append_event(repo, "question_bank.import_locked", {**existing, "locked_changes": changed_locked_fields})
                continue
            duplicates.append(
                {
                    "question_id": question["question_id"],
                    "message": "duplicate question identity skipped",
                }
            )
            continue
        if errors:
            question["verification_status"] = "rejected"
            question["validation_errors"] = errors
            question["validation_warnings"] = warnings
            rejected.append(
                {
                    "question_id": question["question_id"],
                    "errors": errors,
                    "warnings": warnings,
                    "source_ref": f"{source_file}:{raw.get('page', '')}",
                }
            )
            _append_event(repo, "question_bank.import_rejected", question)
            continue
        requested_status = question.get("verification_status", "")
        question["verification_status"] = "verified" if requested_status == "verified" and _is_complete(question) else "quarantined"
        if question["verification_status"] == "verified":
            question["published_at"] = datetime.now(UTC).isoformat()
        if warnings:
            question["validation_warnings"] = warnings
        stored.append(question)
        accepted.append(question)
        existing_by_id[question["question_id"]] = question
        _append_event(repo, "question_bank.imported", question)
    _save_questions(repo, stored)
    return {
        "imported_count": len(accepted),
        "accepted_count": len(accepted),
        "verified_count": sum(1 for question in accepted if question["verification_status"] == "verified"),
        "quarantined_count": sum(1 for question in accepted if question["verification_status"] == "quarantined"),
        "rejected_count": len(rejected),
        "duplicate_count": len(duplicates),
        "locked_count": len(locked),
        "questions": accepted,
        "accepted": accepted,
        "rejected": rejected,
        "duplicates": duplicates,
        "locked": locked,
    }


def review_question(repo: Repository, question_id: str, action: str, patch: dict | None = None) -> dict:
    questions = load_questions(repo)
    patch = patch or {}
    for question in questions:
        if question["question_id"] != question_id:
            continue
        allow_locked_update = bool(patch.pop("allow_locked_update", False) or action == "override")
        if question.get("verification_status") in LOCKED_STATUSES and not allow_locked_update:
            locked_updates = [field for field in LOCKED_FIELDS if field in patch and patch[field] != question.get(field)]
            if locked_updates:
                fields = ", ".join(locked_updates)
                raise PermissionError(f"Published question fields are locked: {fields}")
        if patch:
            question.update(patch)
            _hydrate_review_metadata(question)
        if action == "reject":
            question["verification_status"] = "rejected"
        elif action == "approve" and _is_complete(question):
            question["verification_status"] = "verified"
            question.setdefault("published_at", datetime.now(UTC).isoformat())
        elif action == "override" and _is_complete(question):
            question["verification_status"] = "verified"
            question["override_reviewed_at"] = datetime.now(UTC).isoformat()
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


def _normalize_practice_request(payload: dict) -> dict[str, Any]:
    tag_filter = payload.get("tag_filter") if isinstance(payload.get("tag_filter"), dict) else {}
    tags = _normalize_list(tag_filter.get("tags") or payload.get("tags") or payload.get("knowledge_tags"))
    tag_mode = _as_clean_string(tag_filter.get("mode") or payload.get("tag_mode") or "or").lower()
    if tag_mode not in {"and", "or"}:
        raise ValueError("tag_mode must be 'and' or 'or'")
    count = int(payload.get("count") or payload.get("question_count") or 10)
    if count <= 0:
        raise ValueError("count must be greater than zero")
    seed = int(payload.get("seed") or 0)
    return {
        "exam": _as_clean_string(payload.get("exam") or payload.get("exam_project") or "CFA Level I"),
        "topic": _as_clean_string(payload.get("topic") or payload.get("subject")),
        "chapter": _as_clean_string(payload.get("chapter") or payload.get("module")),
        "difficulty": _as_clean_string(payload.get("difficulty")).lower(),
        "count": count,
        "tag_filter": {"mode": tag_mode, "tags": tags},
        "seed": seed,
    }


def _tag_set(question: dict) -> set[str]:
    values = [
        *list(question.get("knowledge_tags") or []),
        question.get("los", ""),
        question.get("topic", ""),
        question.get("module", ""),
        question.get("subject", ""),
        question.get("chapter", ""),
    ]
    return {str(value).strip().lower() for value in values if str(value).strip()}


def _matches_practice_request(question: dict, request: dict) -> bool:
    if request["exam"] and question.get("exam") != request["exam"]:
        return False
    if request["topic"] and request["topic"] not in {question.get("topic"), question.get("subject")}:
        return False
    if request["chapter"] and request["chapter"] not in {question.get("module"), question.get("chapter")}:
        return False
    if request["difficulty"] and question.get("difficulty") != request["difficulty"]:
        return False
    tags = {tag.lower() for tag in request["tag_filter"]["tags"]}
    if not tags:
        return True
    question_tags = _tag_set(question)
    if request["tag_filter"]["mode"] == "and":
        return tags.issubset(question_tags)
    return bool(tags & question_tags)


def _practice_question_ref(question: dict) -> dict[str, str]:
    return {
        "question_id": str(question.get("question_id", "")),
        "source_file": str(question.get("source_file", "")),
        "exam": str(question.get("exam", "")),
        "topic": str(question.get("topic", "")),
        "module": str(question.get("module", "")),
        "los": str(question.get("los", "")),
    }


def generate_practice_session(repo: Repository, payload: dict) -> dict:
    request = _normalize_practice_request(payload)
    candidates = [
        question
        for question in sorted(load_verified_questions(repo), key=lambda item: str(item.get("question_id", "")))
        if _matches_practice_request(question, request)
    ]
    rng = random.Random(request["seed"])
    selected = rng.sample(candidates, k=min(request["count"], len(candidates))) if candidates else []
    question_ids = [str(question["question_id"]) for question in selected]
    session_id = stable_id(
        "practice-session",
        json.dumps(request, ensure_ascii=False, sort_keys=True),
        ",".join(question_ids),
    )
    session = {
        "session_id": session_id,
        "status": "generated",
        "created_at": datetime.now(UTC).isoformat(),
        "request": request,
        "candidate_count": len(candidates),
        "question_count": len(question_ids),
        "question_ids": question_ids,
        "question_refs": [_practice_question_ref(question) for question in selected],
    }
    sessions = load_practice_sessions(repo)
    if not any(item.get("session_id") == session_id for item in sessions):
        sessions.append(session)
        _save_practice_sessions(repo, sessions)
    repo.append_jsonl_event(
        "practice",
        {
            "schema_version": 1,
            "event_id": stable_id("practice-session-event", session_id),
            "event_type": "question_bank.practice_generated",
            "learner_id": "local",
            "occurred_at": session["created_at"],
            "source_refs": question_ids,
            "payload": {
                "session_id": session_id,
                "request": request,
                "question_ids": question_ids,
            },
        },
    )
    return session


def _load_question(repo: Repository, question_id: str) -> dict:
    for question in load_verified_questions(repo):
        if question.get("question_id") == question_id:
            return question
    raise FileNotFoundError(f"Verified question not found: {question_id}")


def _load_session(repo: Repository, session_id: str) -> dict:
    for session in load_practice_sessions(repo):
        if session.get("session_id") == session_id:
            return session
    raise FileNotFoundError(f"Practice session not found: {session_id}")


def _update_wrongbook(wrongbook: dict[str, dict], question: dict, attempt: dict) -> dict | None:
    question_id = str(question["question_id"])
    existing = wrongbook.get(question_id)
    if not attempt["is_correct"]:
        if existing:
            existing["wrong_count"] = int(existing.get("wrong_count", 0)) + 1
            existing["priority"] = min(100, int(existing.get("priority", 70)) + 10)
        else:
            existing = {
                "question_id": question_id,
                "topic": question.get("topic", ""),
                "module": question.get("module", ""),
                "los": question.get("los", ""),
                "first_wrong_at": attempt["created_at"],
                "wrong_count": 1,
                "correct_retry_count": 0,
                "priority": 80,
            }
            wrongbook[question_id] = existing
        existing["last_wrong_at"] = attempt["created_at"]
        existing["last_is_correct"] = False
        existing["last_attempt_id"] = attempt["attempt_id"]
        return existing

    if existing:
        existing["correct_retry_count"] = int(existing.get("correct_retry_count", 0)) + 1
        existing["priority"] = max(10, int(existing.get("priority", 80)) - 25)
        existing["last_correct_at"] = attempt["created_at"]
        existing["last_is_correct"] = True
        existing["last_attempt_id"] = attempt["attempt_id"]
        return existing
    return None


def _save_note_if_present(repo: Repository, question_id: str, note_text: str, attempt_id: str) -> dict | None:
    note = _as_clean_string(note_text)
    if not note:
        return None
    notes = load_question_notes(repo)
    entry = {
        "note_id": stable_id("question-note", question_id, attempt_id, note),
        "question_id": question_id,
        "attempt_id": attempt_id,
        "note": note,
        "created_at": datetime.now(UTC).isoformat(),
    }
    notes.setdefault(question_id, []).append(entry)
    _save_question_notes(repo, notes)
    return entry


def _save_favorite_if_requested(repo: Repository, question: dict, attempt_id: str, favorite: bool) -> dict | None:
    if not favorite:
        return None
    favorites = load_favorites(repo)
    question_id = str(question["question_id"])
    entry = favorites.get(question_id) or {
        "question_id": question_id,
        "topic": question.get("topic", ""),
        "module": question.get("module", ""),
        "los": question.get("los", ""),
        "created_at": datetime.now(UTC).isoformat(),
    }
    entry["last_attempt_id"] = attempt_id
    entry["favorite"] = True
    favorites[question_id] = entry
    _save_favorites(repo, favorites)
    return entry


def submit_practice_answer(repo: Repository, payload: dict) -> dict:
    session_id = _as_clean_string(payload.get("session_id"))
    question_id = _as_clean_string(payload.get("question_id"))
    selected_answer = _as_clean_string(payload.get("selected_answer") or payload.get("answer_text"))
    if not question_id:
        raise ValueError("question_id is required")
    if not selected_answer:
        raise ValueError("selected_answer is required")
    question = _load_question(repo, question_id)
    if session_id:
        session = _load_session(repo, session_id)
        if question_id not in set(session.get("question_ids") or []):
            raise ValueError("question_id does not belong to the provided practice session")

    created_at = datetime.now(UTC).isoformat()
    is_correct = _answer_is_correct(selected_answer, question)
    attempt_id = stable_id("practice-attempt", session_id, question_id, selected_answer, created_at)
    attempt = {
        "attempt_id": attempt_id,
        "session_id": session_id,
        "question_id": question_id,
        "selected_answer": selected_answer,
        "is_correct": is_correct,
        "time_spent": int(payload.get("time_spent") or payload.get("time_spent_seconds") or 0),
        "confidence": int(payload.get("confidence") or payload.get("confidence_before") or 0),
        "created_at": created_at,
        "topic": question.get("topic", ""),
        "module": question.get("module", ""),
        "los": question.get("los", ""),
    }
    attempts = load_practice_attempts(repo)
    attempts.append(attempt)
    _save_practice_attempts(repo, attempts)
    repo.append_attempt_record(
        {
            "schema_version": 1,
            "event_id": attempt_id,
            "event_type": "question_bank.answer_submitted",
            "learner_id": "local",
            "occurred_at": created_at,
            "source_refs": [ref for ref in (session_id, question_id) if ref],
            "attempt_id": attempt_id,
            "session_id": session_id,
            "question_id": question_id,
            "topic": question.get("topic", ""),
            "los": question.get("los", ""),
            "is_correct": is_correct,
            "selected_answer": selected_answer,
            "time_spent": attempt["time_spent"],
            "confidence": attempt["confidence"],
            "mistake_event_id": "",
        }
    )

    wrongbook = load_wrongbook(repo)
    wrongbook_record = _update_wrongbook(wrongbook, question, attempt)
    _save_wrongbook(repo, wrongbook)
    note = _save_note_if_present(repo, question_id, _as_clean_string(payload.get("note")), attempt_id)
    favorite = _save_favorite_if_requested(repo, question, attempt_id, bool(payload.get("favorite", False)))
    return {
        "attempt": attempt,
        "wrongbook_record": wrongbook_record,
        "note": note,
        "favorite": favorite,
        "feedback": {
            "is_correct": is_correct,
            "correct_answer": question.get("answer", ""),
        },
    }


def get_practice_question_display(repo: Repository, session_id: str, question_id: str) -> dict:
    session = _load_session(repo, session_id)
    if question_id not in set(session.get("question_ids") or []):
        raise ValueError("question_id does not belong to the provided practice session")
    question = _load_question(repo, question_id)
    attempts = [
        attempt
        for attempt in load_practice_attempts(repo)
        if attempt.get("session_id") == session_id and attempt.get("question_id") == question_id
    ]
    latest_attempt = attempts[-1] if attempts else None
    notes = load_question_notes(repo).get(question_id, [])
    favorite = load_favorites(repo).get(question_id, {})
    return {
        "session_id": session_id,
        "question_id": question_id,
        "state": "answered" if latest_attempt else "unanswered",
        "prompt": question.get("prompt", ""),
        "choices": list(question.get("choices") or []),
        "exam": question.get("exam", ""),
        "topic": question.get("topic", ""),
        "module": question.get("module", ""),
        "los": question.get("los", ""),
        "note_count": len(notes),
        "favorite": bool(favorite.get("favorite", False)),
        "latest_attempt": {
            "attempt_id": latest_attempt.get("attempt_id", ""),
            "selected_answer": latest_attempt.get("selected_answer", ""),
            "is_correct": latest_attempt.get("is_correct", False),
            "created_at": latest_attempt.get("created_at", ""),
        }
        if latest_attempt
        else None,
    }
