from __future__ import annotations

import base64
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.storage import Repository
from learning_records import EventEnvelopeV2


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _append(repo: Repository, stream: str, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    envelope = EventEnvelopeV2.create(
        event_type=event_type,
        source_layer=stream,
        payload=payload,
        consent_scope=["local_storage"],
        idempotency_key=f"{event_type}:{json.dumps(payload, ensure_ascii=False, sort_keys=True)}",
    ).as_dict()
    repo.append_jsonl_event(stream, envelope)
    return envelope


def record_provenance(
    repo: Repository,
    *,
    entity_id: str,
    activity_type: str,
    evidence_refs: list[str] | None = None,
    agent_id: str = "local-openexam",
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "entity_id": entity_id,
        "activity_type": activity_type,
        "agent_id": agent_id,
        "evidence_refs": list(evidence_refs or []),
        "attributes": dict(attributes or {}),
    }
    return _append(repo, "provenance", "provenance.recorded", payload)["payload"]


def get_provenance(repo: Repository, entity_id: str) -> dict[str, Any]:
    for event in reversed(repo.load_jsonl_events("provenance")):
        payload = event.get("payload", {})
        if payload.get("entity_id") == entity_id:
            return payload
    raise KeyError(entity_id)


def record_consent(repo: Repository, *, provider: str, purpose: str, granted: bool) -> dict[str, Any]:
    return _append(
        repo,
        "consent",
        "consent.recorded",
        {"provider": provider, "purpose": purpose, "granted": bool(granted), "recorded_at": _now()},
    )["payload"]


def provider_is_allowed(repo: Repository, provider: str, purpose: str) -> bool:
    for event in reversed(repo.load_jsonl_events("consent")):
        payload = event.get("payload", {})
        if payload.get("provider") == provider and payload.get("purpose") == purpose:
            return bool(payload.get("granted"))
    return False


def _load_stream(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def export_privacy_bundle(repo: Repository) -> dict[str, Any]:
    streams: dict[str, list[dict[str, Any]]] = {}
    for directory in sorted(repo.events_root.iterdir()):
        if not directory.is_dir():
            continue
        path = directory / f"{directory.name}-events.jsonl"
        if path.exists():
            streams[directory.name] = _load_stream(path)
    private_resources = []
    private_root = repo.system_root / "private" / "resources"
    for path in sorted(private_root.glob("**/*")) if private_root.exists() else []:
        if not path.is_file():
            continue
        body = path.read_bytes()
        private_resources.append(
            {
                "path": path.relative_to(repo.root).as_posix(),
                "sha256": sha256(body).hexdigest(),
                "content_base64": base64.b64encode(body).decode("ascii"),
            }
        )
    return {
        "schema_version": 2,
        "exported_at": _now(),
        "learner_id": "local-default",
        "streams": streams,
        "private_resources": private_resources,
    }


def _privacy_files(repo: Repository) -> list[Path]:
    candidates = list(repo.events_root.glob("*/*-events.jsonl"))
    candidates.extend((repo.memory_root / "progress").glob("*.jsonl"))
    candidates.extend((repo.memory_root / "review").glob("**/*.json"))
    candidates.extend((repo.memory_root / "todo").glob("**/*.json"))
    candidates.extend((repo.memory_root / "resources").glob("**/*"))
    candidates.extend((repo.system_root / "private" / "resources").glob("**/*"))
    return sorted({path for path in candidates if path.is_file()})


def request_privacy_purge(repo: Repository) -> dict[str, Any]:
    manifest = [path.relative_to(repo.root).as_posix() for path in _privacy_files(repo)]
    issued_at = _now()
    token = stable_id("purge", issued_at, *manifest)
    request = {"confirmation_token": token, "issued_at": issued_at, "deletion_manifest": manifest}
    path = repo.system_root / "private" / "privacy-purge-request.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request


def confirm_privacy_purge(repo: Repository, confirmation_token: str) -> dict[str, Any]:
    request_path = repo.system_root / "private" / "privacy-purge-request.json"
    if not request_path.exists():
        raise ValueError("Privacy purge must be requested before confirmation.")
    request = json.loads(request_path.read_text(encoding="utf-8"))
    if confirmation_token != request["confirmation_token"]:
        raise ValueError("Invalid privacy purge confirmation token.")
    deleted: list[str] = []
    for relative in request["deletion_manifest"]:
        path = (repo.root / relative).resolve()
        if repo.root.resolve() not in path.parents:
            raise ValueError("Refusing to purge a path outside the repository.")
        if path.exists() and path.is_file():
            path.unlink()
            deleted.append(relative)
    request_path.unlink(missing_ok=True)
    return {"deleted_count": len(deleted), "deleted": deleted}


def build_xapi_statements(repo: Repository) -> list[dict[str, Any]]:
    statements = []
    for attempt in repo.load_attempt_records():
        attempt_id = str(attempt.get("attempt_id") or attempt.get("event_id") or "unknown")
        statements.append(
            {
                "actor": {"account": {"homePage": "https://openexam.local", "name": "local-default"}},
                "verb": {"id": "https://adlnet.gov/expapi/verbs/answered", "display": {"en-US": "answered"}},
                "object": {"id": f"https://openexam.local/attempts/{attempt_id}"},
                "result": {"success": bool(attempt.get("is_correct"))},
            }
        )
    return statements


@dataclass(slots=True)
class EvidenceClaim:
    claim_id: str
    text: str
    evidence_refs: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)


def ground_claim(claim: EvidenceClaim) -> dict[str, Any]:
    if not claim.evidence_refs:
        raise ValueError("Grounded claims require at least one evidence reference.")
    return {**asdict(claim), "grounded": True}


class ReadOnlyMCPAdapter:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def list_tools(self) -> list[str]:
        return ["find_evidence", "get_due_reviews", "trace_provenance"]

    def trace_provenance(self, entity_id: str) -> dict[str, Any]:
        return get_provenance(self.repo, entity_id)

    def find_evidence(self, evidence_ref: str) -> list[dict[str, Any]]:
        return [event.as_dict() for event in self.repo.load_events() if evidence_ref in event.evidence_refs]

    def get_due_reviews(self) -> list[dict[str, Any]]:
        from app.workflows import collect_due_card_items
        from datetime import date

        return collect_due_card_items(self.repo, date.today())


def compare_scheduler_variants(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total = max(1, len(attempts))
    accuracy = sum(1 for attempt in attempts if attempt.get("is_correct")) / total
    return [
        {"variant": "static-spacing", "predicted_retention": round(0.55 + accuracy * 0.25, 4)},
        {"variant": "half-life", "predicted_retention": round(0.6 + accuracy * 0.3, 4)},
    ]


def build_learner_twin(repo: Repository) -> dict[str, Any]:
    from learner_twin import LearnerTwin

    return LearnerTwin.from_attempts(repo.load_attempt_records()).as_dict()


def export_caliper_events(repo: Repository) -> dict[str, Any]:
    return {
        "sensor": "OpenExam",
        "sendTime": _now(),
        "data": [
            {"type": "AssessmentItemEvent", "action": "Completed", "object": {"id": attempt.get("attempt_id", "")}}
            for attempt in repo.load_attempt_records()
        ],
    }


def export_open_badge(name: str) -> dict[str, Any]:
    return {
        "@context": ["https://www.w3.org/ns/credentials/v2", "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json"],
        "type": ["VerifiableCredential", "OpenBadgeCredential"],
        "name": name,
        "issuer": {"id": "https://openexam.local"},
    }


def anonymized_cohort_view(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    accuracy = sum(1 for row in rows if row.get("is_correct")) / total if total else 0.0
    return {"learner_count": total, "accuracy": round(accuracy, 4), "privacy_mode": "aggregate-only"}


def signed_evidence_snapshot(repo: Repository) -> dict[str, Any]:
    exported = export_privacy_bundle(repo)
    canonical = json.dumps(exported, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {"algorithm": "sha256-local-snapshot", "digest": sha256(canonical).hexdigest(), "payload": exported}
