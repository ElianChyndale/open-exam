"""Unified Focus Session API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from deps import get_repo

router = APIRouter()


class FocusStartRequest(BaseModel):
    profile_id: str = "default"
    plan_id: str | None = None
    source: str = "today_plan"
    force_new: bool = False


class FocusStepCompleteRequest(BaseModel):
    outcome: str = Field("recalled")
    actual_minutes: int | None = Field(default=None, ge=0)
    notes: str = ""


class FocusStepSkipRequest(BaseModel):
    reason: str = ""


class FocusAbandonRequest(BaseModel):
    reason: str = ""


def _check_flag(repo, flag_name: str = "focus_session_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.focus_session import FocusSessionService

    return FocusSessionService(repo.root)


@router.post("/start", response_model=dict[str, Any])
async def start_focus_session(req: FocusStartRequest, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    _check_flag(repo, "unified_study_flow_enabled")
    try:
        return _service(repo).start(
            profile_id=req.profile_id,
            plan_id=req.plan_id,
            source=req.source,
            force_new=req.force_new,
        ).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study plan not found: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/current", response_model=dict[str, Any])
async def get_current_focus_session(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    session = _service(repo).current(profile_id=profile_id or "default")
    return {"focus_session": session.as_dict() if session else None}


@router.get("/{focus_id}", response_model=dict[str, Any])
async def get_focus_session(focus_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    session = _service(repo).get(focus_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Focus session not found")
    return session.as_dict()


@router.post("/{focus_id}/steps/{step_id}/start", response_model=dict[str, Any])
async def start_focus_step(focus_id: str, step_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    try:
        return _service(repo).start_step(focus_id, step_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Focus item not found: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{focus_id}/steps/{step_id}/complete", response_model=dict[str, Any])
async def complete_focus_step(focus_id: str, step_id: str, req: FocusStepCompleteRequest, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    try:
        return _service(repo).complete_step(
            focus_id,
            step_id,
            outcome=req.outcome,
            actual_minutes=req.actual_minutes,
            notes=req.notes,
        ).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Focus item not found: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{focus_id}/steps/{step_id}/skip", response_model=dict[str, Any])
async def skip_focus_step(focus_id: str, step_id: str, req: FocusStepSkipRequest, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    try:
        return _service(repo).skip_step(focus_id, step_id, reason=req.reason).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Focus item not found: {exc.args[0]}") from exc


@router.post("/{focus_id}/complete", response_model=dict[str, Any])
async def complete_focus_session(focus_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    try:
        return _service(repo).complete(focus_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Focus session not found: {exc.args[0]}") from exc


@router.post("/{focus_id}/abandon", response_model=dict[str, Any])
async def abandon_focus_session(focus_id: str, req: FocusAbandonRequest, repo=Depends(get_repo)):
    _check_flag(repo, "focus_session_enabled")
    try:
        return _service(repo).abandon(focus_id, reason=req.reason).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Focus session not found: {exc.args[0]}") from exc
