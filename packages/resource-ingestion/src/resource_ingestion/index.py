from __future__ import annotations

from contextlib import closing
from datetime import UTC, datetime
from hashlib import sha256
import json
from pathlib import Path
import re
import sqlite3
from typing import Any

from resource_ingestion.models import ResourceDocument, ResourceSegment
from resource_ingestion.policy import can_retain_fulltext


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _segments(text: str) -> list[str]:
    chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n+", text) if chunk.strip()]
    return chunks or ([text.strip()] if text.strip() else [])


class ResourcePrivateIndex:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.private_root = root / ".system" / "private" / "resources"
        self.raw_root = self.private_root / "raw"
        self.manifest_root = self.private_root / "manifests"
        self.audit_root = self.private_root / "audits"
        self.db_path = self.private_root / "resource-index.sqlite3"
        for path in (self.raw_root, self.manifest_root, self.audit_root):
            path.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with closing(sqlite3.connect(self.db_path)) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    content_hash TEXT NOT NULL UNIQUE,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS resource_segments_fts USING fts5(
                    segment_id UNINDEXED,
                    document_id UNINDEXED,
                    lane UNINDEXED,
                    language UNINDEXED,
                    topic UNINDEXED,
                    title,
                    body
                )
                """
            )
            connection.commit()

    def ingest(
        self,
        *,
        lane: str,
        provider: str,
        url: str,
        title: str,
        text: str,
        license_mode: str,
        language: str = "",
        topic: str = "",
        answer_bearing: bool = False,
        metadata: dict[str, Any] | None = None,
        retrieved_at: str = "",
    ) -> dict[str, Any]:
        content_hash = sha256(text.encode("utf-8")).hexdigest() if text else sha256(f"{url}|{title}".encode("utf-8")).hexdigest()
        with closing(sqlite3.connect(self.db_path)) as connection:
            row = connection.execute("SELECT payload_json FROM documents WHERE content_hash = ?", (content_hash,)).fetchone()
        if row:
            manifest = json.loads(row[0])
            return {"duplicate": True, "document": manifest["document"], "segments": manifest["segments"]}

        document_id = _stable_id("resource", provider, url, content_hash)
        retain_fulltext = can_retain_fulltext(license_mode)
        content_ref = ""
        if retain_fulltext and text:
            raw_path = self.raw_root / f"{content_hash}.txt"
            raw_path.write_text(text, encoding="utf-8")
            content_ref = raw_path.relative_to(self.root).as_posix()
        document = ResourceDocument(
            document_id=document_id,
            lane=lane,
            provider=provider,
            url=url,
            title=title,
            content_hash=content_hash,
            license_mode=license_mode,
            content_ref=content_ref,
            excerpt=text.strip()[:280],
            retrieved_at=retrieved_at or _now(),
            language=language,
            topic=topic,
            answer_bearing=answer_bearing,
            metadata=dict(metadata or {}),
        )
        segments = [
            ResourceSegment(
                segment_id=_stable_id("resource-segment", document_id, str(index), body),
                document_id=document_id,
                locator=f"segment:{index + 1}",
                text_ref=f"{content_ref}#segment={index + 1}" if content_ref else "",
                excerpt=body[:280],
                language=language,
                topic=topic,
            )
            for index, body in enumerate(_segments(text) if retain_fulltext else [])
        ]
        manifest = {"document": document.as_dict(), "segments": [segment.as_dict() for segment in segments]}
        manifest_path = self.manifest_root / f"{document_id}.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with closing(sqlite3.connect(self.db_path)) as connection:
            connection.execute(
                "INSERT INTO documents (document_id, content_hash, payload_json) VALUES (?, ?, ?)",
                (document_id, content_hash, json.dumps(manifest, ensure_ascii=False)),
            )
            for segment, body in zip(segments, _segments(text), strict=False):
                connection.execute(
                    """
                    INSERT INTO resource_segments_fts
                    (segment_id, document_id, lane, language, topic, title, body)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (segment.segment_id, document_id, lane, language, topic, title, body),
                )
            connection.commit()
        return {"duplicate": False, **manifest}

    def documents(self) -> list[dict[str, Any]]:
        with closing(sqlite3.connect(self.db_path)) as connection:
            rows = connection.execute("SELECT payload_json FROM documents ORDER BY document_id").fetchall()
        return [json.loads(row[0])["document"] for row in rows]

    def search(self, query: str, *, lane: str = "", limit: int = 20) -> list[dict[str, Any]]:
        terms = re.findall(r"[\w-]+", query, flags=re.UNICODE)
        if not terms:
            return []
        statement = "SELECT segment_id, document_id, lane, language, topic, title, snippet(resource_segments_fts, 6, '<mark>', '</mark>', '...', 18) FROM resource_segments_fts WHERE resource_segments_fts MATCH ?"
        params: list[Any] = [" ".join(terms)]
        if lane:
            statement += " AND lane = ?"
            params.append(lane)
        statement += " LIMIT ?"
        params.append(max(1, min(limit, 100)))
        with closing(sqlite3.connect(self.db_path)) as connection:
            rows = connection.execute(statement, params).fetchall()
        return [
            {
                "segment_id": row[0],
                "document_id": row[1],
                "lane": row[2],
                "language": row[3],
                "topic": row[4],
                "title": row[5],
                "excerpt": row[6],
            }
            for row in rows
        ]

    def rebuild(self) -> dict[str, int]:
        with closing(sqlite3.connect(self.db_path)) as connection:
            connection.execute("DELETE FROM documents")
            connection.execute("DELETE FROM resource_segments_fts")
            connection.commit()
        document_count = 0
        segment_count = 0
        for path in sorted(self.manifest_root.glob("*.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            document = manifest["document"]
            text = ""
            if document.get("content_ref"):
                raw_path = self.root / document["content_ref"]
                if raw_path.exists():
                    text = raw_path.read_text(encoding="utf-8")
            segments = manifest.get("segments", [])
            with closing(sqlite3.connect(self.db_path)) as connection:
                connection.execute(
                    "INSERT OR REPLACE INTO documents (document_id, content_hash, payload_json) VALUES (?, ?, ?)",
                    (document["document_id"], document["content_hash"], json.dumps(manifest, ensure_ascii=False)),
                )
                for segment, body in zip(segments, _segments(text), strict=False):
                    connection.execute(
                        """
                        INSERT INTO resource_segments_fts
                        (segment_id, document_id, lane, language, topic, title, body)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            segment["segment_id"],
                            document["document_id"],
                            document["lane"],
                            segment.get("language", ""),
                            segment.get("topic", ""),
                            document["title"],
                            body,
                        ),
                    )
                connection.commit()
            document_count += 1
            segment_count += len(segments)
        return {"documents": document_count, "segments": segment_count}
