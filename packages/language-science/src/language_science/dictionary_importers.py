from __future__ import annotations

import csv
import json
import re
import struct
import xml.etree.ElementTree as ET
import zlib
from datetime import UTC, datetime
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Protocol

from language_science.dictionary_models import (
    BilingualMapping,
    DictionarySource,
    LexicalEntry,
    Sense,
)
from language_science.models import stable_id


MAGIC_SIGNATURES: dict[bytes, str] = {
    b"<?xml": "xml",
    b"<TEI": "tei",
    b"{\"": "json",
    b"[\n": "json",
    b"2of12id": "wordnet",
    b"data.adj": "wordnet",
    b"dict.dz": "stardict",
    b"\x00\x01": "stardict",
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _detect_format(content: bytes) -> str:
    for magic, fmt in MAGIC_SIGNATURES.items():
        if content.startswith(magic):
            return fmt
    text = content[:256].decode("utf-8", errors="ignore")
    if text.strip().startswith("<"):
        if "TEI" in text:
            return "tei"
        return "xml"
    try:
        json.loads(content.decode("utf-8"))
        return "json"
    except Exception:
        pass
    if b"\t" in content[:2048] and content.count(b"\t") > content.count(b","):
        return "tsv"
    if b"," in content[:2048]:
        return "csv"
    return "unknown"


class DictionaryParser(Protocol):
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        ...


class WordNetParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        text = content.decode("utf-8", errors="ignore")
        current_lemma = ""
        current_pos = ""
        senses: list[Sense] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith(" "):
                continue
            parts = line.split(" ")
            if parts[0].isdigit():
                synset_offset = parts[0]
                lex_filenum = parts[1]
                ss_type = parts[2]
                w_cnt = int(parts[3], 16)
                words = parts[4 : 4 + w_cnt * 2 : 2]
                current_lemma = words[0] if words else synset_offset
                current_pos = {"n": "noun", "v": "verb", "a": "adj", "s": "adj", "r": "adv"}.get(ss_type, "")
                gloss = " ".join(parts[parts.index("|") + 1 :]) if "|" in parts else ""
                sense = Sense(
                    sense_id=stable_id("sense", source_id, synset_offset),
                    definition=gloss,
                )
                senses = [sense]
                entries.append(
                    LexicalEntry(
                        entry_id=stable_id("entry", source_id, current_lemma, current_pos),
                        lemma=current_lemma,
                        pos=current_pos,
                        language="en",
                        source_id=source_id,
                        senses=senses,
                    )
                )
        return entries


class FreeDictTEIParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        root = ET.fromstring(content)
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        for entry_elem in root.iter("{http://www.tei-c.org/ns/1.0}entry"):
            lemma = ""
            pos = ""
            for form in entry_elem.iter("{http://www.tei-c.org/ns/1.0}form"):
                for orth in form.iter("{http://www.tei-c.org/ns/1.0}orth"):
                    lemma = (orth.text or "").strip()
                for gram in form.iter("{http://www.tei-c.org/ns/1.0}gram"):
                    if gram.get("type") == "pos":
                        pos = (gram.text or "").strip()
            senses: list[Sense] = []
            for sense_elem in entry_elem.iter("{http://www.tei-c.org/ns/1.0}sense"):
                defs: list[str] = []
                examples: list[str] = []
                translations: list[BilingualMapping] = []
                for cit in sense_elem.iter("{http://www.tei-c.org/ns/1.0}cit"):
                    cit_type = cit.get("type", "")
                    quote = cit.find("{http://www.tei-c.org/ns/1.0}quote")
                    if quote is not None and quote.text:
                        if cit_type == "trans":
                            translations.append(
                                BilingualMapping(
                                    mapping_id=stable_id("map", source_id, lemma, quote.text),
                                    target_lemma=quote.text,
                                    target_language="",
                                )
                            )
                        else:
                            examples.append(quote.text)
                for defn in sense_elem.iter("{http://www.tei-c.org/ns/1.0}def"):
                    if defn.text:
                        defs.append(defn.text.strip())
                senses.append(
                    Sense(
                        sense_id=stable_id("sense", source_id, lemma, str(len(senses))),
                        definition="; ".join(defs),
                        examples=examples,
                        translations=translations,
                    )
                )
            if lemma:
                lang = entry_elem.get("{http://www.w3.org/XML/1998/namespace}lang", "")
                entries.append(
                    LexicalEntry(
                        entry_id=stable_id("entry", source_id, lemma, pos),
                        lemma=lemma,
                        pos=pos,
                        language=lang or "",
                        source_id=source_id,
                        senses=senses,
                    )
                )
        return entries


class WikidataParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        try:
            data = json.loads(content.decode("utf-8"))
        except Exception:
            return entries
        if isinstance(data, dict):
            entities = data.get("entities", data)
        else:
            entities = data
        for key, entity in (entities.items() if isinstance(entities, dict) else enumerate(entities)):
            if not isinstance(entity, dict):
                continue
            lemma = ""
            lang = ""
            pos = ""
            for code, label in entity.get("labels", {}).items():
                lemma = label.get("value", "")
                lang = code
                break
            for claim in entity.get("claims", {}).get("P31", []):
                if claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q1084":
                    pos = "noun"
                elif claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q24905":
                    pos = "verb"
            senses: list[Sense] = []
            for gloss in entity.get("descriptions", {}).values():
                senses.append(
                    Sense(
                        sense_id=stable_id("sense", source_id, str(key), str(len(senses))),
                        definition=gloss.get("value", ""),
                    )
                )
            if lemma:
                entries.append(
                    LexicalEntry(
                        entry_id=stable_id("entry", source_id, lemma, pos),
                        lemma=lemma,
                        pos=pos,
                        language=lang,
                        source_id=source_id,
                        senses=senses,
                    )
                )
        return entries


class CSVParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        text = content.decode("utf-8", errors="ignore")
        reader = csv.DictReader(StringIO(text))
        for row in reader:
            lemma = row.get("lemma", row.get("word", row.get("term", "")))
            pos = row.get("pos", row.get("part_of_speech", ""))
            definition = row.get("definition", row.get("meaning", row.get("gloss", "")))
            language = row.get("language", row.get("lang", ""))
            if not lemma:
                continue
            sense = Sense(
                sense_id=stable_id("sense", source_id, lemma, "0"),
                definition=definition,
                examples=[row.get("example", "")] if row.get("example") else [],
            )
            entries.append(
                LexicalEntry(
                    entry_id=stable_id("entry", source_id, lemma, pos),
                    lemma=lemma,
                    pos=pos,
                    language=language,
                    source_id=source_id,
                    senses=[sense],
                )
            )
        return entries


class TSVParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        text = content.decode("utf-8", errors="ignore")
        reader = csv.DictReader(StringIO(text), delimiter="\t")
        for row in reader:
            lemma = row.get("lemma", row.get("word", row.get("term", "")))
            pos = row.get("pos", row.get("part_of_speech", ""))
            definition = row.get("definition", row.get("meaning", row.get("gloss", "")))
            language = row.get("language", row.get("lang", ""))
            if not lemma:
                continue
            sense = Sense(
                sense_id=stable_id("sense", source_id, lemma, "0"),
                definition=definition,
            )
            entries.append(
                LexicalEntry(
                    entry_id=stable_id("entry", source_id, lemma, pos),
                    lemma=lemma,
                    pos=pos,
                    language=language,
                    source_id=source_id,
                    senses=[sense],
                )
            )
        return entries


class JSONParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        try:
            data = json.loads(content.decode("utf-8"))
        except Exception:
            return entries
        if isinstance(data, dict):
            data = [data]
        for item in data:
            if not isinstance(item, dict):
                continue
            lemma = item.get("lemma", item.get("word", item.get("term", "")))
            pos = item.get("pos", item.get("partOfSpeech", ""))
            language = item.get("language", item.get("lang", ""))
            senses_data = item.get("senses", item.get("meanings", []))
            senses: list[Sense] = []
            for idx, s in enumerate(senses_data):
                if isinstance(s, str):
                    senses.append(Sense(sense_id=stable_id("sense", source_id, lemma, str(idx)), definition=s))
                elif isinstance(s, dict):
                    senses.append(
                        Sense(
                            sense_id=stable_id("sense", source_id, lemma, str(idx)),
                            definition=s.get("definition", s.get("gloss", "")),
                            examples=s.get("examples", []),
                            synonyms=s.get("synonyms", []),
                            antonyms=s.get("antonyms", []),
                            cefr_level=s.get("cefr", s.get("cefr_level", "")),
                        )
                    )
            if not senses and item.get("definition"):
                senses.append(
                    Sense(
                        sense_id=stable_id("sense", source_id, lemma, "0"),
                        definition=item["definition"],
                    )
                )
            if lemma:
                entries.append(
                    LexicalEntry(
                        entry_id=stable_id("entry", source_id, lemma, pos),
                        lemma=lemma,
                        pos=pos,
                        language=language,
                        source_id=source_id,
                        senses=senses,
                    )
                )
        return entries


class StarDictParser:
    def parse(self, content: bytes, source_id: str) -> list[LexicalEntry]:
        entries: list[LexicalEntry] = []
        try:
            dz = zlib.decompress(content)
            text = dz.decode("utf-8", errors="ignore")
        except Exception:
            text = content.decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if not line or "\t" not in line:
                continue
            lemma, definition = line.split("\t", 1)
            sense = Sense(
                sense_id=stable_id("sense", source_id, lemma, "0"),
                definition=definition,
            )
            entries.append(
                LexicalEntry(
                    entry_id=stable_id("entry", source_id, lemma, ""),
                    lemma=lemma,
                    pos="",
                    language="",
                    source_id=source_id,
                    senses=[sense],
                )
            )
        return entries


class DictionaryFormatDetector:
    """Detects dictionary format from file content or extension."""

    PARSERS: dict[str, type[DictionaryParser]] = {
        "wordnet": WordNetParser,
        "tei": FreeDictTEIParser,
        "xml": FreeDictTEIParser,
        "freedict": FreeDictTEIParser,
        "wikidata": WikidataParser,
        "json": JSONParser,
        "csv": CSVParser,
        "tsv": TSVParser,
        "stardict": StarDictParser,
    }

    @classmethod
    def detect(cls, content: bytes, filename: str = "") -> str:
        ext = Path(filename).suffix.lower().lstrip(".")
        if ext in {"csv", "tsv", "json", "xml"}:
            return ext
        if "freedict" in filename.lower() or "tei" in filename.lower():
            return "tei"
        if "wordnet" in filename.lower():
            return "wordnet"
        if "wikidata" in filename.lower():
            return "wikidata"
        if "stardict" in filename.lower() or filename.endswith(".dz"):
            return "stardict"
        return _detect_format(content)

    @classmethod
    def get_parser(cls, fmt: str) -> DictionaryParser:
        parser_cls = cls.PARSERS.get(fmt, JSONParser)
        return parser_cls()


def import_dictionary(
    repo_root: Path,
    *,
    title: str,
    language_pair: str,
    content: bytes,
    filename: str = "",
    license_mode: str = "unknown",
    priority: int = 0,
) -> dict[str, Any]:
    """Import a dictionary file: detect format, parse entries, store source metadata.

    Returns {"source": DictionarySource, "entries": list[LexicalEntry], "count": int}
    """
    file_hash = sha256(content).hexdigest()
    storage_dir = repo_root / ".system" / "private" / "language-dictionaries"
    storage_dir.mkdir(parents=True, exist_ok=True)

    fmt = DictionaryFormatDetector.detect(content, filename)
    parser = DictionaryFormatDetector.get_parser(fmt)
    source_id = stable_id("dict", file_hash[:16], title)
    source = DictionarySource(
        dictionary_id=source_id,
        language_pair=language_pair,
        title=title,
        format=fmt,
        file_hash=file_hash,
        license_mode=license_mode,
        imported_at=_now(),
        priority=priority,
    )

    entries = parser.parse(content, source_id)

    dest = storage_dir / f"{source_id}.{fmt}"
    dest.write_bytes(content)

    return {"source": source, "entries": entries, "count": len(entries)}
