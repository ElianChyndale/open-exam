from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_repo
from schemas import ConsentRecordRequest, PrivacyPurgeRequest

router = APIRouter()


@router.post("/consent", status_code=status.HTTP_201_CREATED)
async def create_consent(request: ConsentRecordRequest, repo=Depends(get_repo)):
    from app.roadmap_waves import record_consent

    return record_consent(repo, **request.model_dump())


@router.get("/export")
async def export_privacy_data(repo=Depends(get_repo)):
    from app.roadmap_waves import export_privacy_bundle

    return export_privacy_bundle(repo)


@router.post("/purge")
async def purge_privacy_data(request: PrivacyPurgeRequest, repo=Depends(get_repo)):
    from app.roadmap_waves import confirm_privacy_purge, request_privacy_purge

    try:
        if not request.confirmation_token:
            return request_privacy_purge(repo)
        return confirm_privacy_purge(repo, request.confirmation_token)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
