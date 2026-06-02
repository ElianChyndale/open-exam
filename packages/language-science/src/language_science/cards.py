from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

from language_science.models import CardDimension, LanguageCard


def fuzzy_match(actual: str, expected: str, threshold: float = 0.8) -> float:
    a, b = actual.lower().strip(), expected.lower().strip()
    if a == b:
        return 1.0
    ratio = SequenceMatcher(None, a, b).ratio()
    a_tokens = set(re.findall(r"\w+", a))
    b_tokens = set(re.findall(r"\w+", b))
    if a_tokens and b_tokens:
        jaccard = len(a_tokens & b_tokens) / len(a_tokens | b_tokens)
        return max(ratio, jaccard * 0.9)
    return ratio


def _build_cloze(item: dict[str, Any]) -> tuple[str, str]:
    form = item.get("canonical_form", "")
    for ctx in item.get("context_window", []):
        if form.lower() in ctx.lower():
            pattern = re.compile(re.escape(form), re.IGNORECASE)
            cloze = pattern.sub("____", ctx, count=1)
            return cloze, form
    return f"____ (from: {form})", form


def _build_excerpt(item: dict[str, Any]) -> str:
    return " ".join(item.get("context_window", []))


class CardFactory:
    @staticmethod
    def create_card(item: dict[str, Any], card_type: str, *, fsrs_state: dict[str, Any] | None = None) -> LanguageCard:
        ctype = CardDimension(card_type) if card_type in CardDimension._value2member_map_ else CardDimension.RECOGNITION
        form = item.get("canonical_form", "")
        gloss = item.get("native_gloss", "")

        front_payload: dict[str, Any] = {"prompt": form, "card_type": ctype.value}
        back_payload: dict[str, Any] = {"answer": form, "gloss": gloss}
        cloze_sentence = ""
        cloze_token = ""
        source_excerpt = ""

        if ctype == CardDimension.CLOZE:
            cloze_sentence, cloze_token = _build_cloze(item)
            front_payload["prompt"] = cloze_sentence
            front_payload["cloze_token"] = cloze_token
            back_payload["answer"] = cloze_token
        elif ctype == CardDimension.PRODUCTION:
            front_payload = {"prompt": gloss or f"Translate: {form}", "card_type": "production"}
            back_payload = {"answer": form, "gloss": gloss}
        elif ctype == CardDimension.CONTEXT:
            source_excerpt = _build_excerpt(item)
            front_payload = {"prompt": f"Understand:\n{source_excerpt}", "card_type": "context"}
        elif ctype == CardDimension.DICTATION:
            front_payload = {"prompt": f"Type what you hear: '{form}'", "card_type": "dictation"}
        elif ctype == CardDimension.FREE_RECALL:
            context = _build_excerpt(item)
            front_payload = {"prompt": f"Recall:\n{context.replace(form, '______')}", "card_type": "free_recall"}

        return LanguageCard(
            card_id=f"lcard-{item['item_id']}-{ctype.value}",
            item_id=item["item_id"],
            card_type=ctype.value,
            card_dimensions=[ctype.value],
            front_payload=front_payload,
            back_payload=back_payload,
            context_window=item.get("context_window", []),
            fsrs_state=fsrs_state or {"state": "new", "repetitions": 0, "stability": 1.0, "difficulty": 5.0, "retrievability": 1.0},
            due_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            cloze_sentence=cloze_sentence,
            cloze_token=cloze_token,
            source_excerpt=source_excerpt,
            audio_ref=item.get("audio_ref", ""),
        )
