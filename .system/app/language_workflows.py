from __future__ import annotations

import base64
import csv
from datetime import UTC, datetime
from hashlib import sha256
from io import StringIO
from pathlib import Path
from typing import Any

from app.feature_flags import FeatureFlags
from app.language_storage import LanguageRepository
from app.models import stable_id
from language_science.grammar import analyze_sentence
from language_science.importers import segment_content
from language_science.intuition_graph import build_edges, search_items
from language_science.scheduler import FSRS6Scheduler
from language_science.fsrs_cache import FSRSStateCache


_FSRS_CACHE = FSRSStateCache(maxsize=256)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def list_profiles(repo: LanguageRepository) -> list[dict[str, Any]]:
    return list(repo.replay()["profiles"].values())


def select_profile(repo: LanguageRepository, profile_id: str) -> dict[str, Any]:
    state = repo.replay()
    if profile_id not in state["profiles"]:
        raise KeyError(profile_id)
    repo.append("language.profile.selected", {"profile_id": profile_id})
    return state["profiles"][profile_id]


def _safe_attachment(repo: LanguageRepository, attachment_name: str, content: str) -> dict[str, Any]:
    filename = Path(attachment_name or "audio-asset.bin").name
    digest = sha256(content.encode("utf-8")).hexdigest()
    path = repo.asset_root / f"{digest[:12]}-{filename}"
    try:
        body = base64.b64decode(content, validate=True)
    except ValueError:
        body = content.encode("utf-8")
    path.write_bytes(body)
    return {"stored_locally": True, "path": path.relative_to(repo.root).as_posix(), "sha256": digest, "filename": filename}


def import_source(
    repo: LanguageRepository,
    *,
    source_type: str,
    title: str,
    language: str,
    content: str = "",
    url: str = "",
    import_format: str = "",
    attachment_name: str = "",
) -> dict[str, Any]:
    content_hash = sha256(f"{source_type}|{language}|{url}|{content}".encode("utf-8")).hexdigest()
    state = repo.replay()
    existing = next((source for source in state["sources"].values() if source["content_hash"] == content_hash), None)
    if existing:
        repo.append("language.source.duplicate_detected", {"source_id": existing["source_id"], "content_hash": content_hash})
        segments = [segment for segment in state["segments"].values() if segment["source_id"] == existing["source_id"]]
        return {"duplicate": True, "source": existing, "segments": segments}

    source_id = stable_id("lsource", content_hash)
    attachment_manifest = _safe_attachment(repo, attachment_name, content) if source_type == "audio" or import_format == "audio" else {}
    source = {
        "source_id": source_id,
        "source_type": source_type,
        "title": title,
        "language": language,
        "content_hash": content_hash,
        "imported_at": _now(),
        "url": url,
        "duration_seconds": None,
        "attachment_manifest": attachment_manifest,
    }
    raw_segments = segment_content(content, import_format or source_type)
    segment_ids = [stable_id("lseg", source_id, str(index), segment["locator"], segment["text"]) for index, segment in enumerate(raw_segments)]
    segments = []
    for index, raw in enumerate(raw_segments):
        segment = {
            "segment_id": segment_ids[index],
            "source_id": source_id,
            "text": raw["text"],
            "locator": raw["locator"],
            "start_time": raw.get("start_time"),
            "end_time": raw.get("end_time"),
            "page_locator": raw.get("page_locator", ""),
            "previous_segment_id": segment_ids[index - 1] if index else "",
            "next_segment_id": segment_ids[index + 1] if index + 1 < len(segment_ids) else "",
            "confidence": 1.0,
        }
        segments.append(segment)
    rows = [
        ("language.source.imported", {"source": source}, [content_hash], ["local_storage"]),
        *[
            ("language.segment.created", {"segment": segment}, [source_id, content_hash], ["local_storage"])
            for segment in segments
        ],
    ]
    repo.append_many(rows)
    return {"duplicate": False, "source": source, "segments": segments}


def create_segment(repo: LanguageRepository, *, source_id: str, text: str, locator: str, **extra: Any) -> dict[str, Any]:
    if source_id not in repo.replay()["sources"]:
        raise KeyError(source_id)
    segment = {
        "segment_id": stable_id("lseg", source_id, locator, text),
        "source_id": source_id,
        "text": text,
        "locator": locator,
        "start_time": extra.get("start_time"),
        "end_time": extra.get("end_time"),
        "page_locator": extra.get("page_locator", ""),
        "previous_segment_id": extra.get("previous_segment_id", ""),
        "next_segment_id": extra.get("next_segment_id", ""),
        "confidence": float(extra.get("confidence", 1.0)),
    }
    repo.append("language.segment.created", {"segment": segment}, evidence_refs=[source_id])
    return segment


def collect_item(
    repo: LanguageRepository,
    *,
    item_type: str,
    canonical_form: str,
    language: str,
    segment_id: str,
    surface_form: str = "",
    native_gloss: str = "",
    tags: list[str] | None = None,
    created_from: str = "manual",
) -> dict[str, Any]:
    state = repo.replay()
    segment = state["segments"].get(segment_id)
    if segment is None:
        raise KeyError(segment_id)
    normalized = canonical_form.strip().lower()
    existing = next(
        (item for item in state["items"].values() if item["language"] == language and item["item_type"] == item_type and item["canonical_form"].lower() == normalized),
        None,
    )
    if existing:
        repo.append(
            "language.item.merged",
            {"item_id": existing["item_id"], "source_segment_ids": [segment_id], "aliases": [surface_form or canonical_form]},
            evidence_refs=[segment_id],
        )
        return {"merged": True, "item": repo.replay()["items"][existing["item_id"]]}
    context_ids = [segment.get("previous_segment_id"), segment_id, segment.get("next_segment_id")]
    context_window = [state["segments"][item_id]["text"] for item_id in context_ids if item_id and item_id in state["segments"]]
    item = {
        "item_id": stable_id("litem", language, item_type, normalized),
        "item_type": item_type,
        "canonical_form": canonical_form.strip(),
        "surface_form": surface_form or canonical_form.strip(),
        "language": language,
        "source_segment_ids": [segment_id],
        "context_window": context_window,
        "native_gloss": native_gloss,
        "cefr_level": "",
        "pos": "",
        "tags": list(tags or []),
        "created_from": created_from,
        "aliases": [],
    }
    repo.append("language.item.collected", {"item": item}, evidence_refs=[segment["source_id"], segment_id])
    return {"merged": False, "item": item}


def _infer_pos(item: dict[str, Any], flags: FeatureFlags) -> str:
    if item.get("pos"):
        return str(item["pos"]).strip().lower()
    canonical = str(item.get("canonical_form", "")).strip().lower()
    if item.get("language") == "es" and flags.enabled("spanish_morphology_engine"):
        if canonical.endswith(("ar", "er", "ir")):
            return "verb"
        if " " not in canonical and canonical:
            return "noun"
    return "phrase" if " " in canonical else "word"


def _infer_cefr(item: dict[str, Any], context_text: str) -> str:
    cefr_level = str(item.get("cefr_level", "")).strip()
    if cefr_level:
        return cefr_level.upper()
    try:
        from language_science.cefr import CEFR_NUMERIC

        token_count = max(len(context_text.split()), len(str(item.get("canonical_form", "")).split()))
        if token_count <= 2:
            candidate = "A1"
        elif token_count <= 5:
            candidate = "A2"
        elif token_count <= 10:
            candidate = "B1"
        else:
            candidate = "B2"
        return candidate if candidate.lower() in CEFR_NUMERIC else ""
    except Exception:
        return ""


def _build_dictionary_entry(item: dict[str, Any], flags: FeatureFlags) -> Any:
    from language_science.dictionary_models import BilingualMapping, LexicalEntry, Sense

    canonical = str(item["canonical_form"]).strip()
    context_window = [str(part).strip() for part in item.get("context_window", []) if str(part).strip()]
    context_text = context_window[0] if context_window else canonical
    native_gloss = str(item.get("native_gloss", "")).strip()
    pos = _infer_pos(item, flags)
    cefr_level = _infer_cefr(item, context_text)
    translations = []
    if native_gloss and native_gloss.lower() != canonical.lower():
        translations.append(
            BilingualMapping(
                mapping_id=stable_id("lmap", item["item_id"], native_gloss.lower()),
                target_lemma=native_gloss,
                target_language="en" if item.get("language") != "en" else "zh",
                verified=False,
            )
        )
    sense = Sense(
        sense_id=stable_id("lsense", item["item_id"], "primary"),
        definition=native_gloss or f"Meaning of '{canonical}' in context",
        examples=context_window[:2] or [canonical],
        synonyms=context_window[1:2],
        cefr_level=cefr_level,
        translations=translations,
    )
    inflections: list[Any] = []
    gender = ""
    if item.get("language") == "es" and flags.enabled("spanish_morphology_engine"):
        from language_science.spanish_morphology import conjugate, detect_gender

        if pos == "verb":
            inflections.append(conjugate(canonical, mood="indicative", tense="present").forms)
        elif pos == "noun":
            agreement = detect_gender(canonical)
            gender = agreement.gender
    return LexicalEntry(
        entry_id=stable_id("lentry", item["item_id"]),
        lemma=canonical,
        pos=pos,
        language=str(item.get("language", "")).strip(),
        source_id=item["item_id"],
        inflections=inflections,
        gender=gender,
        senses=[sense],
    )


def _legacy_prompt_from_v2(card_type: str, v2_card: Any, item: dict[str, Any]) -> str:
    prompt = str(v2_card.front).strip()
    answer = str(v2_card.answer).strip()
    if prompt.lower() != answer.lower():
        return prompt
    fallback_parts = [
        f"Recall the meaning and usage of: {item['canonical_form']}",
        str(item.get("native_gloss", "")).strip(),
        str(v2_card.context).strip(),
    ]
    return next((part for part in fallback_parts if part and part.lower() != answer.lower()), item["canonical_form"])


def _create_cards_v2(repo: LanguageRepository, item: dict[str, Any], requested_types: list[str]) -> list[dict[str, Any]]:
    from language_science import models as language_models

    if not hasattr(language_models, "stable_id"):
        language_models.stable_id = stable_id
    from language_science.cards_v2 import CardFactoryV2
    entry = _build_dictionary_entry(item, FeatureFlags.load(repo.root))
    v2_cards = CardFactoryV2(native_language="en").create_cards(entry, source_id=item["item_id"])
    if not v2_cards:
        return []

    preferred_types: dict[str, list[str]] = {
        "recognition": ["definition_to_word", "reverse_translation", "word_to_sense"],
        "production": ["reverse_translation", "word_to_sense", "definition_to_word"],
        "cloze": ["example_cloze", "collocation_completion", "word_to_sense"],
    }
    by_type = {card.card_type: card for card in v2_cards}
    cards = []
    for requested_type in requested_types:
        selected = next((by_type[name] for name in preferred_types.get(requested_type, []) if name in by_type), None)
        if selected is None:
            selected = next(iter(v2_cards), None)
        if selected is None:
            continue
        prompt = _legacy_prompt_from_v2(requested_type, selected, item)
        answer = str(selected.answer).strip() or str(item["canonical_form"]).strip()
        if prompt.strip().lower() == answer.strip().lower():
            continue
        card_id = stable_id("lcard", item["item_id"], requested_type)
        cards.append({
            "card_id": card_id,
            "item_id": item["item_id"],
            "card_type": requested_type,
            "front_payload": {
                "prompt": prompt,
                "card_type": requested_type,
                "source_card_type": selected.card_type,
                "lemma": selected.lemma,
                "context": selected.context,
                "cefr_level": selected.cefr_level,
                "tags": selected.tags,
            },
            "back_payload": {
                "answer": answer,
                "gloss": str(item.get("native_gloss", "")).strip(),
                "collocations": selected.collocations,
            },
            "audio_ref": selected.audio_ref,
            "context_window": item["context_window"],
            "fsrs_state": {"state": "new", "repetitions": 0, "stability": 1.0, "difficulty": 5.0, "retrievability": 1.0},
            "due_at": _now(),
        })
    return cards


def generate_cards(repo: LanguageRepository, item_id: str, *, card_types: list[str] | None = None) -> list[dict[str, Any]]:
    state = repo.replay()
    item = state["items"].get(item_id)
    if item is None:
        raise KeyError(item_id)
    selected = card_types or ["recognition", "production", "cloze"]
    flags = FeatureFlags.load(repo.root)
    if flags.enabled("language_cards_v2"):
        cards = []
        generated = {card["card_id"]: card for card in _create_cards_v2(repo, item, selected)}
        for card_type in selected:
            card_id = stable_id("lcard", item_id, card_type)
            existing = state["cards"].get(card_id)
            if existing:
                cards.append(existing)
                continue
            card = generated.get(card_id)
            if card is None:
                continue
            repo.append("language.card.created", {"card": card}, evidence_refs=item["source_segment_ids"])
            cards.append(card)
        if cards:
            return cards
    cards = []
    for card_type in selected:
        card_id = stable_id("lcard", item_id, card_type)
        existing = state["cards"].get(card_id)
        if existing:
            cards.append(existing)
            continue
        card = {
            "card_id": card_id,
            "item_id": item_id,
            "card_type": card_type,
            "front_payload": {"prompt": item["canonical_form"], "card_type": card_type},
            "back_payload": {"answer": item["canonical_form"], "gloss": item.get("native_gloss", "")},
            "audio_ref": "",
            "context_window": item["context_window"],
            "fsrs_state": {"state": "new", "repetitions": 0, "stability": 1.0, "difficulty": 5.0, "retrievability": 1.0},
            "due_at": _now(),
        }
        repo.append("language.card.created", {"card": card}, evidence_refs=item["source_segment_ids"])
        cards.append(card)
    return cards


def generate_multidim_cards(
    repo: LanguageRepository,
    item_id: str,
    *,
    card_dimensions: list[str] | None = None,
) -> list[dict[str, Any]]:
    from language_science.cards import CardFactory
    state = repo.replay()
    item = state["items"].get(item_id)
    if item is None:
        raise KeyError(item_id)
    selected = card_dimensions or ["recognition", "production", "cloze"]
    cards = []
    for ctype in selected:
        card = CardFactory.create_card(item, ctype)
        existing = state["cards"].get(card.card_id)
        if existing:
            cards.append(existing)
            continue
        repo.append("language.card.created", {"card": card.as_dict()}, evidence_refs=item["source_segment_ids"])
        cards.append(card.as_dict())
    return cards


def due_cards(repo: LanguageRepository) -> list[dict[str, Any]]:
    now = _now()
    return [card for card in repo.replay()["cards"].values() if card["due_at"] <= now]


def review_card(repo: LanguageRepository, card_id: str, rating: str) -> dict[str, Any]:
    from app.feature_flags import FeatureFlags

    card = repo.replay()["cards"].get(card_id)
    if card is None:
        raise KeyError(card_id)

    flags = FeatureFlags.load(repo.root)
    if flags.enabled("language_fsrs_v2_enabled"):
        events = repo.events()
        decision = FSRS6Scheduler.schedule(
            card.get("fsrs_state"), rating,
            _cache=_FSRS_CACHE,
        )
    else:
        from language_science.scheduler import _FallbackScheduler
        decision = _FallbackScheduler.schedule(card.get("fsrs_state"), rating)

    card = {**card, "fsrs_state": decision.as_dict(), "due_at": decision.next_due_at}
    _FSRS_CACHE.invalidate(card_id)
    repo.append("language.review.completed", {"card": card, "rating": rating}, evidence_refs=[card_id])
    return card


def analyze_grammar(repo: LanguageRepository, segment_id: str) -> dict[str, Any]:
    state = repo.replay()
    segment = state["segments"].get(segment_id)
    if segment is None:
        raise KeyError(segment_id)
    source = state["sources"][segment["source_id"]]
    result = analyze_sentence(segment["text"], source["language"])
    existing = state["grammar_analyses"].get(segment_id)
    if existing and existing["text_hash"] == result["text_hash"]:
        return {**existing, "cache_hit": True}
    analysis = {
        "analysis_id": stable_id("lanalysis", segment_id, result["text_hash"]),
        "segment_id": segment_id,
        "language": source["language"],
        **result,
        "notes": "",
    }
    repo.append("language.grammar.analyzed", {"analysis": analysis}, evidence_refs=[segment_id])
    return {**analysis, "cache_hit": False}


def edit_grammar(repo: LanguageRepository, segment_id: str, patch: dict[str, Any]) -> dict[str, Any]:
    analysis = repo.replay()["grammar_analyses"].get(segment_id)
    if analysis is None:
        analysis = analyze_grammar(repo, segment_id)
    edited = {**analysis, **patch}
    edited.pop("cache_hit", None)
    repo.append("language.grammar.edited", {"analysis": edited}, evidence_refs=[segment_id])
    return edited


def rebuild_intuition_graph(repo: LanguageRepository) -> list[dict[str, Any]]:
    edges = build_edges(list(repo.replay()["items"].values()))
    repo.append("language.intuition.rebuilt", {"edges": edges})
    return edges


def search_intuition(repo: LanguageRepository, query: str) -> list[dict[str, Any]]:
    return search_items(list(repo.replay()["items"].values()), query)


def record_session(repo: LanguageRepository, *, session_type: str, language: str, score: float, output_gap: bool = False, recognition_gap: bool = False) -> dict[str, Any]:
    session = {
        "session_id": stable_id("lsession", session_type, language, _now()),
        "session_type": session_type,
        "language": language,
        "score": max(0.0, min(1.0, float(score))),
        "output_gap": bool(output_gap),
        "recognition_gap": bool(recognition_gap),
        "evidence_refs": [],
    }
    repo.append("language.session.completed", {"session": session})
    return session


def record_exam_language_bridge(repo: LanguageRepository, *, bridge_type: str, text: str, evidence_refs: list[str] | None = None) -> dict[str, Any]:
    payload = {
        "bridge_id": stable_id("lbridge", bridge_type, text),
        "bridge_type": bridge_type,
        "text": text,
        "evidence_refs": list(evidence_refs or []),
    }
    repo.append("exam.language_gap.detected", payload, evidence_refs=payload["evidence_refs"])
    return payload


def request_transcription(repo: LanguageRepository, source_id: str, *, provider: str, feature_enabled: bool) -> dict[str, Any]:
    from app.roadmap_waves import provider_is_allowed

    source = repo.replay()["sources"].get(source_id)
    if source is None:
        raise KeyError(source_id)
    if not source.get("attachment_manifest", {}).get("stored_locally"):
        raise ValueError("Audio must be stored locally before transcription.")
    if not feature_enabled or not provider_is_allowed(repo.repo, provider, "language_cloud_transcription"):
        raise PermissionError("Cloud transcription requires feature enablement and recorded consent.")
    payload = {"source_id": source_id, "provider": provider, "requested_at": _now()}
    repo.append("language.cloud_transcription.requested", payload, evidence_refs=[source_id], consent_scope=["local_storage", "language_cloud_transcription"])
    return payload


def language_stats(repo: LanguageRepository) -> dict[str, Any]:
    state = repo.replay()
    return {
        "active_profile_id": state["active_profile_id"],
        "source_count": len(state["sources"]),
        "segment_count": len(state["segments"]),
        "item_count": len(state["items"]),
        "card_count": len(state["cards"]),
        "due_count": len(due_cards(repo)),
        "session_count": len(state["sessions"]),
        "output_gap_count": sum(1 for session in state["sessions"] if session.get("output_gap")),
        "recognition_gap_count": sum(1 for session in state["sessions"] if session.get("recognition_gap")),
        "exam_bridge_count": len(state["exam_bridges"]),
    }


def export_language(repo: LanguageRepository, format_: str) -> dict[str, Any]:
    state = repo.replay()
    items = list(state["items"].values())
    if format_ in {"markdown", "obsidian"}:
        lines = ["# LanguageOS Export", "", *[f"- **{item['canonical_form']}** ({item['item_type']})" for item in items]]
        content = "\n".join(lines) + "\n"
    elif format_ in {"csv", "anki"}:
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["item_id", "item_type", "canonical_form", "language", "native_gloss"])
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in writer.fieldnames} for item in items)
        content = buffer.getvalue()
    else:
        raise ValueError(f"Unsupported language export format: {format_}")
    repo.append("language.export.created", {"format": format_, "item_count": len(items)})
    return {"format": format_, "content": content, "item_count": len(items)}
