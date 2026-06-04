from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from language_science.dictionary_models import LexicalEntry


class DictionaryIndex:
    """SQLite FTS5-backed index for lexical entries."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS dictionary_fts USING fts5(
                    lemma,
                    pos,
                    definition,
                    translation,
                    language,
                    source_id,
                    entry_json,
                    tokenize='porter unicode61'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS dictionary_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """
            )
            conn.commit()

    def bulk_insert(self, entries: list[LexicalEntry]) -> int:
        """Insert entries into FTS5. Returns count inserted."""
        with sqlite3.connect(self.db_path) as conn:
            count = 0
            for entry in entries:
                for sense in entry.senses:
                    translations = " ".join(
                        t.target_lemma for t in sense.translations
                    )
                    conn.execute(
                        """
                        INSERT INTO dictionary_fts(lemma, pos, definition, translation, language, source_id, entry_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            entry.lemma,
                            entry.pos,
                            sense.definition,
                            translations,
                            entry.language,
                            entry.source_id,
                            json.dumps(entry.as_dict(), ensure_ascii=False),
                        ),
                    )
                    count += 1
            conn.commit()
        return count

    def search(
        self,
        query: str,
        *,
        language: str = "",
        pos: str = "",
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Full-text search across lemma, definition, and translation."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if pos or language:
                conditions = []
                params: list[Any] = [query]
                if language:
                    conditions.append("language = ?")
                    params.append(language)
                if pos:
                    conditions.append("pos = ?")
                    params.append(pos)
                where = " AND ".join(conditions)
                sql = f"""
                    SELECT lemma, pos, definition, translation, language, source_id, entry_json, rank
                    FROM dictionary_fts
                    WHERE dictionary_fts MATCH ? AND {where}
                    ORDER BY rank
                    LIMIT ? OFFSET ?
                """
                params.extend([limit, offset])
            else:
                sql = """
                    SELECT lemma, pos, definition, translation, language, source_id, entry_json, rank
                    FROM dictionary_fts
                    WHERE dictionary_fts MATCH ?
                    ORDER BY rank
                    LIMIT ? OFFSET ?
                """
                params = [query, limit, offset]
            rows = conn.execute(sql, params).fetchall()
            return [dict(row) for row in rows]

    def lookup_lemma(self, lemma: str, language: str = "") -> list[dict[str, Any]]:
        """Exact lemma lookup with optional language filter."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if language:
                sql = """
                    SELECT lemma, pos, definition, translation, language, source_id, entry_json
                    FROM dictionary_fts
                    WHERE lemma = ? AND language = ?
                    ORDER BY rank
                """
                rows = conn.execute(sql, (lemma, language)).fetchall()
            else:
                sql = """
                    SELECT lemma, pos, definition, translation, language, source_id, entry_json
                    FROM dictionary_fts
                    WHERE lemma = ?
                    ORDER BY rank
                """
                rows = conn.execute(sql, (lemma,)).fetchall()
            return [dict(row) for row in rows]

    def count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM dictionary_fts").fetchone()
            return row[0] if row else 0

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM dictionary_fts")
            conn.commit()
