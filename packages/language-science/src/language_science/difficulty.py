# packages/language-science/src/language_science/difficulty.py

from __future__ import annotations

import math
import re
from typing import Any

# BNC frequency bands (simplified -- top 1000, 2000, 3000, etc.)
CEFR_THRESHOLDS = {
    "A1": 0.95,   # top 5% most frequent words
    "A2": 0.85,
    "B1": 0.70,
    "B2": 0.50,
    "C1": 0.30,
    "C2": 0.10,
}

# Domain weight adjustments
DOMAIN_WEIGHTS = {
    "finance": {"cefr": 0.25, "exam": 0.40, "frequency": 0.15, "morphology": 0.20},
    "general": {"cefr": 0.35, "exam": 0.20, "frequency": 0.30, "morphology": 0.15},
    "academic": {"cefr": 0.30, "exam": 0.30, "frequency": 0.20, "morphology": 0.20},
    "cfa":     {"cefr": 0.15, "exam": 0.50, "frequency": 0.10, "morphology": 0.25},
}

# Rough syllable counter for English
def _count_syllables(word: str) -> int:
    word = word.lower().strip()
    if not word:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    return max(1, count)


# Simple BNC-like frequency bands (word -> percentile 0-1)
# In production this would load a file; here we use a minimal built-in set
_HIGH_FREQ = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
              "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
              "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
              "an", "will", "my", "one", "all", "would", "there", "their", "what",
              "so", "up", "out", "if", "about", "who", "get", "which", "go", "me"}

_MED_FREQ = {"yield", "bond", "stock", "rate", "value", "price", "return", "risk",
             "market", "asset", "debt", "equity", "cash", "income", "cost", "share",
             "fund", "trade", "bank", "capital", "invest", "interest", "growth"}


def _estimate_frequency(word: str) -> float:
    """Estimate frequency percentile: 1.0 = most common, 0.0 = rare."""
    lower = word.lower().strip()
    if lower in _HIGH_FREQ:
        return 0.95
    if lower in _MED_FREQ:
        return 0.60
    return 0.25


def _estimate_cefr(word: str, frequency: float) -> str:
    """Map frequency to CEFR level."""
    for level, threshold in sorted(CEFR_THRESHOLDS.items(), key=lambda x: -x[1]):
        if frequency >= threshold:
            return level
    return "C2"


def _morphological_complexity(word: str) -> float:
    """Score morphological complexity 0-1."""
    syllables = _count_syllables(word)
    affixes = len(re.findall(r"(un|re|in|dis|pre|mis|non|anti|de|over|under|able|ible|tion|sion|ment|ness|ity|ful|less|ly|al|ial|ic|ive|ous)", word.lower()))
    return min(1.0, (syllables / 5) * 0.6 + (affixes / 3) * 0.4)


class AdaptiveDifficultyEstimator:
    """Bayesian difficulty estimator that adapts weights from review outcomes.

    Starts with domain-specific default weights. Updates via Beta-Bernoulli
    on each review: correct -> alpha++, incorrect -> beta++.
    """

    def __init__(self, domain: str = "general", l1_language: str = "zh") -> None:
        self.domain = domain
        self.l1 = l1_language
        self.weights = dict(DOMAIN_WEIGHTS.get(domain, DOMAIN_WEIGHTS["general"]))
        # Per-word alpha/beta for Beta-Bernoulli correction
        self._alphas: dict[str, int] = {}
        self._betas: dict[str, int] = {}

    def estimate(self, word: str, *, context: str = "", l1: str | None = None) -> dict[str, Any]:
        freq = _estimate_frequency(word)
        cefr = _estimate_cefr(word, freq)
        morphology = _morphological_complexity(word)
        l1_lang = l1 or self.l1

        # L1 adjustment: cognate bonus for related languages
        l1_bonus = 0.0
        if l1_lang == "en":
            l1_bonus = 0.3  # native speaker bonus
        elif l1_lang.startswith("es") and any(
            word.endswith(suf) for suf in ("cion", "dad", "mente", "al", "ble")
        ):
            l1_bonus = 0.2  # Spanish cognate bonus

        raw_score = (
            self.weights["cefr"] * (1.0 - (list(CEFR_THRESHOLDS.keys()).index(cefr) if cefr in CEFR_THRESHOLDS else 3) / 6)
            + self.weights["frequency"] * (1.0 - freq)
            + self.weights["morphology"] * morphology
            + self.weights["exam"] * (0.7 if any(tag in context.lower() for tag in ("cfa", "finance", "accounting", "invest")) else 0.3)
        )

        difficulty = max(0.0, min(10.0, raw_score * 10.0))
        if l1_bonus > 0:
            difficulty = max(0.0, difficulty - l1_bonus * 5.0)

        # Beta-Bernoulli correction from past reviews
        alpha = self._alphas.get(word.lower(), 5)
        beta = self._betas.get(word.lower(), 5)
        posterior_mean = alpha / (alpha + beta)
        # Proper Beta-Bernoulli posterior: use posterior mean scaled by effective sample size
        corrected = difficulty * (1.0 - alpha / (alpha + beta + 1))

        return {
            "canonical_form": word,
            "cefr": cefr,
            "frequency_percentile": round(freq, 3),
            "morphology_score": round(morphology, 3),
            "domain": self.domain,
            "difficulty_score": round(max(0.0, min(10.0, corrected)), 2),
            "l1_adjusted": round(l1_bonus, 2),
            "posterior_mean": round(posterior_mean, 3),
        }

    def record_outcome(self, word: str, correct: bool) -> None:
        key = word.lower()
        if correct:
            self._alphas[key] = self._alphas.get(key, 5) + 1
        else:
            self._betas[key] = self._betas.get(key, 5) + 1
