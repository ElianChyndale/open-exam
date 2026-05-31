"""Private question-bank import and quarantine review endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo

router = APIRouter()


@router.post("/import")
async def import_bank(payload: dict, repo=Depends(get_repo)):
    from app.question_banks import import_questions

    return import_questions(repo, str(payload.get("source_file", "")), list(payload.get("questions", [])))


@router.get("/quarantine")
async def list_quarantine(repo=Depends(get_repo)):
    from app.question_banks import load_questions

    questions = [
        question for question in load_questions(repo)
        if question.get("verification_status") == "quarantined"
    ]
    return {"count": len(questions), "questions": questions}


@router.post("/{question_id}/review")
async def review_import(question_id: str, payload: dict, repo=Depends(get_repo)):
    from app.question_banks import review_question

    try:
        question = review_question(repo, question_id, str(payload.get("action", "")), dict(payload.get("patch", {})))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"question": question}
