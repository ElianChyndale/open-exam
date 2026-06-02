from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ResourceSubscription:
    subscription_id: str
    lane: str
    provider: str
    target: str
    schedule: str
    budget: int
    enabled: bool
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ResourceDocument:
    document_id: str
    lane: str
    provider: str
    url: str
    title: str
    content_hash: str
    license_mode: str
    content_ref: str
    excerpt: str
    retrieved_at: str
    language: str = ""
    topic: str = ""
    answer_bearing: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ResourceSegment:
    segment_id: str
    document_id: str
    locator: str
    text_ref: str
    excerpt: str
    language: str = ""
    topic: str = ""
    confidence: float = 1.0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class IngestionJob:
    job_id: str
    trigger: str
    status: str
    budget_usage: int
    retry_state: dict[str, Any]
    audit_summary: dict[str, Any]
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PromotionDecision:
    promotion_id: str
    lane: str
    target: str
    policy_version: str
    confidence: float
    evidence_refs: list[str]
    approved: bool
    revoked: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AuditFinding:
    finding_id: str
    scope: str
    check_id: str
    severity: str
    evidence: list[str]
    remediation: str
    status: str = "open"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AIEnhancementRecord:
    enhancement_id: str
    provider: str
    model: str
    prompt_version: str
    input_hash: str
    output_hash: str
    citations: list[str]
    cost: float
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
