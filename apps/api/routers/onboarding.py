"""First-run onboarding and readiness API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "first_run_onboarding_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.goals import GoalOnboardingService

    return GoalOnboardingService(repo.root)


@router.get("/state", response_model=dict[str, Any])
async def state(profile_id: str = Query(default=""), repo=Depends(get_repo)):
    _check_flag(repo, "first_run_onboarding_enabled")
    return _service(repo).onboarding_state(profile_id=profile_id)


@router.post("/step", response_model=dict[str, Any])
async def complete_step(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "first_run_onboarding_enabled")
    return _service(repo).complete_step(
        profile_id=str(req.get("profile_id") or ""),
        step_id=str(req.get("step_id") or req.get("step") or ""),
    )


@router.post("/skip-step", response_model=dict[str, Any])
async def skip_step(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "first_run_onboarding_enabled")
    return _service(repo).skip_step(
        profile_id=str(req.get("profile_id") or ""),
        step_id=str(req.get("step_id") or req.get("step") or ""),
    )


@router.post("/generate-day1-plan", response_model=dict[str, Any])
async def generate_day1_plan(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "day1_plan_enabled")
    req = req or {}
    return _service(repo).generate_day1_plan(
        profile_id=str(req.get("profile_id") or ""),
        goal_id=str(req.get("goal_id") or ""),
    )


@router.get("/readiness", response_model=dict[str, Any])
async def readiness(profile_id: str = Query(default=""), repo=Depends(get_repo)):
    _check_flag(repo, "onboarding_readiness_enabled")
    return _service(repo).readiness(profile_id=profile_id)


@router.post("/reset", response_model=dict[str, Any])
async def reset(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "first_run_onboarding_enabled")
    req = req or {}
    return _service(repo).reset_onboarding(profile_id=str(req.get("profile_id") or ""))
