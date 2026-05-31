"""Mixed practice sessions and evidence-backed remediation."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import PracticeAnswer, PracticeSessionCreate
from services.practice_service import answer_practice_question, start_practice_session

router = APIRouter()


@router.post("")
async def create_practice_session(req: PracticeSessionCreate, repo=Depends(get_repo)):
    return start_practice_session(repo, req.max_items, req.topic)


@router.post("/{session_id}/answers")
async def answer_question(session_id: str, req: PracticeAnswer, repo=Depends(get_repo)):
    try:
        result = answer_practice_question(repo, session_id, req.model_dump())
    except PermissionError as error:
        raise HTTPException(status_code=409, detail=str(error))
    if result is None:
        raise HTTPException(status_code=404, detail="Unknown practice session or question")
    return result
