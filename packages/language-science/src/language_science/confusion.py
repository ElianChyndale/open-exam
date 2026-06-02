# packages/language-science/src/language_science/confusion.py

from __future__ import annotations

from typing import Any

from language_science.confusion_map import CONFUSION_MAP, lookup_confusions


def detect_term_confusion(item: dict[str, Any], existing_items: list[dict[str, Any]]) -> dict[str, Any]:
    """Detect if a new item is confusable with any existing item.

    Returns dict with:
      - confusable: bool
      - pairs: list of confusable pair dicts
      - strategy: how it was detected
    """
    form = item.get("canonical_form", "").lower().strip()
    domain = "cfa" if item.get("item_type", "").startswith("cfa_") else "language"

    # Strategy 1: Explicit lookup in confusion map
    explicit = lookup_confusions(form, domain=domain) if domain in ("cfa", "language") else []
    if explicit:
        return {"confusable": True, "pairs": explicit, "strategy": "explicit"}

    # Strategy 2: Token overlap with existing items (for detection within review session)
    form_tokens = set(form.split())
    token_overlaps = []
    for existing in existing_items:
        existing_form = existing.get("canonical_form", "").lower().strip()
        if existing_form == form:
            continue
        existing_tokens = set(existing_form.split())
        shared = form_tokens & existing_tokens
        if len(shared) >= 1 and len(shared) / max(len(form_tokens | existing_tokens), 1) > 0.3:
            token_overlaps.append({
                "pair_id": f"tokenconf-{existing.get('item_id', 'unknown')}",
                "term_a": form, "term_b": existing_form,
                "explanation": f"Shared tokens: {', '.join(shared)}",
                "detection_strategy": "token_overlap",
                "domain": domain,
            })
    if token_overlaps:
        return {"confusable": True, "pairs": token_overlaps, "strategy": "token_overlap"}

    return {"confusable": False, "pairs": [], "strategy": "none"}
