from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from deps import get_repo

router = APIRouter()


def _kernel(repo):
    from language_science.lexical_kernel import LexicalKernel

    return LexicalKernel(repo.root)


def _check_flag(repo, flag_name: str = "dictionary_kernel_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not (flags.enabled("language_os_enabled") or flags.enabled("language_os")):
        raise HTTPException(status_code=403, detail="language_os_enabled feature flag is disabled")
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _check_dictionary_file_import(repo) -> None:
    from app.feature_flags import FeatureFlags

    _check_flag(repo, "dictionary_kernel_enabled")
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("dictionary_file_import_enabled"):
        raise HTTPException(status_code=403, detail="dictionary_file_import_enabled feature flag is disabled")
    if not flags.enabled("file_ingestion_enabled"):
        raise HTTPException(status_code=403, detail="file_ingestion_enabled feature flag is disabled")


def _pdf_extraction_enabled(repo) -> bool:
    from app.feature_flags import FeatureFlags

    return FeatureFlags.load(repo.root).enabled("pdf_text_extraction_enabled")


async def _read_upload(file: UploadFile) -> bytes:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")
    return data


def _raise(exc: Exception) -> None:
    if isinstance(exc, KeyError):
        raise HTTPException(status_code=404, detail=f"LanguageOS dictionary resource not found: {exc.args[0]}") from exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    raise exc


@router.post("/dictionaries/import-text", status_code=status.HTTP_201_CREATED)
async def import_dictionary_text(payload: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    try:
        return _kernel(repo).import_text(
            profile_id=str(payload.get("profile_id", "default")),
            title=str(payload.get("title", "Imported dictionary")),
            dictionary_type=str(payload.get("dictionary_type", "custom_monolingual")),
            text=str(payload.get("text", "")),
        )
    except Exception as exc:
        _raise(exc)


@router.post("/dictionaries/import-json", status_code=status.HTTP_201_CREATED)
async def import_dictionary_json(payload: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    try:
        return _kernel(repo).import_json(
            profile_id=str(payload.get("profile_id", "default")),
            title=str(payload.get("title", "Imported dictionary")),
            dictionary_type=str(payload.get("dictionary_type", "custom_monolingual")),
            entries=payload.get("entries", payload.get("content", [])),
        )
    except Exception as exc:
        _raise(exc)


@router.post("/dictionaries/import-csv", status_code=status.HTTP_201_CREATED)
async def import_dictionary_csv(payload: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    try:
        return _kernel(repo).import_csv(
            profile_id=str(payload.get("profile_id", "default")),
            title=str(payload.get("title", "Imported dictionary")),
            dictionary_type=str(payload.get("dictionary_type", "custom_monolingual")),
            csv_text=str(payload.get("csv_text", payload.get("content", ""))),
        )
    except Exception as exc:
        _raise(exc)


@router.post("/dictionaries/import-file", status_code=status.HTTP_201_CREATED)
async def import_dictionary_file(
    file: UploadFile = File(...),
    profile_id: str = Form(default="default"),
    title: str = Form(default=""),
    dictionary_type: str = Form(default="custom_monolingual"),
    force_reimport: bool = Form(default=False),
    repo=Depends(get_repo),
):
    _check_dictionary_file_import(repo)
    from study_science.file_ingestion import FileIngestionService

    service = FileIngestionService(repo.root)
    try:
        imported_file = service.import_bytes(
            profile_id=profile_id,
            filename=file.filename or "dictionary",
            content_type=file.content_type or "",
            data=await _read_upload(file),
            force_reimport=force_reimport,
            pdf_text_extraction_enabled=_pdf_extraction_enabled(repo),
        )
        file_payload = imported_file["file"]
        if file_payload["extraction_status"] == "duplicate" and file_payload.get("dictionary_id"):
            existing = _kernel(repo).get_dictionary(file_payload["dictionary_id"])
            if existing is None:
                raise KeyError(file_payload["dictionary_id"])
            return {
                "duplicate": True,
                "file": file_payload,
                "warnings": imported_file.get("warnings", []),
                **existing,
            }
        if file_payload["extraction_status"] != "extracted":
            return {
                "duplicate": bool(imported_file.get("duplicate")),
                "file": file_payload,
                "warnings": imported_file.get("warnings", []),
                "dictionary": None,
                "asset_count": 0,
                "lexical_assets": [],
            }

        content = service.combined_text(file_payload["file_id"])
        display_title = title.strip() or file_payload["filename"]
        source_type = str(file_payload.get("source_type") or "")
        kernel = _kernel(repo)
        if source_type == "json_dictionary":
            imported = kernel.import_json(
                profile_id=profile_id,
                title=display_title,
                dictionary_type=dictionary_type,
                entries=json.loads(content),
            )
        elif source_type == "csv_dictionary":
            imported = kernel.import_csv(
                profile_id=profile_id,
                title=display_title,
                dictionary_type=dictionary_type,
                csv_text=content,
            )
        else:
            imported = kernel.import_text(
                profile_id=profile_id,
                title=display_title,
                dictionary_type=dictionary_type,
                text=content,
            )
        attached = kernel.attach_file_refs(imported["dictionary"]["dictionary_id"], file_payload.get("source_refs", []))
        file_payload = service.update_links(
            file_payload["file_id"],
            dictionary_id=attached["dictionary"]["dictionary_id"],
            source_refs=attached["dictionary"].get("source_refs", []),
        )
        return {
            "duplicate": bool(imported_file.get("duplicate") or imported.get("duplicate")),
            "file": file_payload,
            "warnings": imported_file.get("warnings", []),
            **attached,
        }
    except Exception as exc:
        _raise(exc)


@router.get("/dictionaries")
async def list_dictionaries(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    dictionaries = _kernel(repo).list_dictionaries(profile_id=profile_id)
    return {"count": len(dictionaries), "dictionaries": dictionaries}


@router.get("/dictionaries/{dictionary_id}")
async def get_dictionary(dictionary_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    result = _kernel(repo).get_dictionary(dictionary_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    return result


@router.post("/dictionaries/{dictionary_id}/score")
async def score_dictionary(dictionary_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_quality_gate_enabled")
    try:
        return _kernel(repo).score_dictionary(dictionary_id)
    except Exception as exc:
        _raise(exc)


@router.post("/dictionaries/{dictionary_id}/confirm")
async def confirm_dictionary(dictionary_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_quality_gate_enabled")
    try:
        return _kernel(repo).confirm_dictionary(dictionary_id)
    except Exception as exc:
        _raise(exc)


@router.post("/dictionaries/{dictionary_id}/reject")
async def reject_dictionary(dictionary_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_quality_gate_enabled")
    try:
        return _kernel(repo).reject_dictionary(dictionary_id)
    except Exception as exc:
        _raise(exc)


@router.get("/lexical-assets")
async def list_lexical_assets(
    profile_id: str = Query(default="default"),
    dictionary_id: str = Query(default=""),
    validation_status: str = Query(default=""),
    repo=Depends(get_repo),
):
    _check_flag(repo, "dictionary_kernel_enabled")
    assets = _kernel(repo).list_lexical_assets(
        profile_id=profile_id,
        dictionary_id=dictionary_id,
        validation_status=validation_status,
    )
    return {"count": len(assets), "assets": assets}


@router.get("/lexical-assets/{lexical_id}")
async def get_lexical_asset(lexical_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_kernel_enabled")
    asset = _kernel(repo).get_lexical_asset(lexical_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Lexical asset not found")
    return {"asset": asset}


@router.post("/lexical-assets/{lexical_id}/confirm")
async def confirm_lexical_asset(lexical_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_quality_gate_enabled")
    try:
        return _kernel(repo).confirm_lexical_asset(lexical_id)
    except Exception as exc:
        _raise(exc)


@router.post("/lexical-assets/{lexical_id}/reject")
async def reject_lexical_asset(lexical_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "dictionary_quality_gate_enabled")
    try:
        return _kernel(repo).reject_lexical_asset(lexical_id)
    except Exception as exc:
        _raise(exc)


@router.post("/review/generate-session")
async def generate_lexical_review_session(payload: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "lexical_review_enabled")
    try:
        session = _kernel(repo).generate_review_session(
            profile_id=str(payload.get("profile_id", "default")),
            max_units=int(payload.get("max_units", 12)),
        )
        return session.as_dict()
    except Exception as exc:
        _raise(exc)


@router.get("/review/sessions/{session_id}")
async def get_lexical_review_session(session_id: str, repo=Depends(get_repo)):
    _check_flag(repo, "lexical_review_enabled")
    session = _kernel(repo).get_review_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Lexical review session not found")
    return session.as_dict()


@router.post("/review/units/{unit_id}/complete")
async def complete_lexical_review_unit(unit_id: str, payload: dict[str, Any], repo=Depends(get_repo)):
    _check_flag(repo, "lexical_review_enabled")
    try:
        return _kernel(repo).complete_review_unit(
            unit_id,
            session_id=str(payload.get("session_id", "")),
            outcome=str(payload.get("outcome", "partial")),
            time_spent_seconds=int(payload.get("time_spent_seconds", 0)),
        )
    except Exception as exc:
        _raise(exc)
