from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from hashlib import sha1
from typing import Any


def utc_now() -> datetime:
    return datetime.now(UTC)


def stable_id(prefix: str, *parts: str) -> str:
    raw = "||".join(parts).encode("utf-8")
    return f"{prefix}-{sha1(raw).hexdigest()[:12]}"


@dataclass(slots=True)
class MistakeEvent:
    source_layer: str
    topic: str
    los: str
    prompt_or_question: str
    wrong_choice_or_output: str
    correct_resolution: str
    error_type: str
    confidence: int
    time_spent: int
    evidence_refs: list[str]
    question_source: str = ""
    source_type: str = ""
    evidence_assets: list[str] = field(default_factory=list)
    moc_target: str = ""
    question_format: str = ""
    choices: list[str] = field(default_factory=list)
    event_id: str | None = None
    created_at: str = field(default_factory=lambda: utc_now().isoformat())

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "MistakeEvent":
        event = cls(**payload)
        if not event.event_id:
            event.event_id = stable_id(
                "evt",
                event.source_layer,
                event.topic,
                event.los,
                event.prompt_or_question,
                event.wrong_choice_or_output,
                ",".join(event.evidence_refs),
            )
        return event

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MistakeCard:
    card_id: str
    source_layer: str
    topic: str
    los: str
    root_cause: str
    fix_rule: str
    next_drill: str
    review_due_at: str
    linked_patterns: list[str]
    prompt_or_question: str
    wrong_choice_or_output: str
    correct_resolution: str
    evidence_refs: list[str]
    question_source: str
    source_type: str
    evidence_assets: list[str]
    moc_target: str
    question_format: str
    choices: list[str]

    @classmethod
    def from_event(cls, event: MistakeEvent, fix_rule: str, next_drill: str) -> "MistakeCard":
        days = 1 if event.confidence <= 1 else 3 if event.confidence <= 3 else 7
        return cls(
            card_id=stable_id("card", event.event_id or "", event.topic, event.los),
            source_layer=event.source_layer,
            topic=event.topic,
            los=event.los,
            root_cause=event.error_type,
            fix_rule=fix_rule,
            next_drill=next_drill,
            review_due_at=(utc_now() + timedelta(days=days)).date().isoformat(),
            linked_patterns=[],
            prompt_or_question=event.prompt_or_question,
            wrong_choice_or_output=event.wrong_choice_or_output,
            correct_resolution=event.correct_resolution,
            evidence_refs=event.evidence_refs,
            question_source=event.question_source,
            source_type=event.source_type,
            evidence_assets=event.evidence_assets,
            moc_target=event.moc_target,
            question_format=event.question_format,
            choices=event.choices,
        )


@dataclass(slots=True)
class PatternInsight:
    pattern_id: str
    pattern_key: str
    recurrence: int
    severity: str
    affected_topics: list[str]
    recommended_intervention: str


@dataclass(slots=True)
class StrategyRule:
    rule_id: str
    trigger: str
    decision: str
    why_it_works: str


@dataclass(slots=True)
class ValidationRule:
    rule_id: str
    trigger: str
    check_steps: list[str]
    failure_message: str
