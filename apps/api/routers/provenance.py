from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_repo
from schemas import ProvenanceRecordRequest

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_provenance(request: ProvenanceRecordRequest, repo=Depends(get_repo)):
    from app.roadmap_waves import record_provenance

    return record_provenance(repo, **request.model_dump())


@router.get("/{entity_id}")
async def read_provenance(entity_id: str, repo=Depends(get_repo)):
    from app.roadmap_waves import get_provenance

    try:
        return get_provenance(repo, entity_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Provenance not found: {entity_id}") from exc
