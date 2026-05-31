"""Interactive retrieval review sessions."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import ReviewResponseSubmit, ReviewSessionCreate
from services.daily_loop_service import start_review_session, submit_review_response

router = APIRouter()


@router.post("")
async def create_review_session(req: ReviewSessionCreate, repo=Depends(get_repo)):
    return start_review_session(repo, req.max_items)


@router.post("/{session_id}/responses")
async def record_review_response(session_id: str, req: ReviewResponseSubmit, repo=Depends(get_repo)):
    response = submit_review_response(repo, session_id, req.model_dump())
    if response is None:
        raise HTTPException(status_code=404, detail="Unknown review session or prompt")
    return response
