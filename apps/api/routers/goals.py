"""Goal profiles and safe local course packs API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "goal_profiles_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.goals import GoalOnboardingService

    return GoalOnboardingService(repo.root)


@router.get("/packs", response_model=dict[str, Any])
async def packs(repo=Depends(get_repo)):
    _check_flag(repo, "course_packs_enabled")
    return _service(repo).list_course_packs()


@router.post("", response_model=dict[str, Any])
async def create_goal(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "goal_profiles_enabled")
    try:
        return _service(repo).create_goal(req)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("", response_model=dict[str, Any])
async def goals(
    profile_id: str = Query(default=""),
    include_archived: bool = Query(default=False),
    repo=Depends(get_repo),
):
    _check_flag(repo, "goal_profiles_enabled")
    return _service(repo).list_goals(profile_id=profile_id, include_archived=include_archived)


@router.get("/{goal_id}", response_model=dict[str, Any])
async def goal(goal_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "goal_profiles_enabled")
    payload = _service(repo).get_goal(goal_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Goal profile not found")
    return payload


@router.post("/{goal_id}/activate", response_model=dict[str, Any])
async def activate(goal_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "goal_profiles_enabled")
    try:
        return _service(repo).activate_goal(goal_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Goal profile not found: {exc.args[0]}") from exc


@router.post("/{goal_id}/archive", response_model=dict[str, Any])
async def archive(goal_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "goal_profiles_enabled")
    try:
        return _service(repo).archive_goal(goal_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Goal profile not found: {exc.args[0]}") from exc


@router.patch("/{goal_id}", response_model=dict[str, Any])
async def patch(goal_id: str, req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "goal_profiles_enabled")
    try:
        return _service(repo).patch_goal(goal_id, req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Goal profile not found: {exc.args[0]}") from exc
