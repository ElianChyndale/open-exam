"""Private question-bank import and quarantine review endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo, require_admin_user

router = APIRouter()


@router.post("/import")
async def import_bank(payload: dict, _: dict = Depends(require_admin_user), repo=Depends(get_repo)):
    from app.question_banks import import_questions

    return import_questions(repo, str(payload.get("source_file", "")), list(payload.get("questions", [])))


@router.get("/all")
async def list_all_questions(
    status: str = Query("", alias="status"),
    search: str = Query("", alias="search"),
    subject: str = Query("", alias="subject"),
    _: dict = Depends(require_admin_user),
    repo=Depends(get_repo),
):
    from app.question_banks import load_questions

    questions = load_questions(repo)
    if status:
        questions = [q for q in questions if q.get("verification_status") == status]
    if search:
        q = search.lower()
        questions = [
            qs for qs in questions
            if q in (qs.get("prompt") or "").lower()
            or q in (qs.get("subject") or "").lower()
            or q in (qs.get("chapter") or "").lower()
            or q in (qs.get("question_id") or "").lower()
        ]
    if subject:
        questions = [qs for qs in questions if qs.get("subject") == subject]
    return {"count": len(questions), "questions": questions}


@router.get("/quarantine")
async def list_quarantine(_: dict = Depends(require_admin_user), repo=Depends(get_repo)):
    from app.question_banks import load_questions

    questions = [
        question for question in load_questions(repo)
        if question.get("verification_status") == "quarantined"
    ]
    return {"count": len(questions), "questions": questions}


@router.post("/practice-sessions")
async def generate_practice(payload: dict, repo=Depends(get_repo)):
    from app.question_banks import generate_practice_session

    try:
        return generate_practice_session(repo, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/wrongbook")
async def list_wrongbook(sort_by: str = Query("priority", alias="sort"), repo=Depends(get_repo)):
    from app.question_banks import load_questions, load_wrongbook

    questions = load_questions(repo)
    wrongbook = load_wrongbook(repo)
    verified_ids = {q["question_id"] for q in questions if q.get("verification_status") in ("verified", "published")}
    result = []
    for qid, entry in wrongbook.items():
        if qid not in verified_ids:
            continue
        question = next((q for q in questions if q["question_id"] == qid), None)
        if not question:
            continue
        result.append({
            "question_id": qid,
            "wrong_count": entry.get("wrong_count", 0),
            "correct_retry_count": entry.get("correct_retry_count", 0),
            "priority": entry.get("priority", 50),
            "last_seen": entry.get("last_seen", ""),
            "subject": question.get("subject", ""),
            "chapter": question.get("chapter", ""),
            "prompt": question.get("prompt", "")[:120],
            "difficulty": question.get("difficulty", "unknown"),
            "knowledge_tags": question.get("knowledge_tags", []),
        })
    reverse = sort_by.startswith("-")
    key = sort_by.lstrip("-")
    result.sort(key=lambda x: x.get(key, 0) if isinstance(x.get(key, 0), (int, float)) else str(x.get(key, "")), reverse=reverse)
    return {"count": len(result), "items": result}


@router.get("/wrongbook/questions/{question_id}")
async def get_wrongbook_question(question_id: str, repo=Depends(get_repo)):
    from app.question_banks import load_questions, load_wrongbook, load_practice_attempts

    questions = load_questions(repo)
    question = next((q for q in questions if q["question_id"] == question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    wrongbook = load_wrongbook(repo)
    entry = wrongbook.get(question_id, {})
    attempts = [a for a in load_practice_attempts(repo) if a.get("question_id") == question_id][-20:]
    return {
        "question": question,
        "wrongbook": entry,
        "recent_attempts": attempts,
    }


@router.get("/practice-sessions/{session_id}/questions/{question_id}")
async def get_practice_session_question(session_id: str, question_id: str, repo=Depends(get_repo)):
    from app.question_banks import get_practice_question_display

    try:
        return get_practice_question_display(repo, session_id, question_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/practice-sessions/{session_id}/answer")
async def submit_practice_session_answer(session_id: str, payload: dict, repo=Depends(get_repo)):
    from app.question_banks import submit_practice_answer

    try:
        return submit_practice_answer(repo, {**payload, "session_id": session_id})
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{question_id}/review")
async def review_import(question_id: str, payload: dict, _: dict = Depends(require_admin_user), repo=Depends(get_repo)):
    from app.question_banks import review_question

    try:
        question = review_question(repo, question_id, str(payload.get("action", "")), dict(payload.get("patch", {})))
    except PermissionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"question": question}
