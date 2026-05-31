"""Exam profile discovery and durable active-profile selection."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo

router = APIRouter()


@router.get("")
async def list_profiles():
    from app.exam_profile import list_available_profiles

    return {"profiles": list_available_profiles()}


@router.get("/active")
async def get_active_profile(repo=Depends(get_repo)):
    from app.exam_profile import get_profile

    return {"profile": asdict(get_profile(repo.root, refresh=True))}


@router.put("/active")
async def update_active_profile(payload: dict, repo=Depends(get_repo)):
    from app.exam_profile import load_profile, set_profile

    profile_name = str(payload.get("profile_name", "")).strip()
    try:
        profile = load_profile(profile_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    (repo.system_root / "active_profile.txt").write_text(profile_name, encoding="utf-8")
    set_profile(profile)
    return {"profile": asdict(profile)}
