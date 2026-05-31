"""Explicit import/export endpoints. No background synchronization."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import TransferImportRequest
from services.transfer_service import export_bundle, import_bundle

router = APIRouter()


@router.get("/export")
async def export(repo=Depends(get_repo)):
    return export_bundle(repo)


@router.post("/import")
async def import_data(req: TransferImportRequest, repo=Depends(get_repo)):
    try:
        if req.direction == "local-to-cloud":
            if not hasattr(repo, "push_bundle"):
                raise ValueError("OPENEXAM_MODE=supabase is required for cloud transfer")
            summary = repo.push_bundle(req.bundle or export_bundle(repo), req.organization_id, dry_run=req.dry_run)
        else:
            summary = import_bundle(repo, req.bundle, dry_run=req.dry_run)
        return {"summary": summary}
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
