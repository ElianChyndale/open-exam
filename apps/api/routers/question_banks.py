"""Private question import and quarantine review console."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import QuestionBankImport, QuestionReview
from services.practice_service import import_questions, quarantined_questions, review_question

router = APIRouter()


@router.post("/import")
async def import_question_bank(req: QuestionBankImport, repo=Depends(get_repo)):
    return import_questions(repo, req.source_name, [question.model_dump() for question in req.questions])


@router.get("/quarantine")
async def list_quarantine(repo=Depends(get_repo)):
    return {"questions": quarantined_questions(repo)}


@router.post("/{question_id}/review")
async def review_imported_question(question_id: str, req: QuestionReview, repo=Depends(get_repo)):
    try:
        question = review_question(repo, question_id, req.action, req.corrections)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    if question is None:
        raise HTTPException(status_code=404, detail=f"Unknown question: {question_id}")
    return {"question": question}
