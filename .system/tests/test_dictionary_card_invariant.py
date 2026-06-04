from __future__ import annotations

import hashlib
import importlib

import pytest

from language_science.dictionary_models import BilingualMapping, LexicalEntry, Sense
from language_science import models as language_models


if not hasattr(language_models, "stable_id"):
    def _stable_id(*parts: str) -> str:
        data = "::".join(parts).encode("utf-8")
        return hashlib.sha1(data).hexdigest()[:16]

    language_models.stable_id = _stable_id

cards_v2 = importlib.import_module("language_science.cards_v2")
CardFactoryV2 = cards_v2.CardFactoryV2
CardInvariantError = cards_v2.CardInvariantError
CardV2 = cards_v2.CardV2


def test_card_v2_rejects_front_equal_answer() -> None:
    with pytest.raises(CardInvariantError, match="front == answer"):
        CardV2(
            card_id="card-1",
            card_type="definition_to_word",
            entry_id="entry-1",
            lemma="hola",
            language="es",
            front="Hola",
            answer="hola",
        )


def test_card_factory_v2_generates_non_degenerate_cards() -> None:
    entry = LexicalEntry(
        entry_id="entry-comer",
        lemma="comer",
        pos="verb",
        language="es",
        source_id="dict-es-en",
        senses=[
            Sense(
                sense_id="sense-1",
                definition="to eat",
                examples=["Yo como pan todos los dias.", "Nos gusta comer juntos."],
                synonyms=["to consume food"],
                cefr_level="A1",
                translations=[
                    BilingualMapping(
                        mapping_id="map-1",
                        target_lemma="eat",
                        target_language="en",
                    )
                ],
            )
        ],
        inflections=[{"yo": "como", "tú": "comes", "él/ella": "come"}],
    )

    cards = CardFactoryV2(native_language="en").create_cards(entry, source_id=entry.source_id)

    assert cards
    assert any(card.card_type == "definition_to_word" for card in cards)
    assert any(card.card_type == "reverse_translation" for card in cards)
    assert any(card.card_type == "spanish_conjugation" for card in cards)
    assert all(card.front.strip().lower() != card.answer.strip().lower() for card in cards)
