"""POST /api/attempts — Record question attempts and screenshots."""

from __future__ import annotations

import base64

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
    from app.workflows import default_fix_rule, next_drill_for, parse_frontmatter, record_question_attempt

    result = record_question_attempt(repo, req.model_dump())
    if result["event"] is None:
        return AttemptResponse(
            attempt_id=result["attempt_id"],
            event_id="",
            card_id="",
            error_type="",
            fix_rule="",
            next_drill="",
            review_due_at="",
        )

    event = result["event"]
    card_id = result["card_id"]
    card_path = repo.memory_root / "question-errors" / f"{card_id}.md"
    frontmatter = parse_frontmatter(card_path.read_text(encoding="utf-8")) if card_path.exists() else {}
    fix_rule = frontmatter.get("fix_rule") or default_fix_rule(event.error_type)
    next_drill = frontmatter.get("next_drill") or next_drill_for(event)
    review_due_at = frontmatter.get("review_due_at", "")

    return AttemptResponse(
        attempt_id=result["attempt_id"],
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

    from datetime import datetime
    from pathlib import Path as PathLib
    # Sanitize filename: strip directory components to prevent path traversal
    safe_name = PathLib(req.filename).name
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{safe_name}"
    filepath = evidence_dir / filename
    filepath.write_bytes(image_bytes)

    from app.screenshot_capture import create_screenshot_extraction_draft

    draft = create_screenshot_extraction_draft(
        repo,
        evidence_path=str(filepath.relative_to(repo.root)),
        topic=req.topic,
        los=req.los,
    )

    return {
        "status": "screenshot_draft_created",
        "filename": filename,
        "path": str(filepath.relative_to(repo.root)),
        "draft_id": draft.draft_id,
        "draft_path": draft.draft_path,
        "draft": draft.as_dict(),
    }


@router.get("/recent")
async def list_recent_attempts(limit: int = 20, repo=Depends(get_repo)):
    """List recent question attempts."""
    attempts = repo.load_attempt_records()
    recent = attempts[-limit:]

    return {
        "count": len(recent),
        "total": len(attempts),
        "attempts": [
            {
                "attempt_id": attempt.get("attempt_id", ""),
                "topic": attempt.get("topic", ""),
                "los": attempt.get("los", ""),
                "error_type": attempt.get("error_type", ""),
                "confidence": attempt.get("confidence", 0),
                "is_correct": attempt.get("is_correct", False),
                "created_at": attempt.get("created_at", ""),
            }
            for attempt in reversed(recent)
        ],
    }


@router.post("/batch-import")
async def batch_import(req: list[QuestionAttemptRequest], repo=Depends(get_repo)):
    """Batch import multiple question attempts."""
    from app.workflows import batch_import_attempts

    payloads = [r.model_dump() for r in req]
    result = batch_import_attempts(repo, payloads, "api-batch-import")
    return {
        "attempt_count": len(result["attempt_ids"]),
        "mistake_count": len(result["event_ids"]),
        "attempt_ids": result["attempt_ids"],
        "event_ids": result["event_ids"],
    }
