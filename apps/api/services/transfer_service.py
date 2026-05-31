"""Explicit local/cloud transfer bundles with dry-run summaries."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.models import MistakeEvent
from app.storage import CATALOG_SCHEMA_VERSION, PLATFORM_STREAMS
from services.practice_service import _append_question, load_questions


def export_bundle(repo) -> dict[str, Any]:
    return {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "exported_at": datetime.now(UTC).isoformat(),
        "streams": {stream: repo.load_stream_events(stream) for stream in PLATFORM_STREAMS},
        "mistake_events": [event.as_dict() for event in repo.load_events()],
        "attempts": repo.load_attempt_records(),
        "questions": load_questions(repo),
    }


def import_bundle(repo, bundle: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
    if bundle.get("schema_version") != CATALOG_SCHEMA_VERSION:
        raise ValueError(f"Unsupported transfer schema: {bundle.get('schema_version')}")

    existing_source_ids = {
        source_ref.removeprefix("import:")
        for stream in PLATFORM_STREAMS
        for event in repo.load_stream_events(stream)
        for source_ref in [event.get("event_id", ""), *event.get("source_refs", [])]
    }
    planned_events = []
    duplicate_event_count = 0
    for stream, events in bundle.get("streams", {}).items():
        if stream not in PLATFORM_STREAMS:
            raise ValueError(f"Unsupported platform stream: {stream}")
        for event in events:
            if event.get("event_id") in existing_source_ids:
                duplicate_event_count += 1
            else:
                planned_events.append((stream, event))

    existing_question_ids = {question["question_id"] for question in load_questions(repo)}
    planned_questions = [
        question for question in bundle.get("questions", [])
        if question.get("question_id") not in existing_question_ids
    ]
    duplicate_question_count = len(bundle.get("questions", [])) - len(planned_questions)
    existing_mistake_ids = {event.event_id for event in repo.load_events()}
    planned_mistakes = [
        event for event in bundle.get("mistake_events", [])
        if event.get("event_id") not in existing_mistake_ids
    ]

    summary = {
        "dry_run": dry_run,
        "importable_event_count": len(planned_events),
        "duplicate_event_count": duplicate_event_count,
        "importable_question_count": len(planned_questions),
        "duplicate_question_count": duplicate_question_count,
        "importable_mistake_count": len(planned_mistakes),
        "imported_event_count": 0,
        "imported_question_count": 0,
        "imported_mistake_count": 0,
    }
    if dry_run:
        return summary

    for stream, event in planned_events:
        repo.append_stream_event(
            stream,
            event["event_type"],
            event.get("payload", {}),
            learner_id=event.get("learner_id", "local"),
            source_refs=[*event.get("source_refs", []), f"import:{event['event_id']}"],
        )
    for question in planned_questions:
        _append_question(repo, question)
    for payload in planned_mistakes:
        repo.append_event(MistakeEvent.from_payload(payload))
    return {
        **summary,
        "imported_event_count": len(planned_events),
        "imported_question_count": len(planned_questions),
        "imported_mistake_count": len(planned_mistakes),
    }
