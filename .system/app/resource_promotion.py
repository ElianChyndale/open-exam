from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.resource_storage import ResourceRepository
from app.resource_workflows import load_resource_policy
from app.storage import Repository
from resource_ingestion.candidate_queue import ResourceCandidateQueue
from resource_ingestion.models import PromotionDecision
from resource_ingestion.policy import can_retain_fulltext
from resource_ingestion.quality import assess_document_quality


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _resources(repo: Repository | ResourceRepository) -> ResourceRepository:
    return repo if isinstance(repo, ResourceRepository) else ResourceRepository(repo)


def _queue(repo: Repository | ResourceRepository) -> ResourceCandidateQueue:
    return ResourceCandidateQueue(_resources(repo).root)


def _load_document_text(root: Path, document: dict[str, Any]) -> str:
    content_ref = str(document.get("content_ref", "")).strip()
    if not content_ref:
        return ""
    path = (root / content_ref).resolve()
    private_root = (root / ".system" / "private" / "resources").resolve()
    if private_root not in path.parents or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _promotion_target(document: dict[str, Any], policy: dict[str, Any]) -> str:
    if document.get("lane") == "language" and can_retain_fulltext(str(document.get("license_mode", ""))):
        return "language_private_corpus"
    official_providers = set(policy.get("cfa_official_structured_providers", []))
    if (
        document.get("lane") == "cfa"
        and document.get("provider") in official_providers
        and document.get("license_mode") == "official_structured"
    ):
        return "cfa_registry_fact"
    return "resource_reviewed_corpus"


def _evidence_refs(document: dict[str, Any]) -> list[str]:
    return [
        str(item)
        for item in [document.get("document_id", ""), document.get("content_hash", ""), document.get("url", "")]
        if str(item)
    ]


def queue_document_candidate(
    repo: Repository | ResourceRepository,
    *,
    document_id: str,
) -> dict[str, Any]:
    resources = _resources(repo)
    document = resources.replay()["documents"].get(document_id)
    if document is None:
        raise KeyError(document_id)
    full_text = _load_document_text(resources.root, document)
    assessment = assess_document_quality(document, full_text=full_text)
    return _queue(resources).enqueue(
        document=document,
        score=assessment.as_dict(),
        evidence_refs=_evidence_refs(document),
    )


def list_candidates(
    repo: Repository | ResourceRepository,
    *,
    status: str = "",
    lane: str = "",
) -> list[dict[str, Any]]:
    return _queue(repo).list(status=status, lane=lane)


def rescore_candidate(
    repo: Repository | ResourceRepository,
    *,
    candidate_id: str,
) -> dict[str, Any]:
    resources = _resources(repo)
    queue = _queue(resources)
    candidate = queue.get(candidate_id)
    if candidate is None:
        raise KeyError(candidate_id)
    document = resources.replay()["documents"].get(candidate["document_id"]) or candidate["document_snapshot"]
    assessment = assess_document_quality(document, full_text=_load_document_text(resources.root, document))
    return queue.rescore(candidate_id, assessment.as_dict())


def review_candidate(
    repo: Repository | ResourceRepository,
    *,
    candidate_id: str,
    action: str,
    review_note: str = "",
) -> dict[str, Any]:
    resources = _resources(repo)
    queue = _queue(resources)
    candidate = queue.get(candidate_id)
    if candidate is None:
        raise KeyError(candidate_id)
    if action not in {"approve", "reject"}:
        raise ValueError("Candidate action must be approve or reject.")
    document = resources.replay()["documents"].get(candidate["document_id"]) or candidate["document_snapshot"]
    policy = load_resource_policy(resources.root)
    target = _promotion_target(document, policy)
    promotion = PromotionDecision(
        promotion_id=stable_id("resource-promotion", str(candidate["document_id"]), target, action),
        lane=str(document.get("lane", "")),
        target=target,
        policy_version=str(policy.get("version", "resource-policy-v1")),
        confidence=float(candidate.get("score", {}).get("overall_score", 0.0)),
        evidence_refs=_evidence_refs(document),
        approved=action == "approve",
        revoked=False,
    ).as_dict()
    resources.append(
        "resource.promotion.decided",
        {"promotion": {**promotion, "decided_at": _now()}},
        evidence_refs=promotion["evidence_refs"],
    )
    reviewed = queue.review(
        candidate_id,
        status="approved" if action == "approve" else "rejected",
        review_note=review_note,
        promotion=promotion,
    )
    return {"candidate": reviewed, "promotion": promotion}
