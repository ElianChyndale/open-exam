"""Local-first ecosystem interoperability exports and import previews."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, sanitize_payload

ArtifactType = Literal["anki_csv", "anki_tsv", "markdown_zip", "ics", "xapi_json", "import_preview"]

FORBIDDEN_FIELDS = FORBIDDEN_SAFE_PAYLOAD_KEYS

ANKI_FIELDS = [
    "openexam_id",
    "note_type",
    "front",
    "back",
    "tags",
    "source_refs",
    "goal_id",
    "topic_ids",
    "quality_status",
    "validation_status",
    "created_at",
]


@dataclass(slots=True)
class InteropArtifact:
    artifact_id: str
    profile_id: str
    artifact_type: ArtifactType
    created_at: str
    file_path: str
    size_bytes: int
    content_hash: str
    categories: list[str]
    source_filters: dict[str, Any]
    safe_mode: bool
    redaction_report: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class InteropImportPreview:
    preview_id: str
    artifact_type: str
    filename: str
    detected_items: int
    duplicates: int
    warnings: list[dict[str, Any]]
    proposed_records: list[dict[str, Any]]
    will_auto_confirm: bool = False
    created_at: str = field(default_factory=lambda: _now())

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class InteropService:
    """Exports and import previews that preserve provenance and safe-mode redaction."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "interop"
        self.export_root = self.root / "exports"
        self.import_root = self.root / "imports"
        self.artifact_root = self.root / "artifacts"
        self.preview_root = self.root / "previews"
        for path in (self.export_root, self.import_root, self.artifact_root, self.preview_root):
            path.mkdir(parents=True, exist_ok=True)

    def list_artifacts(self) -> dict[str, Any]:
        artifacts = [self._load_artifact(path) for path in self.artifact_root.glob("*.json")]
        artifacts = [artifact for artifact in artifacts if artifact is not None]
        artifacts.sort(key=lambda item: item.created_at, reverse=True)
        return {"count": len(artifacts), "artifacts": [artifact.as_dict() for artifact in artifacts]}

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        artifact = self._load_artifact(self.artifact_root / f"{artifact_id}.json")
        return artifact.as_dict() if artifact else None

    def export_anki(self, req: dict[str, Any] | None = None) -> dict[str, Any]:
        req = req or {}
        profile_id = str(req.get("profile_id") or "default")
        fmt = "tsv" if str(req.get("format") or "csv").lower() == "tsv" else "csv"
        confirmed_only = bool(req.get("confirmed_only", True))
        source_filters = self._source_filters(req, confirmed_only=confirmed_only)
        rows = [
            self._asset_to_anki_row(asset)
            for asset in self._assets(profile_id=profile_id, confirmed_only=confirmed_only, filters=source_filters)
        ]
        delimiter = "\t" if fmt == "tsv" else ","
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=ANKI_FIELDS, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        content = buffer.getvalue()
        content, report = self._redact_text(content)
        artifact_type: ArtifactType = "anki_tsv" if fmt == "tsv" else "anki_csv"
        artifact = self._write_artifact_file(
            profile_id=profile_id,
            artifact_type=artifact_type,
            suffix=fmt,
            content=content.encode("utf-8"),
            categories=["assets", "formulas", "lexical_assets", "assessments", "goals"],
            source_filters={**source_filters, "format": fmt},
            safe_mode=True,
            redaction_report=report,
        )
        return {"artifact": artifact.as_dict(), "item_count": len(rows), "sample_rows": rows[:5], "redaction_report": report}

    def preview_anki_import(self, req: dict[str, Any]) -> dict[str, Any]:
        profile_id = str(req.get("profile_id") or "default")
        file_path = str(req.get("file_path") or "")
        source = self._resolve_repo_path(file_path)
        rows = self._read_anki_rows(source)
        preview = self._build_import_preview(
            artifact_type="anki_csv" if source.suffix.lower() != ".tsv" else "anki_tsv",
            profile_id=profile_id,
            source=source,
            rows=rows,
            source_prefix="anki_import",
        )
        self._persist_preview(preview)
        return preview.as_dict()

    def commit_anki_import(self, req: dict[str, Any]) -> dict[str, Any]:
        preview = self._load_preview(str(req.get("preview_id") or ""))
        records = []
        for record in preview.proposed_records:
            asset = self._record_to_asset(record, created_from="manual")
            self._persist_asset(asset)
            records.append(asset)
        return {"preview_id": preview.preview_id, "committed_count": len(records), "records": records}

    def export_markdown(self, req: dict[str, Any] | None = None) -> dict[str, Any]:
        req = req or {}
        profile_id = str(req.get("profile_id") or "default")
        confirmed_only = bool(req.get("confirmed_only", True))
        source_filters = self._source_filters(req, confirmed_only=confirmed_only)
        assets = self._assets(profile_id=profile_id, confirmed_only=confirmed_only, filters=source_filters)
        now = _now()
        artifact_id = _stable_id("markdown", profile_id, now)
        relative_path = f".system/memory/interop/exports/{artifact_id}.zip"
        archive_path = self.repo_root / relative_path
        report = {"fields_removed_count": 0, "redacted_fields": sorted(FORBIDDEN_FIELDS)}
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.writestr("OpenExam-Export/README.md", "# OpenExam Export\n\nSafe local Markdown/Obsidian export.\n")
            for asset in assets:
                note = self._asset_to_markdown(asset)
                note, redaction = self._redact_text(note)
                report["fields_removed_count"] += redaction["fields_removed_count"]
                archive.writestr(f"OpenExam-Export/Assets/{_slug(asset.get('asset_id') or asset.get('title'))}.md", note)
            for goal in self._goals(profile_id):
                archive.writestr(f"OpenExam-Export/Goals/{_slug(goal.get('goal_id') or goal.get('title'))}.md", self._goal_to_markdown(goal))
        artifact = self._register_artifact(
            profile_id=profile_id,
            artifact_type="markdown_zip",
            file_path=relative_path,
            categories=["assets", "formulas", "lexicon", "goals", "knowledge-map"],
            source_filters=source_filters,
            safe_mode=True,
            redaction_report=report,
        )
        return {"artifact": artifact.as_dict(), "item_count": len(assets), "sample_notes": [self._asset_to_markdown(asset) for asset in assets[:2]], "redaction_report": report}

    def preview_markdown_import(self, req: dict[str, Any]) -> dict[str, Any]:
        profile_id = str(req.get("profile_id") or "default")
        source = self._resolve_repo_path(str(req.get("file_path") or ""))
        rows = self._read_markdown_rows(source)
        preview = self._build_import_preview(
            artifact_type="markdown_zip" if source.suffix.lower() == ".zip" else "markdown",
            profile_id=profile_id,
            source=source,
            rows=rows,
            source_prefix="markdown_import",
        )
        self._persist_preview(preview)
        return preview.as_dict()

    def commit_markdown_import(self, req: dict[str, Any]) -> dict[str, Any]:
        preview = self._load_preview(str(req.get("preview_id") or ""))
        records = []
        for record in preview.proposed_records:
            asset = self._record_to_asset(record, created_from="markdown_note")
            self._persist_asset(asset)
            records.append(asset)
        return {"preview_id": preview.preview_id, "committed_count": len(records), "records": records}

    def export_calendar(self, req: dict[str, Any]) -> dict[str, Any]:
        profile_id = str(req.get("profile_id") or "default")
        plan_id = str(req.get("plan_id") or "")
        include_completed = bool(req.get("include_completed", False))
        start = _parse_datetime(str(req.get("start_datetime") or _now()))
        timezone = str(req.get("timezone") or "UTC")
        plan = self._load_plan(plan_id)
        blocks = [
            block
            for block in plan.get("blocks", [])
            if include_completed or str(block.get("status") or "pending") != "completed"
        ]
        lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//OpenExam//Local Interop//EN", f"X-WR-TIMEZONE:{timezone}"]
        cursor = start
        for block in blocks:
            minutes = max(5, int(block.get("target_minutes") or 30))
            end = cursor + timedelta(minutes=minutes)
            description = "\\n".join(
                [
                    str(block.get("description") or ""),
                    f"launch_route={block.get('launch_route') or ''}",
                    f"goal_id={block.get('goal_id') or plan.get('source_signals', {}).get('goal_id') or ''}",
                    f"block_type={block.get('block_type') or ''}",
                    f"due_reason={block.get('due_reason') or ''}",
                    f"source_refs={','.join(_coerce_list(block.get('source_refs'))[:4])}",
                ]
            )
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    f"UID:{block.get('block_id') or _stable_id('block', plan_id, cursor.isoformat())}@openexam.local",
                    f"DTSTAMP:{_ics_time(datetime.now(tz=UTC))}",
                    f"DTSTART:{_ics_time(cursor)}",
                    f"DTEND:{_ics_time(end)}",
                    f"SUMMARY:{_ics_escape(str(block.get('title') or 'OpenExam study block'))}",
                    f"DESCRIPTION:{_ics_escape(description)}",
                    "END:VEVENT",
                ]
            )
            cursor = end
        lines.append("END:VCALENDAR")
        artifact = self._write_artifact_file(
            profile_id=profile_id,
            artifact_type="ics",
            suffix="ics",
            content=("\r\n".join(lines) + "\r\n").encode("utf-8"),
            categories=["study_plans", "goals"],
            source_filters={"plan_id": plan_id, "include_completed": include_completed, "timezone": timezone},
            safe_mode=True,
            redaction_report={"fields_removed_count": 0, "redacted_fields": sorted(FORBIDDEN_FIELDS)},
        )
        return {"artifact": artifact.as_dict(), "event_count": len(blocks), "sample_events": blocks[:3]}

    def export_learning_records(self, req: dict[str, Any] | None = None) -> dict[str, Any]:
        req = req or {}
        profile_id = str(req.get("profile_id") or "default")
        safe_mode = bool(req.get("safe_mode", True))
        statements = []
        report = {"fields_removed_count": 0, "redacted_fields": sorted(FORBIDDEN_FIELDS)}
        for event in self._event_rows(profile_id=profile_id):
            clean, redaction = self._redact_payload(event) if safe_mode else (event, {"fields_removed_count": 0})
            report["fields_removed_count"] += int(redaction["fields_removed_count"])
            statements.append(self._event_to_statement(clean, profile_id=profile_id))
        for plan in self._plans(profile_id):
            for block in plan.get("blocks", []):
                if str(block.get("status")) == "completed":
                    statements.append(self._block_to_statement(block, profile_id=profile_id, plan=plan))
        artifact = self._write_artifact_file(
            profile_id=profile_id,
            artifact_type="xapi_json",
            suffix="json",
            content=json.dumps(statements, ensure_ascii=False, indent=2).encode("utf-8"),
            categories=["review_lab", "assessments", "learning_analytics", "study_plans", "resources", "coverage"],
            source_filters={"safe_mode": safe_mode},
            safe_mode=safe_mode,
            redaction_report=report,
        )
        return {"artifact": artifact.as_dict(), "statement_count": len(statements), "sample_statements": statements[:5], "redaction_report": report}

    def privacy_report(self, profile_id: str = "default") -> dict[str, Any]:
        artifacts = self.list_artifacts()["artifacts"]
        return {
            "profile_id": profile_id or "default",
            "generated_at": _now(),
            "safe_mode_default": True,
            "artifact_count": len(artifacts),
            "artifact_types": sorted({artifact["artifact_type"] for artifact in artifacts}),
            "redacted_fields": sorted(FORBIDDEN_FIELDS),
            "raw_diagnostic_fields_blocked": sorted(FORBIDDEN_FIELDS),
            "will_auto_confirm_imports": False,
        }

    def _source_filters(self, req: dict[str, Any], *, confirmed_only: bool) -> dict[str, Any]:
        raw_filters = req.get("source_filters") if isinstance(req.get("source_filters"), dict) else {}
        filters: dict[str, Any] = {"confirmed_only": confirmed_only}
        for key in ("module", "topic", "asset_type", "subject", "los"):
            value = req.get(key, raw_filters.get(key))
            if value not in (None, ""):
                filters[key] = str(value)
        asset_ids = req.get("asset_ids", raw_filters.get("asset_ids"))
        if asset_ids:
            filters["asset_ids"] = _coerce_list(asset_ids)
        return filters

    def _assets(
        self,
        *,
        profile_id: str,
        confirmed_only: bool,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        root = self.repo_root / ".system" / "memory" / "review" / "asset-candidates"
        assets = []
        for path in sorted(root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if str(payload.get("profile_id") or profile_id) != profile_id:
                continue
            if confirmed_only and not _is_confirmed(payload):
                continue
            if not self._matches_asset_filters(payload, filters or {}):
                continue
            assets.append(payload)
        return assets

    def _matches_asset_filters(self, asset: dict[str, Any], filters: dict[str, Any]) -> bool:
        asset_ids = set(str(item) for item in _coerce_list(filters.get("asset_ids")))
        if asset_ids and str(asset.get("asset_id") or "") not in asset_ids:
            return False
        for key in ("module", "subject", "asset_type", "los"):
            value = str(filters.get(key) or "").strip().lower()
            if value and value not in str(asset.get(key) or "").strip().lower():
                return False
        topic = str(filters.get("topic") or "").strip().lower()
        if topic:
            topic_fields = [
                asset.get("topic"),
                asset.get("title"),
                asset.get("formula_family"),
                " ".join(str(item) for item in _coerce_list(asset.get("tags"))),
            ]
            if not any(topic in str(field or "").lower() for field in topic_fields):
                return False
        return True

    def _goals(self, profile_id: str) -> list[dict[str, Any]]:
        root = self.repo_root / ".system" / "memory" / "goals" / "profiles"
        goals = []
        for path in sorted(root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if str(payload.get("profile_id") or profile_id) == profile_id:
                goals.append(payload)
        return goals

    def _plans(self, profile_id: str) -> list[dict[str, Any]]:
        root = self.repo_root / ".system" / "memory" / "study-planner" / "plans"
        plans = []
        for path in sorted(root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if str(payload.get("profile_id") or profile_id) == profile_id:
                plans.append(payload)
        return plans

    def _load_plan(self, plan_id: str) -> dict[str, Any]:
        path = self.repo_root / ".system" / "memory" / "study-planner" / "plans" / f"{plan_id}.json"
        if not path.exists():
            raise KeyError(plan_id)
        return json.loads(path.read_text(encoding="utf-8"))

    def _event_rows(self, *, profile_id: str) -> list[dict[str, Any]]:
        rows = []
        event_root = self.repo_root / ".system" / "events"
        for path in sorted(event_root.rglob("*.jsonl")):
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if str(payload.get("profile_id") or profile_id) == profile_id:
                    payload.setdefault("source_refs", [])
                    payload.setdefault("event_source_path", self._relative_path(path))
                    rows.append(payload)
        return rows

    def _asset_to_anki_row(self, asset: dict[str, Any]) -> dict[str, Any]:
        note_type = _note_type(asset)
        front = str(asset.get("trigger") or asset.get("title") or asset.get("asset_id") or "Recall this OpenExam item")
        back = str(asset.get("correct_rule") or asset.get("plain_formula") or asset.get("formula_latex") or asset.get("example") or "")
        if note_type == "Formula":
            front = f"Recall formula: {asset.get('title') or asset.get('formula_family') or asset.get('asset_id')}"
        tags = [str(asset.get("asset_type") or "asset"), str(asset.get("module") or "").strip(), str(asset.get("subject") or "").strip()]
        return {
            "openexam_id": str(asset.get("asset_id") or _stable_id("asset", front, back)),
            "note_type": note_type,
            "front": front,
            "back": back,
            "tags": " ".join(_slug(tag) for tag in tags if tag),
            "source_refs": "|".join(_coerce_list(asset.get("source_refs"))),
            "goal_id": str(asset.get("goal_id") or ""),
            "topic_ids": "|".join([value for value in [str(asset.get("syllabus_topic_id") or "")] if value]),
            "quality_status": str(asset.get("resource_quality_status") or asset.get("quality_status") or ("trusted" if _is_confirmed(asset) else "draft")),
            "validation_status": str(asset.get("validation_status") or "draft"),
            "created_at": str(asset.get("created_at") or _now()),
        }

    def _asset_to_markdown(self, asset: dict[str, Any]) -> str:
        refs = _coerce_list(asset.get("source_refs"))
        frontmatter = [
            "---",
            f"openexam_id: {asset.get('asset_id') or ''}",
            f"type: {asset.get('asset_type') or 'asset'}",
            f"goal_id: {asset.get('goal_id') or ''}",
            f"validation_status: {asset.get('validation_status') or 'draft'}",
            f"quality_status: {asset.get('resource_quality_status') or asset.get('quality_status') or ''}",
            "source_refs:",
            *[f"  - {ref}" for ref in refs],
            "tags:",
            f"  - {_slug(str(asset.get('asset_type') or 'asset'))}",
            f"created_at: {asset.get('created_at') or _now()}",
            f"updated_at: {_now()}",
            "---",
        ]
        return "\n".join(
            [
                *frontmatter,
                "",
                f"# {asset.get('title') or asset.get('asset_id')}",
                "",
                f"Summary: {asset.get('trigger') or asset.get('module') or 'OpenExam learning asset'}",
                "",
                f"Correct rule/answer: {asset.get('correct_rule') or asset.get('plain_formula') or asset.get('formula_latex') or ''}",
                "",
                "Source refs:",
                *[f"- {ref}" for ref in refs],
                "",
                f"OpenExam route: /review/lab?asset_id={asset.get('asset_id') or ''}",
                "",
            ]
        )

    def _goal_to_markdown(self, goal: dict[str, Any]) -> str:
        return "\n".join(
            [
                "---",
                f"openexam_id: {goal.get('goal_id') or ''}",
                "type: goal",
                f"goal_id: {goal.get('goal_id') or ''}",
                "validation_status: confirmed",
                "quality_status: local",
                "source_refs: []",
                "tags:",
                "  - goal",
                f"created_at: {goal.get('created_at') or _now()}",
                f"updated_at: {_now()}",
                "---",
                "",
                f"# {goal.get('title') or goal.get('goal_id') or 'Goal'}",
                "",
                "Local OpenExam goal profile.",
                "",
            ]
        )

    def _read_anki_rows(self, source: Path) -> list[dict[str, Any]]:
        delimiter = "\t" if source.suffix.lower() == ".tsv" else ","
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle, delimiter=delimiter)]

    def _read_markdown_rows(self, source: Path) -> list[dict[str, Any]]:
        files: list[tuple[str, str]]
        if source.suffix.lower() == ".zip":
            with zipfile.ZipFile(source) as archive:
                files = [(name, archive.read(name).decode("utf-8", errors="replace")) for name in archive.namelist() if name.endswith(".md")]
        elif source.is_dir():
            files = [(self._relative_path(path), path.read_text(encoding="utf-8", errors="replace")) for path in source.rglob("*.md")]
        else:
            files = [(self._relative_path(source), source.read_text(encoding="utf-8", errors="replace"))]
        rows = []
        for index, (name, text) in enumerate(files, start=1):
            metadata, body = _parse_frontmatter(text)
            title = _first_heading(body) or str(metadata.get("openexam_id") or Path(name).stem)
            rows.append(
                {
                    "openexam_id": str(metadata.get("openexam_id") or _stable_id("markdown", name, body)),
                    "note_type": str(metadata.get("type") or "Concept recall"),
                    "front": title,
                    "back": _correct_line(body) or body.strip()[:500],
                    "tags": " ".join(_coerce_list(metadata.get("tags"))),
                    "source_refs": "|".join(_coerce_list(metadata.get("source_refs")) + [f"{name}#row={index}"]),
                    "goal_id": str(metadata.get("goal_id") or ""),
                    "topic_ids": "",
                    "quality_status": str(metadata.get("quality_status") or "external"),
                    "validation_status": "draft",
                    "created_at": _now(),
                }
            )
        return rows

    def _build_import_preview(
        self,
        *,
        artifact_type: str,
        profile_id: str,
        source: Path,
        rows: list[dict[str, Any]],
        source_prefix: str,
    ) -> InteropImportPreview:
        existing_ids, existing_hashes = self._existing_asset_keys(profile_id)
        seen_ids: set[str] = set()
        seen_hashes: set[str] = set()
        duplicates = 0
        proposed = []
        warnings = []
        for index, row in enumerate(rows, start=2):
            openexam_id = _safe_id(str(row.get("openexam_id") or _stable_id("interop", row.get("front"), row.get("back"))))
            content_hash = _content_hash(str(row.get("front") or ""), str(row.get("back") or ""))
            is_duplicate = openexam_id in existing_ids or openexam_id in seen_ids or content_hash in existing_hashes or content_hash in seen_hashes
            if is_duplicate:
                duplicates += 1
                warnings.append({"row": index, "code": "duplicate", "message": "Duplicate openexam_id or front/back hash detected."})
                continue
            seen_ids.add(openexam_id)
            seen_hashes.add(content_hash)
            source_refs = _split_refs(str(row.get("source_refs") or ""))
            source_refs.insert(0, f"{source_prefix}:{self._relative_path(source)}#row={index}")
            proposed.append(
                {
                    "asset_id": openexam_id,
                    "openexam_id": openexam_id,
                    "profile_id": profile_id,
                    "asset_type": _asset_type_from_note(str(row.get("note_type") or "")),
                    "title": str(row.get("front") or openexam_id),
                    "trigger": str(row.get("front") or ""),
                    "correct_rule": str(row.get("back") or ""),
                    "source_refs": source_refs,
                    "goal_id": str(row.get("goal_id") or ""),
                    "syllabus_topic_id": _split_refs(str(row.get("topic_ids") or ""))[0] if _split_refs(str(row.get("topic_ids") or "")) else "",
                    "resource_quality_status": "external",
                    "validation_status": "draft",
                    "created_from": "markdown_note" if source_prefix == "markdown_import" else "manual",
                    "content_hash": content_hash,
                }
            )
        preview_id = _stable_id("preview", artifact_type, self._relative_path(source), source.stat().st_mtime_ns, len(rows), len(proposed))
        return InteropImportPreview(
            preview_id=preview_id,
            artifact_type=artifact_type,
            filename=self._relative_path(source),
            detected_items=len(rows),
            duplicates=duplicates,
            warnings=warnings,
            proposed_records=proposed,
            will_auto_confirm=False,
        )

    def _record_to_asset(self, record: dict[str, Any], *, created_from: str) -> dict[str, Any]:
        return {
            "asset_id": _safe_id(str(record.get("asset_id") or record.get("openexam_id") or _stable_id("interop", record))),
            "asset_type": record.get("asset_type") or "definition",
            "profile_id": record.get("profile_id") or "default",
            "title": record.get("title") or record.get("front") or "",
            "trigger": record.get("trigger") or record.get("front") or "",
            "correct_rule": record.get("correct_rule") or record.get("back") or "",
            "source_refs": _coerce_list(record.get("source_refs")),
            "goal_id": record.get("goal_id") or "",
            "syllabus_topic_id": record.get("syllabus_topic_id") or "",
            "resource_quality_status": "external",
            "validation_status": "draft",
            "created_from": created_from,
        }

    def _persist_asset(self, asset: dict[str, Any]) -> None:
        root = self.repo_root / ".system" / "memory" / "review" / "asset-candidates"
        root.mkdir(parents=True, exist_ok=True)
        (root / f"{asset['asset_id']}.json").write_text(json.dumps(asset, ensure_ascii=False, indent=2), encoding="utf-8")

    def _existing_asset_keys(self, profile_id: str) -> tuple[set[str], set[str]]:
        ids = set()
        hashes = set()
        for asset in self._assets(profile_id=profile_id, confirmed_only=False):
            ids.add(_safe_id(str(asset.get("asset_id") or "")))
            front_candidates: list[str] = []
            for candidate in (asset.get("trigger"), asset.get("title")):
                text = str(candidate or "").strip()
                if text and text not in front_candidates:
                    front_candidates.append(text)
            back = str(asset.get("correct_rule") or asset.get("plain_formula") or asset.get("formula_latex") or "")
            for front in front_candidates or [""]:
                hashes.add(_content_hash(front, back))
        return ids, hashes

    def _event_to_statement(self, event: dict[str, Any], *, profile_id: str) -> dict[str, Any]:
        success = bool(event.get("is_correct")) if "is_correct" in event else True
        asset_id = str(event.get("asset_id") or event.get("event_id") or _stable_id("event", event))
        correct_name = str(event.get("correct_resolution") or event.get("topic") or asset_id)
        return {
            "id": _stable_id("xapi", event.get("event_id") or asset_id, event.get("created_at") or event.get("timestamp") or ""),
            "actor": {"account": {"name": profile_id, "homePage": "local://openexam"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/answered", "display": {"en-US": "answered"}},
            "object": {"id": f"local://openexam/asset/{asset_id}", "definition": {"name": {"en-US": correct_name}}},
            "result": {"success": success, "score": {"scaled": 1.0 if success else 0.0}},
            "context": {"extensions": {"source_refs": _coerce_list(event.get("source_refs")), "goal_id": event.get("goal_id") or ""}},
            "timestamp": str(event.get("created_at") or event.get("timestamp") or _now()),
        }

    def _block_to_statement(self, block: dict[str, Any], *, profile_id: str, plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": _stable_id("xapi-block", block.get("block_id"), plan.get("plan_id")),
            "actor": {"account": {"name": profile_id, "homePage": "local://openexam"}},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/completed", "display": {"en-US": "completed"}},
            "object": {"id": f"local://openexam/study-block/{block.get('block_id')}", "definition": {"name": {"en-US": block.get("title") or "Study block"}}},
            "result": {"success": True, "score": {"scaled": 1.0}},
            "context": {"extensions": {"source_refs": _coerce_list(block.get("source_refs")), "goal_id": block.get("goal_id") or plan.get("source_signals", {}).get("goal_id") or ""}},
            "timestamp": _now(),
        }

    def _write_artifact_file(
        self,
        *,
        profile_id: str,
        artifact_type: ArtifactType,
        suffix: str,
        content: bytes,
        categories: list[str],
        source_filters: dict[str, Any],
        safe_mode: bool,
        redaction_report: dict[str, Any],
    ) -> InteropArtifact:
        artifact_id = _stable_id(artifact_type, profile_id, _now(), hashlib.sha256(content).hexdigest()[:12])
        relative_path = f".system/memory/interop/exports/{artifact_id}.{suffix}"
        path = self.repo_root / relative_path
        path.write_bytes(content)
        return self._register_artifact(
            profile_id=profile_id,
            artifact_type=artifact_type,
            file_path=relative_path,
            categories=categories,
            source_filters=source_filters,
            safe_mode=safe_mode,
            redaction_report=redaction_report,
        )

    def _register_artifact(
        self,
        *,
        profile_id: str,
        artifact_type: ArtifactType,
        file_path: str,
        categories: list[str],
        source_filters: dict[str, Any],
        safe_mode: bool,
        redaction_report: dict[str, Any],
    ) -> InteropArtifact:
        path = self.repo_root / file_path
        artifact = InteropArtifact(
            artifact_id=Path(file_path).stem,
            profile_id=profile_id,
            artifact_type=artifact_type,
            created_at=_now(),
            file_path=file_path,
            size_bytes=path.stat().st_size,
            content_hash=_sha256(path.read_bytes()),
            categories=categories,
            source_filters=source_filters,
            safe_mode=safe_mode,
            redaction_report=redaction_report,
        )
        (self.artifact_root / f"{artifact.artifact_id}.json").write_text(json.dumps(artifact.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return artifact

    def _load_artifact(self, path: Path) -> InteropArtifact | None:
        if not path.exists():
            return None
        try:
            return InteropArtifact(**json.loads(path.read_text(encoding="utf-8")))
        except (OSError, TypeError, json.JSONDecodeError):
            return None

    def _persist_preview(self, preview: InteropImportPreview) -> None:
        (self.preview_root / f"{preview.preview_id}.json").write_text(json.dumps(preview.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_preview(self, preview_id: str) -> InteropImportPreview:
        path = self.preview_root / f"{preview_id}.json"
        if not path.exists():
            raise KeyError(preview_id)
        return InteropImportPreview(**json.loads(path.read_text(encoding="utf-8")))

    def _redact_text(self, text: str) -> tuple[str, dict[str, Any]]:
        fields_removed = 0
        for field_name in FORBIDDEN_FIELDS:
            if field_name in text:
                fields_removed += text.count(field_name)
                text = text.replace(field_name, "[redacted]")
        return text, {"fields_removed_count": fields_removed, "redacted_fields": sorted(FORBIDDEN_FIELDS)}

    def _redact_payload(self, payload: Any) -> tuple[Any, dict[str, Any]]:
        clean, report = sanitize_payload(payload)
        return clean, {"fields_removed_count": report["fields_removed_count"], "redacted_fields": sorted(FORBIDDEN_FIELDS) + ["internal_*"]}

    def _resolve_repo_path(self, file_path: str) -> Path:
        candidate = (self.repo_root / file_path).resolve()
        try:
            candidate.relative_to(self.repo_root.resolve())
        except ValueError as exc:
            raise ValueError("Path must stay inside repository root.") from exc
        if not candidate.exists():
            raise FileNotFoundError(file_path)
        return candidate

    def _relative_path(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo_root.resolve()).as_posix()


def _now() -> str:
    return datetime.now(tz=UTC).isoformat()


def _stable_id(*parts: Any) -> str:
    digest = hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]
    prefix = _slug(str(parts[0])) if parts else "id"
    return f"{prefix}-{digest}"


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _content_hash(front: str, back: str) -> str:
    normalized = _normalize_content_key(f"{front}\n{back}")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _normalize_content_key(value: str) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).lower()
    text = re.sub(r"[\W_]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _is_confirmed(payload: dict[str, Any]) -> bool:
    status = str(payload.get("validation_status") or payload.get("resource_validation_status") or "").lower()
    quality = str(payload.get("resource_quality_status") or payload.get("quality_status") or "").lower()
    return status in {"confirmed", "validated"} or quality in {"trusted", "confirmed"}


def _note_type(asset: dict[str, Any]) -> str:
    asset_type = str(asset.get("asset_type") or "").lower()
    if "formula" in asset_type or asset.get("formula_latex") or asset.get("plain_formula"):
        return "Formula"
    if "boundary" in asset_type:
        return "Boundary"
    if "lex" in asset_type or asset.get("lemma"):
        return "Lexical"
    if "assessment" in asset_type:
        return "Assessment-derived"
    return "Concept recall"


def _asset_type_from_note(note_type: str) -> str:
    value = note_type.lower()
    if "formula" in value:
        return "formula"
    if "boundary" in value:
        return "exam_boundary"
    if "lex" in value:
        return "definition"
    return "definition"


def _coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, tuple | set):
        return [str(item) for item in value if str(item)]
    return [str(value)] if str(value) else []


def _split_refs(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[|,;]", value or "") if item.strip()]


def _slug(value: Any) -> str:
    text = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "item").strip().lower()).strip("-")
    return text[:80] or "item"


def _safe_id(value: str) -> str:
    return _slug(value)


def _parse_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        parsed = datetime.now(tz=UTC)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _ics_time(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _ics_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    metadata: dict[str, Any] = {}
    current_list: str | None = None
    for raw_line in parts[1].splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list:
            metadata.setdefault(current_list, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                metadata[key] = value
                current_list = None
            else:
                metadata[key] = []
                current_list = key
    return metadata, parts[2]


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _correct_line(text: str) -> str:
    for line in text.splitlines():
        if "correct rule" in line.lower() or "correct answer" in line.lower():
            return line.split(":", 1)[-1].strip()
    return ""
