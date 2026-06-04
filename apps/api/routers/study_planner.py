"""Adaptive Study Planner API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo
from schemas import (
    StudyPlannerBlockCompleteRequest,
    StudyPlannerBlockSkipRequest,
    StudyPlannerGenerateRequest,
)

router = APIRouter()


def _check_flag(repo, flag_name: str = "study_planner_enabled") -> None:
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.study_planner import StudyPlannerService
    return StudyPlannerService(repo.root)


@router.post("/generate", response_model=dict[str, Any])
async def generate_study_plan(req: StudyPlannerGenerateRequest, repo=Depends(get_repo)):
    """Generate an energy-aware, correct-only daily study plan."""
    _check_flag(repo, "study_planner_enabled")
    _check_flag(repo, "adaptive_session_orchestrator_enabled")
    _check_flag(repo, "energy_aware_planning_enabled")
    try:
        plan = _service(repo).generate_plan(
            profile_id=req.profile_id,
            plan_date=req.plan_date or None,
            energy_mode=req.energy_mode,
            available_minutes=req.available_minutes,
            goal=req.goal or None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return plan.as_dict()


@router.get("/today", response_model=dict[str, Any])
async def get_today_plan(
    profile_id: str = Query(default="default"),
    plan_date: str = Query(default="", alias="date"),
    repo=Depends(get_repo),
):
    """Return the latest generated plan for today, or a safe default plan."""
    _check_flag(repo, "study_planner_enabled")
    return _service(repo).today(profile_id=profile_id, plan_date=plan_date or None).as_dict()


@router.get("/plans/{plan_id}", response_model=dict[str, Any])
async def get_study_plan(plan_id: str, repo=Depends(get_repo)):
    """Return one adaptive study plan."""
    _check_flag(repo, "study_planner_enabled")
    plan = _service(repo).get_plan(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Study plan not found")
    return plan.as_dict()


@router.post("/plans/{plan_id}/activate", response_model=dict[str, Any])
async def activate_study_plan(plan_id: str, repo=Depends(get_repo)):
    """Mark a generated plan active."""
    _check_flag(repo, "study_planner_enabled")
    try:
        return _service(repo).activate_plan(plan_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study plan not found: {exc.args[0]}") from exc


@router.post("/blocks/{block_id}/start", response_model=dict[str, Any])
async def start_study_block(block_id: str, repo=Depends(get_repo)):
    """Start one plan block."""
    _check_flag(repo, "study_planner_enabled")
    try:
        plan, block = _service(repo).start_block(block_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study block not found: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"plan": plan.as_dict(), "block": block.as_dict()}


@router.post("/blocks/{block_id}/complete", response_model=dict[str, Any])
async def complete_study_block(block_id: str, req: StudyPlannerBlockCompleteRequest, repo=Depends(get_repo)):
    """Complete one plan block and update the plan summary."""
    _check_flag(repo, "study_planner_enabled")
    try:
        plan, block = _service(repo).complete_block(
            block_id,
            outcome=req.outcome,
            actual_minutes=req.actual_minutes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study block not found: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"plan": plan.as_dict(), "block": block.as_dict()}


@router.post("/blocks/{block_id}/skip", response_model=dict[str, Any])
async def skip_study_block(block_id: str, req: StudyPlannerBlockSkipRequest, repo=Depends(get_repo)):
    """Skip one plan block and keep the reason for retro."""
    _check_flag(repo, "study_planner_enabled")
    try:
        plan, block = _service(repo).skip_block(block_id, reason=req.reason)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study block not found: {exc.args[0]}") from exc
    return {"plan": plan.as_dict(), "block": block.as_dict()}


@router.post("/plans/{plan_id}/complete", response_model=dict[str, Any])
async def complete_study_plan(plan_id: str, repo=Depends(get_repo)):
    """Complete a plan and generate a local retro summary."""
    _check_flag(repo, "study_planner_enabled")
    _check_flag(repo, "study_plan_retro_enabled")
    try:
        return _service(repo).complete_plan(plan_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study plan not found: {exc.args[0]}") from exc


@router.get("/history", response_model=dict[str, Any])
async def list_study_plan_history(
    profile_id: str = Query(default="default"),
    limit: int = Query(default=50, ge=1, le=200),
    repo=Depends(get_repo),
):
    """List recently generated adaptive study plans."""
    _check_flag(repo, "study_planner_enabled")
    plans = _service(repo).history(profile_id=profile_id, limit=limit)
    return {"count": len(plans), "plans": plans}
