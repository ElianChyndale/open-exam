from __future__ import annotations

import csv
import json
import re
from dataclasses import fields
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from io import StringIO
from pathlib import Path
from typing import Any

from language_science.dictionary_models import (
    DictionarySource,
    LexicalAsset,
    LexicalMemoryState,
    LexicalReviewSession,
    LexicalReviewUnit,
)
from language_science.models import stable_id


def _now() -> str:
    return datetime.now(UTC).isoformat()


class LexicalKernel:
    """Local-first dictionary source, lexical asset, and recall review engine."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel"
        self.dictionary_root = self.root / "dictionaries"
        self.asset_root = self.root / "lexical-assets"
        self.session_root = self.root / "review-sessions"
        self.memory_path = self.root / "lexical-memory.json"
        for path in (self.dictionary_root, self.asset_root, self.session_root):
            path.mkdir(parents=True, exist_ok=True)

    # ── Imports ────────────────────────────────────────────────────────

    def import_json(
        self,
        *,
        profile_id: str = "default",
        title: str,
        dictionary_type: str,
        entries: Any,
    ) -> dict[str, Any]:
        if isinstance(entries, str):
            entries = json.loads(entries)
        if isinstance(entries, dict):
            entries = [entries]
        if not isinstance(entries, list):
            raise ValueError("Dictionary JSON must be a list or object.")
        payload_text = json.dumps(entries, ensure_ascii=False, sort_keys=True)
        dictionary = self._new_dictionary(
            profile_id=profile_id,
            title=title,
            dictionary_type=dictionary_type,
            origin="import_json",
            content=payload_text,
        )
        assets = [
            asset
            for index, item in enumerate(entries, start=1)
            if isinstance(item, dict)
            for asset in self._assets_from_entry(dictionary, item, index=index, confidence=0.82)
        ]
        return self._persist_import(dictionary, assets)

    def import_csv(
        self,
        *,
        profile_id: str = "default",
        title: str,
        dictionary_type: str,
        csv_text: str,
    ) -> dict[str, Any]:
        if not csv_text.strip():
            raise ValueError("CSV content is required.")
        dictionary = self._new_dictionary(
            profile_id=profile_id,
            title=title,
            dictionary_type=dictionary_type,
            origin="import_csv",
            content=csv_text,
        )
        reader = csv.DictReader(StringIO(csv_text))
        assets: list[LexicalAsset] = []
        for index, row in enumerate(reader, start=1):
            assets.extend(self._assets_from_entry(dictionary, row, index=index, confidence=0.74))
        return self._persist_import(dictionary, assets)

    def import_text(
        self,
        *,
        profile_id: str = "default",
        title: str,
        dictionary_type: str,
        text: str,
    ) -> dict[str, Any]:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Dictionary text is required.")
        dictionary = self._new_dictionary(
            profile_id=profile_id,
            title=title,
            dictionary_type=dictionary_type,
            origin="import_text",
            content=cleaned,
        )
        blocks = [block.strip() for block in re.split(r"\n\s*\n+", cleaned) if block.strip()]
        if len(blocks) == 1:
            blocks = [line.strip() for line in cleaned.splitlines() if line.strip()]
        assets: list[LexicalAsset] = []
        for index, block in enumerate(blocks, start=1):
            parsed = self._parse_text_block(block)
            confidence = 0.58 if parsed.get("definition") else 0.38
            assets.extend(self._assets_from_entry(dictionary, parsed, index=index, confidence=confidence))
        return self._persist_import(dictionary, assets)

    # ── Dictionary state ───────────────────────────────────────────────

    def list_dictionaries(self, *, profile_id: str = "default") -> list[dict[str, Any]]:
        dictionaries = [
            self._dictionary_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self.dictionary_root.glob("*.json")
        ]
        dictionaries = [item for item in dictionaries if item.profile_id in {profile_id or "default", "default"}]
        dictionaries.sort(key=lambda item: item.imported_at, reverse=True)
        return [item.as_dict() for item in dictionaries]

    def get_dictionary(self, dictionary_id: str) -> dict[str, Any] | None:
        dictionary = self._load_dictionary(dictionary_id)
        if dictionary is None:
            return None
        assets = self.list_lexical_assets(dictionary_id=dictionary_id)
        return {"dictionary": dictionary.as_dict(), "asset_count": len(assets), "lexical_assets": assets}

    def attach_file_refs(self, dictionary_id: str, file_refs: list[str]) -> dict[str, Any]:
        """Attach local file segment refs to a dictionary import and its draft assets."""
        dictionary = self._load_dictionary(dictionary_id)
        if dictionary is None:
            raise KeyError(dictionary_id)
        trimmed_refs = [ref for ref in file_refs if ref][:20]
        if trimmed_refs:
            dictionary.source_refs = list(dict.fromkeys([*dictionary.source_refs, *trimmed_refs]))
            self._persist_dictionary(dictionary)
            for payload in self.list_lexical_assets(dictionary_id=dictionary_id):
                asset = self._asset_from_dict(payload)
                asset.source_refs = list(dict.fromkeys([*asset.source_refs, *trimmed_refs]))
                self._persist_asset(asset)
        result = self.get_dictionary(dictionary_id)
        if result is None:
            raise KeyError(dictionary_id)
        return result

    def score_dictionary(self, dictionary_id: str) -> dict[str, Any]:
        dictionary = self._require_dictionary(dictionary_id)
        self._score_dictionary_in_place(dictionary)
        self._persist_dictionary(dictionary)
        self._refresh_asset_dictionary_quality(dictionary)
        return {"dictionary": dictionary.as_dict(), "quality_gate": self._dictionary_gate_summary(dictionary)}

    def confirm_dictionary(self, dictionary_id: str) -> dict[str, Any]:
        dictionary = self._require_dictionary(dictionary_id)
        if dictionary.validation_status == "rejected":
            raise ValueError("Rejected dictionaries cannot be confirmed.")
        dictionary.validation_status = "confirmed"
        self._score_dictionary_in_place(dictionary)
        self._persist_dictionary(dictionary)
        self._refresh_asset_dictionary_quality(dictionary)
        return {"dictionary": dictionary.as_dict(), "quality_gate": self._dictionary_gate_summary(dictionary)}

    def reject_dictionary(self, dictionary_id: str) -> dict[str, Any]:
        dictionary = self._require_dictionary(dictionary_id)
        dictionary.validation_status = "rejected"
        dictionary.quality_status = "rejected"
        dictionary.quality_score = 0.0
        self._persist_dictionary(dictionary)
        rejected: list[dict[str, Any]] = []
        for payload in self.list_lexical_assets(dictionary_id=dictionary_id):
            asset = self._asset_from_dict(payload)
            asset.validation_status = "rejected"
            asset.dictionary_quality_status = "rejected"
            self._persist_asset(asset)
            rejected.append(asset.as_dict())
        return {"dictionary": dictionary.as_dict(), "rejected_assets": rejected}

    # ── Lexical assets ─────────────────────────────────────────────────

    def list_lexical_assets(
        self,
        *,
        profile_id: str = "default",
        dictionary_id: str = "",
        validation_status: str = "",
    ) -> list[dict[str, Any]]:
        assets = [
            self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))
            for path in self.asset_root.glob("*.json")
        ]
        filtered = [
            asset for asset in assets
            if asset.profile_id in {profile_id or "default", "default"}
            and (not dictionary_id or asset.dictionary_id == dictionary_id)
            and (not validation_status or asset.validation_status == validation_status)
        ]
        filtered.sort(key=lambda asset: (asset.validation_status, asset.language, asset.headword, asset.sense_number or 0))
        return [asset.as_dict() for asset in filtered]

    def get_lexical_asset(self, lexical_id: str) -> dict[str, Any] | None:
        asset = self._load_asset(lexical_id)
        return asset.as_dict() if asset else None

    def confirm_lexical_asset(self, lexical_id: str) -> dict[str, Any]:
        asset = self._require_asset(lexical_id)
        if not asset.source_refs:
            raise ValueError("Cannot confirm lexical asset without source_refs.")
        if not self._asset_dictionary_gate_passes(asset):
            raise ValueError("Cannot confirm lexical asset before dictionary quality gate passes.")
        asset.validation_status = "confirmed"
        asset.mastery_state = asset.mastery_state or "new"
        self._persist_asset(asset)
        return {"asset": asset.as_dict()}

    def reject_lexical_asset(self, lexical_id: str) -> dict[str, Any]:
        asset = self._require_asset(lexical_id)
        asset.validation_status = "rejected"
        self._persist_asset(asset)
        return {"asset": asset.as_dict()}

    # ── Review ─────────────────────────────────────────────────────────

    def generate_review_session(self, *, profile_id: str = "default", max_units: int = 12) -> LexicalReviewSession:
        candidates = [
            self._asset_from_dict(item)
            for item in self.list_lexical_assets(profile_id=profile_id)
            if item.get("validation_status") == "confirmed"
        ]
        candidates = [asset for asset in candidates if self._asset_dictionary_gate_passes(asset)]
        memory = self._load_memory()
        candidates.sort(key=lambda asset: self._lexical_priority(asset, memory), reverse=True)
        selected = self._select_mix(candidates, memory, max_units=max_units)
        session_id = stable_id("lex-session", profile_id, _now())
        units = [
            self._unit_from_asset(asset, session_id=session_id, index=index, memory=memory)
            for index, asset in enumerate(selected, start=1)
        ]
        session = LexicalReviewSession(
            session_id=session_id,
            profile_id=profile_id or "default",
            status="active",
            units=units,
            current_unit_index=0,
            completed_unit_ids=[],
            outcomes=[],
            started_at=_now(),
        )
        self._persist_session(session)
        return session

    def get_review_session(self, session_id: str) -> LexicalReviewSession | None:
        path = self.session_root / f"{session_id}.json"
        if not path.exists():
            return None
        return self._session_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def complete_review_unit(
        self,
        unit_id: str,
        *,
        outcome: str,
        session_id: str = "",
        time_spent_seconds: int = 0,
    ) -> dict[str, Any]:
        session = self.get_review_session(session_id) if session_id else self._find_session_for_unit(unit_id)
        if session is None:
            raise KeyError(unit_id)
        unit = next((item for item in session.units if item.unit_id == unit_id), None)
        if unit is None:
            raise KeyError(unit_id)
        normalized_outcome = outcome if outcome in {"recalled", "partial", "forgot", "skipped"} else "partial"
        memory_update = self._update_memory(unit, normalized_outcome, time_spent_seconds=time_spent_seconds)
        if unit.unit_id not in session.completed_unit_ids:
            session.completed_unit_ids.append(unit.unit_id)
        session.outcomes.append(
            {
                "unit_id": unit.unit_id,
                "lexical_id": unit.lexical_id,
                "outcome": normalized_outcome,
                "time_spent_seconds": time_spent_seconds,
                "completed_at": _now(),
                "memory_update": memory_update,
            }
        )
        if session.current_unit_index < len(session.units) - 1:
            session.current_unit_index += 1
        else:
            session.status = "completed"
            session.completed_at = _now()
        self._persist_session(session)
        return {"session": session.as_dict(), "unit_id": unit_id, "memory_update": memory_update}

    # ── Internal creation/scoring ──────────────────────────────────────

    def _new_dictionary(
        self,
        *,
        profile_id: str,
        title: str,
        dictionary_type: str,
        origin: str,
        content: str,
    ) -> DictionarySource:
        normalized_type = self._normalize_dictionary_type(dictionary_type)
        source_language, target_language = self._languages_for_type(normalized_type)
        content_hash = sha256(content.encode("utf-8")).hexdigest()
        dictionary_id = stable_id("dict", profile_id or "default", title, content_hash)
        return DictionarySource(
            dictionary_id=dictionary_id,
            language_pair=f"{source_language}-{target_language or source_language}",
            title=title.strip() or "Untitled dictionary",
            format=origin.replace("import_", ""),
            file_hash=content_hash,
            license_mode="manual_local",
            imported_at=_now(),
            priority=0,
            profile_id=profile_id or "default",
            dictionary_type=normalized_type,  # type: ignore[arg-type]
            source_language=source_language,
            target_language=target_language,
            origin=origin,  # type: ignore[arg-type]
            content_hash=content_hash,
            quality_score=0.0,
            quality_status="unscored",
            validation_status="draft",
            source_refs=[f"{dictionary_id}#source"],
        )

    def _persist_import(self, dictionary: DictionarySource, assets: list[LexicalAsset]) -> dict[str, Any]:
        existing = self._load_dictionary(dictionary.dictionary_id)
        if existing is not None:
            return {
                "duplicate": True,
                "dictionary": existing.as_dict(),
                "asset_count": len(self.list_lexical_assets(dictionary_id=existing.dictionary_id)),
                "lexical_assets": self.list_lexical_assets(dictionary_id=existing.dictionary_id),
            }
        self._score_dictionary_in_place(dictionary)
        self._persist_dictionary(dictionary)
        for asset in assets:
            asset.dictionary_quality_status = dictionary.quality_status
            self._persist_asset(asset)
        return {
            "duplicate": False,
            "dictionary": dictionary.as_dict(),
            "asset_count": len(assets),
            "lexical_assets": [asset.as_dict() for asset in assets],
        }

    def _assets_from_entry(
        self,
        dictionary: DictionarySource,
        item: dict[str, Any],
        *,
        index: int,
        confidence: float,
    ) -> list[LexicalAsset]:
        headword = str(item.get("headword") or item.get("lemma") or item.get("word") or item.get("term") or "").strip()
        if not headword:
            return []
        language = str(item.get("language") or item.get("lang") or dictionary.source_language or "").strip() or "en"
        target_language = item.get("target_language") or item.get("targetLanguage") or dictionary.target_language
        part_of_speech = item.get("part_of_speech") or item.get("partOfSpeech") or item.get("pos")
        entries: list[dict[str, Any]]
        senses = item.get("senses") or item.get("meanings")
        if isinstance(senses, list) and senses:
            entries = [sense if isinstance(sense, dict) else {"definition": str(sense)} for sense in senses]
        else:
            entries = [item]
        assets: list[LexicalAsset] = []
        for sense_index, sense in enumerate(entries, start=1):
            definition = str(sense.get("definition") or sense.get("gloss") or item.get("definition") or "").strip()
            translation = sense.get("translation") or item.get("translation")
            example_sentence = sense.get("example_sentence") or sense.get("example") or item.get("example_sentence") or item.get("example")
            source_ref = f"{dictionary.dictionary_id}#entry-{index}#sense-{sense_index}"
            quality_score = self._asset_quality_score(
                definition=definition,
                translation=str(translation or ""),
                example=str(example_sentence or ""),
                collocations=self._coerce_list(sense.get("collocations") or item.get("collocations")),
                confidence=confidence,
            )
            status = "draft" if confidence >= 0.7 and definition else "needs_review"
            assets.append(
                LexicalAsset(
                    lexical_id=stable_id("lex", dictionary.dictionary_id, headword, str(sense_index), definition[:80]),
                    profile_id=dictionary.profile_id,
                    dictionary_id=dictionary.dictionary_id,
                    headword=headword,
                    language=language,
                    target_language=str(target_language) if target_language else None,
                    part_of_speech=str(part_of_speech) if part_of_speech else None,
                    sense_number=sense_index,
                    definition=definition,
                    translation=str(translation) if translation else None,
                    example_sentence=str(example_sentence) if example_sentence else None,
                    example_translation=str(sense.get("example_translation") or item.get("example_translation") or "") or None,
                    collocations=self._coerce_list(sense.get("collocations") or item.get("collocations")),
                    synonyms=self._coerce_list(sense.get("synonyms") or item.get("synonyms")),
                    antonyms=self._coerce_list(sense.get("antonyms") or item.get("antonyms")),
                    register=str(sense.get("register") or item.get("register") or "") or None,
                    usage_notes=self._coerce_list(sense.get("usage_notes") or item.get("usage_notes") or item.get("usage")),
                    morphology=self._coerce_mapping(sense.get("morphology") or item.get("morphology")),
                    pronunciation=str(sense.get("pronunciation") or item.get("pronunciation") or "") or None,
                    tags=self._coerce_list(sense.get("tags") or item.get("tags")),
                    source_refs=[source_ref],
                    quality_score=quality_score,
                    validation_status=status,  # type: ignore[arg-type]
                    mastery_state="new",
                    next_review_at=None,
                    created_at=_now(),
                    dictionary_quality_status=dictionary.quality_status,
                )
            )
        return assets

    @staticmethod
    def _parse_text_block(block: str) -> dict[str, Any]:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        first = lines[0] if lines else block.strip()
        headword = ""
        pos = ""
        if ":" in first:
            headword, rest = [part.strip() for part in first.split(":", 1)]
            if rest:
                lines.insert(1, f"definition: {rest}")
        else:
            match = re.match(r"^([\wáéíóúñüÁÉÍÓÚÑÜ -]+)\s*(?:\(([^)]+)\))?\s*[-–]\s*(.+)$", first)
            if match:
                headword = match.group(1).strip()
                pos = match.group(2) or ""
                lines.insert(1, f"definition: {match.group(3)}")
            else:
                headword = first.split()[0] if first else ""
        parsed: dict[str, Any] = {"headword": headword, "part_of_speech": pos}
        labels = {
            "definition": ("definition", "def", "meaning"),
            "translation": ("translation", "trans"),
            "example_sentence": ("example", "example_sentence", "sentence"),
            "example_translation": ("example_translation", "example translation"),
            "collocations": ("collocations", "collocation"),
            "usage_notes": ("usage", "usage_notes", "note", "notes"),
            "synonyms": ("synonyms", "synonym"),
            "antonyms": ("antonyms", "antonym"),
            "language": ("language", "lang"),
            "target_language": ("target_language", "target"),
        }
        for line in lines[1:]:
            if ":" not in line:
                if not parsed.get("definition"):
                    parsed["definition"] = line
                continue
            label, value = [part.strip() for part in line.split(":", 1)]
            normalized = label.lower().replace("-", "_").replace(" ", "_")
            for key, aliases in labels.items():
                if normalized in aliases:
                    parsed[key] = value
                    break
        return parsed

    def _score_dictionary_in_place(self, dictionary: DictionarySource) -> None:
        if dictionary.validation_status == "rejected":
            dictionary.quality_score = 0.0
            dictionary.quality_status = "rejected"
            dictionary.quality_dimensions = {}
            return
        assets = [self._asset_from_dict(item) for item in self.list_lexical_assets(dictionary_id=dictionary.dictionary_id)]
        if not assets:
            asset_score = 0.35
        else:
            asset_score = sum(asset.quality_score for asset in assets) / len(assets)
        source_type_trust = {
            "english_english": 0.78,
            "spanish_english": 0.76,
            "english_spanish": 0.76,
            "custom_bilingual": 0.62,
            "custom_monolingual": 0.58,
        }.get(dictionary.dictionary_type, 0.45)
        structure_quality = min(1.0, 0.25 + (0.12 * len(assets)) + (0.15 if any(asset.example_sentence for asset in assets) else 0.0))
        bilingual_completeness = 0.8 if dictionary.target_language and any(asset.translation for asset in assets) else 0.55
        source_refs = 1.0 if dictionary.source_refs and all(asset.source_refs for asset in assets) else 0.35
        confirmation = {"confirmed": 1.0, "needs_review": 0.45, "draft": 0.25, "rejected": 0.0}.get(dictionary.validation_status, 0.25)
        dimensions = {
            "source_type_trust": source_type_trust,
            "structure_quality": structure_quality,
            "bilingual_completeness": bilingual_completeness,
            "lexical_asset_quality": asset_score,
            "source_refs": source_refs,
            "user_confirmation_signal": confirmation,
        }
        score = (
            0.22 * source_type_trust
            + 0.20 * structure_quality
            + 0.16 * bilingual_completeness
            + 0.18 * asset_score
            + 0.14 * source_refs
            + 0.10 * confirmation
        )
        dictionary.quality_score = round(self._clamp01(score), 4)
        dictionary.quality_dimensions = {key: round(self._clamp01(value), 4) for key, value in dimensions.items()}
        dictionary.quality_status = self._quality_status(dictionary)

    @staticmethod
    def _quality_status(dictionary: DictionarySource) -> str:
        if dictionary.validation_status == "rejected":
            return "rejected"
        if dictionary.quality_score >= 0.85 and dictionary.validation_status == "confirmed":
            return "trusted"
        if dictionary.quality_score >= 0.70:
            return "high"
        if dictionary.quality_score >= 0.50:
            return "medium"
        return "low"

    def _dictionary_gate_summary(self, dictionary: DictionarySource) -> dict[str, Any]:
        if dictionary.validation_status == "rejected" or dictionary.quality_status == "rejected":
            return {"passes": False, "reason": "dictionary_rejected"}
        if dictionary.validation_status != "confirmed":
            return {"passes": False, "reason": "dictionary_not_confirmed"}
        if dictionary.quality_status not in {"medium", "high", "trusted"}:
            return {"passes": False, "reason": f"dictionary_quality_{dictionary.quality_status}"}
        return {"passes": True, "reason": f"dictionary_quality_{dictionary.quality_status}"}

    def _asset_dictionary_gate_passes(self, asset: LexicalAsset) -> bool:
        if not asset.source_refs:
            return False
        if not asset.dictionary_id:
            return True
        dictionary = self._load_dictionary(asset.dictionary_id)
        return bool(dictionary and self._dictionary_gate_summary(dictionary)["passes"])

    @staticmethod
    def _asset_quality_score(
        *,
        definition: str,
        translation: str,
        example: str,
        collocations: list[str],
        confidence: float,
    ) -> float:
        score = 0.2 + (0.25 if definition else 0.0) + (0.15 if translation else 0.0)
        score += 0.15 if example else 0.0
        score += 0.1 if collocations else 0.0
        score += 0.15 * confidence
        return round(min(score, 1.0), 4)

    def _lexical_priority(self, asset: LexicalAsset, memory: dict[str, Any]) -> float:
        state = memory.get(asset.lexical_id, {})
        due_pressure = self._due_pressure(state.get("next_review_at") or asset.next_review_at)
        frequency_or_user_importance = 0.7 if "frequency_high" in asset.tags else 0.45
        weakness_severity = min(1.0, float(state.get("lapse_count", 0)) / 3 + (0.2 if state.get("weakness_tags") else 0.0))
        production_gap = 1.0 - float(state.get("production_strength", 0.0))
        sense_confusion = min(1.0, float(state.get("sense_confusion_count", 0)) / 3)
        collocation_value = 1.0 if asset.collocations else 0.25
        source_quality = asset.quality_score
        recent_context_relevance = 0.4 if asset.example_sentence else 0.15
        return (
            0.22 * due_pressure
            + 0.18 * frequency_or_user_importance
            + 0.16 * weakness_severity
            + 0.14 * production_gap
            + 0.12 * sense_confusion
            + 0.08 * collocation_value
            + 0.06 * source_quality
            + 0.04 * recent_context_relevance
        )

    def _select_mix(
        self,
        assets: list[LexicalAsset],
        memory: dict[str, Any],
        *,
        max_units: int,
    ) -> list[LexicalAsset]:
        if max_units <= 0:
            return []
        due = [asset for asset in assets if self._due_pressure(memory.get(asset.lexical_id, {}).get("next_review_at") or asset.next_review_at) >= 0.7]
        weak = [asset for asset in assets if memory.get(asset.lexical_id, {}).get("weakness_tags") or memory.get(asset.lexical_id, {}).get("sense_confusion_count", 0)]
        production = [asset for asset in assets if asset.collocations or asset.example_sentence]
        new = [asset for asset in assets if not memory.get(asset.lexical_id)]
        buckets = [
            (due, round(max_units * 0.4)),
            (weak, round(max_units * 0.2)),
            (production, round(max_units * 0.2)),
            (new, max_units),
        ]
        selected: list[LexicalAsset] = []
        seen: set[str] = set()
        for bucket, take in buckets:
            for asset in bucket[:max(0, take)]:
                if asset.lexical_id not in seen:
                    selected.append(asset)
                    seen.add(asset.lexical_id)
                if len(selected) >= max_units:
                    return selected
        for asset in assets:
            if len(selected) >= max_units:
                break
            if asset.lexical_id not in seen:
                selected.append(asset)
                seen.add(asset.lexical_id)
        return selected[:max_units]

    def _unit_from_asset(
        self,
        asset: LexicalAsset,
        *,
        session_id: str,
        index: int,
        memory: dict[str, Any],
    ) -> LexicalReviewUnit:
        mode = "translation_recall" if asset.translation else "definition_recall"
        if asset.collocations:
            mode = "collocation_check"
        if asset.morphology:
            mode = "morphology_check"
        if asset.example_sentence:
            mode = "cloze_context" if asset.headword.lower() in asset.example_sentence.lower() else mode
        front = self._front_prompt(asset, mode)
        answer_parts = [asset.definition]
        if asset.translation:
            answer_parts.append(f"Translation: {asset.translation}")
        if asset.example_sentence:
            answer_parts.append(f"Example: {asset.example_sentence}")
        if asset.collocations:
            answer_parts.append(f"Collocations: {', '.join(asset.collocations)}")
        return LexicalReviewUnit(
            unit_id=stable_id("lex-unit", session_id, asset.lexical_id, mode),
            session_id=session_id,
            lexical_id=asset.lexical_id,
            display_mode=mode,  # type: ignore[arg-type]
            front_prompt=front,
            correct_answer="; ".join(part for part in answer_parts if part),
            correct_reasoning=asset.definition,
            example_sentence=asset.example_sentence,
            collocations=asset.collocations,
            usage_notes=asset.usage_notes,
            source_refs=asset.source_refs,
            memory_state_before=memory.get(asset.lexical_id, {}).get("mastery_state", asset.mastery_state),
            headword=asset.headword,
            translation=asset.translation,
            example_translation=asset.example_translation,
            progress_index=index,
        )

    @staticmethod
    def _front_prompt(asset: LexicalAsset, mode: str) -> str:
        if mode == "translation_recall":
            return f"Recall the English meaning and active use of: {asset.headword}"
        if mode == "collocation_check":
            return f"Produce a natural collocation for: {asset.headword}"
        if mode == "morphology_check":
            return f"Recall morphology or conjugation notes for: {asset.headword}"
        if mode == "cloze_context" and asset.example_sentence:
            cloze = re.sub(re.escape(asset.headword), "____", asset.example_sentence, flags=re.IGNORECASE)
            return f"Fill the lexical gap from context: {cloze}"
        return f"Recall the definition and sense of: {asset.headword}"

    def _update_memory(self, unit: LexicalReviewUnit, outcome: str, *, time_spent_seconds: int) -> dict[str, Any]:
        memory = self._load_memory()
        state = self._memory_from_dict(memory.get(unit.lexical_id, {"lexical_id": unit.lexical_id}))
        now = datetime.now(UTC)
        if outcome == "recalled":
            state.mastery_state = "practiced"
            state.recall_strength = min(1.0, state.recall_strength + 0.3)
            state.production_strength = min(1.0, state.production_strength + (0.25 if unit.display_mode in {"sentence_production", "collocation_check", "translation_recall"} else 0.15))
            interval = 7
            weakness_tags: list[str] = []
        elif outcome == "partial":
            state.mastery_state = "learning"
            state.recall_strength = min(1.0, state.recall_strength + 0.1)
            state.production_strength = max(0.0, state.production_strength - 0.05)
            interval = 2
            weakness_tags = self._weakness_tags_for_unit(unit)
        elif outcome == "forgot":
            state.mastery_state = "learning"
            state.lapse_count += 1
            state.recall_strength = max(0.0, state.recall_strength - 0.1)
            interval = 1
            weakness_tags = self._weakness_tags_for_unit(unit)
        else:
            state.mastery_state = "learning"
            interval = 1
            weakness_tags = ["production_gap"]
        if "sense_confusion" in weakness_tags:
            state.sense_confusion_count += 1
        if "collocation_gap" in weakness_tags:
            state.collocation_confusion_count += 1
        state.weakness_tags = sorted(set(weakness_tags))
        state.last_reviewed_at = now.isoformat()
        state.next_review_at = (now + timedelta(days=interval)).isoformat()
        memory[unit.lexical_id] = state.as_dict()
        self._persist_memory(memory)

        asset = self._load_asset(unit.lexical_id)
        if asset is not None:
            asset.mastery_state = state.mastery_state
            asset.next_review_at = state.next_review_at
            self._persist_asset(asset)
        return state.as_dict()

    @staticmethod
    def _weakness_tags_for_unit(unit: LexicalReviewUnit) -> list[str]:
        tags = ["definition_gap"]
        if unit.translation:
            tags.append("translation_gap")
        if unit.display_mode in {"sense_selection", "synonym_boundary"}:
            tags.append("sense_confusion")
        if unit.collocations or unit.display_mode == "collocation_check":
            tags.append("collocation_gap")
        if unit.display_mode == "morphology_check":
            tags.append("morphology_gap")
        if unit.display_mode in {"sentence_production", "translation_recall"}:
            tags.append("production_gap")
        return tags

    # ── Persistence ────────────────────────────────────────────────────

    def _load_dictionary(self, dictionary_id: str) -> DictionarySource | None:
        path = self.dictionary_root / f"{dictionary_id}.json"
        if not path.exists():
            return None
        return self._dictionary_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _require_dictionary(self, dictionary_id: str) -> DictionarySource:
        dictionary = self._load_dictionary(dictionary_id)
        if dictionary is None:
            raise KeyError(dictionary_id)
        return dictionary

    def _persist_dictionary(self, dictionary: DictionarySource) -> None:
        (self.dictionary_root / f"{dictionary.dictionary_id}.json").write_text(
            json.dumps(dictionary.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load_asset(self, lexical_id: str) -> LexicalAsset | None:
        path = self.asset_root / f"{lexical_id}.json"
        if not path.exists():
            return None
        return self._asset_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _require_asset(self, lexical_id: str) -> LexicalAsset:
        asset = self._load_asset(lexical_id)
        if asset is None:
            raise KeyError(lexical_id)
        return asset

    def _persist_asset(self, asset: LexicalAsset) -> None:
        (self.asset_root / f"{asset.lexical_id}.json").write_text(
            json.dumps(asset.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _persist_session(self, session: LexicalReviewSession) -> None:
        (self.session_root / f"{session.session_id}.json").write_text(
            json.dumps(session.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _find_session_for_unit(self, unit_id: str) -> LexicalReviewSession | None:
        for path in self.session_root.glob("*.json"):
            session = self._session_from_dict(json.loads(path.read_text(encoding="utf-8")))
            if any(unit.unit_id == unit_id for unit in session.units):
                return session
        return None

    def _load_memory(self) -> dict[str, Any]:
        if not self.memory_path.exists():
            return {}
        return json.loads(self.memory_path.read_text(encoding="utf-8"))

    def _persist_memory(self, memory: dict[str, Any]) -> None:
        self.memory_path.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")

    def _refresh_asset_dictionary_quality(self, dictionary: DictionarySource) -> None:
        for payload in self.list_lexical_assets(dictionary_id=dictionary.dictionary_id):
            asset = self._asset_from_dict(payload)
            asset.dictionary_quality_status = dictionary.quality_status
            self._persist_asset(asset)

    @staticmethod
    def _dictionary_from_dict(data: dict[str, Any]) -> DictionarySource:
        allowed = {field.name for field in fields(DictionarySource)}
        return DictionarySource(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _asset_from_dict(data: dict[str, Any]) -> LexicalAsset:
        allowed = {field.name for field in fields(LexicalAsset)}
        return LexicalAsset(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _session_from_dict(data: dict[str, Any]) -> LexicalReviewSession:
        allowed = {field.name for field in fields(LexicalReviewSession)}
        payload = {key: value for key, value in data.items() if key in allowed}
        payload["units"] = [
            LexicalKernel._unit_from_dict(unit) if isinstance(unit, dict) else unit
            for unit in payload.get("units", [])
        ]
        return LexicalReviewSession(**payload)

    @staticmethod
    def _unit_from_dict(data: dict[str, Any]) -> LexicalReviewUnit:
        allowed = {field.name for field in fields(LexicalReviewUnit)}
        return LexicalReviewUnit(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _memory_from_dict(data: dict[str, Any]) -> LexicalMemoryState:
        allowed = {field.name for field in fields(LexicalMemoryState)}
        return LexicalMemoryState(**{key: value for key, value in data.items() if key in allowed})

    @staticmethod
    def _normalize_dictionary_type(dictionary_type: str) -> str:
        normalized = str(dictionary_type or "custom_monolingual").strip().lower().replace("-", "_").replace(" ", "_")
        allowed = {"english_english", "spanish_english", "english_spanish", "custom_bilingual", "custom_monolingual"}
        return normalized if normalized in allowed else "custom_monolingual"

    @staticmethod
    def _languages_for_type(dictionary_type: str) -> tuple[str, str | None]:
        return {
            "english_english": ("en", None),
            "spanish_english": ("es", "en"),
            "english_spanish": ("en", "es"),
            "custom_bilingual": ("", ""),
            "custom_monolingual": ("", None),
        }.get(dictionary_type, ("", None))

    @staticmethod
    def _coerce_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, tuple):
            return [str(item).strip() for item in value if str(item).strip()]
        if not value:
            return []
        return [part.strip() for part in re.split(r"[,;|]", str(value)) if part.strip()]

    @staticmethod
    def _coerce_mapping(value: Any) -> dict[str, Any]:
        return dict(value) if isinstance(value, dict) else {}

    @staticmethod
    def _clamp01(value: float) -> float:
        return min(max(value, 0.0), 1.0)

    @staticmethod
    def _due_pressure(next_review_at: str | None) -> float:
        if not next_review_at:
            return 0.8
        try:
            parsed = datetime.fromisoformat(next_review_at.replace("Z", "+00:00"))
        except ValueError:
            return 0.6
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        delta_days = (parsed - datetime.now(UTC)).total_seconds() / 86400
        if delta_days <= 0:
            return 1.0
        if delta_days <= 2:
            return 0.7
        return 0.25
