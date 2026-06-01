from __future__ import annotations

from hashlib import sha1
import re
from typing import Any


FALSE_FRIENDS = {"actualmente": "actually", "embarazada": "embarrassed", "asistir": "assist"}


def _edge(source: str, target: str, edge_type: str, weight: float, evidence_refs: list[str]) -> dict[str, Any]:
    raw = f"{source}|{target}|{edge_type}"
    return {
        "edge_id": f"ledge-{sha1(raw.encode('utf-8')).hexdigest()[:12]}",
        "source_item_id": source,
        "target_item_id": target,
        "edge_type": edge_type,
        "weight": weight,
        "evidence_refs": evidence_refs,
    }


def build_edges(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for index, left in enumerate(items):
        canonical = left["canonical_form"].lower()
        if canonical in FALSE_FRIENDS:
            edges.append(_edge(left["item_id"], FALSE_FRIENDS[canonical], "false_friend", 1.0, left.get("source_segment_ids", [])))
        for right in items[index + 1:]:
            shared_segments = sorted(set(left.get("source_segment_ids", [])) & set(right.get("source_segment_ids", [])))
            left_tokens = set(re.findall(r"\w+", canonical))
            right_tokens = set(re.findall(r"\w+", right["canonical_form"].lower()))
            if shared_segments:
                edges.append(_edge(left["item_id"], right["item_id"], "co_occurrence", 0.8, shared_segments))
            elif left_tokens & right_tokens:
                edges.append(_edge(left["item_id"], right["item_id"], "translation_confusion", 0.5, []))
    return edges


def search_items(items: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    tokens = set(re.findall(r"\w+", query.lower()))
    scored = []
    for item in items:
        canonical = item["canonical_form"].lower()
        overlap = len(tokens & set(re.findall(r"\w+", canonical)))
        if query.lower() in canonical or overlap:
            scored.append({**item, "search_score": 1.0 if query.lower() in canonical else round(overlap / max(1, len(tokens)), 3)})
    return sorted(scored, key=lambda item: (-item["search_score"], item["canonical_form"]))
