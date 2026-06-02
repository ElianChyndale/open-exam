"""CFA-specific workflows: formula/procedure/concept items, exam-weight scheduling."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.cfa_storage import CfaRepository
from app.models import stable_id
from language_science.scheduler import FSRS6Scheduler


def _now() -> str:
    return datetime.now(UTC).isoformat()


# CFA Level I exam weights (2026)
EXAM_WEIGHTS = {
    "Ethical_and_Professional_Standards": 0.18,
    "Quantitative_Methods": 0.08,
    "Economics": 0.08,
    "Financial_Statement_Analysis": 0.13,
    "Corporate_Issuers": 0.08,
    "Equity": 0.11,
    "Fixed_Income": 0.11,
    "Derivatives": 0.07,
    "Alternative_Investments": 0.08,
    "Portfolio_Management": 0.08,
}


def create_cfa_item(repo: CfaRepository, *, item_type: str, canonical_form: str, topic: str, los: str = "", formula: str = "", variables: dict[str, str] | None = None) -> dict[str, Any]:
    item_id = stable_id("cfa-item", item_type, canonical_form, topic)
    item = {
        "item_id": item_id,
        "item_type": item_type,
        "canonical_form": canonical_form,
        "topic": topic,
        "los": los,
        "formula": formula,
        "variables": dict(variables or {}),
        "exam_weight": EXAM_WEIGHTS.get(topic, 0.08),
        "created_at": _now(),
    }
    repo.append("cfa.item.created", {"item": item})
    return item


def create_cfa_card(repo: CfaRepository, item: dict[str, Any], *, card_type: str = "cfa_calculation") -> dict[str, Any]:
    card_id = stable_id("cfa-card", item["item_id"], card_type)
    weight = item.get("exam_weight", 0.08)
    card = {
        "card_id": card_id,
        "item_id": item["item_id"],
        "card_type": card_type,
        "topic": item["topic"],
        "front_payload": {"prompt": item["canonical_form"], "card_type": card_type, "formula": item.get("formula", "")},
        "back_payload": {"answer": item["canonical_form"], "formula": item.get("formula", "")},
        "fsrs_state": {"state": "new", "repetitions": 0, "stability": 1.0, "difficulty": 5.0, "retrievability": 1.0},
        "exam_weight": weight,
        "due_at": _now(),
    }
    repo.append("cfa.card.created", {"card": card})
    return card


def review_cfa_card(repo: CfaRepository, card_id: str, rating: str) -> dict[str, Any]:
    from app.feature_flags import FeatureFlags
    card = repo.replay()["cards"].get(card_id)
    if card is None:
        raise KeyError(card_id)
    flags = FeatureFlags.load(repo.root)
    if flags.enabled("cfa_extensions_enabled"):
        events = repo.events()
        decision = FSRS6Scheduler.schedule(card.get("fsrs_state"), rating, _cache=None)
    else:
        from language_science.scheduler import _FallbackScheduler
        decision = _FallbackScheduler.schedule(card.get("fsrs_state"), rating)

    weight = card.get("exam_weight", 0.08)
    adjusted_difficulty = decision.difficulty * (1.0 - weight * 0.5)

    card = {
        **card,
        "fsrs_state": {**decision.as_dict(), "difficulty": round(adjusted_difficulty, 4)},
        "due_at": decision.next_due_at,
    }
    repo.append("cfa.review.completed", {"card": card, "rating": rating})
    return card


def due_cfa_cards(repo: CfaRepository) -> list[dict[str, Any]]:
    now = _now()
    cards = list(repo.replay()["cards"].values())
    return sorted(
        [c for c in cards if c["due_at"] <= now],
        key=lambda c: -(c.get("exam_weight", 0.08)),
    )
