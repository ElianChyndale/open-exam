from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, cast

from app.storage import Repository
from learning_records import EventEnvelopeV2
from resource_ingestion.index import ResourcePrivateIndex


class ResourceRepository:
    """Event-backed ResourceOS state with a disposable private FTS5 index."""

    def __init__(self, root: Path | Repository) -> None:
        self.repo = root if isinstance(root, Repository) else Repository(root)
        self.root = self.repo.root
        self.memory_root = self.repo.memory_root / "resources"
        self.memory_root.mkdir(parents=True, exist_ok=True)
        self.index = ResourcePrivateIndex(self.root)

    def events(self) -> list[dict[str, Any]]:
        return cast(list[dict[str, Any]], self.repo.load_jsonl_events("resource"))

    def append(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        evidence_refs: list[str] | None = None,
        consent_scope: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.append_many([(event_type, payload, evidence_refs or [], consent_scope or ["local_storage"])])[0]

    def append_many(
        self,
        rows: list[tuple[str, dict[str, Any], list[str], list[str]]],
    ) -> list[dict[str, Any]]:
        envelopes = [
            EventEnvelopeV2.create(
                event_type=event_type,
                source_layer="resource",
                payload=payload,
                evidence_refs=evidence_refs,
                provenance={"subsystem": "ResourceOS"},
                consent_scope=consent_scope,
                idempotency_key=f"{event_type}:{json.dumps(payload, ensure_ascii=False, sort_keys=True)}",
            ).as_dict()
            for event_type, payload, evidence_refs, consent_scope in rows
        ]
        self.repo.append_jsonl_events("resource", envelopes)
        self.project()
        return envelopes

    def replay(self) -> dict[str, Any]:
        state: dict[str, Any] = {
            "subscriptions": {},
            "documents": {},
            "segments": {},
            "jobs": {},
            "promotions": {},
            "inbox": {},
            "audits": {},
            "ai_enhancements": {},
        }
        for envelope in self.events():
            payload = deepcopy(envelope.get("payload", {}))
            event_type = envelope.get("event_type")
            if event_type == "resource.subscription.created":
                subscription = payload["subscription"]
                state["subscriptions"][subscription["subscription_id"]] = subscription
            elif event_type == "resource.subscription.updated":
                subscription = payload["subscription"]
                state["subscriptions"][subscription["subscription_id"]] = subscription
            elif event_type == "resource.document.ingested":
                document = payload["document"]
                state["documents"][document["document_id"]] = document
                for segment in payload.get("segments", []):
                    state["segments"][segment["segment_id"]] = segment
            elif event_type == "resource.job.updated":
                job = payload["job"]
                state["jobs"][job["job_id"]] = job
            elif event_type in {"resource.promotion.decided", "resource.promotion.revoked"}:
                promotion = payload["promotion"]
                state["promotions"][promotion["promotion_id"]] = promotion
            elif event_type == "resource.inbox.queued":
                item = payload["item"]
                state["inbox"][item["inbox_id"]] = item
            elif event_type == "resource.inbox.resolved":
                state["inbox"].pop(payload["inbox_id"], None)
            elif event_type == "resource.audit.finding":
                finding = payload["finding"]
                state["audits"][finding["finding_id"]] = finding
            elif event_type == "resource.ai.enhanced":
                enhancement = payload["enhancement"]
                state["ai_enhancements"][enhancement["enhancement_id"]] = enhancement
        return state

    def project(self) -> dict[str, Any]:
        state = self.replay()
        (self.memory_root / "state.json").write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return state
