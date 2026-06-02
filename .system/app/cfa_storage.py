"""CFA event repository — exam-specific items, cards, and schedules."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from app.storage import Repository
from learning_records import EventEnvelopeV2


class CfaRepository:
    def __init__(self, root: Path | Repository) -> None:
        self.repo = root if isinstance(root, Repository) else Repository(root)
        self.root = self.repo.root

    def events(self) -> list[dict[str, Any]]:
        return self.repo.load_jsonl_events("cfa")

    def append(self, event_type: str, payload: dict[str, Any], *, evidence_refs: list[str] | None = None, consent_scope: list[str] | None = None) -> dict[str, Any]:
        return self.append_many([(event_type, payload, evidence_refs or [], consent_scope or ["local_storage"])])[0]

    def append_many(self, rows: list[tuple[str, dict[str, Any], list[str], list[str]]]) -> list[dict[str, Any]]:
        envelopes = [
            EventEnvelopeV2.create(
                event_type=event_type, source_layer="cfa",
                payload=payload, evidence_refs=evidence_refs,
                provenance={"subsystem": "CFA-OS"},
                consent_scope=consent_scope,
                idempotency_key=f"{event_type}:{__import__('json').dumps(payload, ensure_ascii=False, sort_keys=True)}",
            ).as_dict()
            for event_type, payload, evidence_refs, consent_scope in rows
        ]
        self.repo.append_jsonl_events("cfa", envelopes)
        return envelopes

    def replay(self) -> dict[str, Any]:
        state: dict[str, Any] = {"items": {}, "cards": {}, "exam_profile": None, "mock_sessions": []}
        for envelope in self.events():
            payload = deepcopy(envelope.get("payload", {}))
            event_type = envelope.get("event_type")
            if event_type == "cfa.item.created":
                state["items"][payload["item"]["item_id"]] = payload["item"]
            elif event_type in {"cfa.card.created", "cfa.review.completed"}:
                state["cards"][payload["card"]["card_id"]] = payload["card"]
            elif event_type == "cfa.exam_profile.updated":
                state["exam_profile"] = payload
            elif event_type == "cfa.mock.completed":
                state["mock_sessions"].append(payload)
        return state
