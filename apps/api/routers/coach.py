"""Deterministic, evidence-linked coaching API."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import CoachAgentAuditRequest, CoachRetroRequest
from services.advanced_service import audit_agent_failure, coach_briefs, create_coach_brief

router = APIRouter()


@router.post("/session-retro")
async def session_retro(req: CoachRetroRequest, repo=Depends(get_repo)):
    try:
        return {"brief": create_coach_brief(repo, req.model_dump())}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))


@router.post("/audit-agent")
async def audit_agent(req: CoachAgentAuditRequest, repo=Depends(get_repo)):
    try:
        return {"brief": audit_agent_failure(repo, req.model_dump())}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))


@router.get("/briefs")
async def list_briefs(repo=Depends(get_repo)):
    return {"briefs": coach_briefs(repo)}
