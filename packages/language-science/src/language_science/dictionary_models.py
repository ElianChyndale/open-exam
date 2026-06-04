from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from typing import Literal

from language_science.models import DictModel


@dataclass(slots=True)
class DictionarySource(DictModel):
    dictionary_id: str
    language_pair: str
    title: str
    format: str
    file_hash: str
    license_mode: str
    imported_at: str
    priority: int = 0
    profile_id: str = "default"
    dictionary_type: Literal[
        "english_english",
        "spanish_english",
        "english_spanish",
        "custom_bilingual",
        "custom_monolingual",
    ] = "custom_monolingual"
    source_language: str = ""
    target_language: str | None = None
    origin: Literal["manual", "import_text", "import_json", "import_csv", "file"] = "manual"
    content_hash: str = ""
    quality_score: float = 0.0
    quality_status: Literal["unscored", "low", "medium", "high", "trusted", "rejected"] = "unscored"
    validation_status: Literal["draft", "needs_review", "confirmed", "rejected"] = "draft"
    source_refs: list[str] = field(default_factory=list)
    quality_dimensions: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class BilingualMapping(DictModel):
    mapping_id: str
    target_lemma: str
    target_language: str
    sense_qualifier: str = ""
    confidence: float = 1.0
    verified: bool = False


@dataclass(slots=True)
class Sense(DictModel):
    sense_id: str
    definition: str
    examples: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    antonyms: list[str] = field(default_factory=list)
    register: str = ""
    domain: str = ""
    cefr_level: str = ""
    frequency_band: str = ""
    translations: list[BilingualMapping] = field(default_factory=list)


@dataclass(slots=True)
class LexicalEntry(DictModel):
    entry_id: str
    lemma: str
    pos: str
    language: str
    source_id: str
    etymology: str = ""
    pronunciation: str = ""
    audio_ref: str = ""
    inflections: list[str] = field(default_factory=list)
    gender: str = ""
    gender_invariable: bool = False
    senses: list[Sense] = field(default_factory=list)


@dataclass(slots=True)
class SpanishConjugation(DictModel):
    conjugation_id: str
    entry_id: str
    infinitive: str
    mood: str
    tense: str
    verb_forms: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SpanishNounForm(DictModel):
    form_id: str
    entry_id: str
    lemma: str
    number: str
    gender: str
    form: str
    definite_article: str = ""


@dataclass(slots=True)
class LexicalAsset(DictModel):
    lexical_id: str
    profile_id: str
    dictionary_id: str | None
    headword: str
    language: str
    target_language: str | None
    part_of_speech: str | None
    sense_number: int | None
    definition: str
    translation: str | None
    example_sentence: str | None
    example_translation: str | None
    collocations: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    antonyms: list[str] = field(default_factory=list)
    register: str | None = None
    usage_notes: list[str] = field(default_factory=list)
    morphology: dict[str, Any] = field(default_factory=dict)
    pronunciation: str | None = None
    tags: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    quality_score: float = 0.0
    validation_status: Literal["draft", "needs_review", "confirmed", "rejected"] = "draft"
    mastery_state: str = "new"
    next_review_at: str | None = None
    created_at: str = ""
    dictionary_quality_status: str = "unscored"


@dataclass(slots=True)
class LexicalReviewUnit(DictModel):
    unit_id: str
    session_id: str
    lexical_id: str
    display_mode: Literal[
        "definition_recall",
        "sense_selection",
        "translation_recall",
        "cloze_context",
        "collocation_check",
        "sentence_production",
        "synonym_boundary",
        "morphology_check",
    ]
    front_prompt: str
    correct_answer: str
    correct_reasoning: str
    example_sentence: str | None
    collocations: list[str]
    usage_notes: list[str]
    source_refs: list[str]
    memory_state_before: str | None
    headword: str = ""
    translation: str | None = None
    example_translation: str | None = None
    progress_index: int = 0


@dataclass(slots=True)
class LexicalReviewSession(DictModel):
    session_id: str
    profile_id: str
    status: Literal["active", "completed"] = "active"
    units: list[LexicalReviewUnit] = field(default_factory=list)
    current_unit_index: int = 0
    completed_unit_ids: list[str] = field(default_factory=list)
    outcomes: list[dict[str, Any]] = field(default_factory=list)
    started_at: str = ""
    completed_at: str | None = None


@dataclass(slots=True)
class LexicalMemoryState(DictModel):
    lexical_id: str
    mastery_state: str = "new"
    next_review_at: str | None = None
    last_reviewed_at: str | None = None
    lapse_count: int = 0
    recall_strength: float = 0.0
    production_strength: float = 0.0
    sense_confusion_count: int = 0
    collocation_confusion_count: int = 0
    weakness_tags: list[str] = field(default_factory=list)
