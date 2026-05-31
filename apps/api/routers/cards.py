"""Mistake-card review and correction-rule feedback endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import CardReviewRequest, FixRuleFeedbackRequest

router = APIRouter()


@router.post("/{card_id}/review")
async def review_card(card_id: str, req: CardReviewRequest, repo=Depends(get_repo)):
    """Record an explicit recall outcome and reschedule the card."""
    from app.workflows import mark_card_reviewed

    try:
        return mark_card_reviewed(repo, card_id, req.outcome, req.confidence_after)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{card_id}/fix-rule-feedback")
async def fix_rule_feedback(card_id: str, req: FixRuleFeedbackRequest, repo=Depends(get_repo)):
    """Append evidence about whether a fix rule was useful."""
    from app.workflows import record_fix_rule_feedback

    try:
        event = record_fix_rule_feedback(repo, card_id, req.helpful, req.note)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"event_id": event["event_id"], **event["payload"]}
