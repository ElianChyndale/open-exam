"""Card Factory v2 — dictionary-driven, invariant-enforced card generation.

Enforces front != answer for all card types. Uses LexicalEntry data to
produce rich, context-bearing cards instead of shallow word->definition
flashcards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from language_science.cefr import _cefr_allowed
from language_science.dictionary_models import LexicalEntry, Sense
from language_science.models import stable_id


class CardInvariantError(ValueError):
    """Raised when front would equal answer."""


@dataclass
class CardV2:
    card_id: str
    card_type: str
    entry_id: str
    lemma: str
    language: str
    front: str
    answer: str
    context: str = ""
    collocations: list[str] = field(default_factory=list)
    cefr_level: str = ""
    source_refs: list[str] = field(default_factory=list)
    audio_ref: str = ""
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.front.strip().lower() == self.answer.strip().lower():
            raise CardInvariantError(
                f"front == answer for card {self.card_id}: '{self.front}'"
            )


class CardFactoryV2:
    """Generate rich language cards from LexicalEntry data."""

    CARD_TYPES: list[str] = [
        "definition_to_word",
        "word_to_sense",
        "example_cloze",
        "collocation_completion",
        "reverse_translation",
        "spanish_gender",
        "spanish_conjugation",
        "false_friend_warning",
        "register_choice",
        "domain_usage",
    ]

    def __init__(
        self,
        native_language: str = "zh",
        cefr_min: str = "a1",
        cefr_max: str = "c2",
    ) -> None:
        self.native_language = native_language
        self.cefr_min = cefr_min
        self.cefr_max = cefr_max

    def create_cards(
        self,
        entry: LexicalEntry,
        source_id: str = "",
    ) -> list[CardV2]:
        """Generate all applicable card types for a lexical entry."""
        cards: list[CardV2] = []
        filtered_senses = [
            s for s in entry.senses
            if _cefr_allowed(s.cefr_level, self.cefr_min, self.cefr_max)
        ]
        if not filtered_senses:
            filtered_senses = entry.senses

        for card_type in self.CARD_TYPES:
            try:
                card = self._build_card(card_type, entry, filtered_senses, source_id)
                if card:
                    cards.append(card)
            except CardInvariantError:
                continue
        return cards

    def _build_card(
        self,
        card_type: str,
        entry: LexicalEntry,
        senses: list[Sense],
        source_id: str,
    ) -> CardV2 | None:
        builders: dict[str, callable] = {
            "definition_to_word": self._build_definition_to_word,
            "word_to_sense": self._build_word_to_sense,
            "example_cloze": self._build_example_cloze,
            "collocation_completion": self._build_collocation_completion,
            "reverse_translation": self._build_reverse_translation,
            "spanish_gender": self._build_spanish_gender,
            "spanish_conjugation": self._build_spanish_conjugation,
            "false_friend_warning": self._build_false_friend_warning,
            "register_choice": self._build_register_choice,
            "domain_usage": self._build_domain_usage,
        }
        builder = builders.get(card_type)
        if not builder:
            return None
        return builder(entry, senses, source_id)

    def _build_definition_to_word(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        if not senses:
            return None
        sense = senses[0]
        front = f"Definition: {sense.definition}"
        answer = entry.lemma
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "def2word"),
            card_type="definition_to_word",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            context=sense.examples[0] if sense.examples else "",
            collocations=sense.synonyms[:3],
            cefr_level=sense.cefr_level,
            source_refs=[source_id],
            tags=["definition", entry.pos],
        )

    def _build_word_to_sense(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        if not senses:
            return None
        sense = senses[0]
        context = sense.examples[0] if sense.examples else ""
        front = f"Word: {entry.lemma}\nContext: {context}"
        answer = f"{sense.definition}\n" + (
            f"Collocations: {', '.join(sense.synonyms[:3])}" if sense.synonyms else ""
        )
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "word2sense"),
            card_type="word_to_sense",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            context=context,
            collocations=sense.synonyms[:3],
            cefr_level=sense.cefr_level,
            source_refs=[source_id],
            tags=["sense", entry.pos],
        )

    def _build_example_cloze(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        for sense in senses:
            for ex in sense.examples:
                if entry.lemma.lower() in ex.lower():
                    cloze = ex.replace(entry.lemma, "_____", 1)
                    if cloze == ex:
                        continue
                    return CardV2(
                        card_id=stable_id("cv2", entry.entry_id, "cloze", ex[:20]),
                        card_type="example_cloze",
                        entry_id=entry.entry_id,
                        lemma=entry.lemma,
                        language=entry.language,
                        front=cloze,
                        answer=entry.lemma,
                        context=ex,
                        cefr_level=sense.cefr_level,
                        source_refs=[source_id],
                        tags=["cloze", entry.pos],
                    )
        return None

    def _build_collocation_completion(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        for sense in senses:
            for col in sense.synonyms:
                if entry.lemma.lower() not in col.lower():
                    parts = col.split()
                    if len(parts) >= 2:
                        missing = parts[0] if parts[0] != entry.lemma else parts[-1]
                        prompt = col.replace(missing, "_____", 1)
                        if prompt != col:
                            return CardV2(
                                card_id=stable_id("cv2", entry.entry_id, "coll", col[:20]),
                                card_type="collocation_completion",
                                entry_id=entry.entry_id,
                                lemma=entry.lemma,
                                language=entry.language,
                                front=f"Complete: {prompt}",
                                answer=missing,
                                context=col,
                                cefr_level=sense.cefr_level,
                                source_refs=[source_id],
                                tags=["collocation", entry.pos],
                            )
        return None

    def _build_reverse_translation(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        if not senses:
            return None
        sense = senses[0]
        translations = [
            t.target_lemma for t in sense.translations
            if t.target_lemma and t.target_lemma != entry.lemma
        ]
        if not translations:
            return None
        front = f"Translate to {entry.language}: {translations[0]}"
        answer = entry.lemma
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "revtrans"),
            card_type="reverse_translation",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            context=sense.examples[0] if sense.examples else "",
            cefr_level=sense.cefr_level,
            source_refs=[source_id],
            tags=["translation", entry.pos],
        )

    def _build_spanish_gender(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        if entry.language != "es" or entry.pos != "noun":
            return None
        if not entry.gender:
            return None
        article = "el" if entry.gender == "masculine" else "la"
        front = f"Spanish noun: {entry.lemma}"
        answer = f"{article} {entry.lemma}"
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "gender"),
            card_type="spanish_gender",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            cefr_level=senses[0].cefr_level if senses else "",
            source_refs=[source_id],
            tags=["gender", "spanish"],
        )

    def _build_spanish_conjugation(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        if entry.language != "es" or entry.pos != "verb":
            return None
        if not entry.inflections:
            return None
        front = f"Conjugate: {entry.lemma} (present indicative, yo)"
        # Try to find yo form in inflections
        yo_form = ""
        for inf in entry.inflections:
            if isinstance(inf, dict):
                yo_form = inf.get("yo", "")
            elif isinstance(inf, str) and "yo:" in inf:
                yo_form = inf.split("yo:", 1)[-1].strip()
        if not yo_form:
            yo_form = entry.inflections[0] if entry.inflections else ""
        answer = yo_form or f"(yo form of {entry.lemma})"
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "conj"),
            card_type="spanish_conjugation",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            cefr_level=senses[0].cefr_level if senses else "",
            source_refs=[source_id],
            tags=["conjugation", "spanish"],
        )

    def _build_false_friend_warning(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        from language_science.false_friends import FALSE_FRIENDS
        pair = FALSE_FRIENDS.get(entry.lemma.lower())
        if not pair:
            return None
        front = f"False friend — choose the right meaning:\n{entry.lemma}"
        answer = f"{pair['correct']}\nNot: {pair['wrong']}\nNote: {pair['note']}"
        return CardV2(
            card_id=stable_id("cv2", entry.entry_id, "ff"),
            card_type="false_friend_warning",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            language=entry.language,
            front=front,
            answer=answer,
            cefr_level=senses[0].cefr_level if senses else "",
            source_refs=[source_id],
            tags=["false_friend", entry.language],
        )

    def _build_register_choice(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        for sense in senses:
            if sense.register:
                context = sense.examples[0] if sense.examples else ""
                front = f"Context: {context}\nWhich register fits?"
                answer = sense.register
                return CardV2(
                    card_id=stable_id("cv2", entry.entry_id, "reg"),
                    card_type="register_choice",
                    entry_id=entry.entry_id,
                    lemma=entry.lemma,
                    language=entry.language,
                    front=front,
                    answer=answer,
                    context=context,
                    cefr_level=sense.cefr_level,
                    source_refs=[source_id],
                    tags=["register", entry.pos],
                )
        return None

    def _build_domain_usage(
        self, entry: LexicalEntry, senses: list[Sense], source_id: str
    ) -> CardV2 | None:
        for sense in senses:
            if sense.domain:
                context = sense.examples[0] if sense.examples else ""
                front = f"Domain: {sense.domain}\nWord: {entry.lemma}\nWhat does it mean here?"
                answer = sense.definition
                return CardV2(
                    card_id=stable_id("cv2", entry.entry_id, "domain"),
                    card_type="domain_usage",
                    entry_id=entry.entry_id,
                    lemma=entry.lemma,
                    language=entry.language,
                    front=front,
                    answer=answer,
                    context=context,
                    cefr_level=sense.cefr_level,
                    source_refs=[source_id],
                    tags=["domain", entry.pos, sense.domain],
                )
        return None
