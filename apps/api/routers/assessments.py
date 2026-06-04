"""Adaptive Assessment API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo
from schemas import (
    AssessmentAnswerRequest,
    AssessmentGenerateRequest,
    AssessmentSelfGradeRequest,
)

router = APIRouter()


def _check_flag(repo, flag_name: str = "adaptive_assessment_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.assessments import AssessmentService

    return AssessmentService(repo.root)


@router.post("/generate", response_model=dict[str, Any])
async def generate_assessment(req: AssessmentGenerateRequest, repo=Depends(get_repo)):
    """Generate a deterministic, evidence-backed assessment session."""
    _check_flag(repo, "adaptive_assessment_enabled")
    if req.mode in {"interleaving_drill", "mixed_exam_drill"}:
        _check_flag(repo, "interleaving_drill_enabled")
    return _service(repo).generate(
        profile_id=req.profile_id,
        mode=req.mode,
        target_minutes=req.target_minutes,
        question_count=req.question_count,
        difficulty=req.difficulty,
        focus=req.focus,
    ).as_dict()


@router.get("/recommendations", response_model=dict[str, Any])
async def assessment_recommendations(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return recommended assessment modes from current signals."""
    _check_flag(repo, "adaptive_assessment_enabled")
    return _service(repo).recommendations(profile_id=profile_id)


@router.get("", response_model=dict[str, Any])
async def list_assessments(
    profile_id: str = Query(default="default"),
    limit: int = Query(default=50, ge=1, le=200),
    repo=Depends(get_repo),
):
    """List generated assessment sessions."""
    _check_flag(repo, "adaptive_assessment_enabled")
    sessions = _service(repo).list_sessions(profile_id=profile_id, limit=limit)
    return {"profile_id": profile_id or "default", "count": len(sessions), "assessments": sessions}


@router.get("/{assessment_id}", response_model=dict[str, Any])
async def get_assessment(assessment_id: str, repo=Depends(get_repo)):
    """Return one assessment session."""
    _check_flag(repo, "adaptive_assessment_enabled")
    session = _service(repo).get(assessment_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return session.as_dict()


@router.post("/{assessment_id}/start", response_model=dict[str, Any])
async def start_assessment(assessment_id: str, repo=Depends(get_repo)):
    """Mark an assessment active."""
    _check_flag(repo, "adaptive_assessment_enabled")
    try:
        return _service(repo).start(assessment_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Assessment not found: {exc.args[0]}") from exc


@router.post("/questions/{question_id}/answer", response_model=dict[str, Any])
async def answer_assessment_question(question_id: str, req: AssessmentAnswerRequest, repo=Depends(get_repo)):
    """Submit an answer and receive correct-only feedback."""
    _check_flag(repo, "adaptive_assessment_enabled")
    _check_flag(repo, "assessment_feedback_correct_only_enabled")
    try:
        return _service(repo).answer_question(
            question_id,
            answer_text=req.answer_text,
            selected_choice=req.selected_choice,
            confidence_before=req.confidence_before,
            time_spent_seconds=req.time_spent_seconds,
        ).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Assessment question not found: {exc.args[0]}") from exc


@router.post("/questions/{question_id}/self-grade", response_model=dict[str, Any])
async def self_grade_assessment_question(question_id: str, req: AssessmentSelfGradeRequest, repo=Depends(get_repo)):
    """Apply manual self-grade fallback to an assessment response."""
    _check_flag(repo, "adaptive_assessment_enabled")
    try:
        return _service(repo).self_grade(question_id, grade=req.grade, confidence_after=req.confidence_after).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Assessment question not found: {exc.args[0]}") from exc


@router.post("/{assessment_id}/complete", response_model=dict[str, Any])
async def complete_assessment(assessment_id: str, repo=Depends(get_repo)):
    """Complete an assessment and generate a correct-only retro."""
    _check_flag(repo, "adaptive_assessment_enabled")
    _check_flag(repo, "assessment_transfer_gap_integration_enabled")
    try:
        return _service(repo).complete(assessment_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Assessment not found: {exc.args[0]}") from exc


@router.get("/{assessment_id}/retro", response_model=dict[str, Any])
async def get_assessment_retro(assessment_id: str, repo=Depends(get_repo)):
    """Return correct-only assessment retro summary."""
    _check_flag(repo, "adaptive_assessment_enabled")
    try:
        return _service(repo).retro(assessment_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Assessment not found: {exc.args[0]}") from exc
