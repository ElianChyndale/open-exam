"""ReviewLabEngine — recall-first interactive review system.

Replaces batch-marking daily review with per-unit scoring. Each unit is
individually assessed (recalled / partial / forgot / skipped) and fed
back into the KnowledgeMemoryEngine for state transitions and scheduling.
"""

from __future__ import annotations

import json
import re
from dataclasses import fields
from datetime import datetime, timedelta, timezone
from hashlib import sha1, sha256
from pathlib import Path
from typing import Any

from study_science.knowledge_memory import (
    KnowledgeFeedbackInput,
    KnowledgeMemoryEngine,
)
from study_science.review_lab_models import (
    AssetSyllabusLink,
    CorrectKnowledgeAsset,
    DailyReviewUnit,
    FormulaMetadata,
    KnowledgeSourceDocument,
    KnowledgeSourceSegment,
    LearningResource,
    MockQuestionEvidence,
    MockSession,
    ReviewLabSession,
    ReviewUnitOutcome,
    SyllabusCoverageRecord,
    SyllabusTopic,
    TransferGapRecord,
)


class ReviewLabEngine:
    """Drives the recall-first review lab lifecycle.

    Responsibilities:
      1. Build review units from a daily-review snapshot.
      2. Manage session state (active / paused / completed).
      3. Map learner outcomes to KnowledgeMemoryEngine vocabulary.
      4. Persist outcomes and update knowledge-status overlay.
    """

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.km_engine = KnowledgeMemoryEngine()
        self._session_root = self.repo_root / ".system" / "memory" / "review" / "lab-sessions"
        self._session_root.mkdir(parents=True, exist_ok=True)
        self._source_root = self.repo_root / ".system" / "memory" / "review" / "asset-sources"
        self._segment_root = self.repo_root / ".system" / "memory" / "review" / "asset-segments"
        self._asset_root = self.repo_root / ".system" / "memory" / "review" / "asset-candidates"
        self._resource_root = self.repo_root / ".system" / "memory" / "review" / "resources"
        self._syllabus_root = self.repo_root / ".system" / "memory" / "review" / "syllabus"
        self._mock_retro_root = self.repo_root / ".system" / "memory" / "review" / "mock-retro"
        self._mock_evidence_root = self._mock_retro_root / "evidence"
        self._transfer_gap_root = self._mock_retro_root / "transfer-gaps"
        for path in (
            self._source_root,
            self._segment_root,
            self._asset_root,
            self._resource_root,
            self._syllabus_root,
            self._mock_retro_root,
            self._mock_evidence_root,
            self._transfer_gap_root,
        ):
            path.mkdir(parents=True, exist_ok=True)

    # ── Session lifecycle ────────────────────────────────────────────────

    def create_session(
        self,
        review_id: str,
        energy_level: int = 2,
        focus_topic: str = "",
        max_units: int = 20,
    ) -> ReviewLabSession:
        """Create a new ReviewLabSession from the latest daily review snapshot."""
        snapshot = self._load_snapshot(review_id)
        actual_review_id = snapshot.get("review_id", review_id)
        units = self._build_units_from_snapshot(snapshot, max_units)

        session_id = self._stable_id("lab-session", actual_review_id, datetime.now(timezone.utc).isoformat())
        session = ReviewLabSession(
            session_id=session_id,
            review_id=actual_review_id,
            status="active",
            units=units,
            current_unit_index=0,
            energy_level=energy_level,
            focus_topic=focus_topic,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._persist_session(session)
        return session

    def get_today_units(self, review_id: str = "", max_units: int = 20) -> dict[str, Any]:
        """Return today's structured Review Lab units without creating a session."""
        snapshot = self._load_snapshot(review_id)
        units = self._build_units_from_snapshot(snapshot, max_units)
        return {
            "review_id": snapshot.get("review_id", review_id),
            "unit_count": len(units),
            "units": [unit.as_dict() for unit in units],
            "mix": self._unit_mix_summary(units),
        }

    def list_assets(self, review_id: str = "") -> list[dict[str, Any]]:
        """List CorrectKnowledgeAsset objects available for a review snapshot."""
        snapshot = self._load_snapshot(review_id)
        return [asset.as_dict() for asset in self._build_assets_from_snapshot(snapshot)]

    def import_text_source(
        self,
        *,
        profile_id: str = "default",
        title: str,
        text: str,
        source_type: str = "text_note",
        file_path: str | None = None,
    ) -> dict[str, Any]:
        """Import note text and persist source-backed segments locally."""
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Source text is required.")

        allowed_types = {"pdf_note", "markdown_note", "text_note", "manual"}
        normalized_source_type = source_type if source_type in allowed_types else "text_note"
        content_hash = sha256(cleaned.encode("utf-8")).hexdigest()
        source_id = self._stable_id("ksource", profile_id, title or "Untitled source", content_hash)

        existing = self.get_source(source_id)
        if existing:
            return existing

        segments = self._segments_from_text(source_id, cleaned)
        source = KnowledgeSourceDocument(
            source_id=source_id,
            profile_id=profile_id or "default",
            title=title.strip() or "Untitled source",
            source_type=normalized_source_type,  # type: ignore[arg-type]
            file_path=file_path,
            content_hash=content_hash,
            imported_at=datetime.now(timezone.utc).isoformat(),
            page_count=None,
            extraction_status="extracted" if segments else "failed",
            extraction_error=None if segments else "No extractable text segments found.",
            source_refs=[segment.source_ref for segment in segments],
        )
        self._persist_source(source)
        self._persist_segments(source_id, segments)
        return {
            "source": source.as_dict(),
            "segments": [segment.as_dict() for segment in segments],
        }

    def import_segmented_source(
        self,
        *,
        profile_id: str = "default",
        title: str,
        source_type: str = "text_note",
        file_path: str | None = None,
        content_hash: str,
        page_count: int | None = None,
        segments: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Import already-extracted file segments while preserving file/page refs."""
        if not segments:
            raise ValueError("At least one extracted file segment is required.")

        allowed_types = {"pdf_note", "markdown_note", "text_note", "manual"}
        normalized_source_type = source_type if source_type in allowed_types else "text_note"
        source_id = self._stable_id("ksource", profile_id or "default", title or "Untitled source", content_hash)

        existing = self.get_source(source_id)
        if existing:
            return existing

        knowledge_segments: list[KnowledgeSourceSegment] = []
        for index, item in enumerate(segments, start=1):
            text = str(item.get("text", "")).strip()
            if not text:
                continue
            source_ref = str(item.get("source_ref") or f"{source_id}#seg-{index}")
            knowledge_segments.append(
                KnowledgeSourceSegment(
                    segment_id=f"segment-{source_id}-{index}",
                    source_id=source_id,
                    page=item.get("page"),
                    heading=item.get("heading"),
                    text=text,
                    char_start=item.get("char_start"),
                    char_end=item.get("char_end"),
                    source_ref=source_ref,
                    evidence_type=str(item.get("evidence_type") or self._evidence_type_from_text(text)),  # type: ignore[arg-type]
                    confidence=float(item.get("confidence") or self._segment_confidence(text)),
                )
            )
        if not knowledge_segments:
            raise ValueError("No extractable text segments found.")

        source = KnowledgeSourceDocument(
            source_id=source_id,
            profile_id=profile_id or "default",
            title=title.strip() or "Untitled source",
            source_type=normalized_source_type,  # type: ignore[arg-type]
            file_path=file_path,
            content_hash=content_hash,
            imported_at=datetime.now(timezone.utc).isoformat(),
            page_count=page_count,
            extraction_status="extracted",
            extraction_error=None,
            source_refs=[segment.source_ref for segment in knowledge_segments],
        )
        self._persist_source(source)
        self._persist_segments(source_id, knowledge_segments)
        return {
            "source": source.as_dict(),
            "segments": [segment.as_dict() for segment in knowledge_segments],
        }

    def list_sources(self) -> list[dict[str, Any]]:
        """List imported Review Lab asset sources, newest first."""
        sources = [self._source_from_dict(json.loads(path.read_text(encoding="utf-8"))) for path in self._source_root.glob("*.json")]
        sources.sort(key=lambda source: source.imported_at, reverse=True)
        return [source.as_dict() for source in sources]

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        """Return one imported source with its segments."""
        source = self._load_source(source_id)
        if source is None:
            return None
        segments = self._load_segments(source_id)
        return {
            "source": source.as_dict(),
            "segments": [segment.as_dict() for segment in segments],
        }

    def extract_assets_from_source(self, source_id: str) -> dict[str, Any]:
        """Generate draft CorrectKnowledgeAsset candidates from a source."""
        source = self._load_source(source_id)
        if source is None:
            raise KeyError(f"Source not found: {source_id}")

        segments = self._load_segments(source_id)
        context_text = "\n".join(segment.text for segment in segments)
        candidates: list[CorrectKnowledgeAsset] = []
        for segment in segments:
            for candidate in self._candidate_assets_from_segment(source, segment, context_text=context_text):
                existing = self._load_ingested_asset(candidate.asset_id)
                if existing is not None:
                    candidates.append(existing)
                    continue
                self._persist_ingested_asset(candidate)
                candidates.append(candidate)

        source.extraction_status = "extracted"
        source.extraction_error = None
        self._persist_source(source)
        return {
            "source": source.as_dict(),
            "count": len(candidates),
            "assets": [asset.as_dict() for asset in candidates],
        }

    # ── ResourceOS quality-gated promotion ──────────────────────────────

    def import_resource_text(
        self,
        *,
        profile_id: str = "default",
        title: str,
        text: str,
        resource_type: str = "text_note",
        origin: str = "import_text",
        url: str | None = None,
        file_path: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        """Import a local learning resource without auto-trusting it."""
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Resource text is required.")
        normalized_type = self._normalize_resource_type(resource_type)
        normalized_origin = origin if origin in {"manual", "import_text", "file", "url", "system_seed"} else "import_text"
        source_type = normalized_type if normalized_type in {"pdf_note", "text_note", "manual"} else "text_note"
        imported = self.import_text_source(
            profile_id=profile_id or "default",
            title=title,
            text=cleaned,
            source_type=source_type,
            file_path=file_path,
        )
        source = self._source_from_dict(imported["source"])
        existing = self._load_resource(source.source_id)
        if existing is not None:
            return {
                "duplicate": bool(existing.duplicate_of),
                "resource": existing.as_dict(),
                "evidence_count": len(imported["segments"]),
                "evidence": imported["segments"],
            }

        duplicate = self._find_resource_by_hash(source.content_hash, exclude_resource_id=source.source_id)
        warnings: list[str] = []
        if duplicate is not None:
            warnings.append(f"duplicate_source_hash:{duplicate.resource_id}")
        resource = LearningResource(
            resource_id=source.source_id,
            profile_id=source.profile_id,
            title=source.title,
            resource_type=normalized_type,  # type: ignore[arg-type]
            origin=normalized_origin,  # type: ignore[arg-type]
            url=url,
            file_path=file_path,
            content_hash=source.content_hash,
            imported_at=source.imported_at,
            source_refs=source.source_refs,
            quality_score=0.0,
            quality_status="unscored",
            validation_status="draft",
            notes=notes,
            source_id=source.source_id,
            duplicate_of=duplicate.resource_id if duplicate is not None else None,
            warnings=warnings,
        )
        self._persist_resource(resource)
        return {
            "duplicate": duplicate is not None,
            "resource": resource.as_dict(),
            "evidence_count": len(imported["segments"]),
            "evidence": imported["segments"],
        }

    def import_segmented_resource(
        self,
        *,
        profile_id: str = "default",
        title: str,
        resource_type: str = "text_note",
        file_path: str | None = None,
        notes: str | None = None,
        content_hash: str,
        page_count: int | None = None,
        segments: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Import a file-backed ResourceOS resource using preserved file refs."""
        normalized_type = self._normalize_resource_type(resource_type)
        source_type = normalized_type if normalized_type in {"pdf_note", "text_note", "manual"} else "text_note"
        imported = self.import_segmented_source(
            profile_id=profile_id or "default",
            title=title,
            source_type=source_type,
            file_path=file_path,
            content_hash=content_hash,
            page_count=page_count,
            segments=segments,
        )
        source = self._source_from_dict(imported["source"])
        existing = self._load_resource(source.source_id)
        if existing is not None:
            return {
                "duplicate": bool(existing.duplicate_of),
                "resource": existing.as_dict(),
                "evidence_count": len(imported["segments"]),
                "evidence": imported["segments"],
            }

        duplicate = self._find_resource_by_hash(source.content_hash, exclude_resource_id=source.source_id)
        warnings: list[str] = []
        if duplicate is not None:
            warnings.append(f"duplicate_source_hash:{duplicate.resource_id}")
        resource = LearningResource(
            resource_id=source.source_id,
            profile_id=source.profile_id,
            title=source.title,
            resource_type=normalized_type,  # type: ignore[arg-type]
            origin="file",
            url=None,
            file_path=file_path,
            content_hash=source.content_hash,
            imported_at=source.imported_at,
            source_refs=source.source_refs,
            quality_score=0.0,
            quality_status="unscored",
            validation_status="draft",
            notes=notes,
            source_id=source.source_id,
            duplicate_of=duplicate.resource_id if duplicate is not None else None,
            warnings=warnings,
        )
        self._persist_resource(resource)
        return {
            "duplicate": duplicate is not None,
            "resource": resource.as_dict(),
            "evidence_count": len(imported["segments"]),
            "evidence": imported["segments"],
        }

    def list_resources(self, *, profile_id: str = "default") -> list[dict[str, Any]]:
        """List ResourceOS resources, newest first."""
        resources = [
            self._resource_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._resource_root.glob("*.json")
        ]
        resources = [
            resource for resource in resources
            if not profile_id or resource.profile_id in {profile_id, "default"}
        ]
        resources.sort(key=lambda resource: resource.imported_at, reverse=True)
        return [resource.as_dict() for resource in resources]

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        """Return one ResourceOS resource with evidence and candidates."""
        resource = self._load_resource(resource_id)
        if resource is None:
            return None
        evidence = self.list_resource_evidence(resource_id)
        candidates = self.list_resource_candidate_assets(resource_id)
        return {
            "resource": resource.as_dict(),
            "evidence_count": len(evidence),
            "evidence": evidence,
            "candidate_count": len(candidates),
            "candidate_assets": candidates,
        }

    def score_resource(self, resource_id: str) -> dict[str, Any]:
        """Deterministically score resource quality without external calls."""
        resource = self._require_resource(resource_id)
        self._score_resource_in_place(resource)
        self._persist_resource(resource)
        self._refresh_resource_asset_metadata(resource)
        return {"resource": resource.as_dict(), "quality_gate": self._resource_gate_summary(resource)}

    def extract_resource_evidence_and_assets(self, resource_id: str) -> dict[str, Any]:
        """Extract evidence segments and draft candidate assets from a resource."""
        resource = self._require_resource(resource_id)
        if resource.quality_status == "unscored":
            self._score_resource_in_place(resource)
            self._persist_resource(resource)

        extracted = self.extract_assets_from_source(resource.source_id or resource.resource_id)
        assets = [self._asset_from_dict(item) for item in extracted["assets"]]
        self._attach_resource_metadata(resource, assets)
        for asset in assets:
            self._persist_ingested_asset(asset)
        evidence = self.list_resource_evidence(resource_id)
        return {
            "resource": resource.as_dict(),
            "evidence_count": len(evidence),
            "evidence": evidence,
            "candidate_count": len(assets),
            "candidate_assets": [asset.as_dict() for asset in assets],
            "conflicts": sorted({conflict for asset in assets for conflict in asset.resource_conflicts}),
        }

    def list_resource_evidence(self, resource_id: str) -> list[dict[str, Any]]:
        """List evidence segments for a resource."""
        resource = self._require_resource(resource_id)
        segments = self._load_segments(resource.source_id or resource.resource_id)
        return [segment.as_dict() for segment in segments]

    def list_resource_candidate_assets(self, resource_id: str) -> list[dict[str, Any]]:
        """List candidate assets extracted from a resource."""
        assets = [
            self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._asset_root.glob("*.json")
        ]
        filtered = [
            asset for asset in assets
            if asset.resource_id == resource_id
            or any(ref.startswith(f"{resource_id}#") for ref in asset.source_refs)
        ]
        filtered.sort(key=lambda asset: (asset.validation_status, -self._asset_priority(asset), asset.title))
        return [asset.as_dict() for asset in filtered]

    def confirm_resource(self, resource_id: str) -> dict[str, Any]:
        """Mark a resource as user-confirmed, then rescore it."""
        resource = self._require_resource(resource_id)
        if resource.validation_status == "rejected":
            raise ValueError("Rejected resources cannot be confirmed.")
        resource.validation_status = "confirmed"
        self._score_resource_in_place(resource)
        self._persist_resource(resource)
        self._refresh_resource_asset_metadata(resource)
        return {"resource": resource.as_dict(), "quality_gate": self._resource_gate_summary(resource)}

    def reject_resource(self, resource_id: str) -> dict[str, Any]:
        """Reject a resource and exclude its candidates from review flows."""
        resource = self._require_resource(resource_id)
        resource.validation_status = "rejected"
        resource.quality_status = "rejected"
        resource.quality_score = 0.0
        self._persist_resource(resource)
        rejected_assets: list[dict[str, Any]] = []
        for asset_payload in self.list_resource_candidate_assets(resource_id):
            asset = self._asset_from_dict(asset_payload)
            asset.validation_status = "rejected"
            asset.resource_validation_status = "rejected"
            asset.resource_quality_status = "rejected"
            self._persist_ingested_asset(asset)
            rejected_assets.append(asset.as_dict())
        return {"resource": resource.as_dict(), "rejected_assets": rejected_assets}

    def promote_resource_assets(self, resource_id: str, asset_ids: list[str] | None = None) -> dict[str, Any]:
        """Promote selected resource candidates only after the resource passes the gate."""
        resource = self._require_resource(resource_id)
        if resource.quality_status == "unscored":
            self._score_resource_in_place(resource)
            self._persist_resource(resource)
        candidates = [
            self._asset_from_dict(item)
            for item in self.list_resource_candidate_assets(resource_id)
        ]
        selected_ids = set(asset_ids or [asset.asset_id for asset in candidates])
        selected = [asset for asset in candidates if asset.asset_id in selected_ids]
        gate = self._resource_gate_summary(resource)
        if not gate["passes"]:
            for asset in selected:
                if asset.validation_status not in {"confirmed", "rejected"}:
                    asset.validation_status = "needs_review"
                    if gate["reason"] not in asset.resource_conflicts:
                        asset.resource_conflicts.append(gate["reason"])
                    self._persist_ingested_asset(asset)
            return {
                "resource": resource.as_dict(),
                "quality_gate": gate,
                "promoted_count": 0,
                "assets": [asset.as_dict() for asset in selected],
            }

        promoted: list[CorrectKnowledgeAsset] = []
        for asset in selected:
            if asset.validation_status == "rejected":
                continue
            asset.validation_status = "confirmed"
            asset.resource_promoted_at = datetime.now(timezone.utc).isoformat()
            asset.source_quality = resource.quality_score
            asset.resource_quality_status = resource.quality_status
            asset.resource_validation_status = resource.validation_status
            if "manual" not in asset.resource_match_reasons:
                asset.resource_match_reasons.append("manual")
            self._persist_ingested_asset(asset)
            promoted.append(asset)
        return {
            "resource": resource.as_dict(),
            "quality_gate": gate,
            "promoted_count": len(promoted),
            "assets": [asset.as_dict() for asset in promoted],
        }

    def resource_quality_report(self, *, profile_id: str = "default") -> dict[str, Any]:
        """Summarize ResourceOS quality and promotion state."""
        resources = [self._resource_from_dict(item) for item in self.list_resources(profile_id=profile_id)]
        summary: dict[str, int] = {
            "unscored": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "trusted": 0,
            "rejected": 0,
        }
        for resource in resources:
            summary[resource.quality_status] = summary.get(resource.quality_status, 0) + 1
        candidates = [
            self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._asset_root.glob("*.json")
        ]
        resource_candidates = [asset for asset in candidates if asset.resource_id]
        return {
            "profile_id": profile_id or "default",
            "resource_count": len(resources),
            "summary": summary,
            "candidate_asset_count": len(resource_candidates),
            "promoted_asset_count": sum(1 for asset in resource_candidates if asset.validation_status == "confirmed"),
            "conflict_count": sum(len(asset.resource_conflicts) for asset in resource_candidates),
            "resources": [resource.as_dict() for resource in resources],
        }

    def list_ingested_assets(
        self,
        *,
        validation_status: str = "",
        source_id: str = "",
        profile_id: str = "",
    ) -> list[dict[str, Any]]:
        """List locally generated source-backed candidate assets."""
        assets: list[CorrectKnowledgeAsset] = []
        for path in self._asset_root.glob("*.json"):
            asset = self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if validation_status and asset.validation_status != validation_status:
                continue
            if source_id:
                source = self._load_source(source_id)
                source_refs = set(source.source_refs if source else [])
                if not any(ref.startswith(f"{source_id}#") or ref in source_refs for ref in asset.source_refs):
                    continue
            if profile_id and asset.profile_id != profile_id:
                continue
            assets.append(asset)
        assets.sort(key=lambda asset: (asset.validation_status, -self._asset_priority(asset), asset.title))
        return [asset.as_dict() for asset in assets]

    def confirm_asset(self, asset_id: str) -> dict[str, Any]:
        """Promote a draft source-backed asset into normal Review Lab eligibility."""
        asset = self._load_ingested_asset(asset_id)
        if asset is None:
            raise KeyError(f"Asset not found: {asset_id}")
        if not asset.source_refs:
            raise ValueError("Cannot confirm an asset without source_refs.")
        if asset.resource_id and not self._asset_passes_resource_gate(asset):
            resource = self._resource_for_asset(asset)
            reason = self._resource_gate_summary(resource)["reason"] if resource is not None else "resource_missing"
            raise ValueError(f"Cannot confirm asset before resource quality gate passes: {reason}.")
        asset.validation_status = "confirmed"
        asset.mastery_state = asset.mastery_state or "new"
        self._persist_ingested_asset(asset)
        return asset.as_dict()

    def reject_asset(self, asset_id: str) -> dict[str, Any]:
        """Mark a source-backed asset as rejected so it is never selected."""
        asset = self._load_ingested_asset(asset_id)
        if asset is None:
            raise KeyError(f"Asset not found: {asset_id}")
        asset.validation_status = "rejected"
        self._persist_ingested_asset(asset)
        return asset.as_dict()

    def list_formula_assets(
        self,
        *,
        validation_status: str = "",
        profile_id: str = "",
    ) -> list[dict[str, Any]]:
        """List formula assets and formula candidates for Formula Lab."""
        assets: list[CorrectKnowledgeAsset] = []
        persisted = [
            self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._asset_root.glob("*.json")
        ]
        assets.extend(asset for asset in persisted if self._is_formula_candidate_asset(asset))

        snapshot = self._load_snapshot("")
        for asset in self._build_assets_from_snapshot(snapshot):
            if self._is_formula_candidate_asset(asset) and asset.asset_id not in {item.asset_id for item in assets}:
                assets.append(asset)

        filtered = []
        for asset in assets:
            if validation_status and asset.validation_status != validation_status:
                continue
            if profile_id and asset.profile_id not in {profile_id, "default"}:
                continue
            filtered.append(asset)
        filtered.sort(key=self._formula_priority, reverse=True)
        return [asset.as_dict() for asset in filtered]

    def enrich_formula_asset(self, asset_id: str) -> dict[str, Any]:
        """Re-run deterministic metadata enrichment for a formula candidate."""
        asset = self._load_ingested_asset(asset_id)
        if asset is None:
            raise KeyError(f"Asset not found: {asset_id}")
        if not self._is_formula_candidate_asset(asset):
            raise ValueError("Asset is not a formula candidate.")
        context = "\n".join(self._source_text_for_refs(asset.source_refs)) or asset.correct_rule
        metadata = self._extract_formula_metadata(asset.formula_latex or asset.correct_rule, context)
        asset.formula_latex = metadata.formula_latex
        asset.plain_formula = metadata.plain_formula or ""
        asset.variables = metadata.variables
        asset.applies_when = metadata.applies_when
        asset.not_when = metadata.not_when or asset.not_when
        asset.assumptions = metadata.assumptions
        asset.common_correct_boundary_rules = metadata.common_correct_boundary_rules
        asset.example = metadata.worked_example or asset.example
        asset.ba_ii_plus_steps = metadata.ba_ii_plus_steps
        asset.formula_family = metadata.formula_family or ""
        asset.difficulty = metadata.difficulty
        self._persist_ingested_asset(asset)
        return asset.as_dict()

    def generate_formula_lab_session(
        self,
        *,
        profile_id: str = "default",
        max_units: int = 12,
    ) -> ReviewLabSession:
        """Create a recall-first Formula Lab session."""
        assets = self._formula_assets_for_session(profile_id=profile_id, max_units=max_units)
        review_id = f"formula-lab-{datetime.now(timezone.utc).date().isoformat()}"
        units = [self._formula_unit_from_asset(asset, review_id) for asset in assets]
        session_id = self._stable_id("formula-session", profile_id, datetime.now(timezone.utc).isoformat())
        session = ReviewLabSession(
            session_id=session_id,
            review_id=review_id,
            status="active",
            units=units,
            current_unit_index=0,
            energy_level=2,
            focus_topic="Formula Lab",
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._persist_session(session)
        return session

    def explain_formula_unit(self, unit_id: str, session_id: str = "") -> dict[str, Any]:
        """Explain formula-specific unit scoring and source metadata."""
        units: list[DailyReviewUnit] = []
        if session_id:
            session = self.get_session(session_id)
            if session:
                units = session.units
        if not units:
            units = [
                self._formula_unit_from_asset(asset, "formula-lab-preview")
                for asset in self._formula_assets_for_session(profile_id="default", max_units=100)
            ]
        unit = next((candidate for candidate in units if candidate.unit_id == unit_id), None)
        if unit is None:
            raise ValueError(f"Formula unit not found: {unit_id}")
        return {
            "unit_id": unit.unit_id,
            "asset_id": unit.asset_id,
            "display_mode": unit.display_mode,
            "formula_family": unit.formula_family,
            "difficulty": unit.difficulty,
            "variables": unit.variables,
            "applies_when": unit.applies_when,
            "not_when": unit.not_when,
            "ba_ii_plus_steps": unit.ba_ii_plus_steps,
            "source_refs": unit.source_refs,
            "priority_formula": (
                "0.25*exam_weight + 0.20*decay_pressure + 0.18*formula_frequency + "
                "0.14*mistake_link_strength + 0.10*boundary_value + "
                "0.08*calculator_value + 0.05*source_quality"
            ),
        }

    # ── Syllabus coverage audit ─────────────────────────────────────────

    def import_syllabus_text(
        self,
        *,
        profile_id: str = "default",
        text: str,
        exam: str | None = None,
    ) -> dict[str, Any]:
        """Import syllabus topics from pasted local text."""
        topics = self._topics_from_syllabus_text(profile_id=profile_id or "default", text=text, exam=exam)
        if not topics:
            raise ValueError("No syllabus topics could be parsed from the pasted text.")
        return self._upsert_syllabus_topics(topics)

    def import_syllabus_json(
        self,
        *,
        profile_id: str = "default",
        payload: Any,
        exam: str | None = None,
    ) -> dict[str, Any]:
        """Import syllabus topics from a JSON list or {topics: [...]} payload."""
        raw_topics = payload.get("topics", []) if isinstance(payload, dict) else payload
        if not isinstance(raw_topics, list):
            raise ValueError("Syllabus JSON must be a list or an object with a topics list.")
        topics = [
            self._topic_from_import_item(item, profile_id=profile_id or "default", exam=exam)
            for item in raw_topics
            if isinstance(item, dict)
        ]
        topics = [topic for topic in topics if topic.title and topic.subject]
        if not topics:
            raise ValueError("No valid syllabus topics found in JSON payload.")
        return self._upsert_syllabus_topics(topics)

    def seed_demo_syllabus(self, *, profile_id: str = "default") -> dict[str, Any]:
        """Seed a compact CFA-like local demo syllabus."""
        return self._upsert_syllabus_topics(self._demo_syllabus_topics(profile_id=profile_id or "default"))

    def list_syllabus_topics(
        self,
        *,
        profile_id: str = "default",
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        """List locally stored syllabus topics."""
        topics = [
            topic for topic in self._load_syllabus_topics()
            if topic.profile_id in {profile_id or "default", "default"}
            and (include_inactive or topic.active)
        ]
        topics.sort(key=lambda topic: (-topic.exam_weight, topic.subject, topic.module, topic.los or "", topic.title))
        return [topic.as_dict() for topic in topics]

    def recompute_syllabus_coverage(self, *, profile_id: str = "default") -> dict[str, Any]:
        """Recompute asset coverage for each active syllabus topic."""
        profile_id = profile_id or "default"
        topics = [
            topic for topic in self._load_syllabus_topics()
            if topic.profile_id in {profile_id, "default"} and topic.active
        ]
        if not topics:
            self.seed_demo_syllabus(profile_id=profile_id)
            topics = [
                topic for topic in self._load_syllabus_topics()
                if topic.profile_id in {profile_id, "default"} and topic.active
            ]

        assets = self._all_assets_for_coverage(profile_id=profile_id)
        links = self._map_assets_to_syllabus_topics(assets, topics)
        assets_by_id = {asset.asset_id: asset for asset in assets}
        links_by_topic: dict[str, list[AssetSyllabusLink]] = {}
        for link in links:
            links_by_topic.setdefault(link.topic_id, []).append(link)

        records: list[dict[str, Any]] = []
        for topic in topics:
            linked_assets = [
                assets_by_id[link.asset_id]
                for link in links_by_topic.get(topic.topic_id, [])
                if link.asset_id in assets_by_id
            ]
            record = self._coverage_record_for_topic(topic, linked_assets)
            record_payload = record.as_dict()
            record_payload["topic"] = topic.as_dict()
            record_payload["links"] = [link.as_dict() for link in links_by_topic.get(topic.topic_id, [])]
            record_payload["linked_assets"] = [asset.as_dict() for asset in linked_assets]
            record_payload["transfer_gaps"] = [
                gap.as_dict() for gap in self._open_transfer_gaps_for_topic(topic)
            ]
            records.append(record_payload)

        records.sort(key=lambda item: (self._coverage_status_rank(item["coverage_status"]), -item["topic"]["exam_weight"], item["topic"]["title"]))
        summary: dict[str, int] = {
            "covered": 0,
            "partial": 0,
            "draft_only": 0,
            "missing": 0,
            "weak": 0,
            "stale": 0,
        }
        for record in records:
            summary[record["coverage_status"]] = summary.get(record["coverage_status"], 0) + 1

        payload = {
            "profile_id": profile_id,
            "topic_count": len(topics),
            "asset_count": len(assets),
            "link_count": len(links),
            "summary": summary,
            "records": records,
            "links": [link.as_dict() for link in links],
            "coverage_scoring_formula": (
                "0.30*confirmed_core_asset_coverage + 0.20*formula_coverage + "
                "0.15*decision_rule_coverage + 0.15*mastery_strength + "
                "0.10*source_quality + 0.10*review_recency"
            ),
        }
        self._persist_syllabus_coverage(profile_id, payload)
        return payload

    def get_syllabus_coverage_record(self, topic_id: str, *, profile_id: str = "default") -> dict[str, Any]:
        """Return one topic coverage record, recomputing if needed."""
        coverage = self.recompute_syllabus_coverage(profile_id=profile_id or "default")
        for record in coverage["records"]:
            if record["topic_id"] == topic_id:
                return record
        raise KeyError(f"Syllabus topic not found: {topic_id}")

    # ── Mock retro / transfer gap analysis ─────────────────────────────

    def import_mock_retro_text(
        self,
        *,
        profile_id: str = "default",
        title: str,
        text: str,
        exam: str | None = None,
    ) -> dict[str, Any]:
        """Import pasted mock/practice retro text as correct-rule evidence."""
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Mock retro text is required.")
        profile_id = profile_id or "default"
        content_hash = sha256(cleaned.encode("utf-8")).hexdigest()
        mock_id = self._stable_id("mock-retro", profile_id, title or "Mock Retro", content_hash)
        existing = self._load_mock_session(mock_id)
        if existing is not None:
            evidence = self._load_mock_evidence(mock_id)
            return {
                "session": existing.as_dict(),
                "evidence_count": len(evidence),
                "evidence": [item.as_dict() for item in evidence],
                "duplicate": True,
            }

        evidence = self._mock_evidence_from_text(mock_id=mock_id, profile_id=profile_id, text=cleaned)
        total_questions = len(evidence)
        correct_count = sum(1 for item in evidence if item.is_correct)
        now = datetime.now(timezone.utc).isoformat()
        session = MockSession(
            mock_id=mock_id,
            profile_id=profile_id,
            title=title.strip() or "Mock Retro",
            exam=exam,
            started_at=None,
            completed_at=now,
            source_type="import_text",
            total_questions=total_questions,
            correct_count=correct_count,
            score=(correct_count / total_questions) if total_questions else None,
            time_spent_seconds=sum(item.time_spent_seconds or 0 for item in evidence) or None,
            source_refs=[item.evidence_id for item in evidence],
        )
        self._persist_mock_session(session)
        self._persist_mock_evidence(mock_id, evidence)
        return {
            "session": session.as_dict(),
            "evidence_count": len(evidence),
            "evidence": [item.as_dict() for item in evidence],
            "duplicate": False,
        }

    def list_mock_retro_sessions(self, *, profile_id: str = "default") -> list[dict[str, Any]]:
        """List imported mock retro sessions, newest first."""
        sessions = [
            self._mock_session_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._mock_retro_root.glob("mock-retro-*.json")
        ]
        sessions = [session for session in sessions if session.profile_id in {profile_id or "default", "default"}]
        sessions.sort(key=lambda session: session.completed_at or "", reverse=True)
        return [session.as_dict() for session in sessions]

    def get_mock_retro_session(self, mock_id: str) -> dict[str, Any] | None:
        """Return one mock retro session with sanitized evidence."""
        session = self._load_mock_session(mock_id)
        if session is None:
            return None
        evidence = self._load_mock_evidence(mock_id)
        return {
            "session": session.as_dict(),
            "evidence_count": len(evidence),
            "evidence": [item.as_dict() for item in evidence],
        }

    def analyze_mock_session(self, mock_id: str) -> dict[str, Any]:
        """Analyze mock evidence into TransferGapRecord objects."""
        session = self._load_mock_session(mock_id)
        if session is None:
            raise KeyError(f"Mock retro session not found: {mock_id}")
        evidence = self._load_mock_evidence(mock_id)
        gaps = self._transfer_gaps_from_evidence(session, evidence)
        persisted = [self._persist_or_merge_transfer_gap(gap) for gap in gaps]
        persisted.sort(key=lambda gap: (gap.status != "open", -gap.severity, gap.gap_type))
        return {
            "session": session.as_dict(),
            "gap_count": len(persisted),
            "gaps": [gap.as_dict() for gap in persisted],
        }

    def list_transfer_gaps(
        self,
        *,
        profile_id: str = "default",
        status: str = "",
    ) -> list[dict[str, Any]]:
        """List transfer gaps inferred from mock/practice evidence."""
        gaps = self._load_transfer_gaps(profile_id=profile_id or "default")
        if status:
            gaps = [gap for gap in gaps if gap.status == status]
        gaps.sort(key=lambda gap: (gap.status != "open", -gap.severity, gap.last_seen_at), reverse=False)
        return [gap.as_dict() for gap in gaps]

    def get_transfer_gap(self, gap_id: str) -> dict[str, Any] | None:
        """Return one transfer gap record."""
        gap = self._load_transfer_gap(gap_id)
        return gap.as_dict() if gap else None

    def resolve_transfer_gap(self, gap_id: str) -> dict[str, Any]:
        """Mark a transfer gap resolved and remove its priority effect."""
        gap = self._load_transfer_gap(gap_id)
        if gap is None:
            raise KeyError(f"Transfer gap not found: {gap_id}")
        gap.status = "resolved"
        gap.severity = 0.0
        self._persist_transfer_gap(gap)
        return gap.as_dict()

    def generate_review_from_transfer_gaps(
        self,
        *,
        profile_id: str = "default",
        max_units: int = 10,
    ) -> ReviewLabSession:
        """Create a correct-only Review Lab session from open transfer gaps."""
        profile_id = profile_id or "default"
        gaps = [
            gap for gap in self._load_transfer_gaps(profile_id=profile_id)
            if gap.status == "open" and gap.severity > 0
        ]
        gaps.sort(key=lambda gap: (-gap.severity, -gap.evidence_count, gap.gap_type))
        units: list[DailyReviewUnit] = []
        for gap in gaps:
            if len(units) >= max_units:
                break
            evidence = self._best_evidence_for_gap(gap)
            if evidence is None:
                continue
            units.append(self._unit_from_transfer_gap(gap, evidence))

        review_id = f"mock-retro-{datetime.now(timezone.utc).date().isoformat()}"
        session_id = self._stable_id("mock-retro-session", profile_id, datetime.now(timezone.utc).isoformat())
        session = ReviewLabSession(
            session_id=session_id,
            review_id=review_id,
            status="active",
            units=units,
            current_unit_index=0,
            energy_level=2,
            focus_topic="Mock Retro Transfer Gaps",
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._persist_session(session)
        return session

    def explain_unit(self, unit_id: str, review_id: str = "") -> dict[str, Any]:
        """Explain why a unit is due today and how it was scored."""
        snapshot = self._load_snapshot(review_id)
        units = self._build_units_from_snapshot(snapshot, max_units=100)
        unit = next((candidate for candidate in units if candidate.unit_id == unit_id), None)
        if unit is None:
            raise ValueError(f"Unit not found: {unit_id}")
        return {
            "unit_id": unit.unit_id,
            "asset_id": unit.asset_id,
            "asset_type": unit.asset_type,
            "due_reason": unit.due_reason,
            "source_refs": unit.source_refs,
            "memory_state_before": unit.memory_state,
            "priority": unit.priority,
            "priority_formula": (
                "0.28*syllabus_importance + 0.22*decay_pressure + "
                "0.18*mistake_link_strength + 0.12*mock_transfer_gap + "
                "0.10*formula_or_boundary_value + 0.06*confidence_mismatch + "
                "0.04*resource_quality"
            ),
        }

    def get_session(self, session_id: str) -> ReviewLabSession | None:
        """Load a persisted session by ID."""
        path = self._session_root / f"{session_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return self._deserialize_session(data)

    def submit_outcome(
        self,
        session_id: str,
        unit_id: str,
        outcome: ReviewUnitOutcome,
    ) -> dict[str, Any]:
        """Record a unit outcome, update KMEngine, and advance session."""
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        if session.status != "active":
            raise ValueError(f"Session is not active: {session.status}")

        unit = next((u for u in session.units if u.unit_id == unit_id), None)
        if unit is None:
            raise ValueError(f"Unit not found in session: {unit_id}")

        # Append outcome
        session.outcomes.append(outcome)
        if unit_id not in session.completed_unit_ids:
            session.completed_unit_ids.append(unit_id)

        # Advance to next uncompleted unit
        self._advance_session(session)

        # Update KnowledgeMemoryEngine
        km_result = self._update_knowledge_memory(unit, outcome)
        formula_result = self._update_formula_memory(unit, outcome)

        # Update mistake card if linked
        card_result = self._update_card_if_linked(unit, outcome)

        self._persist_session(session)

        return {
            "session_id": session.session_id,
            "unit_id": unit_id,
            "outcome": outcome.outcome,
            "km_decision": km_result,
            "formula_update": formula_result,
            "card_update": card_result,
            "progress_pct": session.progress_pct,
            "is_complete": session.is_complete,
        }

    def submit_unit_completion(
        self,
        unit_id: str,
        outcome: ReviewUnitOutcome,
        session_id: str = "",
    ) -> dict[str, Any]:
        """Compatibility workflow for POST /units/{unit_id}/complete."""
        if session_id:
            return self.submit_outcome(session_id, unit_id, outcome)

        session = self._latest_active_session()
        if session is None:
            snapshot = self._load_snapshot("")
            session = self.create_session(snapshot.get("review_id", ""))
        return self.submit_outcome(session.session_id, unit_id, outcome)

    def pause_session(self, session_id: str) -> ReviewLabSession:
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        session.status = "paused"
        session.paused_at = datetime.now(timezone.utc).isoformat()
        self._persist_session(session)
        return session

    def resume_session(self, session_id: str) -> ReviewLabSession:
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        session.status = "active"
        session.resumed_at = datetime.now(timezone.utc).isoformat()
        self._persist_session(session)
        return session

    def complete_session(self, session_id: str) -> ReviewLabSession:
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc).isoformat()
        self._persist_session(session)
        self._record_session_completion_event(session)
        return session

    def get_session_report(self, session_id: str) -> dict[str, Any]:
        session = self.get_session(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")

        outcomes = session.outcomes
        total = len(outcomes)
        if total == 0:
            return {"session_id": session_id, "total_units": 0, "summary": "No outcomes recorded"}

        recalled = sum(1 for o in outcomes if o.outcome == "recalled")
        partial = sum(1 for o in outcomes if o.outcome == "partial")
        forgot = sum(1 for o in outcomes if o.outcome == "forgot")
        skipped = sum(1 for o in outcomes if o.outcome == "skipped")

        avg_confidence_before = sum(o.confidence_before for o in outcomes) / total
        avg_confidence_after = sum(o.confidence_after for o in outcomes) / total
        total_time = sum(o.time_spent_seconds for o in outcomes)

        # Per-subject breakdown
        subject_stats: dict[str, dict[str, Any]] = {}
        for unit, outcome in zip(
            [u for u in session.units if u.unit_id in session.completed_unit_ids],
            outcomes,
        ):
            subj = unit.subject or "Unknown"
            if subj not in subject_stats:
                subject_stats[subj] = {"total": 0, "recalled": 0, "partial": 0, "forgot": 0, "skipped": 0}
            subject_stats[subj]["total"] += 1
            subject_stats[subj][outcome.outcome] += 1

        return {
            "session_id": session_id,
            "review_id": session.review_id,
            "status": session.status,
            "total_units": len(session.units),
            "completed_units": len(session.completed_unit_ids),
            "recalled": recalled,
            "partial": partial,
            "forgot": forgot,
            "skipped": skipped,
            "recall_rate": round(recalled / total, 3) if total else 0,
            "avg_confidence_before": round(avg_confidence_before, 2),
            "avg_confidence_after": round(avg_confidence_after, 2),
            "total_time_seconds": total_time,
            "subject_breakdown": subject_stats,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
        }

    def list_session_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """List lab sessions across active, paused, and completed states, newest first."""
        sessions: list[dict[str, Any]] = []
        for path in sorted(self._session_root.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            data = json.loads(path.read_text(encoding="utf-8"))
            units = data.get("units", [])
            completed_unit_ids = data.get("completed_unit_ids", [])
            sessions.append({
                "session_id": data["session_id"],
                "review_id": data.get("review_id", ""),
                "status": data.get("status", "active"),
                "started_at": data.get("started_at", ""),
                "paused_at": data.get("paused_at", ""),
                "resumed_at": data.get("resumed_at", ""),
                "completed_at": data.get("completed_at", ""),
                "current_unit_index": data.get("current_unit_index", 0),
                "unit_count": len(units),
                "completed_unit_count": len(completed_unit_ids),
                "outcome_count": len(data.get("outcomes", [])),
                "progress_pct": (len(completed_unit_ids) / len(units)) if units else 0.0,
                "is_complete": len(completed_unit_ids) >= len(units) if units else False,
            })
            if len(sessions) >= limit:
                break
        return sessions

    # ── Unit building ────────────────────────────────────────────────────

    def _build_units_from_snapshot(
        self,
        snapshot: dict[str, Any],
        max_units: int,
    ) -> list[DailyReviewUnit]:
        """Transform a daily review snapshot into ordered review units."""
        assets = self._build_assets_from_snapshot(snapshot)
        selected = self._select_assets_for_mix(assets, max_units)
        review_id = snapshot.get("review_id", "")
        return [self._unit_from_asset(asset, review_id) for asset in selected]

    def _build_assets_from_snapshot(self, snapshot: dict[str, Any]) -> list[CorrectKnowledgeAsset]:
        """Build correct-knowledge assets from syllabus points and mistake cards."""
        assets: list[CorrectKnowledgeAsset] = []
        seen_ids: set[str] = set()

        for point in snapshot.get("knowledge_points", []):
            kid = point.get("knowledge_id", "")
            if not kid or kid in seen_ids:
                continue
            seen_ids.add(kid)

            subject = point.get("subject", "")
            heading = point.get("heading", "")
            trigger = point.get("trigger", "")
            formula = point.get("formula", "")
            boundaries = self._coerce_list(point.get("boundaries", []))
            asset_type = "formula_lab" if self._is_formula_asset(subject, trigger, formula) else "syllabus_core"
            correct_rule = point.get("decision") or self._default_correct_rule(heading, trigger)

            assets.append(
                CorrectKnowledgeAsset(
                    asset_id=kid,
                    asset_type=asset_type,
                    subject=subject,
                    module=heading,
                    los=trigger,
                    title=heading or trigger or "Core knowledge",
                    trigger=trigger,
                    correct_rule=correct_rule,
                    formula_latex=formula,
                    not_when=boundaries,
                    source_refs=point.get("source_refs", []),
                    exam_weight=float(point.get("exam_weight", 0.7 if asset_type == "formula_lab" else 0.6)),
                    mistake_link_count=int(point.get("mistake_link_count", 0)),
                    decay_risk=self._decay_risk_value(point.get("decay_risk", point.get("state", ""))),
                    mastery_state=point.get("state", "New"),
                    next_review_at=point.get("next_review_at", ""),
                    created_from="formula" if asset_type == "formula_lab" else "syllabus",
                    validation_status="derived",
                    source_quality=0.8 if point.get("source_refs") else 0.6,
                )
            )

        for card in snapshot.get("mistake_cards", []):
            cid = card.get("card_id", "")
            if not cid or cid in seen_ids:
                continue
            seen_ids.add(cid)

            card_content = self._load_card_content(cid) or {}
            topic = card.get("topic", "") or card_content.get("topic", "")
            los = card.get("los", "") or card_content.get("los", "")
            correct_rule = (
                card_content.get("correct_resolution")
                or card_content.get("fix_rule")
                or "Recall and apply the corrected rule for this LOS."
            )
            title = topic or los or "Corrected mistake knowledge"

            assets.append(
                CorrectKnowledgeAsset(
                    asset_id=cid,
                    asset_type="mistake_corrected",
                    subject=topic,
                    module=topic,
                    los=los,
                    title=title,
                    trigger=los or topic,
                    correct_rule=correct_rule,
                    example=card_content.get("next_drill", ""),
                    correct_steps=self._steps_from_text(correct_rule),
                    source_refs=card.get("source_refs", []),
                    source_quality=0.65,
                    exam_weight=float(card.get("exam_weight", 0.55)),
                    mistake_link_count=1,
                    decay_risk=0.7,
                    mastery_state=card.get("state", "New"),
                    created_from="mistake",
                    validation_status="derived",
                )
            )

        profile_id = snapshot.get("profile_id", "default")
        for asset in self._load_confirmed_ingested_assets(profile_id=profile_id):
            if asset.asset_id in seen_ids:
                continue
            seen_ids.add(asset.asset_id)
            assets.append(asset)

        for asset in assets:
            asset.exam_weight = min(max(float(asset.exam_weight), 0.0), 1.0)
        assets.sort(key=self._asset_priority, reverse=True)
        return assets

    def _select_assets_for_mix(
        self,
        assets: list[CorrectKnowledgeAsset],
        max_units: int,
    ) -> list[CorrectKnowledgeAsset]:
        if max_units <= 0:
            return []

        ranked_assets = sorted(
            assets,
            key=lambda asset: self._asset_priority(asset) + self._coverage_guidance_boost(asset),
            reverse=True,
        ) if self._coverage_guided_selection_enabled() else assets
        source_backed_ids = {
            asset.asset_id
            for asset in ranked_assets
            if asset.created_from in {"pdf_note", "markdown_note", "text_note", "manual"}
        }
        core = [asset for asset in ranked_assets if asset.asset_type == "syllabus_core" or asset.asset_id in source_backed_ids]
        formula = [asset for asset in ranked_assets if asset.asset_type in {"formula_lab", "formula"}]
        mistakes = [asset for asset in ranked_assets if asset.asset_type == "mistake_corrected"]
        transfer = [asset for asset in ranked_assets if asset.asset_type == "transfer_or_interleaving"]

        target_core = max(1, (max_units + 1) // 2) if core else 0
        target_mistake = max(0, round(max_units * 0.3)) if mistakes else 0
        target_formula = max(0, round(max_units * 0.1)) if formula else 0
        target_transfer = max(0, max_units - target_core - target_mistake - target_formula) if transfer else 0

        raw_selected = [
            *core[:target_core],
            *mistakes[:target_mistake],
            *formula[:target_formula],
            *transfer[:target_transfer],
        ]
        selected: list[CorrectKnowledgeAsset] = []
        selected_ids: set[str] = set()
        for asset in raw_selected:
            if asset.asset_id in selected_ids:
                continue
            selected.append(asset)
            selected_ids.add(asset.asset_id)
        for asset in ranked_assets:
            if len(selected) >= max_units:
                break
            if asset.asset_id not in selected_ids:
                selected.append(asset)
                selected_ids.add(asset.asset_id)

        selected.sort(key=lambda asset: self._asset_priority(asset) + self._coverage_guidance_boost(asset), reverse=True)
        return selected[:max_units]

    def _unit_from_asset(self, asset: CorrectKnowledgeAsset, review_id: str) -> DailyReviewUnit:
        priority = int(round(self._asset_priority(asset) * 100))
        is_formula = asset.asset_type in {"formula_lab", "formula"}
        is_mistake = asset.asset_type == "mistake_corrected"
        unit_type = "mistake_corrected" if is_mistake else asset.asset_type
        display_mode = "formula_input" if is_formula else "recall_reveal"
        prompt = asset.title or asset.trigger or "Recall this correct rule"
        front_prompt = (
            f"Recall the correct rule for: {asset.los or asset.title}"
            if is_mistake else
            f"Recall from memory: {prompt}"
        )
        correct_reasoning = asset.correct_rule
        if asset.correct_steps:
            correct_reasoning = "\n".join(asset.correct_steps)

        return DailyReviewUnit(
            unit_id=f"unit-{asset.asset_id}",
            review_id=review_id,
            asset_id=asset.asset_id,
            asset_type=asset.asset_type,
            unit_type=unit_type,  # type: ignore[arg-type]
            display_mode=display_mode,
            prompt=front_prompt,
            front_prompt=front_prompt,
            recall_instruction=(
                "Write the formula and variables first, then reveal the correct version."
                if is_formula else
                "Answer from memory first. Reveal only after committing to your recall."
            ),
            answer=asset.correct_rule,
            correct_answer=asset.correct_rule,
            correct_reasoning=correct_reasoning,
            correct_steps=asset.correct_steps,
            formula_latex=asset.formula_latex,
            worked_example=asset.example,
            boundary_rules=asset.common_correct_boundary_rules or asset.not_when,
            variables=asset.variables,
            applies_when=asset.applies_when,
            not_when=asset.not_when,
            assumptions=asset.assumptions,
            ba_ii_plus_steps=asset.ba_ii_plus_steps,
            formula_family=asset.formula_family,
            difficulty=asset.difficulty,
            source_refs=asset.source_refs,
            due_reason=self._due_reason(asset),
            memory_state=asset.mastery_state,
            priority=priority,
            interaction_mode=display_mode,
            knowledge_id=asset.asset_id if asset.created_from != "mistake" else "",
            card_id=asset.asset_id if asset.created_from == "mistake" else "",
            subject=asset.subject,
            heading=asset.module,
            los=asset.los,
        )

    def _asset_priority(self, asset: CorrectKnowledgeAsset) -> float:
        """Transparent priority scoring from the TASK-001 formula."""
        syllabus_importance = asset.exam_weight
        decay_pressure = asset.decay_risk
        mistake_link_strength = min(asset.mistake_link_count / 3, 1.0)
        transfer_gap_severity = self._transfer_gap_severity_for_asset(asset) if self._transfer_gap_priority_enabled() else 0.0
        mock_transfer_gap = max(transfer_gap_severity, 0.6 if asset.asset_type == "transfer_or_interleaving" else 0.3)
        formula_or_boundary_value = 1.0 if asset.formula_latex or asset.not_when or asset.asset_type in {"formula_lab", "formula", "exam_boundary"} else 0.4
        has_confidence_gap = transfer_gap_severity if self._asset_has_gap_type(asset, "confidence_mismatch") else 0.0
        confidence_mismatch = max(has_confidence_gap, 0.6 if asset.mastery_state in {"New", "new", "Reviewed once", "Learning"} else 0.2)
        resource_quality = asset.source_quality
        return (
            0.28 * syllabus_importance
            + 0.22 * decay_pressure
            + 0.18 * mistake_link_strength
            + 0.12 * mock_transfer_gap
            + 0.10 * formula_or_boundary_value
            + 0.06 * confidence_mismatch
            + 0.04 * resource_quality
        )

    @staticmethod
    def _coerce_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, tuple):
            return [str(item) for item in value if str(item).strip()]
        if not value:
            return []
        return [part.strip() for part in str(value).split(";") if part.strip()]

    @staticmethod
    def _decay_risk_value(value: Any) -> float:
        if isinstance(value, int | float):
            return min(max(float(value), 0.0), 1.0)
        mapping = {
            "overdue": 1.0,
            "high": 0.85,
            "medium": 0.65,
            "low": 0.35,
            "new": 0.7,
            "reviewed once": 0.55,
            "learning": 0.6,
            "familiar": 0.35,
            "practiced": 0.25,
            "proficient": 0.15,
            "mastered": 0.05,
        }
        return mapping.get(str(value).strip().lower(), 0.5)

    @staticmethod
    def _is_formula_asset(subject: str, trigger: str, formula: str) -> bool:
        if formula:
            return True
        text = f"{subject} {trigger}".lower()
        return any(
            token in text
            for token in (
                "formula",
                "eps",
                "duration",
                "yield",
                "return",
                "standard error",
                "quantitative",
                "fixed income",
                "derivatives",
            )
        )

    @staticmethod
    def _default_correct_rule(heading: str, trigger: str) -> str:
        if heading and trigger:
            return f"{heading}: correctly define, recall, and apply {trigger}."
        if heading:
            return f"Correctly define and apply {heading}."
        if trigger:
            return f"Correctly recall and apply {trigger}."
        return "Recall the correct concept, boundary, and next action."

    @staticmethod
    def _steps_from_text(text: str) -> list[str]:
        lines = [line.strip("- ").strip() for line in text.splitlines()]
        steps = [line for line in lines if line]
        if len(steps) <= 1 and text:
            return [text.strip()]
        return steps[:6]

    def _due_reason(self, asset: CorrectKnowledgeAsset) -> str:
        if asset.resource_id:
            resource = self._resource_for_asset(asset)
            if resource is not None and resource.quality_status in {"high", "trusted"}:
                if asset.syllabus_topic_id:
                    return "High-quality resource supports weak syllabus topic."
                return "Confirmed high-quality resource selected for recall."
            if resource is not None and self._asset_has_open_transfer_gap(asset):
                return "Resource addresses recent transfer gap."
            return "Confirmed resource fills coverage gap."
        if asset.created_from in {"pdf_note", "markdown_note", "text_note", "manual"}:
            return "Confirmed source-backed note asset selected for recall."
        if asset.asset_type == "mistake_corrected":
            return "Corrected from a prior mistake; rehearse the right rule only."
        if asset.asset_type in {"formula_lab", "formula"}:
            return "Formula or boundary-heavy syllabus item selected for recall."
        return "Syllabus/core knowledge selected by priority and decay risk."

    @staticmethod
    def _unit_mix_summary(units: list[DailyReviewUnit]) -> dict[str, int]:
        summary: dict[str, int] = {}
        for unit in units:
            key = unit.asset_type or unit.unit_type
            summary[key] = summary.get(key, 0) + 1
        return summary

    def _latest_active_session(self) -> ReviewLabSession | None:
        for item in self.list_session_history(limit=20):
            if item.get("status") in {"active", "paused"}:
                return self.get_session(item["session_id"])
        return None

    # ── Source-backed asset ingestion ───────────────────────────────────

    def _segments_from_text(self, source_id: str, text: str) -> list[KnowledgeSourceSegment]:
        segments: list[KnowledgeSourceSegment] = []
        heading: str | None = None
        cursor = 0
        for raw_chunk in re.split(r"\n+|(?<=\.)\s+(?=[A-Z0-9#])", text):
            chunk = raw_chunk.strip()
            if not chunk:
                cursor += len(raw_chunk)
                continue
            if chunk.startswith("#"):
                heading = chunk.lstrip("#").strip() or heading
                cursor += len(raw_chunk)
                continue
            start = text.find(chunk, cursor)
            if start < 0:
                start = None  # type: ignore[assignment]
                end = None
            else:
                end = start + len(chunk)
                cursor = end
            segment_index = len(segments) + 1
            segment_id = f"segment-{source_id}-{segment_index}"
            source_ref = f"{source_id}#seg-{segment_index}"
            segments.append(
                KnowledgeSourceSegment(
                    segment_id=segment_id,
                    source_id=source_id,
                    page=None,
                    heading=heading,
                    text=chunk,
                    char_start=start,
                    char_end=end,
                    source_ref=source_ref,
                    evidence_type=self._evidence_type_from_text(chunk),  # type: ignore[arg-type]
                    confidence=self._segment_confidence(chunk),
                )
            )
        return segments

    def _candidate_assets_from_segment(
        self,
        source: KnowledgeSourceDocument,
        segment: KnowledgeSourceSegment,
        context_text: str = "",
    ) -> list[CorrectKnowledgeAsset]:
        text = " ".join(segment.text.split())
        if len(text) < 8:
            return []

        asset_type = self._classify_segment(text)
        if asset_type is None:
            return []

        formula_metadata = self._extract_formula_metadata(text, context_text or text) if asset_type == "formula" else None
        title = self._candidate_title(text, segment.heading)
        formula_latex = formula_metadata.formula_latex if formula_metadata else ""
        boundary_rules = [text] if asset_type in {"exam_boundary", "decision_rule"} else []
        asset_id = self._stable_id("asset", source.source_id, segment.source_ref, asset_type, text[:120])
        status = "draft" if asset_type in {"definition", "formula", "exam_boundary", "procedure"} else "needs_review"

        return [
            CorrectKnowledgeAsset(
                asset_id=asset_id,
                asset_type=asset_type,  # type: ignore[arg-type]
                profile_id=source.profile_id,
                subject=source.title,
                module=segment.heading or source.title,
                title=title,
                trigger=title,
                correct_rule=self._correct_rule_from_candidate(asset_type, text),
                formula_latex=formula_latex,
                plain_formula=formula_metadata.plain_formula or "" if formula_metadata else "",
                variables=formula_metadata.variables if formula_metadata else [],
                applies_when=formula_metadata.applies_when if formula_metadata else [],
                not_when=boundary_rules,
                assumptions=formula_metadata.assumptions if formula_metadata else [],
                common_correct_boundary_rules=formula_metadata.common_correct_boundary_rules if formula_metadata else [],
                example=formula_metadata.worked_example or "" if formula_metadata else "",
                ba_ii_plus_steps=formula_metadata.ba_ii_plus_steps if formula_metadata else [],
                formula_family=formula_metadata.formula_family or "" if formula_metadata else "",
                difficulty=formula_metadata.difficulty if formula_metadata else "basic",
                source_refs=[segment.source_ref],
                source_quality=0.45,
                exam_weight=0.68 if asset_type in {"formula", "exam_boundary", "decision_rule"} else 0.58,
                decay_risk=0.7,
                mastery_state="new",
                created_from=source.source_type,  # type: ignore[arg-type]
                validation_status=status,  # type: ignore[arg-type]
            )
        ]

    @staticmethod
    def _classify_segment(text: str) -> str | None:
        lowered = text.lower()
        formula_tokens = (
            "=",
            "≈",
            "Δ",
            "Σ",
            "%",
            "÷",
            "×",
            "^",
            " npv",
            " irr",
            " wacc",
            " roe",
            " roa",
            " pv",
            " fv",
            " pmt",
            " d/e",
            " d/v",
            "duration",
            "convexity",
            "yield",
            "return",
            "tax",
            "depreciation",
            "fcff",
            "fcfe",
            "公式",
            "计算",
            "等于",
            "formula",
            "calculate",
            "is calculated as",
        )
        has_formula_operator = any(token in text for token in ("=", "≈", "Δ", "Σ", "÷", "×", "^"))
        has_variable_expression = bool(re.search(r"\b[A-Z][A-Za-z0-9_/]*\b\s*[=+/()^*-]", text))
        if has_formula_operator or has_variable_expression or any(token in lowered for token in formula_tokens[8:]) or any(token in text for token in formula_tokens[:8]):
            return "formula"
        if re.search(r"\b(if|when|only if|unless|not when|except)\b", lowered):
            if re.search(r"\b(use|choose|apply|select)\b", lowered):
                return "decision_rule"
            return "exam_boundary"
        if re.search(r"\b(vs\.?|versus|whereas|difference between)\b", lowered):
            return "concept_comparison"
        if re.search(r"(^|\s)(step\s+\d+|\d+\.|first,|then,|finally,)", lowered):
            return "procedure"
        if re.search(r"\b(is|are|refers to|means|defined as)\b", lowered):
            return "definition"
        if re.search(r"\b(example|for example|worked example|e\.g\.)\b", lowered):
            return "worked_example"
        return None

    @classmethod
    def _evidence_type_from_text(cls, text: str) -> str:
        asset_type = cls._classify_segment(text)
        if asset_type == "formula":
            return "formula"
        if asset_type in {"decision_rule", "exam_boundary"}:
            return "boundary" if asset_type == "exam_boundary" else "rule"
        if asset_type == "worked_example":
            return "example"
        if asset_type == "procedure":
            return "procedure"
        if asset_type == "definition":
            return "definition"
        lowered = text.lower()
        if re.search(r"\b(source|cited|reference|curriculum|los)\b", lowered):
            return "citation"
        if re.search(r"\b(dictionary|definition|entry)\b", lowered):
            return "dictionary_entry"
        return "other"

    @staticmethod
    def _segment_confidence(text: str) -> float:
        lowered = text.lower()
        confidence = 0.45
        if len(text) >= 40:
            confidence += 0.15
        if any(token in lowered for token in ("=", "defined as", "refers to", "use when", "only if", "step")):
            confidence += 0.2
        if re.search(r"\b(los|reading|module|source|curriculum|cfa)\b", lowered):
            confidence += 0.1
        if len(text) < 18:
            confidence -= 0.15
        return round(min(max(confidence, 0.0), 1.0), 4)

    def _extract_formula_metadata(self, formula_text: str, context_text: str) -> FormulaMetadata:
        plain_formula = self._extract_plain_formula(formula_text)
        variables = self._extract_variables(plain_formula or formula_text, context_text)
        applies_when = self._sentences_matching(context_text, r"\b(use|apply|when|only if|target capital structure|stable|calculate)\b")
        not_when = self._sentences_matching(context_text, r"\b(not when|do not|unless|except|not appropriate|avoid)\b")
        assumptions = self._sentences_matching(context_text, r"\b(assume|assumption|stable|constant|target|perpetual)\b")
        ba_steps = self._extract_ba_ii_plus_steps(context_text)
        worked_example = self._first_sentence_matching(context_text, r"\b(example|for example|worked example|e\.g\.|given)\b")
        boundary_rules = [
            f"Use only when {item}" if not item.lower().startswith(("use", "apply", "when")) else item
            for item in applies_when[:3]
        ]
        boundary_rules.extend(not_when[:3])
        difficulty = "advanced" if len(variables) >= 5 else "intermediate" if len(variables) >= 3 else "basic"
        return FormulaMetadata(
            formula_latex=plain_formula or formula_text,
            plain_formula=plain_formula or formula_text,
            variables=variables,
            applies_when=applies_when[:4],
            not_when=not_when[:4],
            assumptions=assumptions[:4],
            common_correct_boundary_rules=boundary_rules[:5],
            worked_example=worked_example,
            ba_ii_plus_steps=ba_steps,
            formula_family=self._formula_family(context_text),
            difficulty=difficulty,  # type: ignore[arg-type]
        )

    @staticmethod
    def _extract_plain_formula(text: str) -> str:
        lines = [line.strip(" .") for line in text.splitlines() if line.strip()]
        for line in lines:
            if any(token in line for token in ("=", "≈", "Δ", "Σ", "÷", "×", "^", "/")):
                return line
        return lines[0] if lines else text.strip()

    @staticmethod
    def _extract_variables(formula: str, context_text: str) -> list[dict]:
        raw_symbols = re.findall(r"\b[A-Za-z][A-Za-z0-9_/]*\b", formula)
        stop = {
            "Use",
            "When",
            "If",
            "The",
            "And",
            "Or",
            "CPT",
            "BA",
            "II",
            "Plus",
            "Intrinsic",
            "value",
        }
        symbols: list[str] = []
        for symbol in raw_symbols:
            if symbol in stop or symbol.isdigit() or symbol in symbols:
                continue
            symbols.append(symbol)

        variables: list[dict] = []
        for symbol in symbols[:10]:
            meaning = ""
            patterns = [
                rf"\b{re.escape(symbol)}\b\s*[:=]\s*([^.;\n]+)",
                rf"\b{re.escape(symbol)}\b\s+(?:is|means|=)\s+([^.;\n]+)",
            ]
            for pattern in patterns:
                match = re.search(pattern, context_text, flags=re.IGNORECASE)
                if match:
                    meaning = match.group(1).strip()
                    break
            variables.append({"symbol": symbol, "meaning": meaning, "unit": ""})
        return variables

    @staticmethod
    def _sentences_matching(text: str, pattern: str) -> list[str]:
        sentences = [part.strip(" -") for part in re.split(r"(?<=[.!?。])\s+|\n+", text) if part.strip()]
        matches: list[str] = []
        for sentence in sentences:
            if re.search(pattern, sentence, flags=re.IGNORECASE) and sentence not in matches:
                matches.append(sentence)
        return matches

    @staticmethod
    def _first_sentence_matching(text: str, pattern: str) -> str | None:
        matches = ReviewLabEngine._sentences_matching(text, pattern)
        return matches[0] if matches else None

    @staticmethod
    def _extract_ba_ii_plus_steps(text: str) -> list[str]:
        steps: list[str] = []
        for line in text.splitlines():
            if re.search(r"\b(BA II|BAII|CPT|N=|I/Y|PV|PMT|FV|CF0|CF1|NPV)\b", line, flags=re.IGNORECASE):
                cleaned = line.strip(" -")
                if cleaned and cleaned not in steps:
                    steps.append(cleaned)
        return steps[:8]

    @staticmethod
    def _formula_family(text: str) -> str:
        lowered = text.lower()
        if "wacc" in lowered or "capital structure" in lowered:
            return "cost_of_capital"
        if "gordon" in lowered or "dividend" in lowered or "d1" in lowered:
            return "equity_valuation"
        if "pv" in lowered or "fv" in lowered or "pmt" in lowered or "npv" in lowered or "irr" in lowered:
            return "time_value_of_money"
        if "duration" in lowered or "convexity" in lowered or "yield" in lowered:
            return "fixed_income"
        if "roe" in lowered or "roa" in lowered:
            return "financial_statement_analysis"
        return "general"

    @staticmethod
    def _candidate_title(text: str, heading: str | None) -> str:
        words = re.findall(r"[A-Za-z0-9%+-]+", text)
        summary = " ".join(words[:9]).strip()
        if heading and summary:
            return f"{heading}: {summary}"
        return summary or (heading or "Source-backed asset")

    @staticmethod
    def _correct_rule_from_candidate(asset_type: str, text: str) -> str:
        if asset_type == "formula":
            return f"Recall and apply this formula exactly: {text}"
        if asset_type == "procedure":
            return f"Follow this procedure in order: {text}"
        if asset_type in {"exam_boundary", "decision_rule"}:
            return f"Apply this boundary rule: {text}"
        if asset_type == "concept_comparison":
            return f"Distinguish the concepts using this rule: {text}"
        if asset_type == "worked_example":
            return f"Reconstruct the worked example logic: {text}"
        return text

    @staticmethod
    def _is_formula_candidate_asset(asset: CorrectKnowledgeAsset) -> bool:
        return asset.asset_type in {"formula", "formula_lab"} or bool(asset.formula_latex or asset.plain_formula)

    def _formula_assets_for_session(self, *, profile_id: str, max_units: int) -> list[CorrectKnowledgeAsset]:
        assets: list[CorrectKnowledgeAsset] = []
        for path in self._asset_root.glob("*.json"):
            asset = self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if not self._is_formula_candidate_asset(asset):
                continue
            if asset.validation_status != "confirmed":
                continue
            if not asset.source_refs:
                continue
            if asset.profile_id not in {profile_id, "default"}:
                continue
            assets.append(asset)

        snapshot = self._load_snapshot("")
        for asset in self._build_assets_from_snapshot(snapshot):
            if not self._is_formula_candidate_asset(asset):
                continue
            if asset.validation_status in {"draft", "needs_review", "rejected"}:
                continue
            if asset.asset_id not in {item.asset_id for item in assets}:
                assets.append(asset)

        assets.sort(key=self._formula_priority, reverse=True)
        return assets[:max_units]

    def _formula_unit_from_asset(self, asset: CorrectKnowledgeAsset, review_id: str) -> DailyReviewUnit:
        formula = asset.formula_latex or asset.plain_formula or asset.correct_rule
        mode = "ba_ii_plus_procedure" if asset.ba_ii_plus_steps else "recall_formula"
        boundary_rules = asset.common_correct_boundary_rules or asset.not_when
        correct_steps = asset.correct_steps or [formula, *[f"{item.get('symbol', '')}: {item.get('meaning', '')}".strip(": ") for item in asset.variables[:6]]]
        return DailyReviewUnit(
            unit_id=f"formula-unit-{asset.asset_id}",
            review_id=review_id,
            asset_id=asset.asset_id,
            asset_type=asset.asset_type,
            unit_type="formula",
            display_mode=mode,  # type: ignore[arg-type]
            interaction_mode=mode,  # type: ignore[arg-type]
            prompt=f"Recall the formula for: {asset.title or asset.trigger or asset.formula_family or 'Formula'}",
            front_prompt=f"Recall the formula for: {asset.title or asset.trigger or asset.formula_family or 'Formula'}",
            recall_instruction="Write the formula and key variables before revealing.",
            answer=formula,
            correct_answer=formula,
            correct_reasoning=asset.correct_rule,
            correct_steps=[step for step in correct_steps if step],
            formula_latex=formula,
            worked_example=asset.example,
            boundary_rules=boundary_rules,
            variables=asset.variables,
            applies_when=asset.applies_when,
            not_when=asset.not_when,
            assumptions=asset.assumptions,
            ba_ii_plus_steps=asset.ba_ii_plus_steps,
            formula_family=asset.formula_family,
            difficulty=asset.difficulty,
            source_refs=asset.source_refs,
            due_reason="Formula Lab selected this confirmed formula by exam value, decay, boundaries, and source quality.",
            memory_state=asset.mastery_state,
            priority=int(round(self._formula_priority(asset) * 100)),
            knowledge_id=asset.asset_id,
            subject=asset.subject,
            heading=asset.module,
            los=asset.los,
        )

    def _formula_priority(self, asset: CorrectKnowledgeAsset) -> float:
        exam_weight = asset.exam_weight
        decay_pressure = asset.decay_risk
        formula_frequency = 1.0 if asset.asset_type in {"formula", "formula_lab"} else 0.5
        mistake_link_strength = min(asset.mistake_link_count / 3, 1.0)
        boundary_value = 1.0 if asset.applies_when or asset.not_when or asset.common_correct_boundary_rules else 0.35
        calculator_value = 1.0 if asset.ba_ii_plus_steps else 0.15
        source_quality = asset.source_quality
        transfer_gap_boost = min(0.15, 0.12 * self._transfer_gap_severity_for_asset(asset)) if self._transfer_gap_priority_enabled() else 0.0
        return (
            0.25 * exam_weight
            + 0.20 * decay_pressure
            + 0.18 * formula_frequency
            + 0.14 * mistake_link_strength
            + 0.10 * boundary_value
            + 0.08 * calculator_value
            + 0.05 * source_quality
            + transfer_gap_boost
        )

    def _source_text_for_refs(self, source_refs: list[str]) -> list[str]:
        texts: list[str] = []
        seen_sources: set[str] = set()
        for ref in source_refs:
            if ref.startswith("file:"):
                for path in self._segment_root.glob("*.json"):
                    try:
                        segments = [self._segment_from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]
                    except (json.JSONDecodeError, OSError):
                        continue
                    for segment in segments:
                        if segment.source_ref == ref:
                            texts.append(segment.text)
                continue
            source_id = ref.split("#", 1)[0]
            if source_id in seen_sources:
                continue
            seen_sources.add(source_id)
            for segment in self._load_segments(source_id):
                texts.append(segment.text)
        return texts

    @staticmethod
    def _normalize_resource_type(resource_type: str) -> str:
        allowed = {
            "text_note",
            "pdf_note",
            "web_article",
            "official_syllabus",
            "textbook",
            "lecture_slide",
            "dictionary",
            "manual",
            "unknown",
        }
        normalized = str(resource_type or "text_note").strip().lower().replace("-", "_").replace(" ", "_")
        return normalized if normalized in allowed else "unknown"

    def _resource_text(self, resource: LearningResource) -> str:
        source_id = resource.source_id or resource.resource_id
        return "\n".join(segment.text for segment in self._load_segments(source_id))

    def _score_resource_in_place(self, resource: LearningResource) -> None:
        if resource.validation_status == "rejected":
            resource.quality_score = 0.0
            resource.quality_status = "rejected"
            resource.quality_dimensions = {}
            return

        segments = self._load_segments(resource.source_id or resource.resource_id)
        text = self._resource_text(resource)
        source_type_trust = self._resource_source_type_trust(resource.resource_type)
        structure_quality = self._resource_structure_quality(resource, text, segments)
        citation_or_reference_presence = self._resource_reference_presence(resource, text)
        syllabus_alignment = self._resource_syllabus_alignment(resource, text)
        extraction_confidence = (
            sum(segment.confidence for segment in segments) / len(segments)
            if segments else 0.0
        )
        user_confirmation_signal = {
            "confirmed": 1.0,
            "needs_review": 0.45,
            "draft": 0.25,
            "rejected": 0.0,
        }.get(resource.validation_status, 0.25)
        freshness_or_version_signal = self._resource_freshness_signal(resource, text)
        dimensions = {
            "source_type_trust": source_type_trust,
            "structure_quality": structure_quality,
            "citation_or_reference_presence": citation_or_reference_presence,
            "syllabus_alignment": syllabus_alignment,
            "extraction_confidence": extraction_confidence,
            "user_confirmation_signal": user_confirmation_signal,
            "freshness_or_version_signal": freshness_or_version_signal,
        }
        score = (
            0.25 * source_type_trust
            + 0.20 * structure_quality
            + 0.15 * citation_or_reference_presence
            + 0.15 * syllabus_alignment
            + 0.10 * extraction_confidence
            + 0.10 * user_confirmation_signal
            + 0.05 * freshness_or_version_signal
        )
        if resource.duplicate_of:
            score = max(0.0, score - 0.05)
        resource.quality_score = round(self._clamp01(score), 4)
        resource.quality_dimensions = {key: round(self._clamp01(value), 4) for key, value in dimensions.items()}
        resource.quality_status = self._quality_status_for_resource(resource)

    @staticmethod
    def _resource_source_type_trust(resource_type: str) -> float:
        return {
            "official_syllabus": 0.95,
            "textbook": 0.9,
            "lecture_slide": 0.82,
            "dictionary": 0.72,
            "manual": 0.65,
            "pdf_note": 0.58,
            "web_article": 0.5,
            "text_note": 0.45,
            "unknown": 0.25,
        }.get(resource_type, 0.25)

    @staticmethod
    def _resource_structure_quality(
        resource: LearningResource,
        text: str,
        segments: list[KnowledgeSourceSegment],
    ) -> float:
        score = 0.15
        if len(text) >= 120:
            score += 0.2
        if len(text) >= 500:
            score += 0.15
        if len(segments) >= 2:
            score += 0.18
        if any(segment.heading for segment in segments) or re.search(r"(?m)^#{1,4}\s+", text):
            score += 0.12
        if re.search(r"(?m)^\s*(-|\d+[.)])\s+", text):
            score += 0.1
        if any(token in text for token in ("=", "Use when", "Only if", "LOS:", "Module:")):
            score += 0.1
        if len(resource.title.strip()) >= 8:
            score += 0.1
        return min(score, 1.0)

    @staticmethod
    def _resource_reference_presence(resource: LearningResource, text: str) -> float:
        score = 0.0
        if resource.source_refs:
            score += 0.45
        if resource.url or resource.file_path:
            score += 0.2
        if re.search(r"\b(source|citation|reading|curriculum|los|page)\b", text, flags=re.IGNORECASE):
            score += 0.25
        if resource.resource_type in {"official_syllabus", "textbook", "lecture_slide", "dictionary"}:
            score += 0.1
        return min(score, 1.0)

    def _resource_syllabus_alignment(self, resource: LearningResource, text: str) -> float:
        topics = [topic for topic in self._load_syllabus_topics() if topic.profile_id in {resource.profile_id, "default"}]
        haystack = f"{resource.title} {text}"
        if not topics:
            finance_markers = {"wacc", "duration", "npv", "gordon", "los", "cfa", "equity", "fixed income"}
            return 0.55 if finance_markers.intersection(self._keywords_for_match(haystack)) else 0.25
        best = 0.0
        resource_keywords = self._keywords_for_match(haystack)
        normalized_text = self._normalize_match_text(haystack)
        for topic in topics:
            topic_keywords = self._keywords_for_match(f"{topic.subject} {topic.module} {topic.los or ''} {topic.title}")
            overlap = resource_keywords.intersection(topic_keywords)
            denominator = max(1, min(len(topic_keywords), 10))
            score = min(0.8, len(overlap) / denominator)
            if topic.los and self._normalize_match_text(topic.los) in normalized_text:
                score = max(score, 0.95)
            if topic.module and self._normalize_match_text(topic.module) in normalized_text:
                score = max(score, 0.72)
            best = max(best, score)
        return best

    @staticmethod
    def _resource_freshness_signal(resource: LearningResource, text: str) -> float:
        if resource.resource_type in {"official_syllabus", "textbook", "lecture_slide"}:
            base = 0.75
        else:
            base = 0.55
        if re.search(r"\b(202[0-9]|version|updated|current|latest)\b", text, flags=re.IGNORECASE):
            base += 0.2
        return min(base, 1.0)

    def _quality_status_for_resource(self, resource: LearningResource) -> str:
        if resource.validation_status == "rejected":
            return "rejected"
        if (
            resource.quality_score >= 0.85
            and resource.validation_status == "confirmed"
            and resource.resource_type in {"official_syllabus", "textbook", "lecture_slide", "dictionary"}
        ):
            return "trusted"
        if resource.quality_score >= 0.70:
            return "high"
        if resource.quality_score >= 0.50:
            return "medium"
        return "low"

    def _attach_resource_metadata(
        self,
        resource: LearningResource,
        assets: list[CorrectKnowledgeAsset],
    ) -> None:
        topics = [topic for topic in self._load_syllabus_topics() if topic.profile_id in {resource.profile_id, "default"}]
        links = self._map_assets_to_syllabus_topics(assets, topics) if topics else []
        links_by_asset: dict[str, AssetSyllabusLink] = {link.asset_id: link for link in links}
        transfer_gaps = self._load_transfer_gaps(profile_id=resource.profile_id)
        for asset in assets:
            asset.resource_id = resource.resource_id
            asset.resource_quality_status = resource.quality_status
            asset.resource_validation_status = resource.validation_status
            asset.source_quality = resource.quality_score or asset.source_quality
            reasons = set(asset.resource_match_reasons)
            reasons.add("source_ref_shared")
            link = links_by_asset.get(asset.asset_id)
            if link is not None:
                asset.syllabus_topic_id = link.topic_id
                reasons.add(self._resource_match_reason_from_link(link))
                topic = next((item for item in topics if item.topic_id == link.topic_id), None)
                if topic is not None:
                    asset.subject = asset.subject or topic.subject
                    asset.module = asset.module or topic.module
                    asset.los = asset.los or (topic.los or "")
                    asset.exam_weight = max(asset.exam_weight, topic.exam_weight)
            if asset.formula_family:
                reasons.add("formula_family")
            if any(self._asset_addresses_transfer_gap(asset, gap) for gap in transfer_gaps):
                reasons.add("transfer_gap_keyword")
                asset.decay_risk = max(asset.decay_risk, 0.82)
            conflicts = self._resource_conflicts_for_asset(asset, resource)
            asset.resource_match_reasons = sorted(reasons)
            asset.resource_conflicts = sorted(set(asset.resource_conflicts + conflicts + resource.warnings))
            if asset.resource_conflicts and asset.validation_status not in {"confirmed", "rejected"}:
                asset.validation_status = "needs_review"

    def _refresh_resource_asset_metadata(self, resource: LearningResource) -> None:
        assets = [self._asset_from_dict(item) for item in self.list_resource_candidate_assets(resource.resource_id)]
        if not assets:
            return
        self._attach_resource_metadata(resource, assets)
        for asset in assets:
            self._persist_ingested_asset(asset)

    @staticmethod
    def _resource_match_reason_from_link(link: AssetSyllabusLink) -> str:
        mapping = {
            "exact_los": "exact_los",
            "keyword_match": "title_keyword",
            "module_match": "module_match",
            "manual": "manual",
        }
        return mapping.get(link.created_by, link.created_by or "title_keyword")

    def _asset_addresses_transfer_gap(self, asset: CorrectKnowledgeAsset, gap: TransferGapRecord) -> bool:
        if gap.status != "open":
            return False
        if gap.asset_id and gap.asset_id == asset.asset_id:
            return True
        if gap.topic_id and asset.syllabus_topic_id and gap.topic_id == asset.syllabus_topic_id:
            return True
        if gap.formula_family and asset.formula_family and gap.formula_family == asset.formula_family:
            return True
        gap_terms = self._keywords_for_match(" ".join([gap.gap_type, " ".join(gap.recommended_actions)]))
        asset_terms = self._keywords_for_match(" ".join([asset.title, asset.correct_rule, asset.formula_latex, asset.module]))
        return bool(gap_terms.intersection(asset_terms))

    def _resource_conflicts_for_asset(
        self,
        asset: CorrectKnowledgeAsset,
        resource: LearningResource,
    ) -> list[str]:
        if not self._resource_conflict_detection_enabled():
            return []
        conflicts: list[str] = []
        normalized_title = self._normalize_match_text(asset.title)
        normalized_module = self._normalize_match_text(asset.module)
        formula = self._normalize_formula_text(asset.formula_latex or asset.plain_formula)
        for path in self._asset_root.glob("*.json"):
            existing = self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if existing.asset_id == asset.asset_id:
                continue
            if existing.validation_status == "rejected":
                continue
            if normalized_title and normalized_title == self._normalize_match_text(existing.title):
                if not normalized_module or normalized_module == self._normalize_match_text(existing.module):
                    conflicts.append(f"duplicate_asset_title:{existing.asset_id}")
            if asset.formula_family and existing.formula_family == asset.formula_family:
                existing_formula = self._normalize_formula_text(existing.formula_latex or existing.plain_formula)
                if formula and existing_formula and formula != existing_formula:
                    conflicts.append(f"conflicting_formula_candidate:{existing.asset_id}")
            if set(asset.source_refs).intersection(existing.source_refs) and existing.validation_status == "confirmed":
                conflicts.append(f"source_ref_already_promoted:{existing.asset_id}")
        if resource.duplicate_of:
            conflicts.append(f"duplicate_source_hash:{resource.duplicate_of}")
        return list(dict.fromkeys(conflicts))

    @staticmethod
    def _normalize_formula_text(text: str) -> str:
        return re.sub(r"[^a-z0-9+=*/().-]+", "", str(text or "").lower())

    def _resource_gate_summary(self, resource: LearningResource) -> dict[str, Any]:
        if not self._resource_quality_gate_enabled():
            return {"passes": True, "reason": "resource_quality_gate_disabled"}
        if resource.validation_status == "rejected" or resource.quality_status == "rejected":
            return {"passes": False, "reason": "resource_rejected"}
        if resource.validation_status != "confirmed":
            return {"passes": False, "reason": "resource_not_confirmed"}
        if resource.quality_status not in {"medium", "high", "trusted"}:
            return {"passes": False, "reason": f"resource_quality_{resource.quality_status}"}
        return {"passes": True, "reason": f"resource_quality_{resource.quality_status}"}

    def _asset_passes_resource_gate(self, asset: CorrectKnowledgeAsset) -> bool:
        if not asset.resource_id or not self._resource_quality_gate_enabled():
            return True
        resource = self._load_resource(asset.resource_id)
        if resource is None:
            return False
        return bool(self._resource_gate_summary(resource)["passes"])

    def _resource_for_asset(self, asset: CorrectKnowledgeAsset) -> LearningResource | None:
        if asset.resource_id:
            loaded = self._load_resource(asset.resource_id)
            if loaded is not None:
                return loaded
        for ref in asset.source_refs:
            loaded = self._load_resource(ref.split("#", 1)[0])
            if loaded is not None:
                return loaded
        return None

    def _require_resource(self, resource_id: str) -> LearningResource:
        resource = self._load_resource(resource_id)
        if resource is None:
            raise KeyError(f"Resource not found: {resource_id}")
        return resource

    def _find_resource_by_hash(
        self,
        content_hash: str,
        *,
        exclude_resource_id: str = "",
    ) -> LearningResource | None:
        for path in self._resource_root.glob("*.json"):
            resource = self._resource_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if resource.resource_id == exclude_resource_id:
                continue
            if resource.content_hash == content_hash:
                return resource
        return None

    def _resource_quality_gate_enabled(self) -> bool:
        try:
            from app.feature_flags import FeatureFlags
            flags = FeatureFlags.load(self.repo_root)
            return flags.enabled("resource_quality_gate_enabled")
        except Exception:
            return True

    def _resource_quality_guided_review_enabled(self) -> bool:
        try:
            from app.feature_flags import FeatureFlags
            flags = FeatureFlags.load(self.repo_root)
            return flags.enabled("resource_quality_guided_review_enabled")
        except Exception:
            return True

    def _resource_conflict_detection_enabled(self) -> bool:
        try:
            from app.feature_flags import FeatureFlags
            flags = FeatureFlags.load(self.repo_root)
            return flags.enabled("resource_conflict_detection_enabled")
        except Exception:
            return True

    def _load_confirmed_ingested_assets(self, *, profile_id: str = "default") -> list[CorrectKnowledgeAsset]:
        assets = [
            self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self._asset_root.glob("*.json")
        ]
        confirmed = [
            asset
            for asset in assets
            if asset.validation_status == "confirmed"
            and asset.source_refs
            and asset.profile_id in {profile_id, "default"}
            and self._asset_passes_resource_gate(asset)
        ]
        confirmed.sort(key=self._asset_priority, reverse=True)
        return confirmed

    def _mock_evidence_from_text(
        self,
        *,
        mock_id: str,
        profile_id: str,
        text: str,
    ) -> list[MockQuestionEvidence]:
        blocks = [
            block.strip()
            for block in re.split(r"\n\s*(?=(?:Q(?:uestion)?\s*)?\d{1,3}[.)\s-])", text)
            if block.strip()
        ]
        if len(blocks) <= 1:
            blocks = [block.strip() for block in re.split(r"\n\s*\n+", text) if block.strip()]
        evidence: list[MockQuestionEvidence] = []
        for index, block in enumerate(blocks, start=1):
            if not block:
                continue
            question_number = self._question_number_from_block(block) or index
            result = self._extract_labeled_value(block, ("Result", "Outcome", "Status"))
            is_correct = self._result_is_correct(result)
            confidence = self._confidence_value(self._extract_labeled_value(block, ("Confidence", "Confidence Before")))
            time_spent = self._time_seconds(self._extract_labeled_value(block, ("Time", "Time Spent", "Seconds")))
            correct_rule = (
                self._extract_labeled_value(block, ("Correct Rule", "Correct Resolution", "Correct Answer", "Rule"))
                or self._first_sentence_matching(block, r"\b(correct|after-tax|use|applies|equals|formula)\b")
                or "Recall and apply the correct rule for this tested concept."
            )
            tested_formula = self._extract_labeled_value(block, ("Tested Formula", "Formula"))
            boundary_rule = self._extract_labeled_value(block, ("Boundary Rule", "Boundary", "Decision Rule"))
            subject = self._extract_labeled_value(block, ("Subject", "Topic")) or self._infer_subject_from_text(block)
            module = self._extract_labeled_value(block, ("Module", "Reading")) or self._infer_module_from_text(block, subject)
            los = self._extract_labeled_value(block, ("LOS", "Learning Outcome"))
            tested_skill = self._extract_labeled_value(block, ("Tested Skill", "Skill")) or module or subject
            correct_steps = self._steps_from_text(
                self._extract_labeled_value(block, ("Correct Steps", "Steps", "Procedure")) or correct_rule
            )
            ba_steps = self._extract_ba_ii_plus_steps(block)
            wrong_choice = self._extract_labeled_value(block, ("Wrong Output", "Wrong Choice", "Wrong Answer"))
            wrong_reasoning = self._extract_labeled_value(block, ("Wrong Reasoning", "Wrong Logic"))
            wrong_formula = self._extract_labeled_value(block, ("Wrong Formula",))
            evidence_id = self._stable_id("mock-evidence", mock_id, str(question_number), block[:160])
            item = MockQuestionEvidence(
                evidence_id=evidence_id,
                mock_id=mock_id,
                profile_id=profile_id,
                question_number=question_number,
                topic_id=None,
                asset_id=None,
                subject=subject,
                module=module,
                los=los,
                is_correct=is_correct,
                confidence_before=confidence,
                time_spent_seconds=time_spent,
                correct_rule=correct_rule,
                tested_skill=tested_skill,
                tested_formula=tested_formula,
                boundary_rule=boundary_rule,
                correct_steps=correct_steps,
                ba_ii_plus_steps=ba_steps,
                wrong_choice_or_output=wrong_choice,
                wrong_reasoning=wrong_reasoning,
                wrong_formula=wrong_formula,
                source_refs=[f"{mock_id}#q-{question_number}"],
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            self._attach_mock_evidence_links(item)
            evidence.append(item)
        return evidence

    def _attach_mock_evidence_links(self, evidence: MockQuestionEvidence) -> None:
        asset = CorrectKnowledgeAsset(
            asset_id=evidence.evidence_id,
            asset_type="formula" if evidence.tested_formula else "decision_rule" if evidence.boundary_rule else "syllabus_core",
            profile_id=evidence.profile_id,
            subject=evidence.subject or "",
            module=evidence.module or "",
            los=evidence.los or "",
            title=evidence.tested_skill or evidence.correct_rule[:80],
            trigger=evidence.tested_skill or evidence.correct_rule[:80],
            correct_rule=evidence.correct_rule,
            formula_latex=evidence.tested_formula or "",
            formula_family=self._formula_family(f"{evidence.tested_formula or ''} {evidence.correct_rule} {evidence.module or ''}"),
            source_refs=evidence.source_refs,
            validation_status="derived",
        )
        topics = [topic for topic in self._load_syllabus_topics() if topic.profile_id in {evidence.profile_id, "default"}]
        links = self._map_assets_to_syllabus_topics([asset], topics) if topics else []
        if links:
            evidence.topic_id = links[0].topic_id

        for candidate in self._all_assets_for_coverage(profile_id=evidence.profile_id):
            if evidence.los and candidate.los and self._normalize_match_text(evidence.los) == self._normalize_match_text(candidate.los):
                evidence.asset_id = candidate.asset_id
                return
            candidate_text = f"{candidate.title} {candidate.module} {candidate.correct_rule} {candidate.formula_latex}".lower()
            formula = (evidence.tested_formula or "").lower()
            if formula and formula in candidate_text:
                evidence.asset_id = candidate.asset_id
                return

    def _transfer_gaps_from_evidence(
        self,
        session: MockSession,
        evidence_items: list[MockQuestionEvidence],
    ) -> list[TransferGapRecord]:
        failures_by_topic: dict[str, int] = {}
        for evidence in evidence_items:
            if evidence.is_correct:
                continue
            key = evidence.topic_id or evidence.los or evidence.module or evidence.subject or "unmapped"
            failures_by_topic[key] = failures_by_topic.get(key, 0) + 1

        grouped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        for evidence in evidence_items:
            gap_types = self._gap_types_for_evidence(evidence, failures_by_topic)
            for gap_type in gap_types:
                formula_family = self._formula_family(
                    f"{evidence.tested_formula or ''} {evidence.correct_rule} {evidence.module or ''}"
                ) if evidence.tested_formula or self._classify_segment(evidence.correct_rule) == "formula" else None
                topic_key = evidence.topic_id or evidence.los or evidence.module or evidence.subject or ""
                key = (topic_key, evidence.asset_id or "", formula_family or "", gap_type)
                bucket = grouped.setdefault(
                    key,
                    {
                        "profile_id": session.profile_id,
                        "topic_id": evidence.topic_id,
                        "asset_id": evidence.asset_id,
                        "formula_family": formula_family,
                        "gap_type": gap_type,
                        "severity": 0.0,
                        "source_refs": [],
                        "last_seen_at": evidence.created_at,
                    },
                )
                bucket["severity"] = max(bucket["severity"], self._gap_severity(evidence, gap_type, failures_by_topic))
                bucket["source_refs"].extend(ref for ref in [evidence.evidence_id, *evidence.source_refs] if ref not in bucket["source_refs"])
                bucket["last_seen_at"] = max(bucket["last_seen_at"], evidence.created_at)

        gaps: list[TransferGapRecord] = []
        for bucket in grouped.values():
            source_refs = bucket["source_refs"]
            gap_id = self._stable_id(
                "transfer-gap",
                bucket["profile_id"],
                bucket.get("topic_id") or "",
                bucket.get("asset_id") or "",
                bucket.get("formula_family") or "",
                bucket["gap_type"],
            )
            gaps.append(
                TransferGapRecord(
                    gap_id=gap_id,
                    profile_id=bucket["profile_id"],
                    topic_id=bucket.get("topic_id"),
                    asset_id=bucket.get("asset_id"),
                    formula_family=bucket.get("formula_family"),
                    gap_type=bucket["gap_type"],
                    severity=round(self._clamp01(bucket["severity"]), 4),
                    evidence_count=max(1, len({ref for ref in source_refs if ref.startswith("mock-evidence-")})),
                    last_seen_at=bucket["last_seen_at"],
                    recommended_actions=self._gap_recommended_actions(bucket["gap_type"]),
                    source_refs=source_refs,
                    status="open",
                )
            )
        return gaps

    def _gap_types_for_evidence(
        self,
        evidence: MockQuestionEvidence,
        failures_by_topic: dict[str, int],
    ) -> list[str]:
        if evidence.is_correct:
            if evidence.time_spent_seconds and evidence.time_spent_seconds >= 180:
                return ["time_pressure"]
            return []
        text = " ".join(
            [
                evidence.correct_rule,
                evidence.tested_skill or "",
                evidence.tested_formula or "",
                evidence.boundary_rule or "",
                evidence.wrong_choice_or_output or "",
                evidence.wrong_formula or "",
                evidence.wrong_reasoning or "",
            ]
        ).lower()
        gap_types: list[str] = []
        if (evidence.confidence_before or 0) >= 3:
            gap_types.append("confidence_mismatch")
        is_formula = bool(evidence.tested_formula) or self._classify_segment(evidence.correct_rule) == "formula"
        if is_formula:
            if re.search(r"\b(variable|weight|pretax|pre-tax|after-tax|tax|input)\b", text):
                gap_types.append("variable_confusion")
            else:
                gap_types.append("formula_recall_gap")
            if evidence.ba_ii_plus_steps or re.search(r"\b(ba ii|baii|cpt|i/y|npv|cf0|cf1)\b", text):
                gap_types.append("calculator_procedure_gap")
        if re.search(r"\b(except|least likely|only if|unless|boundary|taxable vs accounting|when|not when)\b", text):
            gap_types.append("boundary_confusion")
        if evidence.time_spent_seconds and evidence.time_spent_seconds >= 180:
            gap_types.append("time_pressure")
        topic_key = evidence.topic_id or evidence.los or evidence.module or evidence.subject or "unmapped"
        if failures_by_topic.get(topic_key, 0) >= 2:
            gap_types.append("interleaving_failure")
        if not gap_types:
            gap_types.append("concept_gap")
        return list(dict.fromkeys(gap_types))

    def _gap_severity(
        self,
        evidence: MockQuestionEvidence,
        gap_type: str,
        failures_by_topic: dict[str, int],
    ) -> float:
        severity = 0.45
        if not evidence.is_correct:
            severity += 0.2
        if (evidence.confidence_before or 0) >= 3:
            severity += 0.15
        if evidence.time_spent_seconds and evidence.time_spent_seconds >= 180:
            severity += 0.1
        topic_key = evidence.topic_id or evidence.los or evidence.module or evidence.subject or "unmapped"
        if failures_by_topic.get(topic_key, 0) >= 2:
            severity += 0.1
        if gap_type in {"calculator_procedure_gap", "boundary_confusion"}:
            severity += 0.05
        return severity

    @staticmethod
    def _gap_recommended_actions(gap_type: str) -> list[str]:
        mapping = {
            "concept_gap": ["review transfer gap", "practice interleaved mini-case"],
            "formula_recall_gap": ["run Formula Lab", "create formula asset"],
            "variable_confusion": ["run Formula Lab", "review transfer gap"],
            "boundary_confusion": ["create decision boundary asset", "practice interleaved mini-case"],
            "procedure_gap": ["review transfer gap", "practice interleaved mini-case"],
            "calculator_procedure_gap": ["review BA II Plus procedure", "run Formula Lab"],
            "time_pressure": ["practice timed mini-set", "review transfer gap"],
            "confidence_mismatch": ["calibrate confidence before reveal", "review transfer gap"],
            "interleaving_failure": ["practice interleaved mini-case", "review transfer gap"],
        }
        return mapping.get(gap_type, ["review transfer gap"])

    def _best_evidence_for_gap(self, gap: TransferGapRecord) -> MockQuestionEvidence | None:
        evidence_ids = [ref for ref in gap.source_refs if ref.startswith("mock-evidence-")]
        candidates: list[MockQuestionEvidence] = []
        for path in self._mock_evidence_root.glob("*.json"):
            for item in [self._mock_evidence_from_dict(raw) for raw in json.loads(path.read_text(encoding="utf-8"))]:
                if item.evidence_id in evidence_ids:
                    candidates.append(item)
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item.is_correct, -(item.confidence_before or 0), -(item.time_spent_seconds or 0)))
        return candidates[0]

    def _unit_from_transfer_gap(
        self,
        gap: TransferGapRecord,
        evidence: MockQuestionEvidence,
    ) -> DailyReviewUnit:
        formula = evidence.tested_formula or ""
        mode = "ba_ii_plus_procedure" if evidence.ba_ii_plus_steps else "recall_formula" if formula else "recall_reveal"
        prompt_target = evidence.tested_skill or evidence.module or evidence.subject or evidence.los or "this tested trigger"
        return DailyReviewUnit(
            unit_id=f"mock-retro-unit-{gap.gap_id}",
            review_id=f"mock-retro-{datetime.now(timezone.utc).date().isoformat()}",
            asset_id=evidence.asset_id or gap.gap_id,
            asset_type="formula" if formula else "transfer_or_interleaving",
            unit_type="transfer_or_interleaving",
            display_mode=mode,  # type: ignore[arg-type]
            interaction_mode=mode,  # type: ignore[arg-type]
            prompt=f"When this trigger appears, which correct rule applies? {prompt_target}",
            front_prompt=f"When this trigger appears, which correct rule applies? {prompt_target}",
            recall_instruction="Commit to the correct rule before revealing.",
            answer=evidence.correct_rule,
            correct_answer=evidence.correct_rule,
            correct_reasoning=evidence.correct_rule,
            correct_steps=evidence.correct_steps,
            formula_latex=formula,
            ba_ii_plus_steps=evidence.ba_ii_plus_steps,
            boundary_rules=[evidence.boundary_rule] if evidence.boundary_rule else [],
            source_refs=evidence.source_refs,
            due_reason=f"Recent mock transfer gap: {gap.gap_type}",
            memory_state="Learning",
            priority=int(round(gap.severity * 100)),
            knowledge_id=evidence.asset_id or gap.gap_id,
            subject=evidence.subject or "",
            heading=evidence.module or "",
            los=evidence.los or "",
        )

    @staticmethod
    def _question_number_from_block(block: str) -> int | None:
        match = re.search(r"(?:Q(?:uestion)?\s*)?(\d{1,3})", block, flags=re.IGNORECASE)
        return int(match.group(1)) if match else None

    @staticmethod
    def _extract_labeled_value(block: str, labels: tuple[str, ...]) -> str:
        for label in labels:
            pattern = rf"(?im)^\s*{re.escape(label)}\s*:\s*(.+?)(?=\n\s*[A-Za-z][A-Za-z /+-]{{1,40}}\s*:|\Z)"
            match = re.search(pattern, block, flags=re.DOTALL)
            if match:
                return " ".join(line.strip() for line in match.group(1).strip().splitlines() if line.strip())
        return ""

    @staticmethod
    def _result_is_correct(result: str) -> bool:
        lowered = result.lower()
        if any(token in lowered for token in ("incorrect", "wrong", "miss", "false", "no")):
            return False
        if any(token in lowered for token in ("correct", "right", "true", "yes")):
            return True
        return False

    @staticmethod
    def _confidence_value(value: str) -> float | None:
        lowered = value.lower().strip()
        if not lowered:
            return None
        if "high" in lowered:
            return 4.0
        if "medium" in lowered or "moderate" in lowered:
            return 2.5
        if "low" in lowered:
            return 1.0
        match = re.search(r"\d+(?:\.\d+)?", lowered)
        return float(match.group(0)) if match else None

    @staticmethod
    def _time_seconds(value: str) -> int | None:
        lowered = value.lower().strip()
        if not lowered:
            return None
        if ":" in lowered:
            parts = [int(part) for part in re.findall(r"\d+", lowered)[:2]]
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
        match = re.search(r"\d+(?:\.\d+)?", lowered)
        if not match:
            return None
        amount = float(match.group(0))
        return int(amount * 60) if "min" in lowered else int(amount)

    @staticmethod
    def _infer_subject_from_text(text: str) -> str:
        subjects = [
            "Corporate Issuers",
            "Fixed Income",
            "Equity",
            "Quantitative Methods",
            "Economics",
            "Financial Statement Analysis",
            "Derivatives",
            "Portfolio Management",
            "Alternative Investments",
            "Ethics",
        ]
        lowered = text.lower()
        for subject in subjects:
            if subject.lower() in lowered:
                return subject
        return "Mock Retro"

    @staticmethod
    def _infer_module_from_text(text: str, subject: str) -> str:
        first_line = text.splitlines()[0].strip() if text.splitlines() else subject
        cleaned = re.sub(r"^(?:Q(?:uestion)?\s*)?\d{1,3}[.)\s-]*", "", first_line, flags=re.IGNORECASE).strip()
        return cleaned or subject or "Mock Retro"

    def _topics_from_syllabus_text(
        self,
        *,
        profile_id: str,
        text: str,
        exam: str | None,
    ) -> list[SyllabusTopic]:
        topics: list[SyllabusTopic] = []
        for raw_line in text.splitlines():
            line = raw_line.strip().strip("|").strip()
            if not line or line.startswith("#") or set(line) <= {"-", "|", " "}:
                continue
            if line.lower().replace(" ", "_").startswith(("los|", "subject|", "topic_id|")):
                continue
            line = re.sub(r"^\s*[-*]\s+", "", line)
            parts = [part.strip() for part in re.split(r"\s*\|\s*|\t+", line) if part.strip()]
            if len(parts) >= 4:
                if self._looks_like_los(parts[0]):
                    los = parts[0]
                    subject = parts[1]
                    module = parts[2]
                    title = parts[3]
                    expected = parts[4] if len(parts) > 4 else ""
                    weight = parts[5] if len(parts) > 5 else ""
                else:
                    subject = parts[0]
                    module = parts[1]
                    los = parts[2] if self._looks_like_los(parts[2]) else ""
                    title = parts[3] if los else parts[2]
                    expected = parts[4] if len(parts) > 4 else ""
                    weight = parts[5] if len(parts) > 5 else ""
            else:
                hierarchy = [part.strip() for part in re.split(r"\s*>\s*", line) if part.strip()]
                subject = hierarchy[0] if hierarchy else "General"
                module = hierarchy[1] if len(hierarchy) > 1 else subject
                tail = hierarchy[-1] if hierarchy else line
                match = re.match(r"(?P<los>[A-Za-z]{1,5}[-._]?\d{1,4}[A-Za-z]?)\s*[:.-]?\s*(?P<title>.+)", tail)
                los = match.group("los") if match else ""
                title = match.group("title") if match else tail
                expected = ""
                weight = ""
            item = {
                "subject": subject,
                "module": module,
                "los": los,
                "title": title,
                "expected_asset_types": self._expected_types_from_text(expected or title),
                "exam_weight": self._safe_float(weight, 0.55),
                "importance": self._safe_float(weight, 0.65),
                "exam": exam,
            }
            topics.append(self._topic_from_import_item(item, profile_id=profile_id, exam=exam))
        return topics

    def _topic_from_import_item(
        self,
        item: dict[str, Any],
        *,
        profile_id: str,
        exam: str | None,
    ) -> SyllabusTopic:
        subject = str(item.get("subject") or item.get("topic") or "General").strip()
        module = str(item.get("module") or item.get("reading") or subject).strip()
        title = str(item.get("title") or item.get("los_title") or module).strip()
        los = str(item.get("los") or item.get("learning_outcome") or "").strip() or None
        expected_types = self._normalize_expected_asset_types(
            item.get("expected_asset_types")
            or item.get("expected_types")
            or item.get("asset_types")
            or []
        )
        expected_types = expected_types or self._expected_types_from_text(f"{title} {item.get('description', '')}")
        formula_expected = bool(item.get("formula_expected")) or "formula" in expected_types
        decision_rule_expected = (
            bool(item.get("decision_rule_expected"))
            or "decision_rule" in expected_types
            or "exam_boundary" in expected_types
        )
        topic_id = str(item.get("topic_id") or "").strip()
        if not topic_id:
            topic_id = self._stable_id("topic", profile_id, subject, module, los or "", title)
        return SyllabusTopic(
            topic_id=topic_id,
            profile_id=str(item.get("profile_id") or profile_id or "default"),
            exam=item.get("exam") or exam,
            subject=subject,
            module=module,
            los=los,
            title=title,
            description=item.get("description"),
            parent_topic_id=item.get("parent_topic_id"),
            exam_weight=self._clamp01(self._safe_float(item.get("exam_weight"), 0.55)),
            importance=self._clamp01(self._safe_float(item.get("importance"), self._safe_float(item.get("exam_weight"), 0.65))),
            expected_asset_types=expected_types,
            formula_expected=formula_expected,
            decision_rule_expected=decision_rule_expected,
            source_refs=self._coerce_list(item.get("source_refs", [])),
            active=bool(item.get("active", True)),
        )

    def _demo_syllabus_topics(self, *, profile_id: str) -> list[SyllabusTopic]:
        demo = [
            {
                "topic_id": "demo-ci-wacc",
                "exam": "CFA Level I",
                "subject": "Corporate Issuers",
                "module": "Cost of Capital",
                "los": "CI-001",
                "title": "Calculate and interpret WACC",
                "description": "Weighted average cost of capital, component weights, tax shield, and use boundaries.",
                "exam_weight": 0.9,
                "importance": 0.95,
                "expected_asset_types": ["definition", "formula", "decision_rule"],
                "formula_expected": True,
                "decision_rule_expected": True,
                "source_refs": ["curriculum/corporate-issuers/cost-of-capital"],
            },
            {
                "topic_id": "demo-equity-gordon-growth",
                "exam": "CFA Level I",
                "subject": "Equity",
                "module": "Equity Valuation",
                "los": "EQ-001",
                "title": "Apply the Gordon growth model",
                "description": "Dividend discount valuation when growth is stable and required return exceeds growth.",
                "exam_weight": 0.8,
                "importance": 0.9,
                "expected_asset_types": ["formula", "decision_rule"],
                "formula_expected": True,
                "decision_rule_expected": True,
                "source_refs": ["curriculum/equity/valuation"],
            },
            {
                "topic_id": "demo-fi-effective-duration",
                "exam": "CFA Level I",
                "subject": "Fixed Income",
                "module": "Duration and Convexity",
                "los": "FI-001",
                "title": "Choose effective duration for option-sensitive bonds",
                "description": "Decision boundary between Macaulay, modified, and effective duration.",
                "exam_weight": 0.78,
                "importance": 0.88,
                "expected_asset_types": ["definition", "formula", "decision_rule"],
                "formula_expected": True,
                "decision_rule_expected": True,
                "source_refs": ["curriculum/fixed-income/duration"],
            },
            {
                "topic_id": "demo-quant-tvm",
                "exam": "CFA Level I",
                "subject": "Quantitative Methods",
                "module": "Time Value of Money",
                "los": "QM-001",
                "title": "Solve TVM and NPV problems",
                "description": "PV, FV, PMT, NPV, IRR, and BA II Plus setup.",
                "exam_weight": 0.72,
                "importance": 0.82,
                "expected_asset_types": ["formula", "procedure"],
                "formula_expected": True,
                "decision_rule_expected": False,
                "source_refs": ["curriculum/quant/time-value-of-money"],
            },
            {
                "topic_id": "demo-econ-business-cycles",
                "exam": "CFA Level I",
                "subject": "Economics",
                "module": "Business Cycles",
                "los": "EC-001",
                "title": "Distinguish leading and lagging indicators",
                "description": "Indicator timing and exam boundaries for cycle interpretation.",
                "exam_weight": 0.58,
                "importance": 0.7,
                "expected_asset_types": ["definition", "decision_rule"],
                "formula_expected": False,
                "decision_rule_expected": True,
                "source_refs": ["curriculum/economics/business-cycles"],
            },
        ]
        return [self._topic_from_import_item(item, profile_id=profile_id, exam=item["exam"]) for item in demo]

    def _upsert_syllabus_topics(self, topics: list[SyllabusTopic]) -> dict[str, Any]:
        existing = {topic.topic_id: topic for topic in self._load_syllabus_topics()}
        created = 0
        updated = 0
        for topic in topics:
            if topic.topic_id in existing:
                updated += 1
            else:
                created += 1
            existing[topic.topic_id] = topic
        ordered = sorted(existing.values(), key=lambda topic: (topic.profile_id, topic.subject, topic.module, topic.los or "", topic.title))
        self._persist_syllabus_topics(ordered)
        return {
            "created": created,
            "updated": updated,
            "count": len(topics),
            "topics": [topic.as_dict() for topic in topics],
        }

    def _all_assets_for_coverage(self, *, profile_id: str) -> list[CorrectKnowledgeAsset]:
        assets_by_id: dict[str, CorrectKnowledgeAsset] = {}
        snapshot = self._load_snapshot("")
        for asset in self._build_assets_from_snapshot(snapshot):
            if asset.profile_id in {profile_id, "default"}:
                assets_by_id[asset.asset_id] = asset
        for path in self._asset_root.glob("*.json"):
            asset = self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if asset.profile_id in {profile_id, "default"}:
                assets_by_id[asset.asset_id] = asset
        return list(assets_by_id.values())

    def _map_assets_to_syllabus_topics(
        self,
        assets: list[CorrectKnowledgeAsset],
        topics: list[SyllabusTopic],
    ) -> list[AssetSyllabusLink]:
        links: list[AssetSyllabusLink] = []
        for asset in assets:
            scored = [self._score_asset_topic_match(asset, topic) for topic in topics]
            scored = [item for item in scored if item is not None]
            if not scored:
                continue
            scored.sort(key=lambda item: item.confidence, reverse=True)
            best = scored[0]
            if best.confidence >= 0.5:
                links.append(best)
        links.sort(key=lambda link: (link.topic_id, -link.confidence, link.asset_id))
        return links

    def _score_asset_topic_match(
        self,
        asset: CorrectKnowledgeAsset,
        topic: SyllabusTopic,
    ) -> AssetSyllabusLink | None:
        if asset.syllabus_topic_id and asset.syllabus_topic_id == topic.topic_id:
            return AssetSyllabusLink(asset.asset_id, topic.topic_id, "manual syllabus_topic_id match", 0.99, "manual")
        if topic.topic_id in asset.source_refs or f"topic:{topic.topic_id}" in asset.source_refs:
            return AssetSyllabusLink(asset.asset_id, topic.topic_id, "manual topic source_ref match", 0.98, "manual")

        asset_los = self._normalize_match_text(asset.los)
        topic_los = self._normalize_match_text(topic.los or "")
        if asset_los and topic_los and asset_los == topic_los:
            return AssetSyllabusLink(asset.asset_id, topic.topic_id, f"exact LOS match: {topic.los}", 0.96, "exact_los")

        asset_refs = {ref.lower() for ref in asset.source_refs}
        topic_refs = {ref.lower() for ref in topic.source_refs}
        if asset_refs and topic_refs and asset_refs.intersection(topic_refs):
            return AssetSyllabusLink(asset.asset_id, topic.topic_id, "shared source_ref metadata", 0.84, "manual")

        asset_subject = self._normalize_match_text(asset.subject)
        asset_module = self._normalize_match_text(asset.module)
        topic_subject = self._normalize_match_text(topic.subject)
        topic_module = self._normalize_match_text(topic.module)
        asset_keywords = self._keywords_for_match(
            f"{asset.title} {asset.trigger} {asset.correct_rule} {asset.formula_latex} {asset.formula_family}"
        )
        topic_keywords = self._keywords_for_match(
            f"{topic.subject} {topic.module} {topic.title} {topic.description or ''} {topic.los or ''}"
        )
        overlap = sorted(asset_keywords.intersection(topic_keywords))
        overlap_ratio = len(overlap) / max(1, min(len(asset_keywords), len(topic_keywords)))

        if asset_subject and asset_subject == topic_subject and asset_module and asset_module == topic_module:
            confidence = min(0.9, 0.74 + (0.12 * overlap_ratio))
            return AssetSyllabusLink(
                asset.asset_id,
                topic.topic_id,
                f"subject/module match with keywords: {', '.join(overlap[:5]) or 'none'}",
                confidence,
                "module_match",
            )
        if asset_module and asset_module == topic_module and overlap_ratio >= 0.12:
            return AssetSyllabusLink(
                asset.asset_id,
                topic.topic_id,
                f"module fallback with keyword overlap: {', '.join(overlap[:5])}",
                min(0.78, 0.58 + (0.16 * overlap_ratio)),
                "module_match",
            )

        family_keywords = self._formula_family_keywords(asset.formula_family)
        if family_keywords and family_keywords.intersection(topic_keywords):
            return AssetSyllabusLink(
                asset.asset_id,
                topic.topic_id,
                f"formula family match: {asset.formula_family}",
                0.72,
                "keyword_match",
            )

        if overlap_ratio >= 0.2 or {"wacc", "gordon", "duration", "npv"}.intersection(overlap):
            return AssetSyllabusLink(
                asset.asset_id,
                topic.topic_id,
                f"keyword overlap: {', '.join(overlap[:6])}",
                min(0.72, 0.48 + (0.3 * overlap_ratio)),
                "keyword_match",
            )
        return None

    def _coverage_record_for_topic(
        self,
        topic: SyllabusTopic,
        linked_assets: list[CorrectKnowledgeAsset],
    ) -> SyllabusCoverageRecord:
        confirmed = [
            asset for asset in linked_assets
            if self._is_confirmed_for_coverage(asset)
            and self._asset_passes_resource_gate(asset)
        ]
        draft = [asset for asset in linked_assets if asset.validation_status in {"draft", "needs_review"}]
        rejected = [asset for asset in linked_assets if asset.validation_status == "rejected"]
        formula_assets = [asset for asset in confirmed if self._is_formula_candidate_asset(asset)]
        decision_assets = [
            asset for asset in confirmed
            if asset.asset_type in {"decision_rule", "exam_boundary"} or bool(asset.common_correct_boundary_rules or asset.not_when)
        ]
        transfer_gaps = self._open_transfer_gaps_for_topic(topic)
        transfer_gap_severity = max([gap.severity for gap in transfer_gaps], default=0.0)
        present_types = self._present_coverage_types(confirmed)
        expected_types = topic.expected_asset_types or ["definition"]
        missing_types = [asset_type for asset_type in expected_types if asset_type not in present_types]
        if topic.formula_expected and "formula" not in present_types and "formula" not in missing_types:
            missing_types.append("formula")
        if topic.decision_rule_expected and "decision_rule" not in present_types and "exam_boundary" not in present_types:
            if "decision_rule" not in missing_types:
                missing_types.append("decision_rule")

        mastery_state = self._aggregate_mastery_state(confirmed)
        mistake_link_count = sum(max(0, int(asset.mistake_link_count)) for asset in confirmed)
        next_review_at = self._earliest_next_review(confirmed)
        is_stale = self._is_stale_coverage(confirmed, next_review_at)
        is_weak = (
            mastery_state.lower() in {"new", "learning", "weak"}
            or mistake_link_count >= 2
            or transfer_gap_severity >= 0.65
        )

        if not confirmed and not draft:
            status = "missing"
        elif not confirmed and draft:
            status = "draft_only"
        elif is_weak:
            status = "weak"
        elif missing_types:
            status = "partial"
        elif is_stale:
            status = "stale"
        else:
            status = "covered"

        score = self._coverage_score(
            topic=topic,
            confirmed=confirmed,
            expected_types=expected_types,
            present_types=present_types,
            formula_assets=formula_assets,
            decision_assets=decision_assets,
            mastery_state=mastery_state,
            next_review_at=next_review_at,
        )
        return SyllabusCoverageRecord(
            record_id=self._stable_id("coverage", topic.profile_id, topic.topic_id),
            profile_id=topic.profile_id,
            topic_id=topic.topic_id,
            confirmed_asset_count=len(confirmed),
            draft_asset_count=len(draft),
            rejected_asset_count=len(rejected),
            formula_asset_count=len(formula_assets),
            decision_rule_asset_count=len(decision_assets),
            mistake_link_count=mistake_link_count,
            mastery_state=mastery_state,
            coverage_status=status,  # type: ignore[arg-type]
            coverage_score=round(score, 4),
            missing_asset_types=missing_types,
            recommended_actions=self._coverage_recommended_actions(
                topic=topic,
                status=status,
                missing_types=missing_types,
                confirmed=confirmed,
                draft=draft,
                transfer_gaps=transfer_gaps,
            ),
            last_reviewed_at=None,
            next_review_at=next_review_at,
        )

    def _coverage_score(
        self,
        *,
        topic: SyllabusTopic,
        confirmed: list[CorrectKnowledgeAsset],
        expected_types: list[str],
        present_types: set[str],
        formula_assets: list[CorrectKnowledgeAsset],
        decision_assets: list[CorrectKnowledgeAsset],
        mastery_state: str,
        next_review_at: str | None,
    ) -> float:
        expected = set(expected_types or ["definition"])
        confirmed_core_asset_coverage = len(expected.intersection(present_types)) / max(1, len(expected))
        formula_coverage = 1.0 if not topic.formula_expected else min(len(formula_assets), 1)
        decision_rule_coverage = 1.0 if not topic.decision_rule_expected else min(len(decision_assets), 1)
        mastery_strength = self._mastery_strength(mastery_state)
        source_quality = sum(asset.source_quality for asset in confirmed) / len(confirmed) if confirmed else 0.0
        review_recency = self._review_recency_strength(next_review_at, bool(confirmed))
        return (
            0.30 * confirmed_core_asset_coverage
            + 0.20 * formula_coverage
            + 0.15 * decision_rule_coverage
            + 0.15 * mastery_strength
            + 0.10 * source_quality
            + 0.10 * review_recency
        )

    def _coverage_recommended_actions(
        self,
        *,
        topic: SyllabusTopic,
        status: str,
        missing_types: list[str],
        confirmed: list[CorrectKnowledgeAsset],
        draft: list[CorrectKnowledgeAsset],
        transfer_gaps: list[TransferGapRecord] | None = None,
    ) -> list[str]:
        actions: list[str] = []
        transfer_gaps = transfer_gaps or []
        if transfer_gaps:
            actions.append("review transfer gap")
        if status == "missing":
            actions.append("import notes for this topic")
        if draft and not confirmed:
            actions.append("confirm draft assets")
        if "formula" in missing_types:
            actions.append("create formula asset")
        if "decision_rule" in missing_types or "exam_boundary" in missing_types:
            actions.append("create decision boundary asset")
        if status == "weak":
            actions.append("review weak confirmed assets")
        if status == "stale":
            actions.append("review stale covered assets")
        gap_types = {gap.gap_type for gap in transfer_gaps if gap.status == "open"}
        if "boundary_confusion" in gap_types and "create decision boundary asset" not in actions:
            actions.append("create decision boundary asset")
        if "interleaving_failure" in gap_types:
            actions.append("practice interleaved mini-case")
        if "calculator_procedure_gap" in gap_types:
            actions.append("review BA II Plus procedure")
        if confirmed and any(not asset.source_refs for asset in confirmed):
            actions.append("add source references")
        if (
            topic.formula_expected
            and (confirmed or "formula" in missing_types or {"formula_recall_gap", "variable_confusion", "calculator_procedure_gap"}.intersection(gap_types))
        ):
            actions.append("run Formula Lab")
        if not actions:
            actions.append("keep in scheduled review rotation")
        return list(dict.fromkeys(actions))

    def _coverage_guidance_boost(self, asset: CorrectKnowledgeAsset) -> float:
        coverage_path = self._syllabus_coverage_path(asset.profile_id or "default")
        if not coverage_path.exists() and asset.profile_id != "default":
            coverage_path = self._syllabus_coverage_path("default")
        if not coverage_path.exists():
            return 0.0
        try:
            coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return 0.0
        boost = 0.0
        for record in coverage.get("records", []):
            linked_ids = {link.get("asset_id") for link in record.get("links", [])}
            if asset.asset_id not in linked_ids:
                continue
            status = record.get("coverage_status", "")
            weight = float(record.get("topic", {}).get("exam_weight", asset.exam_weight) or asset.exam_weight)
            if status in {"weak", "stale"}:
                boost = max(boost, 0.2 + (0.1 * weight))
            elif status == "partial":
                boost = max(boost, 0.08 + (0.06 * weight))
        return boost

    def _coverage_guided_selection_enabled(self) -> bool:
        try:
            from app.feature_flags import FeatureFlags
            flags = FeatureFlags.load(self.repo_root)
            return flags.enabled("coverage_guided_review_selection_enabled")
        except Exception:
            return True

    def _transfer_gap_priority_enabled(self) -> bool:
        try:
            from app.feature_flags import FeatureFlags
            flags = FeatureFlags.load(self.repo_root)
            return flags.enabled("transfer_gap_priority_enabled")
        except Exception:
            return True

    @staticmethod
    def _is_confirmed_for_coverage(asset: CorrectKnowledgeAsset) -> bool:
        return asset.validation_status in {"confirmed", "validated", "derived"} and asset.validation_status != "rejected"

    @classmethod
    def _present_coverage_types(cls, assets: list[CorrectKnowledgeAsset]) -> set[str]:
        present: set[str] = set()
        for asset in assets:
            present.add(asset.asset_type)
            if cls._is_formula_candidate_asset(asset):
                present.add("formula")
            if asset.asset_type in {"decision_rule", "exam_boundary"} or asset.common_correct_boundary_rules or asset.not_when:
                present.add("decision_rule")
                present.add("exam_boundary")
            if asset.asset_type in {"syllabus_core", "mistake_corrected"}:
                present.add("definition")
        return present

    @staticmethod
    def _aggregate_mastery_state(assets: list[CorrectKnowledgeAsset]) -> str:
        if not assets:
            return "none"
        values = [str(asset.mastery_state or "new").strip().lower() for asset in assets]
        if any(value in {"weak", "learning", "new", "reviewed once"} for value in values):
            return "Learning"
        if any(value in {"practiced", "familiar"} for value in values):
            return "Practiced"
        return "Mastered"

    @staticmethod
    def _earliest_next_review(assets: list[CorrectKnowledgeAsset]) -> str | None:
        candidates = [asset.next_review_at for asset in assets if asset.next_review_at]
        if not candidates:
            return None
        return sorted(candidates)[0]

    def _is_stale_coverage(self, assets: list[CorrectKnowledgeAsset], next_review_at: str | None) -> bool:
        if not assets:
            return False
        if any(asset.decay_risk >= 0.88 for asset in assets):
            return True
        if not next_review_at:
            return False
        parsed = self._parse_datetime(next_review_at)
        return parsed is not None and parsed < datetime.now(timezone.utc)

    @staticmethod
    def _review_recency_strength(next_review_at: str | None, has_confirmed: bool) -> float:
        if not has_confirmed:
            return 0.0
        if not next_review_at:
            return 0.45
        parsed = ReviewLabEngine._parse_datetime(next_review_at)
        if parsed is None:
            return 0.45
        delta_days = (parsed - datetime.now(timezone.utc)).total_seconds() / 86400
        if delta_days < 0:
            return 0.2
        if delta_days <= 3:
            return 0.85
        return 0.7

    @staticmethod
    def _mastery_strength(mastery_state: str) -> float:
        mapping = {
            "none": 0.0,
            "new": 0.3,
            "learning": 0.35,
            "reviewed once": 0.45,
            "familiar": 0.7,
            "practiced": 0.8,
            "proficient": 0.9,
            "mastered": 1.0,
        }
        return mapping.get(mastery_state.strip().lower(), 0.5)

    @staticmethod
    def _coverage_status_rank(status: str) -> int:
        return {
            "missing": 0,
            "draft_only": 1,
            "partial": 2,
            "weak": 3,
            "stale": 4,
            "covered": 5,
        }.get(status, 9)

    @staticmethod
    def _normalize_expected_asset_types(value: Any) -> list[str]:
        values = ReviewLabEngine._coerce_list(value)
        normalized: list[str] = []
        aliases = {
            "boundary": "decision_rule",
            "decision": "decision_rule",
            "rule": "decision_rule",
            "calculator": "procedure",
            "ba ii plus": "procedure",
            "ba": "procedure",
            "concept": "definition",
            "core": "definition",
        }
        allowed = {
            "definition",
            "formula",
            "decision_rule",
            "exam_boundary",
            "procedure",
            "concept_comparison",
            "worked_example",
        }
        for item in values:
            key = item.strip().lower().replace("-", "_").replace(" ", "_")
            key = aliases.get(key.replace("_", " "), aliases.get(key, key))
            if key in allowed and key not in normalized:
                normalized.append(key)
        return normalized

    @staticmethod
    def _expected_types_from_text(text: str) -> list[str]:
        lowered = text.lower()
        types = ["definition"]
        if any(token in lowered for token in ("formula", "calculate", "wacc", "npv", "duration", "yield", "pv", "fv")):
            types.append("formula")
        if any(token in lowered for token in ("interpret", "choose", "when", "only if", "boundary", "distinguish", "apply")):
            types.append("decision_rule")
        return list(dict.fromkeys(types))

    @staticmethod
    def _keywords_for_match(text: str) -> set[str]:
        stop = {
            "the", "and", "for", "from", "with", "this", "that", "when", "only", "use",
            "apply", "recall", "correct", "formula", "asset", "source", "note", "cfa",
            "level", "module", "topic", "calculate", "interpret", "model", "value",
        }
        words = {
            word.lower()
            for word in re.findall(r"[A-Za-z][A-Za-z0-9_/-]{2,}", text)
            if word.lower() not in stop
        }
        return words

    @staticmethod
    def _formula_family_keywords(family: str) -> set[str]:
        mapping = {
            "cost_of_capital": {"wacc", "capital", "cost", "debt", "equity"},
            "equity_valuation": {"equity", "valuation", "gordon", "dividend", "ddm"},
            "time_value_of_money": {"tvm", "npv", "irr", "pv", "fv", "pmt"},
            "fixed_income": {"duration", "convexity", "yield", "bond"},
            "financial_statement_analysis": {"roe", "roa", "financial", "statement"},
        }
        return mapping.get(family, set())

    @staticmethod
    def _normalize_match_text(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", str(text or "").lower())

    @staticmethod
    def _looks_like_los(text: str) -> bool:
        value = str(text).strip()
        return bool(re.match(r"^[A-Za-z][A-Za-z0-9._-]{1,24}$", value) and re.search(r"\d", value))

    @staticmethod
    def _safe_float(value: Any, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _clamp01(value: float) -> float:
        return min(max(value, 0.0), 1.0)

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed

    def _syllabus_topics_path(self) -> Path:
        return self._syllabus_root / "topics.json"

    def _syllabus_coverage_path(self, profile_id: str) -> Path:
        return self._syllabus_root / f"coverage-{profile_id or 'default'}.json"

    def _load_syllabus_topics(self) -> list[SyllabusTopic]:
        path = self._syllabus_topics_path()
        if not path.exists():
            return []
        return [self._topic_from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def _persist_syllabus_topics(self, topics: list[SyllabusTopic]) -> None:
        self._syllabus_topics_path().write_text(
            json.dumps([topic.as_dict() for topic in topics], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _persist_syllabus_coverage(self, profile_id: str, payload: dict[str, Any]) -> None:
        self._syllabus_coverage_path(profile_id).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _topic_from_dict(data: dict[str, Any]) -> SyllabusTopic:
        allowed = {field.name for field in fields(SyllabusTopic)}
        return SyllabusTopic(**{key: value for key, value in data.items() if key in allowed})

    def _mock_session_path(self, mock_id: str) -> Path:
        return self._mock_retro_root / f"{mock_id}.json"

    def _mock_evidence_path(self, mock_id: str) -> Path:
        return self._mock_evidence_root / f"{mock_id}.json"

    def _transfer_gap_path(self, gap_id: str) -> Path:
        return self._transfer_gap_root / f"{gap_id}.json"

    def _load_mock_session(self, mock_id: str) -> MockSession | None:
        path = self._mock_session_path(mock_id)
        if not path.exists():
            return None
        return self._mock_session_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _persist_mock_session(self, session: MockSession) -> None:
        self._mock_session_path(session.mock_id).write_text(
            json.dumps(session.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load_mock_evidence(self, mock_id: str) -> list[MockQuestionEvidence]:
        path = self._mock_evidence_path(mock_id)
        if not path.exists():
            return []
        return [self._mock_evidence_from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def _persist_mock_evidence(self, mock_id: str, evidence: list[MockQuestionEvidence]) -> None:
        self._mock_evidence_path(mock_id).write_text(
            json.dumps([item.as_dict(include_internal=True) for item in evidence], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _persist_or_merge_transfer_gap(self, gap: TransferGapRecord) -> TransferGapRecord:
        existing = self._load_transfer_gap(gap.gap_id)
        if existing is not None:
            if existing.status == "resolved":
                return existing
            existing.severity = max(existing.severity, gap.severity)
            existing.evidence_count = max(existing.evidence_count, gap.evidence_count)
            existing.last_seen_at = max(existing.last_seen_at, gap.last_seen_at)
            existing.source_refs = sorted(set(existing.source_refs + gap.source_refs))
            existing.recommended_actions = sorted(set(existing.recommended_actions + gap.recommended_actions))
            self._persist_transfer_gap(existing)
            return existing
        self._persist_transfer_gap(gap)
        return gap

    def _load_transfer_gap(self, gap_id: str) -> TransferGapRecord | None:
        path = self._transfer_gap_path(gap_id)
        if not path.exists():
            return None
        return self._transfer_gap_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _load_transfer_gaps(self, *, profile_id: str = "default") -> list[TransferGapRecord]:
        gaps: list[TransferGapRecord] = []
        for path in self._transfer_gap_root.glob("transfer-gap-*.json"):
            gap = self._transfer_gap_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if gap.profile_id in {profile_id or "default", "default"}:
                gaps.append(gap)
        return gaps

    def _persist_transfer_gap(self, gap: TransferGapRecord) -> None:
        self._transfer_gap_path(gap.gap_id).write_text(
            json.dumps(gap.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _open_transfer_gaps_for_topic(self, topic: SyllabusTopic) -> list[TransferGapRecord]:
        gaps = self._load_transfer_gaps(profile_id=topic.profile_id)
        topic_text = self._keywords_for_match(f"{topic.subject} {topic.module} {topic.title} {topic.los or ''}")
        matches: list[TransferGapRecord] = []
        for gap in gaps:
            if gap.status != "open":
                continue
            if gap.topic_id == topic.topic_id:
                matches.append(gap)
                continue
            if gap.formula_family and self._formula_family_keywords(gap.formula_family).intersection(topic_text):
                matches.append(gap)
        return matches

    def _transfer_gap_severity_for_asset(self, asset: CorrectKnowledgeAsset) -> float:
        gaps = self._load_transfer_gaps(profile_id=asset.profile_id or "default")
        asset_keywords = self._keywords_for_match(f"{asset.subject} {asset.module} {asset.title} {asset.correct_rule} {asset.formula_family}")
        severity = 0.0
        for gap in gaps:
            if gap.status != "open":
                continue
            if gap.asset_id and gap.asset_id == asset.asset_id:
                severity = max(severity, gap.severity)
                continue
            if gap.formula_family and gap.formula_family == asset.formula_family:
                severity = max(severity, gap.severity * 0.85)
                continue
            if gap.formula_family and self._formula_family_keywords(gap.formula_family).intersection(asset_keywords):
                severity = max(severity, gap.severity * 0.7)
        return severity

    def _asset_has_open_transfer_gap(self, asset: CorrectKnowledgeAsset) -> bool:
        return self._transfer_gap_severity_for_asset(asset) > 0.0

    def _asset_has_gap_type(self, asset: CorrectKnowledgeAsset, gap_type: str) -> bool:
        gaps = self._load_transfer_gaps(profile_id=asset.profile_id or "default")
        for gap in gaps:
            if gap.status != "open" or gap.gap_type != gap_type:
                continue
            if gap.asset_id == asset.asset_id:
                return True
            if gap.formula_family and gap.formula_family == asset.formula_family:
                return True
        return False

    @staticmethod
    def _mock_session_from_dict(data: dict[str, Any]) -> MockSession:
        allowed = {field.name for field in fields(MockSession)}
        return MockSession(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _mock_evidence_from_dict(data: dict[str, Any]) -> MockQuestionEvidence:
        allowed = {field.name for field in fields(MockQuestionEvidence)}
        return MockQuestionEvidence(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _transfer_gap_from_dict(data: dict[str, Any]) -> TransferGapRecord:
        allowed = {field.name for field in fields(TransferGapRecord)}
        return TransferGapRecord(**{key: value for key, value in data.items() if key in allowed})

    def _load_source(self, source_id: str) -> KnowledgeSourceDocument | None:
        path = self._source_root / f"{source_id}.json"
        if not path.exists():
            return None
        return self._source_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _persist_source(self, source: KnowledgeSourceDocument) -> None:
        path = self._source_root / f"{source.source_id}.json"
        path.write_text(json.dumps(source.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_segments(self, source_id: str) -> list[KnowledgeSourceSegment]:
        path = self._segment_root / f"{source_id}.json"
        if not path.exists():
            return []
        return [self._segment_from_dict(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def _persist_segments(self, source_id: str, segments: list[KnowledgeSourceSegment]) -> None:
        path = self._segment_root / f"{source_id}.json"
        payload = [segment.as_dict() for segment in segments]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_resource(self, resource_id: str) -> LearningResource | None:
        path = self._resource_root / f"{resource_id}.json"
        if not path.exists():
            return None
        return self._resource_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _persist_resource(self, resource: LearningResource) -> None:
        path = self._resource_root / f"{resource.resource_id}.json"
        path.write_text(json.dumps(resource.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_ingested_asset(self, asset_id: str) -> CorrectKnowledgeAsset | None:
        path = self._asset_root / f"{asset_id}.json"
        if not path.exists():
            return None
        return self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _persist_ingested_asset(self, asset: CorrectKnowledgeAsset) -> None:
        path = self._asset_root / f"{asset.asset_id}.json"
        path.write_text(json.dumps(asset.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _source_from_dict(data: dict[str, Any]) -> KnowledgeSourceDocument:
        allowed = {field.name for field in fields(KnowledgeSourceDocument)}
        return KnowledgeSourceDocument(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _segment_from_dict(data: dict[str, Any]) -> KnowledgeSourceSegment:
        allowed = {field.name for field in fields(KnowledgeSourceSegment)}
        return KnowledgeSourceSegment(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _asset_from_dict(data: dict[str, Any]) -> CorrectKnowledgeAsset:
        allowed = {field.name for field in fields(CorrectKnowledgeAsset)}
        return CorrectKnowledgeAsset(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _resource_from_dict(data: dict[str, Any]) -> LearningResource:
        allowed = {field.name for field in fields(LearningResource)}
        return LearningResource(**{key: value for key, value in data.items() if key in allowed})

    # ── KnowledgeMemoryEngine integration ────────────────────────────────

    def _map_outcome_to_km(self, outcome: str) -> str:
        """Map review-lab outcome vocabulary to KnowledgeMemoryEngine vocabulary.

        recalled  → reviewed   (successful recall)
        partial   → struggled  (partial recall)
        forgot    → forgot     (failed recall)
        skipped   → struggled  (avoided recall — treat as struggle)
        """
        mapping = {
            "recalled": "reviewed",
            "partial": "struggled",
            "forgot": "forgot",
            "skipped": "struggled",
        }
        return mapping.get(outcome, "reviewed")

    def _update_knowledge_memory(
        self,
        unit: DailyReviewUnit,
        outcome: ReviewUnitOutcome,
    ) -> dict[str, Any] | None:
        """Feed a unit outcome into the KnowledgeMemoryEngine."""
        if not unit.knowledge_id:
            return None

        overlay_path = self.repo_root / ".system" / "memory" / "review" / "knowledge-status.json"
        overlay: dict[str, Any] = {"schema_version": 1, "knowledge_points": {}}
        if overlay_path.exists():
            try:
                overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        kp_map = overlay.setdefault("knowledge_points", {})
        current = kp_map.get(unit.knowledge_id)

        km_outcome = self._map_outcome_to_km(outcome.outcome)
        confidence_after = outcome.confidence_after
        if outcome.outcome == "recalled" and outcome.confidence_after >= 3:
            confidence_after = max(confidence_after, 3)

        feedback = KnowledgeFeedbackInput(
            knowledge_id=unit.knowledge_id,
            subject=unit.subject,
            heading=unit.heading,
            trigger=unit.los,
            source_refs=unit.source_refs,
            outcome=km_outcome,
            confidence_after=confidence_after,
            time_spent_seconds=outcome.time_spent_seconds,
        )

        entry, decision = self.km_engine.update_knowledge_point(
            current, feedback,
        )
        kp_map[unit.knowledge_id] = entry
        overlay["knowledge_points"] = kp_map

        overlay_path.parent.mkdir(parents=True, exist_ok=True)
        overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "knowledge_id": decision.knowledge_id,
            "state": decision.status_label,
            "state_value": int(decision.state),
            "next_review_at": decision.next_review_date,
            "review_interval_days": decision.review_interval_days,
            "decay_risk": decision.decay_risk,
            "reasoning": decision.reasoning,
        }

    def _update_formula_memory(
        self,
        unit: DailyReviewUnit,
        outcome: ReviewUnitOutcome,
    ) -> dict[str, Any] | None:
        """Persist formula-specific mastery and weakness tags."""
        is_formula_unit = (
            unit.asset_type in {"formula", "formula_lab"}
            or unit.unit_type == "formula"
            or unit.interaction_mode in {
                "derive_formula",
                "recall_formula",
                "identify_variables",
                "choose_applicability",
                "solve_formula_mini_case",
                "ba_ii_plus_procedure",
            }
            or bool(unit.formula_latex)
        )
        if not is_formula_unit or not unit.asset_id:
            return None

        if outcome.outcome == "recalled" and outcome.confidence_after >= 3:
            mastery_state = "Practiced"
            interval_days = 7
            weakness_tags: list[str] = []
        elif outcome.outcome == "partial":
            mastery_state = "Learning"
            interval_days = 2
            weakness_tags = ["variable_confusion" if unit.variables else "arithmetic_setup_gap"]
            if unit.boundary_rules or unit.applies_when or unit.not_when:
                weakness_tags.append("boundary_confusion")
        elif outcome.outcome == "forgot":
            mastery_state = "Learning"
            interval_days = 1
            weakness_tags = ["forgot_formula"]
        else:
            mastery_state = "Learning"
            interval_days = 1
            weakness_tags = ["arithmetic_setup_gap"]

        if unit.ba_ii_plus_steps and outcome.outcome in {"partial", "forgot", "skipped"}:
            weakness_tags.append("calculator_procedure_gap")

        next_review_at = (datetime.now(timezone.utc) + timedelta(days=interval_days)).isoformat()
        status_path = self.repo_root / ".system" / "memory" / "review" / "formula-status.json"
        status: dict[str, Any] = {"schema_version": 1, "formulas": {}}
        if status_path.exists():
            try:
                status = json.loads(status_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        formulas = status.setdefault("formulas", {})
        formulas[unit.asset_id] = {
            "asset_id": unit.asset_id,
            "mastery_state": mastery_state,
            "next_review_at": next_review_at,
            "weakness_tags": sorted(set(weakness_tags)),
            "last_outcome": outcome.outcome,
            "confidence_after": outcome.confidence_after,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

        asset = self._load_ingested_asset(unit.asset_id)
        if asset is not None:
            asset.mastery_state = mastery_state
            asset.next_review_at = next_review_at
            self._persist_ingested_asset(asset)

        return formulas[unit.asset_id]

    def _update_card_if_linked(
        self,
        unit: DailyReviewUnit,
        outcome: ReviewUnitOutcome,
    ) -> dict[str, Any] | None:
        """Update a mistake card if this unit is linked to one."""
        if not unit.card_id:
            return None

        # Map review-lab outcome to card outcome vocabulary
        card_outcome_map = {
            "recalled": "recalled",
            "partial": "struggled",
            "forgot": "forgot",
            "skipped": "struggled",
        }
        card_outcome = card_outcome_map.get(outcome.outcome, "struggled")
        confidence_after = outcome.confidence_after

        try:
            from app.workflows import mark_card_reviewed
            result = mark_card_reviewed(
                self._repo(),
                unit.card_id,
                card_outcome,
                confidence_after,
            )
            return result
        except Exception:
            # Card may not exist or workflow not available — non-fatal
            return None

    # ── Persistence helpers ──────────────────────────────────────────────

    def _persist_session(self, session: ReviewLabSession) -> None:
        path = self._session_root / f"{session.session_id}.json"
        path.write_text(
            json.dumps(session.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load_snapshot(self, review_id: str) -> dict[str, Any]:
        """Load a daily review snapshot by review_id or latest."""
        snapshot_root = self.repo_root / ".system" / "memory" / "review" / "daily"
        if review_id:
            path = snapshot_root / f"{review_id}.json"
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        # Fallback to latest
        latest = snapshot_root / "latest.json"
        if latest.exists():
            return json.loads(latest.read_text(encoding="utf-8"))
        return {"review_id": review_id or "", "knowledge_points": [], "mistake_cards": []}

    def _load_card_content(self, card_id: str) -> dict[str, Any] | None:
        """Try to load card markdown content for richer prompts."""
        for domain in ("question-errors", "cognitive-bias", "agent-failures"):
            path = self.repo_root / ".system" / "memory" / domain / f"{card_id}.md"
            if path.exists():
                text = path.read_text(encoding="utf-8")
                return self._parse_card_markdown(text)
        return None

    @staticmethod
    def _parse_card_markdown(text: str) -> dict[str, Any]:
        """Simple frontmatter + body parser for mistake cards."""
        lines = text.splitlines()
        frontmatter: dict[str, str] = {}
        in_fm = False
        body_lines: list[str] = []
        section = ""
        sections: dict[str, list[str]] = {}

        for line in lines:
            if line.strip() == "---":
                in_fm = not in_fm
                continue
            if in_fm:
                if ":" in line:
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip()
                continue
            if line.startswith("## "):
                section = line[3:].strip().lower().replace(" ", "_")
                sections[section] = []
                continue
            if section:
                sections[section].append(line)
            else:
                body_lines.append(line)

        return {
            "prompt": "\n".join(sections.get("prompt", body_lines)).strip(),
            "correct_resolution": (
                frontmatter.get("correct_resolution", "")
                or "\n".join(sections.get("correct_resolution", [])).strip()
            ),
            "fix_rule": frontmatter.get("fix_rule", ""),
            "next_drill": frontmatter.get("next_drill", ""),
            "topic": frontmatter.get("topic", ""),
            "los": frontmatter.get("los", ""),
        }

    def _advance_session(self, session: ReviewLabSession) -> None:
        """Move current_unit_index to the next uncompleted unit."""
        completed = set(session.completed_unit_ids)
        for i in range(session.current_unit_index + 1, len(session.units)):
            if session.units[i].unit_id not in completed:
                session.current_unit_index = i
                return
        # No more units — stay at end
        session.current_unit_index = len(session.units)

    def _record_session_completion_event(self, session: ReviewLabSession) -> None:
        """Append a review event for session completion."""
        try:
            from app.workflows import _append_review_event_once, _review_event
            event = _review_event(
                "review_lab.completed",
                session.session_id,
                source_refs=[session.review_id],
                payload={
                    "session_id": session.session_id,
                    "review_id": session.review_id,
                    "unit_count": len(session.units),
                    "outcome_count": len(session.outcomes),
                    "energy_level": session.energy_level,
                },
            )
            _append_review_event_once(self._repo(), event)
        except Exception:
            pass

    def _repo(self):
        """Lazy-load Repository for card updates."""
        from app.storage import Repository
        return Repository(self.repo_root)

    # ── Serialization ────────────────────────────────────────────────────

    @staticmethod
    def _deserialize_session(data: dict[str, Any]) -> ReviewLabSession:
        from dataclasses import fields
        unit_fields = {field.name for field in fields(DailyReviewUnit)}
        outcome_fields = {field.name for field in fields(ReviewUnitOutcome)}
        units = [
            DailyReviewUnit(**{key: value for key, value in u.items() if key in unit_fields})
            for u in data.get("units", [])
        ]
        outcomes = [
            ReviewUnitOutcome(**{key: value for key, value in o.items() if key in outcome_fields})
            for o in data.get("outcomes", [])
        ]
        return ReviewLabSession(
            session_id=data["session_id"],
            review_id=data["review_id"],
            status=data.get("status", "active"),
            units=units,
            current_unit_index=data.get("current_unit_index", 0),
            completed_unit_ids=data.get("completed_unit_ids", []),
            outcomes=outcomes,
            energy_level=data.get("energy_level", 2),
            focus_topic=data.get("focus_topic", ""),
            started_at=data.get("started_at", ""),
            completed_at=data.get("completed_at", ""),
            paused_at=data.get("paused_at", ""),
            resumed_at=data.get("resumed_at", ""),
        )

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        from hashlib import sha1
        raw = "||".join(parts).encode("utf-8")
        return f"{prefix}-{sha1(raw, usedforsecurity=False).hexdigest()[:12]}"
