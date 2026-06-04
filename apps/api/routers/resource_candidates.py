from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from deps import get_repo

router = APIRouter()


def _check_flag(repo) -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not (flags.enabled("resource_quality_gate") and flags.enabled("resource_candidate_queue")):
        raise HTTPException(
            status_code=403,
            detail="resource candidate queue is disabled by feature flags",
        )


class CandidateEnqueueRequest(BaseModel):
    document_id: str


class CandidateReviewRequest(BaseModel):
    review_note: str = ""


@router.get("")
async def list_resource_candidates(
    status_filter: str = Query(default="", alias="status"),
    lane: str = Query(default=""),
    repo=Depends(get_repo),
):
    _check_flag(repo)
    from app.resource_promotion import list_candidates

    return {"candidates": list_candidates(repo, status=status_filter, lane=lane)}


@router.post("/enqueue", status_code=status.HTTP_201_CREATED)
async def enqueue_resource_candidate(request: CandidateEnqueueRequest, repo=Depends(get_repo)):
    _check_flag(repo)
    from app.resource_promotion import queue_document_candidate

    try:
        return queue_document_candidate(repo, document_id=request.document_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Resource document not found: {request.document_id}") from exc


@router.post("/{candidate_id}/rescore")
async def rescore_resource_candidate(candidate_id: str, repo=Depends(get_repo)):
    _check_flag(repo)
    from app.resource_promotion import rescore_candidate

    try:
        return rescore_candidate(repo, candidate_id=candidate_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Resource candidate not found: {candidate_id}") from exc


@router.post("/{candidate_id}/approve")
async def approve_resource_candidate(candidate_id: str, request: CandidateReviewRequest, repo=Depends(get_repo)):
    _check_flag(repo)
    from app.resource_promotion import review_candidate

    try:
        return review_candidate(repo, candidate_id=candidate_id, action="approve", review_note=request.review_note)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Resource candidate not found: {candidate_id}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{candidate_id}/reject")
async def reject_resource_candidate(candidate_id: str, request: CandidateReviewRequest, repo=Depends(get_repo)):
    _check_flag(repo)
    from app.resource_promotion import review_candidate

    try:
        return review_candidate(repo, candidate_id=candidate_id, action="reject", review_note=request.review_note)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Resource candidate not found: {candidate_id}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
