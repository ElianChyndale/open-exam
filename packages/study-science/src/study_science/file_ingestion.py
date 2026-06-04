"""Local-first file ingestion for Review Lab and LanguageOS pipelines."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, fields
from datetime import UTC, datetime
from hashlib import sha1, sha256
from pathlib import Path
from typing import Any, Literal


FILE_STATUSES = {"pending", "extracted", "extracted_no_text", "failed", "unsupported", "duplicate"}
SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".json", ".csv", ".pdf"}
MAX_UPLOAD_BYTES = 20 * 1024 * 1024


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    joined = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(joined.encode('utf-8')).hexdigest()[:16]}"


@dataclass
class IngestedFile:
    file_id: str
    profile_id: str
    filename: str
    content_type: str
    file_size: int
    content_hash: str
    imported_at: str
    storage_path: str | None
    extraction_status: Literal["pending", "extracted", "extracted_no_text", "failed", "unsupported", "duplicate"]
    extraction_error: str | None
    page_count: int | None
    source_type: Literal[
        "pdf_note",
        "markdown_note",
        "text_note",
        "json_dictionary",
        "csv_dictionary",
        "resource",
        "unknown",
    ]
    source_id: str | None = None
    resource_id: str | None = None
    dictionary_id: str | None = None
    source_refs: list[str] = field(default_factory=list)
    duplicate_of: str | None = None
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "file_id": self.file_id,
            "profile_id": self.profile_id,
            "filename": self.filename,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "content_hash": self.content_hash,
            "imported_at": self.imported_at,
            "storage_path": self.storage_path,
            "extraction_status": self.extraction_status,
            "extraction_error": self.extraction_error,
            "page_count": self.page_count,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "resource_id": self.resource_id,
            "dictionary_id": self.dictionary_id,
            "source_refs": self.source_refs,
            "duplicate_of": self.duplicate_of,
            "warnings": self.warnings,
        }


@dataclass
class ExtractedFileSegment:
    segment_id: str
    file_id: str
    page: int | None
    heading: str | None
    text: str
    char_start: int | None
    char_end: int | None
    source_ref: str
    evidence_type: str = "other"
    confidence: float = 0.5

    def as_dict(self) -> dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "file_id": self.file_id,
            "source_id": self.file_id,
            "page": self.page,
            "heading": self.heading,
            "text": self.text,
            "char_start": self.char_start,
            "char_end": self.char_end,
            "source_ref": self.source_ref,
            "evidence_type": self.evidence_type,
            "confidence": self.confidence,
        }


class FileIngestionService:
    """Stores uploaded files locally, extracts text, and tracks file refs."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "review"
        self.file_root = self.root / "files"
        self.storage_root = self.root / "file-storage"
        self.segment_root = self.root / "file-segments"
        for path in (self.file_root, self.storage_root, self.segment_root):
            path.mkdir(parents=True, exist_ok=True)

    def import_bytes(
        self,
        *,
        profile_id: str = "default",
        filename: str,
        content_type: str = "",
        data: bytes,
        force_reimport: bool = False,
        pdf_text_extraction_enabled: bool = True,
    ) -> dict[str, Any]:
        safe_filename = self._sanitize_filename(filename)
        file_size = len(data)
        if file_size <= 0:
            raise ValueError("Uploaded file is empty.")
        if file_size > MAX_UPLOAD_BYTES:
            raise ValueError(f"Uploaded file exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB local limit.")

        normalized_profile = profile_id or "default"
        content_hash = sha256(data).hexdigest()
        existing = self.find_by_hash(content_hash, profile_id=normalized_profile)
        if existing is not None and not force_reimport:
            duplicate = self._duplicate_record(existing, safe_filename, content_type, file_size)
            self._persist_file(duplicate)
            return {
                "duplicate": True,
                "file": duplicate.as_dict(),
                "segments": self.list_segments(duplicate.file_id),
                "warnings": duplicate.warnings,
            }

        timestamp = _now()
        file_id = (
            _stable_id("file", normalized_profile, content_hash)
            if not force_reimport
            else _stable_id("file", normalized_profile, content_hash, timestamp)
        )
        storage_path = self.storage_root / f"{file_id}-{safe_filename}"
        storage_path.write_bytes(data)

        ingested = IngestedFile(
            file_id=file_id,
            profile_id=normalized_profile,
            filename=safe_filename,
            content_type=content_type or "application/octet-stream",
            file_size=file_size,
            content_hash=content_hash,
            imported_at=timestamp,
            storage_path=self._relative_path(storage_path),
            extraction_status="pending",
            extraction_error=None,
            page_count=None,
            source_type=self._source_type_for_filename(safe_filename),
        )
        self._persist_file(ingested)
        extracted = self.extract_file(file_id, pdf_text_extraction_enabled=pdf_text_extraction_enabled)
        extracted["duplicate"] = False
        return extracted

    def extract_file(self, file_id: str, *, pdf_text_extraction_enabled: bool = True) -> dict[str, Any]:
        ingested = self.require_file(file_id)
        if ingested.duplicate_of:
            return {
                "duplicate": True,
                "file": ingested.as_dict(),
                "segments": self.list_segments(file_id),
                "warnings": ingested.warnings,
            }

        if ingested.source_type == "unknown":
            ingested.extraction_status = "unsupported"
            ingested.extraction_error = f"Unsupported file type for {ingested.filename}."
            ingested.warnings = [ingested.extraction_error]
            self._persist_file(ingested)
            return {"duplicate": False, "file": ingested.as_dict(), "segments": [], "warnings": ingested.warnings}

        if not ingested.storage_path:
            ingested.extraction_status = "failed"
            ingested.extraction_error = "No stored file is available for extraction."
            ingested.warnings = [ingested.extraction_error]
            self._persist_file(ingested)
            return {"duplicate": False, "file": ingested.as_dict(), "segments": [], "warnings": ingested.warnings}

        path = self.repo_root / ingested.storage_path
        warnings: list[str] = []
        try:
            pages, page_count, warnings = self._extract_pages(path, ingested.filename, pdf_text_extraction_enabled)
            segments = self._segments_from_pages(ingested.file_id, pages)
        except Exception as exc:
            ingested.extraction_status = "failed"
            ingested.extraction_error = f"Extraction failed: {exc}"
            ingested.warnings = [ingested.extraction_error]
            self._persist_file(ingested)
            self._persist_segments(ingested.file_id, [])
            return {"duplicate": False, "file": ingested.as_dict(), "segments": [], "warnings": ingested.warnings}

        ingested.page_count = page_count
        ingested.source_refs = [segment.source_ref for segment in segments]
        if not segments:
            ingested.extraction_status = "extracted_no_text"
            ingested.extraction_error = "No extractable text was found. OCR is disabled by default."
            warnings.append(ingested.extraction_error)
        else:
            ingested.extraction_status = "extracted"
            ingested.extraction_error = None
        ingested.warnings = sorted(set(warnings))
        self._persist_file(ingested)
        self._persist_segments(ingested.file_id, segments)
        return {
            "duplicate": False,
            "file": ingested.as_dict(),
            "segments": [segment.as_dict() for segment in segments],
            "warnings": ingested.warnings,
        }

    def list_files(self, *, profile_id: str = "") -> list[dict[str, Any]]:
        files = [self._file_from_dict(json.loads(path.read_text(encoding="utf-8"))) for path in self.file_root.glob("*.json")]
        if profile_id:
            files = [item for item in files if item.profile_id in {profile_id, "default"}]
        files.sort(key=lambda item: item.imported_at, reverse=True)
        return [item.as_dict() for item in files]

    def get_file(self, file_id: str) -> dict[str, Any] | None:
        path = self.file_root / f"{file_id}.json"
        if not path.exists():
            return None
        return self._file_from_dict(json.loads(path.read_text(encoding="utf-8"))).as_dict()

    def require_file(self, file_id: str) -> IngestedFile:
        payload = self.get_file(file_id)
        if payload is None:
            raise KeyError(file_id)
        return self._file_from_dict(payload)

    def list_segments(self, file_id: str) -> list[dict[str, Any]]:
        ingested = self.require_file(file_id)
        if ingested.duplicate_of:
            return self.list_segments(ingested.duplicate_of)
        path = self.segment_root / f"{file_id}.json"
        if not path.exists():
            return []
        return [self._segment_from_dict(item).as_dict() for item in json.loads(path.read_text(encoding="utf-8"))]

    def combined_text(self, file_id: str) -> str:
        return "\n\n".join(segment["text"] for segment in self.list_segments(file_id) if segment.get("text"))

    def update_links(
        self,
        file_id: str,
        *,
        source_id: str | None = None,
        resource_id: str | None = None,
        dictionary_id: str | None = None,
        source_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        ingested = self.require_file(file_id)
        if source_id is not None:
            ingested.source_id = source_id
        if resource_id is not None:
            ingested.resource_id = resource_id
        if dictionary_id is not None:
            ingested.dictionary_id = dictionary_id
        if source_refs is not None:
            ingested.source_refs = list(dict.fromkeys(source_refs))
        self._persist_file(ingested)
        return ingested.as_dict()

    def find_by_hash(self, content_hash: str, *, profile_id: str = "") -> IngestedFile | None:
        for payload in self.list_files(profile_id=profile_id):
            item = self._file_from_dict(payload)
            if item.content_hash == content_hash and not item.duplicate_of:
                return item
        return None

    def _duplicate_record(
        self,
        existing: IngestedFile,
        filename: str,
        content_type: str,
        file_size: int,
    ) -> IngestedFile:
        imported_at = _now()
        return IngestedFile(
            file_id=_stable_id("filedup", existing.profile_id, existing.content_hash, filename, imported_at),
            profile_id=existing.profile_id,
            filename=filename,
            content_type=content_type or existing.content_type,
            file_size=file_size,
            content_hash=existing.content_hash,
            imported_at=imported_at,
            storage_path=existing.storage_path,
            extraction_status="duplicate",
            extraction_error=None,
            page_count=existing.page_count,
            source_type=existing.source_type,
            source_id=existing.source_id,
            resource_id=existing.resource_id,
            dictionary_id=existing.dictionary_id,
            source_refs=existing.source_refs,
            duplicate_of=existing.file_id,
            warnings=[f"Duplicate of file {existing.file_id}; no duplicate source/assets were created."],
        )

    def _extract_pages(
        self,
        path: Path,
        filename: str,
        pdf_text_extraction_enabled: bool,
    ) -> tuple[list[dict[str, Any]], int | None, list[str]]:
        suffix = Path(filename).suffix.lower()
        if suffix in {".txt", ".md", ".markdown", ".json", ".csv"}:
            return [{"page": 1, "text": self._decode_bytes(path.read_bytes())}], 1, []
        if suffix == ".pdf":
            if not pdf_text_extraction_enabled:
                raise ValueError("PDF text extraction is disabled by feature flag.")
            return self._extract_pdf_pages(path)
        raise ValueError(f"Unsupported file type {suffix or 'unknown'}.")

    @staticmethod
    def _extract_pdf_pages(path: Path) -> tuple[list[dict[str, Any]], int | None, list[str]]:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as exc:
                raise ValueError("Encrypted PDF cannot be extracted without a password.") from exc
        pages: list[dict[str, Any]] = []
        warnings: list[str] = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
                warnings.append(f"Page {index} could not be text-extracted.")
            pages.append({"page": index, "text": text})
        if pages and not any(page["text"].strip() for page in pages):
            warnings.append("PDF appears to have no extractable text; OCR is disabled.")
        return pages, len(reader.pages), warnings

    def _segments_from_pages(self, file_id: str, pages: list[dict[str, Any]]) -> list[ExtractedFileSegment]:
        segments: list[ExtractedFileSegment] = []
        for page in pages:
            page_number = int(page.get("page") or 1)
            page_text = str(page.get("text") or "").replace("\r\n", "\n").replace("\r", "\n")
            heading: str | None = None
            cursor = 0
            for chunk_heading, chunk in self._iter_page_chunks(page_text):
                if chunk_heading:
                    heading = chunk_heading
                if not chunk:
                    continue
                start = page_text.find(chunk, cursor)
                end: int | None
                if start < 0:
                    start = None  # type: ignore[assignment]
                    end = None
                else:
                    end = start + len(chunk)
                    cursor = end
                segment_index = len(segments) + 1
                source_ref = f"file:{file_id}:page:{page_number}:seg:{segment_index}"
                segments.append(
                    ExtractedFileSegment(
                        segment_id=f"file-segment-{file_id}-{segment_index}",
                        file_id=file_id,
                        page=page_number,
                        heading=heading,
                        text=chunk,
                        char_start=start,
                        char_end=end,
                        source_ref=source_ref,
                        evidence_type=self._evidence_type_from_text(chunk),
                        confidence=self._segment_confidence(chunk),
                    )
                )
        return segments

    def _iter_page_chunks(self, text: str) -> list[tuple[str | None, str]]:
        chunks: list[tuple[str | None, str]] = []
        for block in re.split(r"\n\s*\n+", text):
            cleaned = "\n".join(line.strip() for line in block.splitlines() if line.strip()).strip()
            if not cleaned:
                continue
            lines = cleaned.splitlines()
            heading: str | None = None
            if lines and self._looks_like_heading(lines[0]):
                heading = lines[0].lstrip("#").rstrip(":").strip()
                cleaned = "\n".join(lines[1:]).strip()
                if not cleaned:
                    chunks.append((heading, ""))
                    continue
            for chunk in self._split_long_chunk(cleaned):
                chunks.append((heading, chunk))
                heading = None
        return chunks

    @staticmethod
    def _split_long_chunk(text: str, limit: int = 900) -> list[str]:
        if len(text) <= limit:
            return [text]
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9#])", text)
        chunks: list[str] = []
        current = ""
        for part in parts:
            if not current:
                current = part
                continue
            if len(current) + 1 + len(part) <= limit:
                current = f"{current} {part}"
            else:
                chunks.append(current.strip())
                current = part
        if current.strip():
            chunks.append(current.strip())
        return chunks

    @staticmethod
    def _looks_like_heading(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if stripped.startswith("#"):
            return True
        if len(stripped) <= 90 and stripped.endswith(":"):
            return True
        if len(stripped) <= 80 and any(char.isalpha() for char in stripped) and stripped.upper() == stripped:
            return True
        return bool(re.match(r"^(LOS|Reading|Chapter|Section)\b", stripped, flags=re.IGNORECASE))

    @staticmethod
    def _evidence_type_from_text(text: str) -> str:
        lowered = text.lower()
        if "=" in text or any(token in lowered for token in (" formula", "wacc", "npv", "duration", "intrinsic value")):
            return "formula"
        if any(token in lowered for token in ("if ", "when ", "unless ", "only if", "not when")):
            return "boundary"
        if any(token in lowered for token in ("step", "press ", "calculate", "procedure")):
            return "procedure"
        if any(token in lowered for token in ("means", "is defined", "definition", "refers to")):
            return "definition"
        if any(token in lowered for token in ("example", "for instance")):
            return "example"
        if any(token in lowered for token in ("source:", "reading", "los:")):
            return "citation"
        return "other"

    @staticmethod
    def _segment_confidence(text: str) -> float:
        score = 0.45
        if len(text) >= 40:
            score += 0.12
        if any(token in text.lower() for token in ("source:", "los:", "reading", "chapter")):
            score += 0.12
        if "=" in text:
            score += 0.1
        if len(text) > 600:
            score -= 0.08
        return max(0.25, min(0.9, score))

    @staticmethod
    def _decode_bytes(data: bytes) -> str:
        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", errors="replace")

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        name = Path(filename or "upload").name
        name = re.sub(r"[^A-Za-z0-9._ -]+", "_", name).strip(" ._")
        name = re.sub(r"\s+", "_", name)
        return name[:160] or "upload"

    @staticmethod
    def _source_type_for_filename(filename: str) -> Any:
        suffix = Path(filename).suffix.lower()
        if suffix == ".pdf":
            return "pdf_note"
        if suffix in {".md", ".markdown"}:
            return "markdown_note"
        if suffix == ".txt":
            return "text_note"
        if suffix == ".json":
            return "json_dictionary"
        if suffix == ".csv":
            return "csv_dictionary"
        return "unknown"

    def _relative_path(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo_root.resolve()).as_posix()

    def _persist_file(self, ingested: IngestedFile) -> None:
        path = self.file_root / f"{ingested.file_id}.json"
        path.write_text(json.dumps(ingested.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _persist_segments(self, file_id: str, segments: list[ExtractedFileSegment]) -> None:
        path = self.segment_root / f"{file_id}.json"
        path.write_text(
            json.dumps([segment.as_dict() for segment in segments], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _file_from_dict(data: dict[str, Any]) -> IngestedFile:
        allowed = {field.name for field in fields(IngestedFile)}
        payload = {key: value for key, value in data.items() if key in allowed}
        if payload.get("extraction_status") not in FILE_STATUSES:
            payload["extraction_status"] = "failed"
        return IngestedFile(**payload)

    @staticmethod
    def _segment_from_dict(data: dict[str, Any]) -> ExtractedFileSegment:
        allowed = {field.name for field in fields(ExtractedFileSegment)}
        return ExtractedFileSegment(**{key: value for key, value in data.items() if key in allowed})
