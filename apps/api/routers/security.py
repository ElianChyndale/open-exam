"""Read-only security audit routes for local admin review."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from deps import get_repo, require_admin_user

router = APIRouter()


@router.get("/events")
async def list_security_events(
    limit: int = Query(50, ge=1, le=500),
    _: dict = Depends(require_admin_user),
    repo=Depends(get_repo),
):
    events = list(reversed(repo.load_jsonl_events("security")))[:limit]
    redacted = []
    for event in events:
        safe_event = dict(event)
        safe_event.pop("session_token", None)
        redacted.append(safe_event)
    return {"count": len(redacted), "events": redacted}
