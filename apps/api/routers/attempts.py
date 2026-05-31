"""POST /api/attempts — Record question attempts and screenshots."""

from __future__ import annotations

import base64
from pathlib import Path
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import AttemptResponse, QuestionAttemptRequest, ScreenshotUploadRequest

router = APIRouter()


@router.post("", response_model=AttemptResponse)
async def record_attempt(req: QuestionAttemptRequest, repo=Depends(get_repo)):
    """Record a question attempt and create a mistake card.

    This is the primary learning event entry point.
    Returns the event ID, card ID, fix rule, next drill, and review due date.
    """
    from app.models import stable_id
    from app.workflows import default_fix_rule, next_drill_for, parse_frontmatter, record_event

    created_at = datetime.now(UTC).isoformat()
    request_payload = req.model_dump()
    attempt_id = stable_id(
        "attempt",
        request_payload.get("topic", ""),
        request_payload.get("los", ""),
        request_payload.get("prompt_or_question", ""),
        request_payload.get("wrong_choice_or_output", ""),
        ",".join(request_payload.get("evidence_refs", [])),
        created_at,
    )
    attempt_record = {
        "attempt_id": attempt_id,
        "is_correct": req.is_correct,
        "created_at": created_at,
        **request_payload,
    }
    repo.append_attempt_record(attempt_record)

    if req.is_correct:
        return AttemptResponse(
            attempt_id=attempt_id,
            event_id="",
            card_id="",
            error_type="",
            fix_rule="",
            next_drill="",
            review_due_at="",
        )

    payload = {
        key: value
        for key, value in request_payload.items()
        if key != "is_correct"
    }
    payload["source_layer"] = "question"
    event = record_event(repo, payload, mode="record-mistake")

    card_id = stable_id("card", event.event_id or "", event.topic, event.los)
    card_path = repo.memory_root / "question-errors" / f"{card_id}.md"
    frontmatter = parse_frontmatter(card_path.read_text(encoding="utf-8")) if card_path.exists() else {}
    fix_rule = frontmatter.get("fix_rule") or default_fix_rule(event.error_type)
    next_drill = frontmatter.get("next_drill") or next_drill_for(event)
    review_due_at = frontmatter.get("review_due_at", "")

    return AttemptResponse(
        attempt_id=attempt_id,
        event_id=event.event_id or "",
        card_id=card_id,
        error_type=event.error_type,
        fix_rule=fix_rule,
        next_drill=next_drill,
        review_due_at=review_due_at,
    )


@router.post("/screenshot")
async def upload_screenshot(req: ScreenshotUploadRequest, repo=Depends(get_repo)):
    """Upload a screenshot for AI-powered structured extraction.

    Saves the screenshot as evidence and triggers agent-based extraction
    to convert the image into a structured question attempt.
    """
    # Decode and save the screenshot
    try:
        image_bytes = base64.b64decode(req.image_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

    evidence_dir = repo.root / "evidence" / "screenshots"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    import time
    filename = f"{int(time.time())}-{req.filename}"
    filepath = evidence_dir / filename
    filepath.write_bytes(image_bytes)

    # Return a pre-filled payload for the agent to complete
    return {
        "status": "screenshot_saved",
        "filename": filename,
        "path": str(filepath.relative_to(repo.root)),
        "suggested_payload": {
            "source_layer": "question",
            "topic": req.topic,
            "los": req.los,
            "source_type": "screenshot",
            "evidence_assets": [str(filepath.relative_to(repo.root))],
        },
    }


@router.get("/recent")
async def list_recent_attempts(limit: int = 20, repo=Depends(get_repo)):
    """List recent question attempts."""
    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]
    recent = question_events[-limit:]

    return {
        "count": len(recent),
        "total": len(question_events),
        "attempts": [
            {
                "event_id": e.event_id,
                "topic": e.topic,
                "los": e.los,
                "error_type": e.error_type,
                "confidence": e.confidence,
                "created_at": e.created_at,
            }
            for e in reversed(recent)
        ],
    }


@router.post("/batch-import")
async def batch_import(req: list[QuestionAttemptRequest], repo=Depends(get_repo)):
    """Batch import multiple question attempts."""
    from app.workflows import batch_import_events

    payloads = [r.model_dump() for r in req]
    event_ids = batch_import_events(repo, payloads, "api-batch-import")
    return {
        "imported_count": len(event_ids),
        "event_ids": event_ids,
    }
