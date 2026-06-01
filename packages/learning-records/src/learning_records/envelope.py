from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from hashlib import sha1
import json
from typing import Any


def _stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(slots=True)
class EventEnvelopeV2:
    event_id: str
    schema_version: int
    event_type: str
    learner_id: str
    occurred_at: str
    source_layer: str
    payload: dict[str, Any]
    evidence_refs: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    consent_scope: list[str] = field(default_factory=list)
    idempotency_key: str = ""

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        source_layer: str,
        payload: dict[str, Any],
        learner_id: str = "local-default",
        evidence_refs: list[str] | None = None,
        provenance: dict[str, Any] | None = None,
        consent_scope: list[str] | None = None,
        idempotency_key: str = "",
        occurred_at: str | None = None,
    ) -> EventEnvelopeV2:
        fingerprint = {
            "event_type": event_type,
            "idempotency_key": idempotency_key,
            "learner_id": learner_id,
            "payload": payload,
            "source_layer": source_layer,
        }
        digest = sha1(_stable_json(fingerprint).encode("utf-8")).hexdigest()[:20]
        return cls(
            event_id=f"evt2-{digest}",
            schema_version=2,
            event_type=event_type,
            learner_id=learner_id,
            occurred_at=occurred_at or datetime.now(UTC).isoformat(),
            source_layer=source_layer,
            payload=payload,
            evidence_refs=list(evidence_refs or []),
            provenance=dict(provenance or {}),
            consent_scope=list(consent_scope or []),
            idempotency_key=idempotency_key,
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> EventEnvelopeV2:
        return cls(**payload)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
