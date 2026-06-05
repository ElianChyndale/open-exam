from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str) -> None:
    from app.feature_flags import FeatureFlags

    if not FeatureFlags.load(repo.root).enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


@router.get("/registry", response_model=dict)
async def skill_registry(repo=Depends(get_repo)):
    _check_flag(repo, "skill_reflection_enabled")
    from app.skill_registry import load_skill_registry

    skills = load_skill_registry(repo.root)
    return {"skills": [item.as_dict() for item in skills]}


@router.get("/{skill_id}/health", response_model=dict)
async def skill_health(skill_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "skill_reflection_enabled")
    from app.skill_upgrade import compute_skill_health

    return {"health": compute_skill_health(repo.root, skill_id).as_dict()}


@router.get("/upgrade-proposals", response_model=dict)
async def upgrade_proposals(repo=Depends(get_repo)):
    _check_flag(repo, "skill_upgrade_proposals_enabled")
    from app.skill_upgrade import load_upgrade_proposals

    return {"proposals": [item.as_dict() for item in load_upgrade_proposals(repo.root)]}
