from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from hashlib import sha1
import json
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    raw = "||".join(parts).encode("utf-8")
    return f"{prefix}-{sha1(raw, usedforsecurity=False).hexdigest()[:12]}"


@dataclass(frozen=True, slots=True)
class ResourceCandidate:
    candidate_id: str
    document_id: str
    lane: str
    provider: str
    url: str
    title: str
    status: str
    score: dict[str, Any]
    evidence_refs: list[str]
    created_at: str
    updated_at: str
    review_note: str = ""
    reviewed_at: str = ""
    promotion: dict[str, Any] = field(default_factory=dict)
    document_snapshot: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ResourceCandidateQueue:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.queue_root = root / ".system" / "memory" / "resources" / "candidate_queue"
        self.queue_root.mkdir(parents=True, exist_ok=True)
        self.events_path = self.queue_root / "events.jsonl"
        self.state_path = self.queue_root / "state.json"

    def _append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        envelope = {
            "event_id": _stable_id("resource-candidate-event", event_type, json.dumps(payload, ensure_ascii=False, sort_keys=True), _now()),
            "event_type": event_type,
            "occurred_at": _now(),
            "payload": payload,
        }
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(envelope, ensure_ascii=False) + "\n")
        self.project()
        return envelope

    def events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.events_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def replay(self) -> dict[str, dict[str, Any]]:
        state: dict[str, dict[str, Any]] = {}
        for event in self.events():
            payload = deepcopy(event.get("payload", {}))
            event_type = str(event.get("event_type", ""))
            if event_type == "resource.candidate.enqueued":
                item = payload["candidate"]
                state[item["candidate_id"]] = item
            elif event_type == "resource.candidate.rescored":
                candidate_id = str(payload["candidate_id"])
                current = state.get(candidate_id)
                if current is not None:
                    current["score"] = payload["score"]
                    current["updated_at"] = payload["updated_at"]
            elif event_type == "resource.candidate.reviewed":
                candidate_id = str(payload["candidate_id"])
                current = state.get(candidate_id)
                if current is not None:
                    current["status"] = payload["status"]
                    current["review_note"] = payload.get("review_note", "")
                    current["reviewed_at"] = payload["reviewed_at"]
                    current["updated_at"] = payload["reviewed_at"]
                    if payload.get("promotion"):
                        current["promotion"] = payload["promotion"]
        return state

    def project(self) -> dict[str, Any]:
        state = {"candidates": sorted(self.replay().values(), key=lambda item: item["updated_at"], reverse=True)}
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return state

    def enqueue(
        self,
        *,
        document: dict[str, Any],
        score: dict[str, Any],
        evidence_refs: list[str],
    ) -> dict[str, Any]:
        candidate_id = _stable_id("resource-candidate", str(document.get("document_id", "")))
        existing = self.replay().get(candidate_id)
        created_at = existing["created_at"] if existing is not None else _now()
        candidate = ResourceCandidate(
            candidate_id=candidate_id,
            document_id=str(document.get("document_id", "")),
            lane=str(document.get("lane", "")),
            provider=str(document.get("provider", "")),
            url=str(document.get("url", "")),
            title=str(document.get("title", "")),
            status="pending",
            score=score,
            evidence_refs=list(evidence_refs),
            created_at=created_at,
            updated_at=_now(),
            review_note="",
            reviewed_at="",
            promotion={},
            document_snapshot=deepcopy(document),
        ).as_dict()
        self._append("resource.candidate.enqueued", {"candidate": candidate})
        return candidate

    def list(self, *, status: str = "", lane: str = "") -> list[dict[str, Any]]:
        items = list(self.replay().values())
        if status:
            items = [item for item in items if item.get("status") == status]
        if lane:
            items = [item for item in items if item.get("lane") == lane]
        return sorted(items, key=lambda item: item.get("updated_at", ""), reverse=True)

    def get(self, candidate_id: str) -> dict[str, Any] | None:
        return self.replay().get(candidate_id)

    def rescore(self, candidate_id: str, score: dict[str, Any]) -> dict[str, Any]:
        current = self.get(candidate_id)
        if current is None:
            raise KeyError(candidate_id)
        updated_at = _now()
        self._append(
            "resource.candidate.rescored",
            {
                "candidate_id": candidate_id,
                "score": score,
                "updated_at": updated_at,
            },
        )
        refreshed = self.get(candidate_id)
        if refreshed is None:
            raise KeyError(candidate_id)
        return refreshed

    def review(
        self,
        candidate_id: str,
        *,
        status: str,
        review_note: str = "",
        promotion: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        current = self.get(candidate_id)
        if current is None:
            raise KeyError(candidate_id)
        if status not in {"approved", "rejected"}:
            raise ValueError("Candidate status must be approved or rejected.")
        reviewed_at = _now()
        self._append(
            "resource.candidate.reviewed",
            {
                "candidate_id": candidate_id,
                "status": status,
                "review_note": review_note,
                "reviewed_at": reviewed_at,
                "promotion": promotion or {},
            },
        )
        refreshed = self.get(candidate_id)
        if refreshed is None:
            raise KeyError(candidate_id)
        return refreshed
