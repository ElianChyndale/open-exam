"""Review Lab 2.0 API — per-unit interactive review endpoints.

Feature-flagged behind `daily_review_lab`. All endpoints operate on
ReviewLabSession objects persisted in `.system/memory/review/lab-sessions/`.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile

from deps import get_repo
from schemas import (
    FormulaImportTextRequest,
    FormulaLabGenerateRequest,
    MockRetroGenerateReviewRequest,
    MockRetroImportTextRequest,
    ResourceImportTextRequest,
    ResourcePromoteAssetsRequest,
    ReviewAssetImportTextRequest,
    ReviewLabCreateRequest,
    ReviewLabHintRequest,
    ReviewLabOutcomeRequest,
    ReviewLabUnitCompleteRequest,
    ReviewLabSessionResponse,
    ReviewLabReportResponse,
    SyllabusImportJsonRequest,
    SyllabusImportTextRequest,
)

router = APIRouter()


def _get_engine(repo):
    from study_science.review_lab import ReviewLabEngine
    return ReviewLabEngine(repo.root)


def _get_file_service(repo):
    from study_science.file_ingestion import FileIngestionService
    return FileIngestionService(repo.root)


def _check_flag(repo):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not (flags.enabled("daily_review_lab") or flags.enabled("daily_review_lab_enabled")):
        raise HTTPException(status_code=403, detail="daily_review_lab feature flag is disabled")


def _check_asset_ingestion_flag(repo):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("review_asset_ingestion_enabled"):
        raise HTTPException(status_code=403, detail="review_asset_ingestion_enabled feature flag is disabled")


def _check_formula_flag(repo):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not (flags.enabled("formula_lab") or flags.enabled("formula_lab_enabled")):
        raise HTTPException(status_code=403, detail="formula_lab_enabled feature flag is disabled")


def _check_syllabus_flag(repo):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("syllabus_coverage_enabled"):
        raise HTTPException(status_code=403, detail="syllabus_coverage_enabled feature flag is disabled")


def _check_mock_retro_flag(repo):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("mock_retro_enabled"):
        raise HTTPException(status_code=403, detail="mock_retro_enabled feature flag is disabled")


def _check_resource_flag(repo, flag_name: str = "resource_quality_gate_enabled"):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _check_file_ingestion_flag(repo, flag_name: str = "file_ingestion_enabled"):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _check_mission_control_flag(repo, flag_name: str = "mission_control_enabled"):
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _pdf_extraction_enabled(repo) -> bool:
    from app.feature_flags import FeatureFlags
    return FeatureFlags.load(repo.root).enabled("pdf_text_extraction_enabled")


async def _read_upload(file: UploadFile) -> bytes:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")
    return data


def _source_type_for_review_file(file_payload: dict[str, Any], requested: str = "") -> str:
    allowed = {"pdf_note", "markdown_note", "text_note", "manual"}
    if requested in allowed:
        return requested
    file_source_type = str(file_payload.get("source_type") or "")
    return file_source_type if file_source_type in allowed else "text_note"


@router.get("/mission-control", response_model=dict[str, Any])
async def get_mission_control(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return a correct-only cross-subsystem learning operations summary."""
    _check_mission_control_flag(repo, "mission_control_enabled")
    from study_science.mission_control import MissionControlService

    return MissionControlService(repo.root).summary(profile_id=profile_id)


@router.get("/route-registry", response_model=dict[str, Any])
async def get_route_registry(request: Request, repo=Depends(get_repo)):
    """Return expected feature groups and route/page registry for integration checks."""
    _check_mission_control_flag(repo, "integration_health_checks_enabled")
    from app.feature_flags import FeatureFlags
    from study_science.mission_control import MissionControlService

    mounted_paths = {getattr(route, "path", "") for route in request.app.routes}
    return MissionControlService(repo.root).route_registry(
        flags=FeatureFlags.load(repo.root),
        mounted_paths=mounted_paths,
    )


@router.get("/today", response_model=dict[str, Any])
async def get_today_units(
    review_id: str = Query(default=""),
    max_units: int = Query(default=20, ge=1, le=100),
    repo=Depends(get_repo),
):
    """Return structured DailyReviewUnit objects for today's Review Lab."""
    _check_flag(repo)
    engine = _get_engine(repo)
    return engine.get_today_units(review_id=review_id, max_units=max_units)


@router.post("/generate", response_model=ReviewLabSessionResponse)
async def generate_lab(req: ReviewLabCreateRequest, repo=Depends(get_repo)):
    """TASK-001 endpoint: generate a Review Lab session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    session = engine.create_session(
        review_id=req.review_id,
        energy_level=req.energy_level,
        focus_topic=req.focus_topic,
        max_units=req.max_units,
    )
    return _session_to_response(session)


@router.post("/sources/import-text", response_model=dict[str, Any])
async def import_text_source(req: ReviewAssetImportTextRequest, repo=Depends(get_repo)):
    """Import pasted note text as a local source document with source refs."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.import_text_source(
            profile_id=req.profile_id,
            title=req.title,
            text=req.text,
            source_type=req.source_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/sources/import-file", response_model=dict[str, Any])
async def import_file_source(
    file: UploadFile = File(...),
    profile_id: str = Form(default="default"),
    title: str = Form(default=""),
    source_type: str = Form(default=""),
    force_reimport: bool = Form(default=False),
    repo=Depends(get_repo),
):
    """Import a local file into source-backed Review Lab candidate assets."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    _check_file_ingestion_flag(repo)
    service = _get_file_service(repo)
    engine = _get_engine(repo)
    try:
        imported_file = service.import_bytes(
            profile_id=profile_id,
            filename=file.filename or "upload",
            content_type=file.content_type or "",
            data=await _read_upload(file),
            force_reimport=force_reimport,
            pdf_text_extraction_enabled=_pdf_extraction_enabled(repo),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    file_payload = imported_file["file"]
    response: dict[str, Any] = {
        "duplicate": bool(imported_file.get("duplicate")),
        "file": file_payload,
        "segments": imported_file.get("segments", []),
        "warnings": imported_file.get("warnings", []),
        "count": 0,
        "assets": [],
    }
    if file_payload["extraction_status"] == "extracted":
        display_title = title.strip() or file_payload["filename"]
        try:
            source_import = engine.import_segmented_source(
                profile_id=profile_id,
                title=display_title,
                source_type=_source_type_for_review_file(file_payload, source_type),
                file_path=file_payload.get("storage_path"),
                content_hash=file_payload["content_hash"],
                page_count=file_payload.get("page_count"),
                segments=response["segments"],
            )
            extracted = engine.extract_assets_from_source(source_import["source"]["source_id"])
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        file_payload = service.update_links(
            file_payload["file_id"],
            source_id=source_import["source"]["source_id"],
            source_refs=source_import["source"]["source_refs"],
        )
        response.update(
            {
                "file": file_payload,
                "source": source_import["source"],
                "segments": source_import["segments"],
                "count": extracted["count"],
                "assets": extracted["assets"],
            }
        )
    elif file_payload.get("source_id"):
        source = engine.get_source(file_payload["source_id"])
        assets = engine.list_ingested_assets(source_id=file_payload["source_id"]) if source else []
        response.update(
            {
                "source": source["source"] if source else None,
                "segments": source["segments"] if source else response["segments"],
                "count": len(assets),
                "assets": assets,
            }
        )
    return response


@router.get("/files", response_model=dict[str, Any])
async def list_ingested_files(profile_id: str = Query(default=""), repo=Depends(get_repo)):
    """List locally uploaded files and extraction statuses."""
    _check_flag(repo)
    _check_file_ingestion_flag(repo)
    files = _get_file_service(repo).list_files(profile_id=profile_id)
    return {"count": len(files), "files": files}


@router.get("/files/{file_id}", response_model=dict[str, Any])
async def get_ingested_file(file_id: str, repo=Depends(get_repo)):
    """Return one uploaded file metadata record."""
    _check_flag(repo)
    _check_file_ingestion_flag(repo)
    payload = _get_file_service(repo).get_file(file_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"file": payload}


@router.post("/files/{file_id}/extract", response_model=dict[str, Any])
async def extract_ingested_file(file_id: str, repo=Depends(get_repo)):
    """Re-run local text extraction for a stored file."""
    _check_flag(repo)
    _check_file_ingestion_flag(repo)
    try:
        return _get_file_service(repo).extract_file(file_id, pdf_text_extraction_enabled=_pdf_extraction_enabled(repo))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"File not found: {exc.args[0]}") from exc


@router.get("/files/{file_id}/segments", response_model=dict[str, Any])
async def list_ingested_file_segments(file_id: str, repo=Depends(get_repo)):
    """List extracted file/page segments for a stored file."""
    _check_flag(repo)
    _check_file_ingestion_flag(repo)
    try:
        segments = _get_file_service(repo).list_segments(file_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"File not found: {exc.args[0]}") from exc
    return {"count": len(segments), "segments": segments}


@router.get("/files/{file_id}/candidate-assets", response_model=dict[str, Any])
async def list_ingested_file_candidate_assets(file_id: str, repo=Depends(get_repo)):
    """List Review Lab, ResourceOS, or LanguageOS candidates created from a file."""
    _check_flag(repo)
    _check_file_ingestion_flag(repo)
    service = _get_file_service(repo)
    engine = _get_engine(repo)
    try:
        file_record = service.require_file(file_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"File not found: {exc.args[0]}") from exc

    assets: list[dict[str, Any]] = []
    seen: set[str] = set()
    if file_record.source_id:
        for asset in engine.list_ingested_assets(source_id=file_record.source_id):
            asset_id = str(asset.get("asset_id"))
            if asset_id not in seen:
                seen.add(asset_id)
                assets.append(asset)
    if file_record.resource_id:
        try:
            for asset in engine.list_resource_candidate_assets(file_record.resource_id):
                asset_id = str(asset.get("asset_id"))
                if asset_id not in seen:
                    seen.add(asset_id)
                    assets.append(asset)
        except KeyError:
            pass
    if file_record.dictionary_id:
        try:
            from language_science.lexical_kernel import LexicalKernel
            for asset in LexicalKernel(repo.root).list_lexical_assets(dictionary_id=file_record.dictionary_id):
                asset_id = str(asset.get("lexical_id"))
                if asset_id not in seen:
                    seen.add(asset_id)
                    assets.append(asset)
        except Exception:
            pass
    return {"count": len(assets), "assets": assets}


@router.get("/sources", response_model=dict[str, Any])
async def list_sources(repo=Depends(get_repo)):
    """List imported source documents for Review Lab asset ingestion."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    sources = engine.list_sources()
    return {"count": len(sources), "sources": sources}


@router.get("/sources/{source_id}", response_model=dict[str, Any])
async def get_source(source_id: str, repo=Depends(get_repo)):
    """Get one source document and its extracted segments."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    result = engine.get_source(source_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return result


@router.post("/sources/{source_id}/extract-assets", response_model=dict[str, Any])
async def extract_assets(source_id: str, repo=Depends(get_repo)):
    """Generate draft/needs_review CorrectKnowledgeAsset candidates from a source."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.extract_assets_from_source(source_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/resources/import-text", response_model=dict[str, Any])
async def import_resource_text(req: ResourceImportTextRequest, repo=Depends(get_repo)):
    """Import pasted text into ResourceOS as an untrusted resource."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    try:
        return engine.import_resource_text(
            profile_id=req.profile_id,
            title=req.title,
            text=req.text,
            resource_type=req.resource_type,
            origin=req.origin,
            url=req.url,
            file_path=req.file_path,
            notes=req.notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/resources/import-file", response_model=dict[str, Any])
async def import_resource_file(
    file: UploadFile = File(...),
    profile_id: str = Form(default="default"),
    title: str = Form(default=""),
    resource_type: str = Form(default="unknown"),
    notes: str = Form(default=""),
    force_reimport: bool = Form(default=False),
    repo=Depends(get_repo),
):
    """Import an uploaded file into ResourceOS with scoring and evidence extraction."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    _check_resource_flag(repo, "resource_file_import_enabled")
    _check_file_ingestion_flag(repo)
    service = _get_file_service(repo)
    engine = _get_engine(repo)
    try:
        imported_file = service.import_bytes(
            profile_id=profile_id,
            filename=file.filename or "upload",
            content_type=file.content_type or "",
            data=await _read_upload(file),
            force_reimport=force_reimport,
            pdf_text_extraction_enabled=_pdf_extraction_enabled(repo),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    file_payload = imported_file["file"]
    response: dict[str, Any] = {
        "duplicate": bool(imported_file.get("duplicate")),
        "file": file_payload,
        "segments": imported_file.get("segments", []),
        "warnings": imported_file.get("warnings", []),
        "evidence_count": 0,
        "evidence": [],
        "candidate_count": 0,
        "candidate_assets": [],
    }
    if file_payload["extraction_status"] == "extracted":
        display_title = title.strip() or file_payload["filename"]
        try:
            imported_resource = engine.import_segmented_resource(
                profile_id=profile_id,
                title=display_title,
                resource_type=resource_type,
                file_path=file_payload.get("storage_path"),
                notes=notes or None,
                content_hash=file_payload["content_hash"],
                page_count=file_payload.get("page_count"),
                segments=response["segments"],
            )
            resource_id = imported_resource["resource"]["resource_id"]
            quality = engine.score_resource(resource_id)
            extracted = engine.extract_resource_evidence_and_assets(resource_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        file_payload = service.update_links(
            file_payload["file_id"],
            source_id=imported_resource["resource"].get("source_id"),
            resource_id=resource_id,
            source_refs=imported_resource["resource"].get("source_refs", []),
        )
        response.update(
            {
                "file": file_payload,
                "resource": extracted["resource"],
                "quality_gate": quality["quality_gate"],
                "evidence_count": extracted["evidence_count"],
                "evidence": extracted["evidence"],
                "candidate_count": extracted["candidate_count"],
                "candidate_assets": extracted["candidate_assets"],
                "conflicts": extracted.get("conflicts", []),
            }
        )
    elif file_payload.get("resource_id"):
        detail = engine.get_resource(file_payload["resource_id"])
        if detail:
            response.update(
                {
                    "resource": detail["resource"],
                    "evidence_count": detail["evidence_count"],
                    "evidence": detail["evidence"],
                    "candidate_count": detail["candidate_count"],
                    "candidate_assets": detail["candidate_assets"],
                }
            )
    return response


@router.get("/resources", response_model=dict[str, Any])
async def list_resources(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """List ResourceOS resources."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    resources = engine.list_resources(profile_id=profile_id)
    return {"count": len(resources), "resources": resources}


@router.get("/resources/quality-report", response_model=dict[str, Any])
async def get_resource_quality_report(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Summarize ResourceOS quality gate state."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    return engine.resource_quality_report(profile_id=profile_id)


@router.get("/resources/{resource_id}", response_model=dict[str, Any])
async def get_resource(resource_id: str, repo=Depends(get_repo)):
    """Get one ResourceOS resource with evidence and candidates."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    result = engine.get_resource(resource_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return result


@router.post("/resources/{resource_id}/score", response_model=dict[str, Any])
async def score_resource(resource_id: str, repo=Depends(get_repo)):
    """Score ResourceOS quality deterministically."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    try:
        return engine.score_resource(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/resources/{resource_id}/extract-evidence", response_model=dict[str, Any])
async def extract_resource_evidence(resource_id: str, repo=Depends(get_repo)):
    """Extract ResourceOS evidence segments and candidate assets."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_evidence_extraction_enabled")
    engine = _get_engine(repo)
    try:
        return engine.extract_resource_evidence_and_assets(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/resources/{resource_id}/evidence", response_model=dict[str, Any])
async def list_resource_evidence(resource_id: str, repo=Depends(get_repo)):
    """List evidence segments for a ResourceOS resource."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_evidence_extraction_enabled")
    engine = _get_engine(repo)
    try:
        evidence = engine.list_resource_evidence(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"count": len(evidence), "evidence": evidence}


@router.get("/resources/{resource_id}/candidate-assets", response_model=dict[str, Any])
async def list_resource_candidate_assets(resource_id: str, repo=Depends(get_repo)):
    """List ResourceOS candidate assets."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_asset_promotion_enabled")
    engine = _get_engine(repo)
    try:
        assets = engine.list_resource_candidate_assets(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"count": len(assets), "assets": assets}


@router.post("/resources/{resource_id}/confirm", response_model=dict[str, Any])
async def confirm_resource(resource_id: str, repo=Depends(get_repo)):
    """Confirm a resource before asset promotion."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    try:
        return engine.confirm_resource(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/resources/{resource_id}/reject", response_model=dict[str, Any])
async def reject_resource(resource_id: str, repo=Depends(get_repo)):
    """Reject a resource and all of its candidates."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_quality_gate_enabled")
    engine = _get_engine(repo)
    try:
        return engine.reject_resource(resource_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/resources/{resource_id}/promote-assets", response_model=dict[str, Any])
async def promote_resource_assets(resource_id: str, req: ResourcePromoteAssetsRequest, repo=Depends(get_repo)):
    """Promote selected ResourceOS candidates if quality gate passes."""
    _check_flag(repo)
    _check_resource_flag(repo, "resource_asset_promotion_enabled")
    engine = _get_engine(repo)
    try:
        return engine.promote_resource_assets(resource_id, asset_ids=req.asset_ids)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/formulas", response_model=dict[str, Any])
async def list_formulas(
    validation_status: str = Query(default=""),
    profile_id: str = Query(default=""),
    repo=Depends(get_repo),
):
    """List formula assets and formula candidates for Formula Lab."""
    _check_flag(repo)
    _check_formula_flag(repo)
    engine = _get_engine(repo)
    formulas = engine.list_formula_assets(validation_status=validation_status, profile_id=profile_id)
    return {"count": len(formulas), "assets": formulas}


@router.post("/formulas/import-text", response_model=dict[str, Any])
async def import_formula_text(req: FormulaImportTextRequest, repo=Depends(get_repo)):
    """Import formula text and return formula candidates."""
    _check_flag(repo)
    _check_formula_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        imported = engine.import_text_source(
            profile_id=req.profile_id,
            title=req.title,
            text=req.text,
            source_type="text_note",
        )
        extracted = engine.extract_assets_from_source(imported["source"]["source_id"])
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    formulas = [asset for asset in extracted["assets"] if asset.get("asset_type") == "formula" or asset.get("formula_latex")]
    return {
        "source": imported["source"],
        "segments": imported["segments"],
        "count": len(formulas),
        "assets": formulas,
    }


@router.post("/formulas/generate-session", response_model=ReviewLabSessionResponse)
async def generate_formula_session(req: FormulaLabGenerateRequest, repo=Depends(get_repo)):
    """Create a recall-first Formula Lab session."""
    _check_flag(repo)
    _check_formula_flag(repo)
    engine = _get_engine(repo)
    session = engine.generate_formula_lab_session(profile_id=req.profile_id, max_units=req.max_units)
    return _session_to_response(session)


@router.post("/formulas/units/{unit_id}/complete", response_model=dict[str, Any])
async def complete_formula_unit(unit_id: str, req: ReviewLabUnitCompleteRequest, repo=Depends(get_repo)):
    """Complete a Formula Lab unit and update formula-specific memory."""
    _check_flag(repo)
    _check_formula_flag(repo)
    engine = _get_engine(repo)
    from study_science.review_lab_models import ReviewUnitOutcome
    outcome = ReviewUnitOutcome(
        unit_id=unit_id,
        confidence_before=req.confidence_before,
        time_spent_seconds=req.time_spent_seconds,
        needed_hint=req.needed_hint,
        outcome=req.outcome,
        confidence_after=req.confidence_after,
        answer_quality=req.answer_quality,
        fix_rule_helpful=req.fix_rule_helpful,
        next_action=req.next_action,
    )
    try:
        return engine.submit_unit_completion(unit_id, outcome, session_id=req.session_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/formulas/explain/{unit_id}", response_model=dict[str, Any])
async def explain_formula_unit(
    unit_id: str,
    session_id: str = Query(default=""),
    repo=Depends(get_repo),
):
    """Explain formula-specific scoring and metadata for a unit."""
    _check_flag(repo)
    _check_formula_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.explain_formula_unit(unit_id, session_id=session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/syllabus/import-text", response_model=dict[str, Any])
async def import_syllabus_text(req: SyllabusImportTextRequest, repo=Depends(get_repo)):
    """Import pasted local syllabus/LOS text."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.import_syllabus_text(profile_id=req.profile_id, text=req.text, exam=req.exam)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/syllabus/import-json", response_model=dict[str, Any])
async def import_syllabus_json(req: SyllabusImportJsonRequest, repo=Depends(get_repo)):
    """Import local syllabus JSON."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    payload = req.topics if req.topics is not None else req.payload
    engine = _get_engine(repo)
    try:
        return engine.import_syllabus_json(profile_id=req.profile_id, payload=payload, exam=req.exam)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/syllabus/seed-demo", response_model=dict[str, Any])
async def seed_demo_syllabus(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Seed a compact CFA-like demo syllabus."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("syllabus_demo_seed_enabled"):
        raise HTTPException(status_code=403, detail="syllabus_demo_seed_enabled feature flag is disabled")
    engine = _get_engine(repo)
    return engine.seed_demo_syllabus(profile_id=profile_id)


@router.get("/syllabus/topics", response_model=dict[str, Any])
async def list_syllabus_topics(
    profile_id: str = Query(default="default"),
    include_inactive: bool = Query(default=False),
    repo=Depends(get_repo),
):
    """List local syllabus topics used for coverage audit."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    engine = _get_engine(repo)
    topics = engine.list_syllabus_topics(profile_id=profile_id, include_inactive=include_inactive)
    return {"count": len(topics), "topics": topics}


@router.get("/syllabus/coverage", response_model=dict[str, Any])
async def get_syllabus_coverage(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Compute and return syllabus coverage records."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    engine = _get_engine(repo)
    return engine.recompute_syllabus_coverage(profile_id=profile_id)


@router.get("/syllabus/coverage/{topic_id}", response_model=dict[str, Any])
async def get_syllabus_coverage_record(
    topic_id: str,
    profile_id: str = Query(default="default"),
    repo=Depends(get_repo),
):
    """Return one topic coverage record."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.get_syllabus_coverage_record(topic_id, profile_id=profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/syllabus/recompute-coverage", response_model=dict[str, Any])
async def recompute_syllabus_coverage(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Explicitly recompute syllabus coverage."""
    _check_flag(repo)
    _check_syllabus_flag(repo)
    engine = _get_engine(repo)
    return engine.recompute_syllabus_coverage(profile_id=profile_id)


@router.post("/mock-retro/import-text", response_model=dict[str, Any])
async def import_mock_retro_text(req: MockRetroImportTextRequest, repo=Depends(get_repo)):
    """Import pasted mock retro text as correct-rule evidence."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.import_mock_retro_text(
            profile_id=req.profile_id,
            title=req.title,
            text=req.text,
            exam=req.exam,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/mock-retro/sessions", response_model=dict[str, Any])
async def list_mock_retro_sessions(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """List mock retro sessions."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    sessions = engine.list_mock_retro_sessions(profile_id=profile_id)
    return {"count": len(sessions), "sessions": sessions}


@router.get("/mock-retro/sessions/{mock_id}", response_model=dict[str, Any])
async def get_mock_retro_session(mock_id: str, repo=Depends(get_repo)):
    """Get one mock retro session with sanitized evidence."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    result = engine.get_mock_retro_session(mock_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Mock retro session not found")
    return result


@router.post("/mock-retro/sessions/{mock_id}/analyze", response_model=dict[str, Any])
async def analyze_mock_retro_session(mock_id: str, repo=Depends(get_repo)):
    """Analyze a mock retro session into transfer gap records."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.analyze_mock_session(mock_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/mock-retro/transfer-gaps", response_model=dict[str, Any])
async def list_transfer_gaps(
    profile_id: str = Query(default="default"),
    status: str = Query(default=""),
    repo=Depends(get_repo),
):
    """List transfer gaps inferred from mock retro evidence."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    gaps = engine.list_transfer_gaps(profile_id=profile_id, status=status)
    return {"count": len(gaps), "gaps": gaps}


@router.get("/mock-retro/transfer-gaps/{gap_id}", response_model=dict[str, Any])
async def get_transfer_gap(gap_id: str, repo=Depends(get_repo)):
    """Get one transfer gap."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    gap = engine.get_transfer_gap(gap_id)
    if gap is None:
        raise HTTPException(status_code=404, detail="Transfer gap not found")
    return {"gap": gap}


@router.post("/mock-retro/transfer-gaps/{gap_id}/resolve", response_model=dict[str, Any])
async def resolve_transfer_gap(gap_id: str, repo=Depends(get_repo)):
    """Resolve a transfer gap."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"gap": engine.resolve_transfer_gap(gap_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/mock-retro/generate-review", response_model=ReviewLabSessionResponse)
async def generate_mock_retro_review(req: MockRetroGenerateReviewRequest, repo=Depends(get_repo)):
    """Generate correct-only Review Lab units from open transfer gaps."""
    _check_flag(repo)
    _check_mock_retro_flag(repo)
    from app.feature_flags import FeatureFlags
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("mock_retro_review_generation_enabled"):
        raise HTTPException(status_code=403, detail="mock_retro_review_generation_enabled feature flag is disabled")
    engine = _get_engine(repo)
    session = engine.generate_review_from_transfer_gaps(profile_id=req.profile_id, max_units=req.max_units)
    return _session_to_response(session)


@router.post("/formulas/{asset_id}/enrich", response_model=dict[str, Any])
async def enrich_formula(asset_id: str, repo=Depends(get_repo)):
    """Enrich a formula candidate with deterministic metadata."""
    _check_flag(repo)
    _check_formula_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"asset": engine.enrich_formula_asset(asset_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/formulas/{asset_id}/confirm", response_model=dict[str, Any])
async def confirm_formula(asset_id: str, repo=Depends(get_repo)):
    """Alias for confirming a formula asset candidate."""
    _check_flag(repo)
    _check_formula_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"asset": engine.confirm_asset(asset_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/formulas/{asset_id}/reject", response_model=dict[str, Any])
async def reject_formula(asset_id: str, repo=Depends(get_repo)):
    """Alias for rejecting a formula asset candidate."""
    _check_flag(repo)
    _check_formula_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"asset": engine.reject_asset(asset_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/units/{unit_id}/complete", response_model=dict[str, Any])
async def complete_unit(unit_id: str, req: ReviewLabUnitCompleteRequest, repo=Depends(get_repo)):
    """TASK-001 endpoint: complete a single unit independently."""
    _check_flag(repo)
    engine = _get_engine(repo)
    from study_science.review_lab_models import ReviewUnitOutcome
    outcome = ReviewUnitOutcome(
        unit_id=unit_id,
        confidence_before=req.confidence_before,
        time_spent_seconds=req.time_spent_seconds,
        needed_hint=req.needed_hint,
        outcome=req.outcome,
        confidence_after=req.confidence_after,
        answer_quality=req.answer_quality,
        fix_rule_helpful=req.fix_rule_helpful,
        next_action=req.next_action,
    )
    try:
        return engine.submit_unit_completion(unit_id, outcome, session_id=req.session_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/assets", response_model=dict[str, Any])
async def list_assets(
    review_id: str = Query(default=""),
    validation_status: str = Query(default=""),
    source_id: str = Query(default=""),
    repo=Depends(get_repo),
):
    """List CorrectKnowledgeAsset objects available to Review Lab."""
    _check_flag(repo)
    engine = _get_engine(repo)
    if validation_status or source_id:
        _check_asset_ingestion_flag(repo)
        assets = engine.list_ingested_assets(validation_status=validation_status, source_id=source_id)
        return {"count": len(assets), "assets": assets}
    assets = engine.list_assets(review_id=review_id)
    return {"count": len(assets), "assets": assets}


@router.post("/assets/{asset_id}/confirm", response_model=dict[str, Any])
async def confirm_asset(asset_id: str, repo=Depends(get_repo)):
    """Promote a draft asset after manual review."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"asset": engine.confirm_asset(asset_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/assets/{asset_id}/reject", response_model=dict[str, Any])
async def reject_asset(asset_id: str, repo=Depends(get_repo)):
    """Reject a draft asset so it cannot enter Review Lab."""
    _check_flag(repo)
    _check_asset_ingestion_flag(repo)
    engine = _get_engine(repo)
    try:
        return {"asset": engine.reject_asset(asset_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/explain/{unit_id}", response_model=dict[str, Any])
async def explain_unit(
    unit_id: str,
    review_id: str = Query(default=""),
    repo=Depends(get_repo),
):
    """Explain why this unit appears today."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        return engine.explain_unit(unit_id, review_id=review_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/sessions", response_model=ReviewLabSessionResponse)
async def create_session(req: ReviewLabCreateRequest, repo=Depends(get_repo)):
    """Create a new review lab session from a daily review snapshot."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        session = engine.create_session(
            review_id=req.review_id,
            energy_level=req.energy_level,
            focus_topic=req.focus_topic,
            max_units=req.max_units,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _session_to_response(session)


@router.get("/sessions/{session_id}", response_model=ReviewLabSessionResponse)
async def get_session(session_id: str, repo=Depends(get_repo)):
    """Get the current state of a review lab session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _session_to_response(session)


@router.post("/sessions/{session_id}/units/{unit_id}/outcome", response_model=dict[str, Any])
async def submit_outcome(
    session_id: str,
    unit_id: str,
    req: ReviewLabOutcomeRequest,
    repo=Depends(get_repo),
):
    """Submit a per-unit outcome and advance the session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    from study_science.review_lab_models import ReviewUnitOutcome
    outcome = ReviewUnitOutcome(
        unit_id=unit_id,
        confidence_before=req.confidence_before,
        time_spent_seconds=req.time_spent_seconds,
        needed_hint=req.needed_hint,
        outcome=req.outcome,
        confidence_after=req.confidence_after,
        answer_quality=req.answer_quality,
        fix_rule_helpful=req.fix_rule_helpful,
        next_action=req.next_action,
    )
    try:
        result = engine.submit_outcome(session_id, unit_id, outcome)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@router.post("/sessions/{session_id}/units/{unit_id}/hint", response_model=dict[str, Any])
async def request_hint(session_id: str, unit_id: str, req: ReviewLabHintRequest, repo=Depends(get_repo)):
    """Request a hint for the current unit. Records that a hint was used."""
    _check_flag(repo)
    engine = _get_engine(repo)
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    unit = next((u for u in session.units if u.unit_id == unit_id), None)
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")

    hint = _generate_hint(unit, req.hint_level)
    return {
        "session_id": session_id,
        "unit_id": unit_id,
        "hint": hint,
        "hint_level": req.hint_level,
    }


@router.post("/sessions/{session_id}/pause", response_model=ReviewLabSessionResponse)
async def pause_session(session_id: str, repo=Depends(get_repo)):
    """Pause an active session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        session = engine.pause_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _session_to_response(session)


@router.post("/sessions/{session_id}/resume", response_model=ReviewLabSessionResponse)
async def resume_session(session_id: str, repo=Depends(get_repo)):
    """Resume a paused session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        session = engine.resume_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _session_to_response(session)


@router.post("/sessions/{session_id}/complete", response_model=ReviewLabSessionResponse)
async def complete_session(session_id: str, repo=Depends(get_repo)):
    """Mark a session as completed and run final knowledge-memory updates."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        session = engine.complete_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _session_to_response(session)


@router.get("/sessions/{session_id}/report", response_model=ReviewLabReportResponse)
async def get_session_report(session_id: str, repo=Depends(get_repo)):
    """Get a quality report for a completed (or in-progress) session."""
    _check_flag(repo)
    engine = _get_engine(repo)
    try:
        report = engine.get_session_report(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ReviewLabReportResponse(**report)


@router.get("/history")
async def list_history(limit: int = Query(default=50, ge=1, le=200), repo=Depends(get_repo)):
    """List completed review lab sessions."""
    _check_flag(repo)
    engine = _get_engine(repo)
    return {"sessions": engine.list_session_history(limit=limit)}


# ── Helpers ────────────────────────────────────────────────────────────


def _session_to_response(session) -> ReviewLabSessionResponse:
    current = session.current_unit
    return ReviewLabSessionResponse(
        session_id=session.session_id,
        review_id=session.review_id,
        status=session.status,
        units=[u.as_dict() for u in session.units],
        current_unit_index=session.current_unit_index,
        current_unit=current.as_dict() if current else None,
        completed_unit_ids=session.completed_unit_ids,
        outcomes=[o.as_dict() for o in session.outcomes],
        progress_pct=session.progress_pct,
        is_complete=session.is_complete,
        energy_level=session.energy_level,
        focus_topic=session.focus_topic,
        started_at=session.started_at,
        completed_at=session.completed_at,
        paused_at=session.paused_at,
        resumed_at=session.resumed_at,
    )


def _generate_hint(unit, hint_level: int) -> str:
    """Generate a contextual hint based on unit type and hint level."""
    if hint_level <= 1:
        return unit.recall_instruction or "Think about the key variables or conditions."
    if unit.unit_type == "formula_lab":
        return f"Formula structure: {unit.formula_latex[:60]}..." if unit.formula_latex else "Recall the formula variables."
    if unit.common_wrong_path:
        return f"Common mistake to avoid: {unit.common_wrong_path[:120]}"
    if unit.exam_trap:
        return f"Exam trap: {unit.exam_trap[:120]}"
    return unit.recall_instruction or "Break the problem into steps."
