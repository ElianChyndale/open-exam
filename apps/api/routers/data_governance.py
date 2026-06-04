"""Data governance, backup, restore, and privacy controls API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "data_governance_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.data_governance import DataGovernanceService

    return DataGovernanceService(repo.root)


@router.get("/inventory", response_model=dict[str, Any])
async def inventory(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo)
    return _service(repo).inventory(profile_id=profile_id or "default")


@router.get("/snapshots", response_model=dict[str, Any])
async def snapshots(repo=Depends(get_repo)):
    _check_flag(repo, "backup_restore_enabled")
    return {"snapshots": _service(repo).snapshots()}


@router.post("/snapshots", response_model=dict[str, Any])
async def create_snapshot(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "backup_restore_enabled")
    req = req or {}
    try:
        return _service(repo).export_backup(
            profile_id=str(req.get("profile_id") or "default"),
            mode=str(req.get("mode") or "safe"),
            categories=list(req.get("categories") or []),
            include_raw_diagnostics=bool(req.get("include_raw_diagnostics")),
            label=req.get("label"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/snapshots/{snapshot_id}", response_model=dict[str, Any])
async def snapshot(snapshot_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "backup_restore_enabled")
    row = _service(repo).get_snapshot(snapshot_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return row


@router.post("/export", response_model=dict[str, Any])
async def export_backup(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "safe_export_enabled")
    req = req or {}
    mode = str(req.get("mode") or "safe")
    if mode == "full":
        _check_flag(repo, "full_export_enabled")
    try:
        return _service(repo).export_backup(
            profile_id=str(req.get("profile_id") or "default"),
            mode=mode,
            categories=list(req.get("categories") or []),
            include_raw_diagnostics=bool(req.get("include_raw_diagnostics")),
            label=req.get("label"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/restore/dry-run", response_model=dict[str, Any])
async def restore_dry_run(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "backup_restore_enabled")
    return _service(repo).restore_dry_run(
        profile_id=str(req.get("profile_id") or "default"),
        file_path=str(req.get("file_path") or ""),
        mode=str(req.get("mode") or "dry_run"),
        categories=list(req.get("categories") or []),
    )


@router.post("/restore", response_model=dict[str, Any])
async def restore(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "backup_restore_enabled")
    try:
        return _service(repo).restore_backup(
            profile_id=str(req.get("profile_id") or "default"),
            file_path=str(req.get("file_path") or ""),
            mode=str(req.get("mode") or "merge"),
            categories=list(req.get("categories") or []),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/rollback/{snapshot_id}", response_model=dict[str, Any])
async def rollback(snapshot_id: str, req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    _check_flag(repo, "snapshot_rollback_enabled")
    req = req or {}
    try:
        return _service(repo).rollback(
            snapshot_id=snapshot_id,
            profile_id=str(req.get("profile_id") or "default"),
            categories=list(req.get("categories") or []),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/reset", response_model=dict[str, Any])
async def reset(req: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "category_reset_enabled")
    try:
        return _service(repo).reset_category(
            profile_id=str(req.get("profile_id") or "default"),
            category=str(req.get("category") or ""),
            confirmation=str(req.get("confirmation") or ""),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/privacy-report", response_model=dict[str, Any])
async def privacy_report(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "privacy_redaction_enabled")
    return _service(repo).privacy_report(profile_id=profile_id or "default")
