"""Grounded Tutor Copilot API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "tutor_copilot_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.tutor import TutorService

    return TutorService(repo.root)


@router.post("/conversations", response_model=dict[str, Any])
async def create_conversation(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "tutor_conversation_memory_enabled")
    req = req or {}
    return _service(repo).create_conversation(
        profile_id=str(req.get("profile_id") or "default"),
        mode=req.get("mode") or "general",
        title=req.get("title"),
    )


@router.get("/conversations", response_model=dict[str, Any])
async def conversations(
    profile_id: str = Query(default="default"),
    include_archived: bool = Query(default=False),
    repo=Depends(get_repo),
):
    _check_flag(repo, "tutor_conversation_memory_enabled")
    return _service(repo).list_conversations(profile_id=profile_id or "default", include_archived=include_archived)


@router.get("/conversations/{conversation_id}", response_model=dict[str, Any])
async def conversation(conversation_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "tutor_conversation_memory_enabled")
    payload = _service(repo).get_conversation(conversation_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Tutor conversation not found")
    return payload


@router.post("/conversations/{conversation_id}/message", response_model=dict[str, Any])
async def add_message(conversation_id: str, req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "tutor_conversation_memory_enabled")
    try:
        return _service(repo).add_message(conversation_id, content=str(req.get("content") or ""))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Tutor conversation not found: {exc.args[0]}") from exc


@router.post("/ask", response_model=dict[str, Any])
async def ask(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "tutor_copilot_enabled")
    _check_flag(repo, "grounded_tutor_retrieval_enabled")
    return _service(repo).ask(
        profile_id=str(req.get("profile_id") or "default"),
        mode=req.get("mode") or "general",
        query=str(req.get("query") or ""),
        context_node_id=req.get("context_node_id"),
    )


@router.get("/search-context", response_model=dict[str, Any])
async def search_context(
    profile_id: str = Query(default="default"),
    q: str = Query(default=""),
    mode: str = Query(default="general"),
    limit: int = Query(default=8, ge=1, le=20),
    repo=Depends(get_repo),
):
    _check_flag(repo, "grounded_tutor_retrieval_enabled")
    return _service(repo).search_context_payload(profile_id=profile_id or "default", query=q, mode=mode, limit=limit)


@router.get("/suggestions", response_model=dict[str, Any])
async def suggestions(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "tutor_copilot_enabled")
    return _service(repo).suggestions(profile_id=profile_id or "default")


@router.post("/conversations/{conversation_id}/archive", response_model=dict[str, Any])
async def archive_conversation(conversation_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "tutor_conversation_memory_enabled")
    try:
        return _service(repo).archive_conversation(conversation_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Tutor conversation not found: {exc.args[0]}") from exc
