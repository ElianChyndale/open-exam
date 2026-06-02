from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path
from time import monotonic
from typing import Any, Iterable

import yaml

from app.models import MistakeCard, MistakeEvent, PatternInsight, StrategyRule, ValidationRule, stable_id


MISTAKE_EVENT_LAYERS = ("question", "bias", "agent")
EVENT_CACHE_TTL_SECONDS = 60.0


def _parse_frontmatter_block(text: str) -> tuple[dict[str, Any], str, str]:
    """Parse YAML frontmatter from markdown text.

    Returns (frontmatter_dict, body_text, trailing_newline).
    Returns ({}, text, "") if no valid frontmatter found.
    """
    if not text.startswith("---"):
        return {}, text, ""
    end_index = text.find("---", 3)
    if end_index == -1:
        return {}, text, ""
    frontmatter_raw = text[3:end_index].strip()
    body = text[end_index + 3:]
    trailing_newline = "\n" if text.endswith("\n") else ""
    try:
        fm = yaml.safe_load(frontmatter_raw) or {}
        if not isinstance(fm, dict):
            return {}, text, ""
        return fm, body, trailing_newline
    except yaml.YAMLError:
        return {}, text, ""


def _set_frontmatter_value(text: str, key: str, value: object) -> str:
    fm, body, trailing_newline = _parse_frontmatter_block(text)
    if not fm:
        return text
    fm[key] = value
    frontmatter_out = yaml.dump(
        fm,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    ).strip()
    return f"---\n{frontmatter_out}\n---{body}{trailing_newline}"


class Repository:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.system_root = root / ".system"
        self.events_root = self.system_root / "events"
        self.memory_root = self.system_root / "memory"
        self.vault_root = root / "CFA_tier1"
        self.obsidian_root = self.vault_root / "dashboard"
        self.obsidian_config_root = root / ".obsidian"
        self.schedule_root = root / "schedule"
        self.skills_root = root / "skills"
        self.evals_root = self.system_root / "evals"
        self.catalog_path = self.events_root / "catalog.sqlite3"
        self._events_cache: tuple[float, tuple[tuple[str, int, int], ...], tuple[MistakeEvent, ...]] | None = None
        self.ensure_layout()

    def ensure_layout(self) -> None:
        directories = [
            self.events_root / "question",
            self.events_root / "bias",
            self.events_root / "agent",
            self.events_root / "attempt",
            self.events_root / "energy",
            self.events_root / "review",
            self.events_root / "todo",
            self.events_root / "language",
            self.events_root / "resource",
            self.memory_root / "question-errors",
            self.memory_root / "cognitive-bias",
            self.memory_root / "agent-failures",
            self.memory_root / "patterns",
            self.memory_root / "strategy",
            self.memory_root / "validation",
            self.memory_root / "progress",
            self.memory_root / "review" / "daily",
            self.memory_root / "todo" / "snapshots",
            self.memory_root / "language",
            self.memory_root / "resources",
            self.vault_root / "Alternative_Investments",
            self.vault_root / "Corporate_Issuers",
            self.vault_root / "Derivatives",
            self.vault_root / "Economics",
            self.vault_root / "Equity",
            self.vault_root / "Ethical_and_Professional_Standards",
            self.vault_root / "Financial_Statement_Analysis",
            self.vault_root / "Fixed_Income",
            self.vault_root / "Portfolio_Management",
            self.vault_root / "Quantitative_Methods",
            self.vault_root / "mock" / "AltInv",
            self.vault_root / "mock" / "CorpIss",
            self.vault_root / "mock" / "Derivatives",
            self.vault_root / "mock" / "Economics",
            self.vault_root / "mock" / "Equity",
            self.vault_root / "mock" / "Ethics",
            self.vault_root / "mock" / "FI",
            self.vault_root / "mock" / "FRA",
            self.vault_root / "mock" / "Portfolio",
            self.vault_root / "mock" / "Quant",
            self.obsidian_root,
            self.obsidian_config_root,
            self.schedule_root / "todo_archive",
            self.skills_root,
            self.evals_root / "results",
        ]
        for path in directories:
            path.mkdir(parents=True, exist_ok=True)

        self._initialize_catalog()

    def _initialize_catalog(self) -> None:
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS catalog_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS mistake_events (
                    event_id TEXT PRIMARY KEY,
                    source_layer TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    los TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    artifact_type TEXT NOT NULL,
                    path TEXT NOT NULL,
                    source_event_id TEXT
                )
                """
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO catalog_metadata (key, value)
                VALUES ('schema_version', '1')
                """
            )
            connection.commit()

    def event_log_path(self, source_layer: str) -> Path:
        return self.events_root / source_layer / f"{source_layer}-events.jsonl"

    def has_event(self, event_id: str | None) -> bool:
        """Check if an event already exists, using the SQLite catalog."""
        if not event_id:
            return False
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            row = connection.execute(
                "SELECT 1 FROM mistake_events WHERE event_id = ?", (event_id,)
            ).fetchone()
            return row is not None

    def append_event(self, event: MistakeEvent) -> None:
        # Replay guard at the storage layer (defense in depth)
        if event.event_id and self.has_event(event.event_id):
            return
        payload = event.as_dict()
        with self.event_log_path(event.source_layer).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._events_cache = None
        self._index_event(event)

    def _index_event(self, event: MistakeEvent) -> None:
        payload = event.as_dict()
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO mistake_events
                (event_id, source_layer, topic, los, error_type, created_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.source_layer,
                    event.topic,
                    event.los,
                    event.error_type,
                    event.created_at,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            connection.commit()

    def rebuild_catalog(self) -> dict[str, int]:
        """Rebuild the disposable SQLite query index from canonical JSONL streams."""
        self._initialize_catalog()
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            connection.execute("DELETE FROM mistake_events")
            connection.execute("DELETE FROM artifacts")
            connection.commit()

        events = self.load_events()
        for event in events:
            self._index_event(event)
        return {"mistake_events": len(events), "artifacts": 0}

    def migrate_catalog(self) -> dict[str, int]:
        """Apply local catalog schema migrations without changing canonical JSONL."""
        self._initialize_catalog()
        events = self.load_events()
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            indexed = connection.execute("SELECT COUNT(*) FROM mistake_events").fetchone()[0]
            if indexed != len(events):
                connection.execute("DELETE FROM mistake_events")
                connection.commit()
        if indexed != len(events):
            for event in events:
                self._index_event(event)
        return {"schema_version": 1, "mistake_events": len(events)}

    def load_events(self) -> list[MistakeEvent]:
        signature = self._event_log_signature()
        if self._events_cache:
            cached_at, cached_signature, cached_rows = self._events_cache
            if monotonic() - cached_at <= EVENT_CACHE_TTL_SECONDS and signature == cached_signature:
                return list(cached_rows)

        rows: list[MistakeEvent] = []
        for source_layer in MISTAKE_EVENT_LAYERS:
            log_path = self.event_log_path(source_layer)
            if not log_path.exists():
                continue
            for line in log_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(MistakeEvent.from_payload(json.loads(line)))
        sorted_rows = tuple(sorted(rows, key=lambda item: item.created_at))
        self._events_cache = (monotonic(), signature, sorted_rows)
        return list(sorted_rows)

    def _event_log_signature(self) -> tuple[tuple[str, int, int], ...]:
        signature = []
        for source_layer in MISTAKE_EVENT_LAYERS:
            path = self.event_log_path(source_layer)
            if path.exists():
                stat = path.stat()
                signature.append((source_layer, stat.st_mtime_ns, stat.st_size))
        return tuple(signature)

    def load_incorrect_question_events(self) -> list[MistakeEvent]:
        return [
            event
            for event in self.load_events()
            if event.source_layer == "question" and not event.is_correct
        ]

    def load_unified_events(self) -> dict[str, list]:
        return {
            "mistakes": self.load_events(),
            "attempts": self.load_attempt_records(),
        }

    def jsonl_event_path(self, stream: str) -> Path:
        return self.events_root / stream / f"{stream}-events.jsonl"

    def append_jsonl_event(self, stream: str, payload: dict[str, Any]) -> Path:
        return self.append_jsonl_events(stream, [payload])

    def append_jsonl_events(self, stream: str, payloads: Iterable[dict[str, Any]]) -> Path:
        """Append an idempotent event batch after scanning the stream once."""
        path = self.jsonl_event_path(stream)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = {
            json.loads(line).get("event_id")
            for line in (path.read_text(encoding="utf-8").splitlines() if path.exists() else [])
            if line.strip()
        }
        pending: list[dict[str, Any]] = []
        for payload in payloads:
            if "event_id" not in payload:
                content_fingerprint = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                payload["event_id"] = stable_id(stream, content_fingerprint)
            if payload.get("event_id") in existing:
                continue
            pending.append(payload)
            existing.add(payload.get("event_id"))
        with path.open("a", encoding="utf-8") as handle:
            for payload in pending:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return path

    def load_jsonl_events(self, stream: str) -> list[dict[str, Any]]:
        path = self.jsonl_event_path(stream)
        if not path.exists():
            return []

        rows: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def append_attempt_record(self, payload: dict[str, Any]) -> Path:
        return self.append_jsonl_event("attempt", payload)

    def load_attempt_records(self) -> list[dict[str, Any]]:
        return self.load_jsonl_events("attempt")

    def append_energy_event(self, payload: dict[str, Any]) -> Path:
        return self.append_jsonl_event("energy", payload)

    def load_energy_events(self) -> list[dict[str, Any]]:
        return self.load_jsonl_events("energy")

    def write_markdown(self, path: Path, body: str, artifact_type: str, artifact_id: str, source_event_id: str | None = None) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO artifacts (artifact_id, artifact_type, path, source_event_id)
                VALUES (?, ?, ?, ?)
                """,
                (artifact_id, artifact_type, str(path.relative_to(self.root)), source_event_id),
            )
            connection.commit()

    def save_card(self, domain: str, card: MistakeCard, source_event_id: str) -> Path:
        filename = f"{card.card_id}.md"
        path = self.memory_root / domain / filename
        extra_fields = []
        if domain == "cognitive-bias":
            extra_fields.append(f"bias_signal: {card.root_cause}")
        if card.question_source:
            extra_fields.append(f"question_source: {card.question_source}")
        if card.source_type:
            extra_fields.append(f"source_type: {card.source_type}")
        if card.evidence_assets:
            extra_fields.append(f"evidence_assets: {', '.join(card.evidence_assets)}")
        if card.moc_target:
            extra_fields.append(f"moc_target: {card.moc_target}")
        if card.question_format:
            extra_fields.append(f"question_format: {card.question_format}")
        lines = [
            "---",
            f"card_id: {card.card_id}",
            f"source_layer: {card.source_layer}",
            f"topic: {card.topic}",
            f"los: {card.los}",
            f"root_cause: {card.root_cause}",
            *extra_fields,
            f"fix_rule: {card.fix_rule}",
            f"next_drill: {card.next_drill}",
            f"review_due_at: {card.review_due_at}",
            "review_status: Not reviewed",
            f"spacing_interval_days: {card.spacing_interval_days}",
            f"spacing_priority: {card.spacing_priority}",
            f"previous_reviews: {card.previous_reviews}",
            f"last_reviewed_at: {card.last_reviewed_at}",
            f"exam_date: {card.exam_date}",
            f"spacing_reasoning: {card.spacing_reasoning}",
            f"confidence_before: {card.confidence_before}",
            f"linked_patterns: {', '.join(card.linked_patterns)}",
            f"correct_resolution: {card.correct_resolution}",
            "---",
            "",
            f"## Prompt\n{card.prompt_or_question}",
            "",
            f"## Wrong Output\n{card.wrong_choice_or_output}",
            "",
            "## Choices",
            *(card.choices or []),
            "",
            f"## Evidence\n{', '.join(card.evidence_refs)}",
        ]
        self.write_markdown(path, "\n".join(lines), "mistake_card", card.card_id, source_event_id)
        return path

    def update_card_review(self, domain: str, card_id: str, previous_reviews: int,
                            review_due_at: str, spacing_interval_days: int,
                            spacing_priority: int, last_reviewed_at: str = "",
                            spacing_reasoning: str = "", confidence_before: int = 0,
                            exam_date: str = "") -> Path:
        """Update a card's review metadata after a review session."""
        path = self.memory_root / domain / f"{card_id}.md"
        if not path.exists():
            raise FileNotFoundError(f"Card not found: {path}")

        text = path.read_text(encoding="utf-8")
        text = _set_frontmatter_value(text, "previous_reviews", previous_reviews)
        text = _set_frontmatter_value(text, "review_due_at", review_due_at)
        text = _set_frontmatter_value(text, "spacing_interval_days", spacing_interval_days)
        text = _set_frontmatter_value(text, "spacing_priority", spacing_priority)
        text = _set_frontmatter_value(text, "last_reviewed_at", last_reviewed_at)
        text = _set_frontmatter_value(text, "spacing_reasoning", spacing_reasoning)
        text = _set_frontmatter_value(text, "confidence_before", confidence_before)
        text = _set_frontmatter_value(text, "exam_date", exam_date)

        path.write_text(text, encoding="utf-8")
        return path

    def update_card_status(self, domain: str, card_id: str, status: str) -> Path:
        """Project the latest review exposure status into card frontmatter."""
        path = self.memory_root / domain / f"{card_id}.md"
        if not path.exists():
            raise FileNotFoundError(f"Card not found: {path}")

        text = path.read_text(encoding="utf-8")
        text = _set_frontmatter_value(text, "review_status", status)
        path.write_text(text, encoding="utf-8")
        return path

    def save_validation_rule(self, rule: ValidationRule, source_event_id: str) -> Path:
        path = self.memory_root / "validation" / f"{rule.rule_id}.md"
        lines = [
            "---",
            f"rule_id: {rule.rule_id}",
            f"trigger: {rule.trigger}",
            f"failure_message: {rule.failure_message}",
            f"expiry_date: {rule.expiry_date}",
            f"review_status: {rule.review_status}",
            f"last_reviewed_at: {rule.last_reviewed_at}",
            "---",
            "",
            "## Check Steps",
            *[f"- {step}" for step in rule.check_steps],
        ]
        self.write_markdown(path, "\n".join(lines), "validation_rule", rule.rule_id, source_event_id)
        return path

    def save_pattern(self, insight: PatternInsight) -> Path:
        path = self.memory_root / "patterns" / f"{insight.pattern_id}.md"
        lines = [
            "---",
            f"pattern_id: {insight.pattern_id}",
            f"pattern_key: {insight.pattern_key}",
            f"recurrence: {insight.recurrence}",
            f"severity: {insight.severity}",
            "---",
            "",
            f"affected_topics: {', '.join(insight.affected_topics)}",
            "",
            "## Recommended Intervention",
            insight.recommended_intervention,
        ]
        self.write_markdown(path, "\n".join(lines), "pattern_insight", insight.pattern_id)
        return path

    def save_strategy_rule(self, rule: StrategyRule) -> Path:
        path = self.memory_root / "strategy" / f"{rule.rule_id}.md"
        lines = [
            "---",
            f"rule_id: {rule.rule_id}",
            f"trigger: {rule.trigger}",
            f"decision: {rule.decision}",
            "---",
            "",
            "## Why It Works",
            rule.why_it_works,
        ]
        self.write_markdown(path, "\n".join(lines), "strategy_rule", rule.rule_id)
        return path

    def write_obsidian_page(self, name: str, lines: Iterable[str]) -> Path:
        path = self.obsidian_root / name
        self.write_markdown(path, "\n".join(lines).strip() + "\n", "obsidian_page", name)
        return path
