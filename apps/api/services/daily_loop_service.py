"""Local-first daily learner loop services."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from app.models import stable_id


DEFAULT_PROFILE = {
    "exam_name": "CFA Level I",
    "exam_date": "",
    "current_phase": "foundation",
    "target_score_percentile": 70,
    "daily_minutes_available": 120,
    "weekly_study_days": 6,
    "preferred_session_minutes": 50,
    "peak_energy_window": "09:00-12:00",
    "moderate_energy_window": "14:00-18:00",
    "low_energy_window": "20:00-22:00",
}

TASK_STATUSES = {"pending", "completed", "skipped", "deferred"}


def get_profile(repo) -> dict[str, Any]:
    return {**DEFAULT_PROFILE, **(repo.latest_stream_payload("profile", "profile.updated") or {})}


def update_profile(repo, payload: dict[str, Any]) -> dict[str, Any]:
    profile = {**get_profile(repo), **payload}
    repo.append_stream_event("profile", "profile.updated", profile)
    return profile


def _registry_path(repo) -> Path:
    relative = Path(".system/memory/strategy/cfa-2026-official-module-registry.json")
    candidate = repo.root / relative
    if candidate.exists():
        return candidate
    return Path(__file__).resolve().parents[3] / relative


def load_registry(repo) -> dict[str, Any]:
    return json.loads(_registry_path(repo).read_text(encoding="utf-8"))


def curriculum_summary(repo) -> dict[str, Any]:
    registry = load_registry(repo)
    weakness_events = [event for event in repo.load_events() if event.source_layer == "question"]
    weakness_by_topic = Counter(event.topic for event in weakness_events)
    subjects = []
    for name, subject in registry["subjects"].items():
        subject_events = [event for event in weakness_events if event.topic == name]
        modules = []
        for module in subject["modules"]:
            module_events = [
                event for event in subject_events
                if module["module"].lower() in event.los.lower()
                or any(event.los.lower() in los.lower() for los in module.get("los", []))
            ]
            modules.append(
                {
                    **module,
                    "weakness_count": len(module_events),
                    "weakness_los": sorted({event.los for event in module_events}),
                }
            )
        subjects.append(
            {
                "subject": name,
                "directory": subject["directory"],
                "exam_weight": subject["exam_weight"],
                "module_count": subject["module_count"],
                "modules": modules,
                "weakness_count": weakness_by_topic[name],
                "weakness_los": sorted({event.los for event in subject_events}),
            }
        )
    return {
        "generated_at": registry.get("generated_at", ""),
        "official_source": registry.get("official_source", ""),
        "subject_count": len(subjects),
        "module_count": sum(len(subject["modules"]) for subject in subjects),
        "subjects": subjects,
    }


def curriculum_subject(repo, subject_name: str) -> dict[str, Any] | None:
    summary = curriculum_summary(repo)
    return next((subject for subject in summary["subjects"] if subject["subject"] == subject_name), None)


def _current_tasks(repo) -> dict[str, dict[str, Any]]:
    current: dict[str, dict[str, Any]] = {}
    for event in repo.load_stream_events("task"):
        payload = event.get("payload", {})
        task = payload.get("task", payload)
        if task.get("task_id"):
            current[task["task_id"]] = task
    return current


def _new_task(task_type: str, title: str, topic: str, minutes: int, priority: int, energy_fit: str) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "task_id": stable_id("task", today, task_type, topic, title),
        "date": today,
        "task_type": task_type,
        "title": title,
        "topic": topic,
        "estimated_minutes": minutes,
        "deadline": "",
        "priority": priority,
        "energy_fit": energy_fit,
        "status": "pending",
    }


def today_tasks(repo, focus_topic: str = "") -> list[dict[str, Any]]:
    today = date.today().isoformat()
    existing = [task for task in _current_tasks(repo).values() if task.get("date") == today]
    if existing:
        return sorted(existing, key=lambda task: (-task["priority"], task["title"]))

    topic = focus_topic or "Weak LOS rotation"
    tasks = [
        _new_task("active_recall", "Complete due retrieval review", topic, 25, 95, "moderate"),
        _new_task("interleaved_set", f"Run mixed practice: {topic}", topic, 35, 85, "high"),
        _new_task("light_review", "Inspect today evidence and update next action", topic, 15, 60, "low"),
    ]
    for task in tasks:
        repo.append_stream_event("task", "task.planned", {"task": task})
    return tasks


def set_task_status(repo, task_id: str, status: str) -> dict[str, Any] | None:
    if status not in TASK_STATUSES:
        raise ValueError(f"Unsupported task status: {status}")
    task = _current_tasks(repo).get(task_id)
    if task is None:
        return None
    task = {**task, "status": status}
    repo.append_stream_event("task", f"task.{status}", {"task": task})
    return task


def refit_today_tasks(repo, recommended_order: list[str]) -> list[dict[str, Any]]:
    order = {task_type: index for index, task_type in enumerate(recommended_order)}
    tasks = today_tasks(repo)
    for task in tasks:
        rank = order.get(task["task_type"], len(order) + 1)
        updated = {**task, "priority": max(1, 100 - rank * 5)}
        repo.append_stream_event("task", "task.recommended", {"task": updated})
    return today_tasks(repo)


def notifications(repo) -> list[dict[str, Any]]:
    today = date.today()
    items = []
    activity_dates = []
    for stream in ("profile", "task", "review", "practice", "mock-run", "coach"):
        for event in repo.load_stream_events(stream):
            try:
                activity_dates.append(datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00")))
            except (KeyError, TypeError, ValueError):
                pass
    for event in repo.load_events():
        try:
            activity_dates.append(datetime.fromisoformat(event.created_at.replace("Z", "+00:00")))
        except (TypeError, ValueError):
            pass

    for task in today_tasks(repo):
        if task["status"] == "pending":
            items.append(
                {
                    "notification_id": stable_id("note", task["task_id"], "pending"),
                    "kind": "task.pending",
                    "title": task["title"],
                    "detail": f"{task['estimated_minutes']} min · {task['energy_fit']} energy",
                    "source_ref": task["task_id"],
                }
            )
    for task in _current_tasks(repo).values():
        deadline = task.get("deadline", "")
        if task.get("status") == "pending" and deadline and deadline < today.isoformat():
            items.append(
                {
                    "notification_id": stable_id("note", task["task_id"], "overdue"),
                    "kind": "task.overdue",
                    "title": task.get("title", "Overdue task"),
                    "detail": f"Deadline passed on {deadline}",
                    "source_ref": task["task_id"],
                }
            )
    latest_reviews = {}
    for event in repo.load_stream_events("review"):
        payload = event.get("payload", {})
        if event.get("event_type") == "review.responded" and payload.get("prompt_id"):
            latest_reviews[payload["prompt_id"]] = payload
    for review in latest_reviews.values():
        next_date = review.get("next_review_date", "")
        if next_date and next_date <= today.isoformat():
            items.append(
                {
                    "notification_id": stable_id("note", review["prompt_id"], "review-due"),
                    "kind": "review.due",
                    "title": "Retrieval review due",
                    "detail": f"Scheduled spacing date: {next_date}",
                    "source_ref": review["prompt_id"],
                }
            )
    mock_dir = repo.memory_root / "mock_sessions"
    for path in sorted(mock_dir.glob("*.json")) if mock_dir.exists() else []:
        mock = json.loads(path.read_text(encoding="utf-8"))
        scheduled_date = mock.get("scheduled_date", "")
        if scheduled_date and scheduled_date <= today.isoformat():
            items.append(
                {
                    "notification_id": stable_id("note", mock.get("session_id", path.stem), "mock-deadline"),
                    "kind": "mock.deadline",
                    "title": mock.get("session_label", "Mock deadline"),
                    "detail": f"Scheduled mock date: {scheduled_date}",
                    "source_ref": mock.get("session_id", path.stem),
                }
            )
    if activity_dates and max(activity_dates) < datetime.now(UTC) - timedelta(days=7):
        items.append(
            {
                "notification_id": stable_id("note", "local", "inactive-streak"),
                "kind": "streak.inactive",
                "title": "Study streak needs attention",
                "detail": "No evidence has been captured for at least seven days.",
                "source_ref": "local",
            }
        )
    return items


def start_review_session(repo, max_items: int) -> dict[str, Any]:
    from study_science.retrieval import RetrievalEngine

    items: list[dict[str, Any]] = []
    for event in reversed([item for item in repo.load_events() if item.source_layer == "question"]):
        prompts = RetrievalEngine.build_prompts(
            topic=event.topic,
            los=event.los,
            error_type=event.error_type,
            correct_resolution=event.correct_resolution,
            question_prompt=event.prompt_or_question,
            count=1,
        )
        if not prompts:
            continue
        prompt = prompts[0]
        items.append(
            {
                "prompt_id": prompt.prompt_id,
                "prompt_text": prompt.prompt_text,
                "answer_text": prompt.answer_text,
                "topic": prompt.topic,
                "los": prompt.los,
                "retrieval_type": prompt.retrieval_type,
                "error_type": event.error_type,
                "source_event_id": event.event_id,
            }
        )
        if len(items) >= max_items:
            break

    session_id = stable_id("review", date.today().isoformat(), str(len(repo.load_stream_events("review"))))
    session = {"session_id": session_id, "items": items, "status": "active"}
    repo.append_stream_event("review", "review.started", session)
    return session


def submit_review_response(repo, session_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    from study_science.spacing import SpacingInput, SpacingScheduler

    started = [
        event["payload"]
        for event in repo.load_stream_events("review")
        if event.get("event_type") == "review.started" and event.get("payload", {}).get("session_id") == session_id
    ]
    if not started:
        return None
    item = next((item for item in started[-1]["items"] if item["prompt_id"] == payload["prompt_id"]), None)
    if item is None:
        return None
    score = payload["score"]
    profile = get_profile(repo)
    decision = SpacingScheduler.schedule(
        SpacingInput(
            topic=item["topic"],
            los=item["los"],
            error_type=item["error_type"],
            confidence=score,
            is_correct=score >= 3,
            exam_date=profile.get("exam_date", ""),
        )
    )
    response = {
        "session_id": session_id,
        "prompt_id": payload["prompt_id"],
        "score": score,
        "self_explanation": payload.get("self_explanation", ""),
        "next_review_date": decision.next_review_date,
        "interval_days": decision.interval_days,
        "priority": decision.priority,
    }
    repo.append_stream_event(
        "review",
        "review.responded",
        response,
        source_refs=[item["source_event_id"]] if item.get("source_event_id") else [],
    )
    return response
