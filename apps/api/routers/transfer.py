"""Explicit local import endpoint. OpenExam never synchronizes silently."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo

router = APIRouter()


@router.post("")
async def import_portable_backup(payload: dict, repo=Depends(get_repo)):
    from app.sync_service import import_all, preview_import

    data = dict(payload.get("data", {}))
    try:
        if payload.get("dry_run", True):
            return preview_import(repo, data)
        return {"dry_run": False, "imported": import_all(repo, data)}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/sync-v2")
async def import_sync_v2_bundle(payload: dict, repo=Depends(get_repo)):
    from app.sync_service import import_sync_v2

    try:
        return import_sync_v2(repo, dict(payload.get("data", {})), dry_run=bool(payload.get("dry_run", True)))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
