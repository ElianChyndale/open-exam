"""Verified private question bank and mixed-practice services."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models import stable_id


QUESTION_STATUSES = {"verified", "quarantined", "rejected"}


def _bank_path(repo) -> Path:
    path = repo.private_root / "question-bank" / "questions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _append_question(repo, question: dict[str, Any]) -> None:
    with _bank_path(repo).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(question, ensure_ascii=False) + "\n")


def load_questions(repo) -> list[dict[str, Any]]:
    path = _bank_path(repo)
    if not path.exists():
        return []
    current: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            current[record["question_id"]] = record
    return list(current.values())


def _choice_matches(question: dict[str, Any]) -> bool:
    answer = str(question.get("correct_answer", "")).strip().upper()
    choices = question.get("choices", [])
    if not answer or not choices:
        return False
    return any(str(choice).strip().upper().startswith(answer) for choice in choices)


def _is_complete(question: dict[str, Any]) -> bool:
    required = ("source_file", "source_page", "prompt", "choices", "correct_answer", "explanation", "topic", "los")
    return all(question.get(field) for field in required) and _choice_matches(question)


def import_questions(repo, source_name: str, questions: list[dict[str, Any]]) -> dict[str, Any]:
    imported = []
    batch_id = stable_id("import", source_name, datetime.now(UTC).isoformat())
    for raw in questions:
        question = {
            "question_id": stable_id(
                "question",
                source_name,
                str(raw.get("source_file", "")),
                str(raw.get("source_page", "")),
                str(raw.get("prompt", "")),
            ),
            "import_batch_id": batch_id,
            "source_name": source_name,
            "source_file": raw.get("source_file", ""),
            "source_page": raw.get("source_page", 0),
            "prompt": raw.get("prompt", ""),
            "choices": raw.get("choices", []),
            "correct_answer": raw.get("correct_answer", ""),
            "explanation": raw.get("explanation", ""),
            "topic": raw.get("topic", ""),
            "module": raw.get("module", ""),
            "los": raw.get("los", ""),
            "error_type": raw.get("error_type", "concept_confusion"),
            "verification_status": "quarantined",
            "updated_at": datetime.now(UTC).isoformat(),
        }
        if _is_complete(question):
            question["verification_status"] = "verified"
        _append_question(repo, question)
        imported.append(question)
    repo.append_stream_event(
        "practice",
        "question-bank.imported",
        {
            "import_batch_id": batch_id,
            "source_name": source_name,
            "question_ids": [question["question_id"] for question in imported],
        },
    )
    return {
        "import_batch_id": batch_id,
        "verified_count": sum(question["verification_status"] == "verified" for question in imported),
        "quarantined_count": sum(question["verification_status"] == "quarantined" for question in imported),
        "questions": imported,
    }


def review_question(repo, question_id: str, action: str, corrections: dict[str, Any]) -> dict[str, Any] | None:
    question = next((item for item in load_questions(repo) if item["question_id"] == question_id), None)
    if question is None:
        return None
    updated = {**question, **corrections, "updated_at": datetime.now(UTC).isoformat()}
    if action == "reject":
        updated["verification_status"] = "rejected"
    elif action == "approve":
        if not _is_complete(updated):
            raise ValueError("Question is still incomplete and cannot be approved")
        updated["verification_status"] = "verified"
    else:
        raise ValueError(f"Unsupported review action: {action}")
    _append_question(repo, updated)
    repo.append_stream_event(
        "practice",
        f"question-bank.{updated['verification_status']}",
        {"question_id": question_id, "action": action},
    )
    return updated


def quarantined_questions(repo) -> list[dict[str, Any]]:
    return [question for question in load_questions(repo) if question["verification_status"] == "quarantined"]


def _public_question(question: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in question.items()
        if key not in {"correct_answer", "explanation"}
    }


def _mistake_card_drills(repo, max_items: int) -> list[dict[str, Any]]:
    drills = []
    for event in reversed([item for item in repo.load_events() if item.source_layer == "question"]):
        drills.append(
            {
                "drill_id": stable_id("drill", event.event_id or "", event.topic, event.los),
                "source_kind": "mistake_card",
                "source_event_id": event.event_id,
                "topic": event.topic,
                "los": event.los,
                "prompt": f"Closed-book correction: {event.prompt_or_question}",
                "answer_text": event.correct_resolution,
                "fix_rule": event.error_type,
            }
        )
        if len(drills) >= max_items:
            break
    return drills


def _remediation_drills(repo, max_items: int) -> list[dict[str, Any]]:
    drills = []
    for event in reversed([item for item in repo.load_events() if item.source_layer == "question"]):
        drills.append(
            {
                "drill_id": stable_id("weak-los", event.event_id or ""),
                "source_kind": "weak_los",
                "source_event_id": event.event_id,
                "topic": event.topic,
                "los": event.los,
                "prompt": f"Weak-LOS retrieval: explain the deciding rule for {event.los}.",
                "answer_text": event.correct_resolution,
                "fix_rule": "Retrieve the rule before attempting a fresh question.",
            }
        )
        if event.error_type == "formula_misuse":
            drills.append(
                {
                    "drill_id": stable_id("formula", event.event_id or ""),
                    "source_kind": "formula_recall",
                    "source_event_id": event.event_id,
                    "topic": event.topic,
                    "los": event.los,
                    "prompt": f"Recall the deciding formula or rule before solving: {event.prompt_or_question}",
                    "answer_text": event.correct_resolution,
                    "fix_rule": "Write the formula before substituting values.",
                }
            )
        if event.error_type in {"concept_confusion", "careless_reading"}:
            drills.append(
                {
                    "drill_id": stable_id("concept", event.event_id or ""),
                    "source_kind": "concept_discrimination",
                    "source_event_id": event.event_id,
                    "topic": event.topic,
                    "los": event.los,
                    "prompt": f"Name the discriminating signal: {event.prompt_or_question}",
                    "answer_text": event.correct_resolution,
                    "fix_rule": "State the contrast before selecting an answer.",
                }
            )
        if len(drills) >= max_items:
            break
    for question in load_questions(repo):
        if question.get("verification_status") != "verified":
            continue
        drills.append(
            {
                "drill_id": stable_id("adjacent", question["question_id"]),
                "source_kind": "adjacent_concept",
                "source_event_id": question["question_id"],
                "topic": question["topic"],
                "los": question["los"],
                "prompt": f"Adjacent-concept check: name the nearest competing rule before answering. {question['prompt']}",
                "answer_text": question["explanation"],
                "fix_rule": "Contrast the correct rule with its nearest alternative.",
            }
        )
        drills.append(
            {
                "drill_id": stable_id("maintenance", question["question_id"]),
                "source_kind": "maintenance",
                "source_event_id": question["question_id"],
                "topic": question["topic"],
                "los": question["los"],
                "prompt": f"Maintenance recall: {question['prompt']}",
                "answer_text": question["explanation"],
                "fix_rule": "Keep verified concepts active between weak-LOS sessions.",
            }
        )
        if len(drills) >= max_items * 2:
            break
    return drills


def start_practice_session(repo, max_items: int, topic: str = "") -> dict[str, Any]:
    questions = [
        question
        for question in load_questions(repo)
        if question["verification_status"] == "verified" and (not topic or question["topic"] == topic)
    ][:max_items]
    session_id = stable_id("practice", datetime.now(UTC).isoformat(), str(len(questions)))
    items = [_public_question(question) for question in questions]
    mistake_drills = _mistake_card_drills(repo, max_items)
    remediation_drills = _remediation_drills(repo, max_items)
    drills = [*mistake_drills, *remediation_drills]
    session = {
        "session_id": session_id,
        "items": items,
        "drills": drills,
        "composition": {
            "verified_imports": len(items),
            "mistake_card_drills": len(mistake_drills),
            "remediation_drills": len(remediation_drills),
        },
        "status": "active",
        "topic": topic,
    }
    repo.append_stream_event("practice", "practice.started", session)
    return session


def _practice_session(repo, session_id: str) -> dict[str, Any] | None:
    sessions = [
        event["payload"]
        for event in repo.load_stream_events("practice")
        if event.get("event_type") == "practice.started" and event.get("payload", {}).get("session_id") == session_id
    ]
    return sessions[-1] if sessions else None


def _failure_count(repo, question_id: str) -> int:
    return sum(
        1
        for event in repo.load_stream_events("practice")
        if event.get("event_type") == "practice.answered"
        and event.get("payload", {}).get("question_id") == question_id
        and not event.get("payload", {}).get("is_correct")
    )


def _worked_example_stage(repo, question_id: str, is_correct: bool, failure_count: int) -> str:
    prior_stages = [
        event.get("payload", {}).get("worked_example_stage")
        for event in repo.load_stream_events("practice")
        if event.get("event_type") == "practice.answered"
        and event.get("payload", {}).get("question_id") == question_id
    ]
    prior_stage = prior_stages[-1] if prior_stages else ""
    if is_correct and prior_stage == "full_solution":
        return "hidden_step_completion"
    if is_correct and prior_stage == "hidden_step_completion":
        return "independent"
    if failure_count >= 3:
        return "full_solution"
    if failure_count >= 2:
        return "hidden_step_completion"
    return "independent"


def answer_practice_question(repo, session_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    from app.workflows import record_event
    from study_science.calibration import ConfidenceCalibration
    from study_science.self_explanation import SelfExplanationPrompt
    from study_science.worked_example import WorkedExampleFader

    session = _practice_session(repo, session_id)
    if session is None or not any(item.get("question_id") == payload["question_id"] for item in session["items"]):
        return None
    question = next((item for item in load_questions(repo) if item["question_id"] == payload["question_id"]), None)
    if question is None:
        return None
    if question["verification_status"] != "verified":
        raise PermissionError("Only verified question records can be graded")

    answer = str(payload["answer"]).strip().upper()
    correct_answer = str(question["correct_answer"]).strip().upper()
    is_correct = answer == correct_answer
    created_at = datetime.now(UTC).isoformat()
    attempt_id = stable_id("attempt", session_id, question["question_id"], created_at)
    attempt = {
        "attempt_id": attempt_id,
        "session_id": session_id,
        "topic": question["topic"],
        "los": question["los"],
        "prompt_or_question": question["prompt"],
        "wrong_choice_or_output": payload["answer"],
        "correct_resolution": question["explanation"],
        "error_type": question["error_type"],
        "confidence": payload["confidence"],
        "time_spent": payload["elapsed_seconds"],
        "evidence_refs": [question["question_id"]],
        "question_source": question["source_name"],
        "source_type": "private_question_bank",
        "choices": question["choices"],
        "is_correct": is_correct,
        "created_at": created_at,
    }
    repo.append_attempt_record(attempt)
    if not is_correct:
        record_event(
            repo,
            {
                key: value
                for key, value in attempt.items()
                if key not in {"attempt_id", "session_id", "is_correct", "created_at"}
            } | {"source_layer": "question", "created_at": created_at},
            mode="record-mistake",
        )

    prompt = SelfExplanationPrompt.generate(
        question["error_type"],
        topic=question["topic"],
        los=question["los"],
        correct_answer=question["correct_answer"],
        user_answer=payload["answer"],
        question_stem=question["prompt"],
    )
    quality = SelfExplanationPrompt.evaluate_quality(prompt, payload.get("self_explanation", ""))
    calibration_state = ConfidenceCalibration.classify(payload["confidence"], is_correct).value
    failure_count = _failure_count(repo, question["question_id"]) + (0 if is_correct else 1)
    WorkedExampleFader.should_use_worked_examples(failure_count, question["error_type"])
    warning = ConfidenceCalibration.generate_warning(question["topic"], question["los"], 1) if ConfidenceCalibration.is_dangerous(payload["confidence"], is_correct) else None
    result = {
        "session_id": session_id,
        "question_id": question["question_id"],
        "attempt_id": attempt_id,
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "explanation": question["explanation"],
        "calibration_state": calibration_state,
        "calibration_warning": warning,
        "self_explanation_prompt": prompt,
        "explanation_quality": quality,
        "worked_example_stage": _worked_example_stage(repo, question["question_id"], is_correct, failure_count),
        "failure_count": failure_count,
    }
    repo.append_stream_event("practice", "practice.answered", result, source_refs=[question["question_id"]])
    return result
