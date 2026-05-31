from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Protocol, runtime_checkable

from app.models import MistakeCard, MistakeEvent, PatternInsight, StrategyRule, ValidationRule, stable_id


MISTAKE_EVENT_LAYERS = ("question", "bias", "agent")
PLATFORM_STREAMS = (
    "profile",
    "task",
    "review",
    "practice",
    "mock-run",
    "coach",
    "graph-overlay",
)
CATALOG_SCHEMA_VERSION = 1


@runtime_checkable
class LearningRepository(Protocol):
    """Storage boundary shared by local and SaaS repository adapters."""

    root: Path

    def append_stream_event(
        self,
        stream: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        learner_id: str = "local",
        source_refs: list[str] | None = None,
    ) -> dict[str, Any]: ...

    def load_stream_events(self, stream: str) -> list[dict[str, Any]]: ...

    def latest_stream_payload(self, stream: str, event_type: str | None = None) -> dict[str, Any] | None: ...


class Repository:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.system_root = root / ".system"
        self.events_root = self.system_root / "events"
        self.memory_root = self.system_root / "memory"
        self.private_root = self.system_root / "private"
        self.vault_root = root / "CFA_tier1"
        self.obsidian_root = self.vault_root / "dashboard"
        self.obsidian_config_root = root / ".obsidian"
        self.schedule_root = root / "schedule"
        self.skills_root = root / "skills"
        self.evals_root = self.system_root / "evals"
        self.catalog_path = self.events_root / "catalog.sqlite3"
        self.ensure_layout()

    def ensure_layout(self) -> None:
        directories = [
            self.events_root / "question",
            self.events_root / "bias",
            self.events_root / "agent",
            self.events_root / "attempt",
            self.events_root / "energy",
            *[self.events_root / stream for stream in PLATFORM_STREAMS],
            self.private_root / "question-bank",
            self.memory_root / "question-errors",
            self.memory_root / "cognitive-bias",
            self.memory_root / "agent-failures",
            self.memory_root / "patterns",
            self.memory_root / "strategy",
            self.memory_root / "validation",
            self.memory_root / "progress",
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

        with closing(sqlite3.connect(self.catalog_path)) as connection:
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
                CREATE TABLE IF NOT EXISTS schema_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO schema_meta (key, value)
                VALUES ('catalog_schema_version', ?)
                """,
                (str(CATALOG_SCHEMA_VERSION),),
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS stream_events (
                    event_id TEXT PRIMARY KEY,
                    stream TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    learner_id TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_stream_events_lookup
                ON stream_events (stream, learner_id, occurred_at)
                """
            )
            connection.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS search_documents USING fts5(
                    document_id UNINDEXED,
                    kind,
                    title,
                    body,
                    source_ref UNINDEXED
                )
                """
            )
            connection.commit()

    def event_log_path(self, source_layer: str) -> Path:
        return self.events_root / source_layer / f"{source_layer}-events.jsonl"

    def append_event(self, event: MistakeEvent) -> None:
        payload = event.as_dict()
        with self.event_log_path(event.source_layer).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
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

    def load_events(self) -> list[MistakeEvent]:
        rows: list[MistakeEvent] = []
        for source_layer in MISTAKE_EVENT_LAYERS:
            log_path = self.event_log_path(source_layer)
            if not log_path.exists():
                continue
            for line in log_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(MistakeEvent.from_payload(json.loads(line)))
        return sorted(rows, key=lambda item: item.created_at)

    def jsonl_event_path(self, stream: str) -> Path:
        return self.events_root / stream / f"{stream}-events.jsonl"

    def append_jsonl_event(self, stream: str, payload: dict[str, Any]) -> Path:
        path = self.jsonl_event_path(stream)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
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

    def append_stream_event(
        self,
        stream: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        learner_id: str = "local",
        source_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        """Append a versioned platform event and update the rebuildable catalog."""
        if stream not in PLATFORM_STREAMS:
            raise ValueError(f"Unsupported platform stream: {stream}")
        occurred_at = datetime.now(UTC).isoformat()
        event_id = stable_id("stream", stream, event_type, learner_id, occurred_at)
        envelope = {
            "schema_version": CATALOG_SCHEMA_VERSION,
            "event_id": event_id,
            "event_type": event_type,
            "learner_id": learner_id,
            "occurred_at": occurred_at,
            "source_refs": source_refs or [],
            "payload": payload,
        }
        self.append_jsonl_event(stream, envelope)
        with closing(sqlite3.connect(self.catalog_path)) as connection:
            connection.execute(
                """
                INSERT INTO stream_events
                (event_id, stream, event_type, learner_id, occurred_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    stream,
                    event_type,
                    learner_id,
                    occurred_at,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            connection.commit()
        return envelope

    def load_stream_events(self, stream: str) -> list[dict[str, Any]]:
        if stream not in PLATFORM_STREAMS:
            raise ValueError(f"Unsupported platform stream: {stream}")
        return self.load_jsonl_events(stream)

    def latest_stream_payload(self, stream: str, event_type: str | None = None) -> dict[str, Any] | None:
        events = self.load_stream_events(stream)
        if event_type:
            events = [event for event in events if event.get("event_type") == event_type]
        return events[-1]["payload"] if events else None

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

    def save_validation_rule(self, rule: ValidationRule, source_event_id: str) -> Path:
        path = self.memory_root / "validation" / f"{rule.rule_id}.md"
        lines = [
            "---",
            f"rule_id: {rule.rule_id}",
            f"trigger: {rule.trigger}",
            f"failure_message: {rule.failure_message}",
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


class LocalRepository(Repository):
    """Filesystem-backed implementation used by the default local mode."""
