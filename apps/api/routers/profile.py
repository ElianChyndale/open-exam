"""Learner profile API."""

from fastapi import APIRouter, Depends

from deps import get_repo
from schemas import ProfileUpdate
from services.daily_loop_service import get_profile, update_profile

router = APIRouter()


@router.get("")
async def read_profile(repo=Depends(get_repo)):
    return {"profile": get_profile(repo)}


@router.put("")
async def write_profile(req: ProfileUpdate, repo=Depends(get_repo)):
    return {"profile": update_profile(repo, req.model_dump())}
