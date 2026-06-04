from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from pydantic import BaseModel

from deps import get_repo

router = APIRouter()


class QuarantineActionRequest(BaseModel):
    action: str
    reviewer_notes: str = ""
    edited_payload: dict[str, Any] | None = None


@router.get("/sources")
async def list_sources(repo=Depends(get_repo)):
    from app.feature_flags import FeatureFlags
    if not FeatureFlags.load(repo.root).enabled("knowledge_pdf_ingestion"):
        return {"enabled": False, "sources": []}

    from app.knowledge_source_workflows import list_sources as _list_sources
    return {"enabled": True, "sources": _list_sources(repo)}


@router.post("/sources/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile,
    subject: str = "",
    module_id: str = "",
    module_title: str = "",
    repo=Depends(get_repo),
):
    from app.feature_flags import FeatureFlags
    if not FeatureFlags.load(repo.root).enabled("knowledge_pdf_ingestion"):
        raise HTTPException(status_code=403, detail="Knowledge PDF ingestion is disabled.")

    from app.knowledge_source_workflows import ingest_pdf

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are supported.")

    temp_path = repo.root / ".system" / "tmp" / file.filename
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_bytes(await file.read())

    try:
        result = ingest_pdf(
            repo,
            temp_path,
            filename=file.filename,
            title=file.filename,
            subject=subject,
            module_id=module_id,
            module_title=module_title,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        if temp_path.exists():
            temp_path.unlink()


@router.get("/quarantine")
async def list_quarantine(repo=Depends(get_repo)):
    from app.feature_flags import FeatureFlags
    if not FeatureFlags.load(repo.root).enabled("knowledge_pdf_ingestion"):
        return {"enabled": False, "items": []}

    from app.knowledge_source_workflows import list_quarantine as _list_quarantine
    return {"enabled": True, "items": _list_quarantine(repo)}


@router.post("/quarantine/{quarantine_id}/resolve")
async def resolve_quarantine(
    quarantine_id: str,
    request: QuarantineActionRequest,
    repo=Depends(get_repo),
):
    from app.feature_flags import FeatureFlags
    if not FeatureFlags.load(repo.root).enabled("knowledge_pdf_ingestion"):
        raise HTTPException(status_code=403, detail="Knowledge PDF ingestion is disabled.")

    from app.knowledge_source_workflows import resolve_quarantine as _resolve_quarantine

    try:
        return _resolve_quarantine(
            repo,
            quarantine_id=quarantine_id,
            action=request.action,
            reviewer_notes=request.reviewer_notes,
            edited_payload=request.edited_payload,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
