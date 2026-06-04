from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal


SCHEMA_VERSION = "1"
APP_VERSION = "0.1.0"

FORBIDDEN_SAFE_PAYLOAD_KEYS = {
    "wrong_choice_or_output",
    "wrong_formula",
    "wrong_reasoning",
    "wrong_answer",
    "wrong_output",
    "answer_text",
    "selected_choice",
    "selected_answer",
    "raw_response",
    "diagnostics",
    "common_wrong_path",
    "internal_secret",
}
FORBIDDEN_KEY_PREFIXES = ("internal_",)
RAW_DIAGNOSTIC_KEYS = FORBIDDEN_SAFE_PAYLOAD_KEYS
ABSOLUTE_LOCAL_PATH_PATTERNS = (
    re.compile(r"\b[A-Za-z]:[\\/](?:[^\\/\s\"'<>|]+[\\/])*[^\\/\s\"'<>|,.;)]+"),
    re.compile(r"(?<!\w)/(?:Users|home|tmp|var|private|mnt|Volumes)/(?:[^\s\"'<>|]+/)*[^\s\"'<>|,.;)]+"),
)


def is_forbidden_key(key: Any) -> bool:
    key_text = str(key).strip().lower()
    return key_text in FORBIDDEN_SAFE_PAYLOAD_KEYS or any(key_text.startswith(prefix) for prefix in FORBIDDEN_KEY_PREFIXES)


@dataclass(slots=True)
class DataInventoryItem:
    category: str
    path: str | None
    record_count: int
    size_bytes: int
    last_modified_at: str | None
    contains_raw_diagnostics: bool
    contains_source_files: bool
    exportable: bool
    resettable: bool
    notes: str | None = None


@dataclass(slots=True)
class BackupSnapshot:
    snapshot_id: str
    profile_id: str
    created_at: str
    label: str | None
    mode: Literal["safe", "full", "category"]
    categories: list[str]
    file_path: str
    size_bytes: int
    content_hash: str
    manifest: dict[str, Any]
    redaction_policy: dict[str, Any]
    app_version: str | None
    schema_version: str


@dataclass(frozen=True, slots=True)
class CategoryDefinition:
    category: str
    relative_path: str | None
    exportable: bool = True
    resettable: bool = True
    contains_source_files: bool = False
    raw_sensitive: bool = False
    notes: str | None = None


CATEGORIES: tuple[CategoryDefinition, ...] = (
    CategoryDefinition("review_lab", ".system/memory/review/lab-sessions", raw_sensitive=True),
    CategoryDefinition("assets", ".system/memory/review/asset-candidates", raw_sensitive=True),
    CategoryDefinition("source_documents", ".system/memory/review/asset-sources", contains_source_files=True),
    CategoryDefinition("source_segments", ".system/memory/review/asset-segments"),
    CategoryDefinition("files", ".system/memory/review/files", contains_source_files=True),
    CategoryDefinition("resources", ".system/memory/review/resources", contains_source_files=True),
    CategoryDefinition("formulas", ".system/memory/review/formula-status.json", raw_sensitive=True),
    CategoryDefinition("syllabus", ".system/memory/review/syllabus"),
    CategoryDefinition("coverage", ".system/memory/review/syllabus/coverage.json"),
    CategoryDefinition("mock_retro", ".system/memory/review/mock-retro", raw_sensitive=True),
    CategoryDefinition("transfer_gaps", ".system/memory/review/mock-retro/transfer-gaps.json", raw_sensitive=True),
    CategoryDefinition("language_dictionaries", ".system/memory/language/dictionary-kernel/dictionaries"),
    CategoryDefinition("lexical_assets", ".system/memory/language/dictionary-kernel/lexical-assets"),
    CategoryDefinition("lexical_memory", ".system/memory/language/dictionary-kernel/lexical-memory.json"),
    CategoryDefinition("assessments", ".system/memory/assessments/sessions", raw_sensitive=True),
    CategoryDefinition("learning_analytics", ".system/memory/learning-analytics"),
    CategoryDefinition("study_plans", ".system/memory/study-planner/plans"),
    CategoryDefinition("knowledge_graph", ".system/memory/knowledge-graph", resettable=True),
    CategoryDefinition("tutor_conversations", ".system/memory/tutor/conversations"),
    CategoryDefinition("goal_profiles", ".system/memory/goals/profiles"),
    CategoryDefinition("onboarding_state", ".system/memory/goals/onboarding"),
    CategoryDefinition("interop_artifacts", ".system/memory/interop"),
    CategoryDefinition("mission_control", ".system/memory/mission-control", resettable=False, notes="Derived runtime summary cache, if present."),
    CategoryDefinition("todos", ".system/memory/todo"),
    CategoryDefinition("feature_flags", ".system/config/features.yaml", resettable=False),
)


class DataGovernanceService:
    """Local-first inventory, backup, restore, redaction, and reset controls."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.backup_root = self.repo_root / ".system" / "memory" / "backups"
        self.snapshot_root = self.backup_root / "snapshots"
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.snapshot_root.mkdir(parents=True, exist_ok=True)

    def inventory(self, *, profile_id: str = "default") -> dict[str, Any]:
        items = [self._inventory_item(definition) for definition in CATEGORIES]
        return {
            "profile_id": profile_id or "default",
            "generated_at": _now(),
            "items": [asdict(item) for item in items],
            "summary": {
                "category_count": len(items),
                "record_count": sum(item.record_count for item in items),
                "size_bytes": sum(item.size_bytes for item in items),
                "raw_diagnostic_categories": [item.category for item in items if item.contains_raw_diagnostics],
                "source_file_categories": [item.category for item in items if item.contains_source_files],
            },
        }

    def export_backup(
        self,
        *,
        profile_id: str = "default",
        mode: Literal["safe", "full", "category"] = "safe",
        categories: list[str] | None = None,
        include_raw_diagnostics: bool = False,
        label: str | None = None,
    ) -> dict[str, Any]:
        if mode == "full" and not include_raw_diagnostics:
            raise ValueError("Full export requires include_raw_diagnostics=true.")
        selected = self._selected_categories(mode=mode, categories=categories)
        inventory_payload = self.inventory(profile_id=profile_id)
        redaction_policy = {
            "include_raw_diagnostics": bool(include_raw_diagnostics and mode == "full"),
            "raw_diagnostic_fields": "included" if mode == "full" and include_raw_diagnostics else "redacted",
            "internal_fields": "included" if mode == "full" and include_raw_diagnostics else "redacted",
        }
        data_payloads: dict[str, Any] = {}
        redaction_report = {
            "fields_removed_count": 0,
            "categories_sanitized": [],
            "warnings": [],
        }
        for category in selected:
            records = self._category_records(category)
            if mode != "full":
                records, report = sanitize_payload(records)
                redaction_report["fields_removed_count"] += report["fields_removed_count"]
                if report["fields_removed_count"]:
                    redaction_report["categories_sanitized"].append(category)
            data_payloads[category] = records
        if mode == "full":
            redaction_report["warnings"].append("Raw diagnostics included by explicit request.")

        manifest = {
            "created_at": _now(),
            "profile_id": profile_id or "default",
            "export_mode": mode,
            "categories": selected,
            "schema_version": SCHEMA_VERSION,
            "app_version": APP_VERSION,
            "redaction_policy": redaction_policy,
            "feature_flags": self._feature_flags_summary(),
            "counts": {category: _count_records(data_payloads[category]) for category in selected},
        }
        snapshot_id = stable_id("backup", profile_id or "default", mode, manifest["created_at"])
        archive_path = self.backup_root / f"{snapshot_id}.zip"
        checksummed_entries: dict[str, bytes] = {
            "manifest.json": _json_bytes(manifest),
            "inventory.json": _json_bytes(inventory_payload),
            "README_RESTORE.md": _readme_bytes(mode=mode),
        }
        for category, payload in data_payloads.items():
            checksummed_entries[f"data/{category}.json"] = _json_bytes(payload)
        checksums = {name: _sha256(content) for name, content in checksummed_entries.items()}
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, content in checksummed_entries.items():
                archive.writestr(name, content)
            archive.writestr("checksums.json", _json_bytes(checksums))
        content_hash = _sha256(archive_path.read_bytes())
        snapshot = BackupSnapshot(
            snapshot_id=snapshot_id,
            profile_id=profile_id or "default",
            created_at=manifest["created_at"],
            label=label,
            mode=mode,
            categories=selected,
            file_path=self._relative_path(archive_path),
            size_bytes=archive_path.stat().st_size,
            content_hash=content_hash,
            manifest=manifest,
            redaction_policy=redaction_policy,
            app_version=APP_VERSION,
            schema_version=SCHEMA_VERSION,
        )
        self._persist_snapshot(snapshot)
        return {
            "snapshot": asdict(snapshot),
            "manifest": manifest,
            "redaction_report": redaction_report,
            "warning": {"includes_raw_diagnostics": bool(mode == "full" and include_raw_diagnostics)},
        }

    def snapshots(self) -> list[dict[str, Any]]:
        rows = []
        for path in sorted(self.snapshot_root.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
            try:
                rows.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue
        return rows

    def get_snapshot(self, snapshot_id: str) -> dict[str, Any] | None:
        path = self.snapshot_root / f"{snapshot_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def restore_dry_run(
        self,
        *,
        file_path: str,
        profile_id: str = "default",
        mode: Literal["dry_run", "merge", "replace_category", "full_replace"] = "dry_run",
        categories: list[str] | None = None,
    ) -> dict[str, Any]:
        try:
            archive_path = self._resolve_repo_path(file_path)
        except ValueError as exc:
            return self._invalid_restore(str(exc), profile_id=profile_id)
        try:
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
                required = {"manifest.json", "inventory.json", "checksums.json"}
                if not required.issubset(names):
                    return self._invalid_restore("Backup is missing manifest/inventory/checksums.", profile_id=profile_id)
                manifest = json.loads(archive.read("manifest.json"))
                checksums = json.loads(archive.read("checksums.json"))
                checksum_errors = [
                    name for name, expected in checksums.items()
                    if name not in names or _sha256(archive.read(name)) != expected
                ]
                data_names = sorted(name for name in names if name.startswith("data/") and name.endswith(".json"))
                archive_categories = [Path(name).stem for name in data_names]
                invalid_categories = [category for category in archive_categories if category not in self._category_names()]
                selected = categories or archive_categories
                not_in_backup = [category for category in selected if category not in archive_categories]
                planned_changes = []
                conflicts = []
                for data_name in data_names:
                    category = Path(data_name).stem
                    if category not in selected:
                        continue
                    payload = json.loads(archive.read(data_name))
                    existing = self._category_definition(category)
                    if existing and existing.relative_path and self._category_path(existing).exists():
                        conflicts.append({"category": category, "path": existing.relative_path, "strategy": mode})
                    planned_changes.append({"category": category, "record_count": _count_records(payload), "mode": mode})
        except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
            return self._invalid_restore(f"Backup validation failed: {exc}", profile_id=profile_id)
        valid = not checksum_errors and not invalid_categories and not not_in_backup and manifest.get("schema_version") == SCHEMA_VERSION
        return {
            "profile_id": profile_id or "default",
            "valid": valid,
            "checksum_valid": not checksum_errors,
            "schema_compatible": manifest.get("schema_version") == SCHEMA_VERSION,
            "errors": checksum_errors + invalid_categories + not_in_backup,
            "warnings": ["Dry run only; no files were written."],
            "manifest": manifest,
            "planned_changes": planned_changes,
            "conflicts": conflicts,
        }

    def restore_backup(
        self,
        *,
        file_path: str,
        profile_id: str = "default",
        mode: Literal["merge", "replace_category", "full_replace"] = "merge",
        categories: list[str] | None = None,
    ) -> dict[str, Any]:
        dry_run = self.restore_dry_run(file_path=file_path, profile_id=profile_id, mode=mode, categories=categories)
        if not dry_run["valid"]:
            return {"restored": False, **dry_run}
        archive_path = self._resolve_repo_path(file_path)
        restored: list[str] = []
        with zipfile.ZipFile(archive_path) as archive:
            for change in dry_run["planned_changes"]:
                category = change["category"]
                definition = self._category_definition(category)
                if not definition or not definition.relative_path:
                    continue
                if mode in {"replace_category", "full_replace"}:
                    self._clear_category(category)
                payload = json.loads(archive.read(f"data/{category}.json"))
                self._restore_category_payload(category, payload, overwrite=mode != "merge")
                restored.append(category)
        return {"restored": True, "restored_categories": restored, "dry_run": dry_run}

    def reset_category(self, *, category: str, confirmation: str, profile_id: str = "default") -> dict[str, Any]:
        if confirmation != f"RESET {category}":
            raise ValueError(f"Reset requires confirmation string: RESET {category}")
        if category == "all":
            categories = [definition.category for definition in CATEGORIES if definition.resettable]
        else:
            categories = [category]
        for name in categories:
            definition = self._category_definition(name)
            if not definition or not definition.resettable:
                raise ValueError(f"Category is not resettable: {name}")
        snapshot = self.export_backup(profile_id=profile_id, mode="category", categories=categories, label=f"Auto snapshot before reset {category}")["snapshot"]
        cleared = [self._clear_category(name) for name in categories]
        return {"reset": True, "category": category, "cleared_categories": cleared, "snapshot": snapshot}

    def rollback(self, *, snapshot_id: str, categories: list[str] | None = None, profile_id: str = "default") -> dict[str, Any]:
        snapshot = self.get_snapshot(snapshot_id)
        if not snapshot:
            raise ValueError("Snapshot not found")
        selected = categories or list(snapshot.get("categories") or [])
        restored = self.restore_backup(
            file_path=snapshot["file_path"],
            profile_id=profile_id,
            mode="replace_category",
            categories=selected,
        )
        if not restored.get("restored"):
            return {"restored": False, "restored_categories": [], "errors": restored.get("errors", [])}
        return {"restored": True, "snapshot_id": snapshot_id, "restored_categories": restored["restored_categories"]}

    def privacy_report(self, *, profile_id: str = "default") -> dict[str, Any]:
        items = [self._inventory_item(definition) for definition in CATEGORIES]
        raw_categories = [item.category for item in items if item.contains_raw_diagnostics]
        redacted_fields = 0
        categories_sanitized: list[str] = []
        for category in self._category_names():
            _, report = sanitize_payload(self._category_records(category))
            if report["fields_removed_count"]:
                categories_sanitized.append(category)
                redacted_fields += report["fields_removed_count"]
        return {
            "profile_id": profile_id or "default",
            "generated_at": _now(),
            "raw_diagnostic_categories": raw_categories,
            "redacted_fields_count": redacted_fields,
            "categories_sanitized": categories_sanitized,
            "safe_export": {
                "includes_raw_diagnostics": False,
                "redacts": sorted(RAW_DIAGNOSTIC_KEYS) + ["internal_*"],
            },
            "full_export": {
                "includes_raw_diagnostics": True,
                "requires_include_raw_diagnostics": True,
            },
        }

    def governance_summary(self, *, profile_id: str = "default") -> dict[str, Any]:
        inventory = self.inventory(profile_id=profile_id)
        snapshots = self.snapshots()
        last_backup = snapshots[0]["created_at"] if snapshots else None
        return {
            "profile_id": profile_id or "default",
            "last_backup_at": last_backup,
            "backup_count": len(snapshots),
            "backup_health": "never_backed_up" if not snapshots else "ok",
            "local_state_size_bytes": inventory["summary"]["size_bytes"],
            "raw_diagnostic_categories": inventory["summary"]["raw_diagnostic_categories"],
            "category_count": inventory["summary"]["category_count"],
            "snapshot_route": "/review/data",
        }

    def _selected_categories(self, *, mode: str, categories: list[str] | None) -> list[str]:
        names = self._category_names()
        if mode == "category":
            selected = categories or []
            unknown = [category for category in selected if category not in names]
            if unknown:
                raise ValueError(f"Unknown categories: {', '.join(unknown)}")
            return selected
        return [definition.category for definition in CATEGORIES if definition.exportable]

    def _category_names(self) -> set[str]:
        return {definition.category for definition in CATEGORIES}

    def _category_definition(self, category: str) -> CategoryDefinition | None:
        return next((definition for definition in CATEGORIES if definition.category == category), None)

    def _inventory_item(self, definition: CategoryDefinition) -> DataInventoryItem:
        path = self._category_path(definition) if definition.relative_path else None
        size = self._path_size(path) if path and path.exists() else 0
        record_count = self._record_count(path) if path and path.exists() else 0
        last_modified = self._last_modified(path) if path and path.exists() else None
        records = self._category_records(definition.category) if path and path.exists() else []
        _, report = sanitize_payload(records)
        return DataInventoryItem(
            category=definition.category,
            path=definition.relative_path if path and path.exists() else definition.relative_path,
            record_count=record_count,
            size_bytes=size,
            last_modified_at=last_modified,
            contains_raw_diagnostics=definition.raw_sensitive or report["fields_removed_count"] > 0,
            contains_source_files=definition.contains_source_files,
            exportable=definition.exportable,
            resettable=definition.resettable,
            notes=definition.notes,
        )

    def _category_records(self, category: str) -> list[dict[str, Any]]:
        definition = self._category_definition(category)
        if not definition or not definition.relative_path:
            return []
        root = self._category_path(definition)
        if not root.exists():
            return []
        paths = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
        records: list[dict[str, Any]] = []
        for path in paths:
            relative = self._relative_path(path)
            try:
                if path.suffix.lower() == ".json":
                    content: Any = json.loads(path.read_text(encoding="utf-8"))
                    records.append({"relative_path": relative, "content_type": "json", "content": content})
                elif path.suffix.lower() == ".jsonl":
                    rows = [
                        json.loads(line)
                        for line in path.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    records.append({"relative_path": relative, "content_type": "jsonl", "content": rows})
                else:
                    records.append({"relative_path": relative, "content_type": "text", "content": path.read_text(encoding="utf-8", errors="replace")})
            except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                records.append({"relative_path": relative, "content_type": "unreadable", "error": str(exc)})
        return records

    def _restore_category_payload(self, category: str, payload: Any, *, overwrite: bool) -> None:
        if not isinstance(payload, list):
            payload = [{"relative_path": self._category_definition(category).relative_path, "content_type": "json", "content": payload}]
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            relative_path = str(entry.get("relative_path") or "")
            if not relative_path:
                continue
            path = self._resolve_repo_path(relative_path)
            if path.exists() and not overwrite:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            content_type = entry.get("content_type")
            content = entry.get("content")
            if content_type == "json":
                path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            elif content_type == "jsonl" and isinstance(content, list):
                path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in content) + "\n", encoding="utf-8")
            elif isinstance(content, str):
                path.write_text(content, encoding="utf-8")

    def _clear_category(self, category: str) -> str:
        definition = self._category_definition(category)
        if not definition or not definition.relative_path:
            raise ValueError(f"Unknown category: {category}")
        path = self._category_path(definition)
        if path.is_dir():
            shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)
        elif path.exists():
            path.unlink()
        return category

    def _feature_flags_summary(self) -> dict[str, Any]:
        path = self.repo_root / ".system" / "config" / "features.yaml"
        if not path.exists():
            return {}
        return {"path": self._relative_path(path), "size_bytes": path.stat().st_size}

    def _category_path(self, definition: CategoryDefinition) -> Path:
        return self.repo_root / str(definition.relative_path)

    def _resolve_repo_path(self, file_path: str) -> Path:
        candidate = (self.repo_root / file_path).resolve()
        try:
            candidate.relative_to(self.repo_root.resolve())
        except ValueError as exc:
            raise ValueError("Path must stay inside repository root.") from exc
        return candidate

    def _relative_path(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo_root.resolve()).as_posix()

    def _persist_snapshot(self, snapshot: BackupSnapshot) -> None:
        self.snapshot_root.mkdir(parents=True, exist_ok=True)
        (self.snapshot_root / f"{snapshot.snapshot_id}.json").write_text(
            json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _path_size(path: Path | None) -> int:
        if not path:
            return 0
        if path.is_file():
            return path.stat().st_size
        return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())

    @staticmethod
    def _record_count(path: Path | None) -> int:
        if not path:
            return 0
        files = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
        count = 0
        for file_path in files:
            try:
                if file_path.suffix.lower() == ".json":
                    payload = json.loads(file_path.read_text(encoding="utf-8"))
                    count += _count_records(payload)
                elif file_path.suffix.lower() == ".jsonl":
                    count += sum(1 for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip())
                else:
                    count += 1
            except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                count += 1
        return count

    @staticmethod
    def _last_modified(path: Path | None) -> str | None:
        if not path:
            return None
        paths = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
        if not paths:
            return None
        latest = max(item.stat().st_mtime for item in paths)
        return datetime.fromtimestamp(latest, tz=UTC).isoformat()

    @staticmethod
    def _invalid_restore(reason: str, *, profile_id: str) -> dict[str, Any]:
        return {
            "profile_id": profile_id or "default",
            "valid": False,
            "checksum_valid": False,
            "schema_compatible": False,
            "errors": [reason],
            "warnings": [],
            "manifest": {},
            "planned_changes": [],
            "conflicts": [],
        }


def sanitize_payload(payload: Any) -> tuple[Any, dict[str, Any]]:
    removed_values: list[str] = []
    report = {
        "fields_removed_count": 0,
        "removed_keys": [],
        "scrubbed_values_count": 0,
        "local_path_redactions_count": 0,
        "redacted_fields": sorted(FORBIDDEN_SAFE_PAYLOAD_KEYS) + ["internal_*"],
    }

    def collect_strings(value: Any) -> None:
        if isinstance(value, dict):
            for child in value.values():
                collect_strings(child)
            return
        if isinstance(value, list):
            for item in value:
                collect_strings(item)
            return
        if isinstance(value, str) and value:
            removed_values.append(value)

    def strip(value: Any) -> Any:
        if isinstance(value, dict):
            clean: dict[str, Any] = {}
            for key, child in value.items():
                key_text = str(key)
                if is_forbidden_key(key_text):
                    report["fields_removed_count"] += 1
                    report["removed_keys"].append(key_text)
                    collect_strings(child)
                    continue
                clean[key] = strip(child)
            return clean
        if isinstance(value, list):
            return [strip(item) for item in value]
        return value

    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: scrub(child) for key, child in value.items()}
        if isinstance(value, list):
            return [scrub(item) for item in value]
        if isinstance(value, str):
            next_value = value
            for raw in removed_values:
                if raw and raw in next_value:
                    next_value = next_value.replace(raw, "[redacted]")
                    report["scrubbed_values_count"] += 1
            for pattern in ABSOLUTE_LOCAL_PATH_PATTERNS:
                next_value, count = pattern.subn("[local-path]", next_value)
                report["local_path_redactions_count"] += count
            return next_value
        return value

    return scrub(strip(payload)), report


def stable_id(prefix: str, *parts: object) -> str:
    digest = hashlib.sha256("::".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _readme_bytes(*, mode: str) -> bytes:
    return (
        "# OpenExam Backup Restore\n\n"
        f"Export mode: {mode}\n\n"
        "Validate checksums before restore. This archive is data-only; do not execute contents.\n"
        "Safe exports redact raw wrong-answer and internal diagnostic fields.\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _count_records(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("items", "records", "sessions", "assets", "dictionaries", "events", "nodes"):
            if isinstance(payload.get(key), list):
                return len(payload[key])
        return 1 if payload else 0
    return 1 if payload is not None else 0
