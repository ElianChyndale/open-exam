from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from hashlib import sha1
from typing import Any


def stable_id(prefix: str, *parts: str) -> str:
    raw = "::".join([prefix, *[str(part) for part in parts]])
    return f"{prefix}-{sha1(raw.encode('utf-8')).hexdigest()[:12]}"


class DictModel:
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class CardDimension(str, Enum):
    RECOGNITION = "recognition"
    PRODUCTION = "production"
    CLOZE = "cloze"
    DICTATION = "dictation"
    SHADOWING = "shadowing"
    GRAMMAR_PARSE = "grammar_parse"
    TRANSLATION_REVERSE = "translation_reverse"
    FREE_RECALL = "free_recall"
    CONTEXT = "context"


class CfaItemType(str, Enum):
    FORMULA = "cfa_formula"
    PROCEDURE = "cfa_procedure"
    CONCEPT = "cfa_concept"
    ETHICS = "cfa_ethics_standard"
    VIGNETTE = "cfa_vignette"


@dataclass(slots=True)
class LanguageProfile(DictModel):
    profile_id: str
    target_language: str
    native_language: str = "zh"
    level_target: str = "B2"
    focus_skills: list[str] = field(default_factory=lambda: ["reading", "listening", "speaking", "writing"])
    domains: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CorpusSource(DictModel):
    source_id: str
    source_type: str
    title: str
    language: str
    content_hash: str
    imported_at: str
    url: str = ""
    duration_seconds: int | None = None
    attachment_manifest: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CorpusSegment(DictModel):
    segment_id: str
    source_id: str
    text: str
    locator: str
    start_time: float | None = None
    end_time: float | None = None
    page_locator: str = ""
    previous_segment_id: str = ""
    next_segment_id: str = ""
    confidence: float = 1.0


@dataclass(slots=True)
class LanguageItem(DictModel):
    item_id: str
    item_type: str
    canonical_form: str
    surface_form: str
    language: str
    source_segment_ids: list[str]
    context_window: list[str]
    native_gloss: str = ""
    cefr_level: str = ""
    pos: str = ""
    tags: list[str] = field(default_factory=list)
    created_from: str = "manual"
    aliases: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LanguageCard(DictModel):
    card_id: str
    item_id: str
    card_type: str
    front_payload: dict[str, Any]
    back_payload: dict[str, Any]
    context_window: list[str]
    fsrs_state: dict[str, Any]
    due_at: str
    card_dimensions: list[str] = field(default_factory=lambda: ["recognition"])
    audio_ref: str = ""
    cloze_sentence: str = ""
    cloze_token: str = ""
    source_excerpt: str = ""


@dataclass(slots=True)
class GrammarAnalysis(DictModel):
    analysis_id: str
    segment_id: str
    language: str
    text_hash: str
    clauses: list[dict[str, Any]]
    phrases: list[str]
    collocations: list[str]
    cefr_level: str
    spanish_features: list[dict[str, Any]] = field(default_factory=list)
    notes: str = ""


@dataclass(slots=True)
class IntuitionEdge(DictModel):
    edge_id: str
    source_item_id: str
    target_item_id: str
    edge_type: str
    weight: float
    evidence_refs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LanguageSession(DictModel):
    session_id: str
    session_type: str
    language: str
    score: float
    output_gap: bool = False
    recognition_gap: bool = False
    evidence_refs: list[str] = field(default_factory=list)


DEFAULT_PROFILES = [
    LanguageProfile("en-general", "en", level_target="B2", domains=["daily", "academic"]),
    LanguageProfile("en-finance", "en", level_target="B2-C1", domains=["finance", "exam"]),
    LanguageProfile("es-general", "es", level_target="A1-B2", domains=["daily", "travel"]),
    LanguageProfile("es-business", "es", level_target="B1-B2", domains=["business", "work"]),
]
