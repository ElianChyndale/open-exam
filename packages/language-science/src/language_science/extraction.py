"""Automatic vocabulary extraction from resource documents."""
from __future__ import annotations

import re
from typing import Any


COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know",
    "take", "people", "into", "year", "your", "good", "some", "could",
    "them", "see", "other", "than", "then", "now", "look", "only", "come",
    "its", "over", "think", "also", "back", "after", "use", "two", "how",
    "our", "work", "first", "well", "way", "even", "new", "want", "because",
    "any", "these", "give", "day", "most", "us",
}

CFA_DOMAIN_MARKERS = {"cfa", "finance", "invest", "bond", "equity", "asset", "portfolio",
                       "derivative", "yield", "duration", "convexity", "spread", "margin",
                       "leverage", "liquidity", "volatility", "amortize", "depreciate"}


def extract_candidate_terms(text: str, min_length: int = 3, max_terms: int = 20) -> list[dict[str, Any]]:
    """Extract candidate vocabulary terms from document text."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", text.lower())
    word_freq: dict[str, int] = {}
    for word in words:
        if word in COMMON_WORDS:
            continue
        word_freq[word] = word_freq.get(word, 0) + 1

    # Score by frequency * rarity
    scored = sorted(word_freq.items(), key=lambda x: -x[1])
    candidates = []
    for word, freq in scored[:max_terms]:
        is_cfa = any(marker in word for marker in CFA_DOMAIN_MARKERS)
        candidates.append({
            "canonical_form": word,
            "frequency": freq,
            "item_type": "term",
            "domain": "cfa" if is_cfa else "general",
            "confidence": min(0.9, 0.3 + freq * 0.02),
        })
    return candidates


def extract_phrases(text: str, max_phrases: int = 10) -> list[dict[str, Any]]:
    """Extract 2-3 word phrases that appear with meaningful frequency."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", text.lower())
    phrases: dict[str, int] = {}
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if words[i] not in COMMON_WORDS or words[i+1] not in COMMON_WORDS:
            phrases[bigram] = phrases.get(bigram, 0) + 1
    for i in range(len(words) - 2):
        trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
        if any(w not in COMMON_WORDS for w in (words[i], words[i+1], words[i+2])):
            phrases[trigram] = phrases.get(trigram, 0) + 1

    scored = sorted(phrases.items(), key=lambda x: -x[1])
    results = []
    for phrase, freq in scored[:max_phrases]:
        is_cfa = any(marker in phrase for marker in CFA_DOMAIN_MARKERS)
        results.append({
            "canonical_form": phrase,
            "frequency": freq,
            "item_type": "phrase",
            "domain": "cfa" if is_cfa else "general",
            "confidence": min(0.85, 0.2 + freq * 0.03),
        })
    return results


def full_extract(text: str, *, max_terms: int = 20, max_phrases: int = 10) -> list[dict[str, Any]]:
    """Full extraction: terms + phrases, sorted by confidence."""
    terms = extract_candidate_terms(text, max_terms=max_terms)
    phrases = extract_phrases(text, max_phrases=max_phrases)
    combined = terms + phrases
    combined.sort(key=lambda x: -x["confidence"])
    return combined
