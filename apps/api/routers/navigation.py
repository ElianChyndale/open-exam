"""Premium navigation and cockpit API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "premium_cockpit_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.navigation import NavigationService

    return NavigationService(repo.root)


@router.get("/summary", response_model=dict[str, Any])
async def summary(repo=Depends(get_repo)):
    _check_flag(repo, "progressive_disclosure_enabled")
    return _service(repo).summary()


@router.get("/tools", response_model=dict[str, Any])
async def tools(repo=Depends(get_repo)):
    _check_flag(repo, "advanced_tools_hub_enabled")
    return _service(repo).tools()


@router.get("/cockpit", response_model=dict[str, Any])
async def cockpit(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "premium_cockpit_enabled")
    return _service(repo).cockpit(profile_id=profile_id or "default")
