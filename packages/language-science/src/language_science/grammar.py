from __future__ import annotations

from hashlib import sha1
import re
from typing import Any


def _spanish_features(text: str) -> list[dict[str, Any]]:
    features = []
    for token in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", text):
        lower = token.lower()
        feature: dict[str, Any] = {"surface": token, "lemma": lower}
        if lower.endswith("a"):
            feature["gender"] = "feminine"
        elif lower.endswith("o"):
            feature["gender"] = "masculine"
        if lower.endswith("s"):
            feature["number"] = "plural"
        if lower in {"estoy", "soy", "hablo", "asisto"}:
            feature.update({"tense": "present", "mood": "indicative", "person": "first-singular"})
        if lower in {"estoy", "soy"}:
            feature["irregularity"] = "irregular"
        if len(feature) > 2:
            features.append(feature)
    return features


def analyze_sentence(text: str, language: str) -> dict[str, Any]:
    clauses = [
        {"clause_type": "subordinate" if index == 0 and re.match(r"(?i)^(if|when|si)\b", clause.strip()) else "main", "text": clause.strip()}
        for index, clause in enumerate(re.split(r"[,;]", text))
        if clause.strip()
    ]
    tokens = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", text.lower())
    collocations = [" ".join(tokens[index:index + 2]) for index in range(max(0, len(tokens) - 1))]
    return {
        "clauses": clauses,
        "phrases": collocations[:4],
        "collocations": collocations,
        "cefr_level": "B2" if len(tokens) >= 8 else "A2",
        "spanish_features": _spanish_features(text) if language == "es" else [],
        "text_hash": sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest(),
    }
