"""Ecosystem interoperability API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "interop_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.interop import InteropService

    return InteropService(repo.root)


@router.get("/artifacts", response_model=dict[str, Any])
async def artifacts(repo=Depends(get_repo)):
    _check_flag(repo)
    return _service(repo).list_artifacts()


@router.get("/artifacts/{artifact_id}", response_model=dict[str, Any])
async def artifact(artifact_id: str, repo=Depends(get_repo)):
    _check_flag(repo)
    payload = _service(repo).get_artifact(artifact_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Interop artifact not found")
    return payload


@router.post("/export/anki", response_model=dict[str, Any])
async def export_anki(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "anki_interop_enabled")
    return _service(repo).export_anki(req or {})


@router.post("/import/anki/preview", response_model=dict[str, Any])
async def import_anki_preview(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "anki_interop_enabled")
    try:
        return _service(repo).preview_anki_import(req)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Import file not found: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/import/anki/commit", response_model=dict[str, Any])
async def import_anki_commit(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "anki_interop_enabled")
    try:
        return _service(repo).commit_anki_import(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Import preview not found: {exc.args[0]}") from exc


@router.post("/export/markdown", response_model=dict[str, Any])
async def export_markdown(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "markdown_interop_enabled")
    return _service(repo).export_markdown(req or {})


@router.post("/import/markdown/preview", response_model=dict[str, Any])
async def import_markdown_preview(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "markdown_interop_enabled")
    try:
        return _service(repo).preview_markdown_import(req)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Import file not found: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/import/markdown/commit", response_model=dict[str, Any])
async def import_markdown_commit(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "markdown_interop_enabled")
    try:
        return _service(repo).commit_markdown_import(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Import preview not found: {exc.args[0]}") from exc


@router.post("/export/calendar", response_model=dict[str, Any])
async def export_calendar(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "calendar_export_enabled")
    try:
        return _service(repo).export_calendar(req)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Study plan not found: {exc.args[0]}") from exc


@router.post("/export/learning-records", response_model=dict[str, Any])
async def export_learning_records(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "learning_record_export_enabled")
    return _service(repo).export_learning_records(req or {})


@router.get("/privacy-report", response_model=dict[str, Any])
async def privacy_report(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "interop_safe_mode_enabled")
    return _service(repo).privacy_report(profile_id=profile_id or "default")
