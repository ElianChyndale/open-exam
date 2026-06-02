from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from app.storage import Repository
from language_science.models import DEFAULT_PROFILES
from learning_records import EventEnvelopeV2


class LanguageRepository:
    def __init__(self, root: Path | Repository) -> None:
        self.repo = root if isinstance(root, Repository) else Repository(root)
        self.root = self.repo.root
        self.memory_root = self.repo.memory_root / "language"
        self.asset_root = self.repo.system_root / "private" / "language-assets"
        self.projection_root = self.repo.obsidian_root / "language"
        for path in (self.memory_root, self.asset_root, self.projection_root):
            path.mkdir(parents=True, exist_ok=True)

    def events(self) -> list[dict[str, Any]]:
        return self.repo.load_jsonl_events("language")

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
                source_layer="language",
                payload=payload,
                evidence_refs=evidence_refs,
                provenance={"subsystem": "LanguageOS"},
                consent_scope=consent_scope,
                idempotency_key=f"{event_type}:{json.dumps(payload, ensure_ascii=False, sort_keys=True)}",
            ).as_dict()
            for event_type, payload, evidence_refs, consent_scope in rows
        ]
        self.repo.append_jsonl_events("language", envelopes)
        self.project()
        return envelopes

    def replay(self) -> dict[str, Any]:
        state: dict[str, Any] = {
            "profiles": {profile.profile_id: profile.as_dict() for profile in DEFAULT_PROFILES},
            "active_profile_id": "en-general",
            "sources": {},
            "segments": {},
            "items": {},
            "cards": {},
            "grammar_analyses": {},
            "intuition_edges": [],
            "sessions": [],
            "transcription_requests": [],
            "exam_bridges": [],
        }
        for envelope in self.events():
            event_type = envelope.get("event_type")
            payload = deepcopy(envelope.get("payload", {}))
            if event_type == "language.profile.selected":
                state["active_profile_id"] = payload["profile_id"]
            elif event_type == "language.source.imported":
                source = payload["source"]
                state["sources"][source["source_id"]] = source
            elif event_type == "language.segment.created":
                segment = payload["segment"]
                state["segments"][segment["segment_id"]] = segment
            elif event_type == "language.item.collected":
                item = payload["item"]
                state["items"][item["item_id"]] = item
            elif event_type == "language.item.merged":
                item = state["items"].get(payload["item_id"])
                if item:
                    item["source_segment_ids"] = sorted(set(item["source_segment_ids"]) | set(payload.get("source_segment_ids", [])))
                    item["aliases"] = sorted(set(item.get("aliases", [])) | set(payload.get("aliases", [])))
            elif event_type in {"language.card.created", "language.review.completed"}:
                card = payload["card"]
                state["cards"][card["card_id"]] = card
            elif event_type in {"language.grammar.analyzed", "language.grammar.edited"}:
                analysis = payload["analysis"]
                state["grammar_analyses"][analysis["segment_id"]] = analysis
            elif event_type == "language.intuition.rebuilt":
                state["intuition_edges"] = payload["edges"]
            elif event_type == "language.session.completed":
                state["sessions"].append(payload["session"])
            elif event_type == "language.cloud_transcription.requested":
                state["transcription_requests"].append(payload)
            elif event_type == "exam.language_gap.detected":
                state["exam_bridges"].append(payload)
        return state

    def project(self) -> dict[str, Any]:
        state = self.replay()
        (self.memory_root / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lines = [
            "# LanguageOS",
            "",
            f"- Active profile: {state['active_profile_id']}",
            f"- Sources: {len(state['sources'])}",
            f"- Segments: {len(state['segments'])}",
            f"- Items: {len(state['items'])}",
            f"- Cards: {len(state['cards'])}",
            f"- Sessions: {len(state['sessions'])}",
        ]
        (self.projection_root / "LanguageOS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return state
