from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any, Mapping
from urllib.parse import urlsplit

from resource_ingestion.models import ResourceDocument


LANGUAGE_SIGNAL_TERMS = {
    "language",
    "grammar",
    "vocabulary",
    "phrase",
    "pronunciation",
    "cefr",
    "listening",
    "reading",
    "speaking",
    "writing",
    "spanish",
    "english",
    "french",
    "german",
    "chinese",
    "japanese",
}

CFA_SIGNAL_TERMS = {
    "cfa",
    "finance",
    "financial",
    "equity",
    "fixed income",
    "portfolio",
    "derivative",
    "economics",
    "fra",
    "accounting",
    "valuation",
    "duration",
    "yield",
    "ethics",
}

ANSWER_SIGNAL_TERMS = {
    "answer",
    "solution",
    "worked example",
    "practice problem",
    "explanation",
    "step-by-step",
    "q&a",
    "faq",
}

NOISE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsubscribe\b", re.IGNORECASE),
    re.compile(r"\bsign\s*up\b", re.IGNORECASE),
    re.compile(r"\bcookie\b", re.IGNORECASE),
    re.compile(r"\bprivacy policy\b", re.IGNORECASE),
    re.compile(r"\badvertis", re.IGNORECASE),
    re.compile(r"\bsponsored\b", re.IGNORECASE),
    re.compile(r"\bnewsletter\b", re.IGNORECASE),
    re.compile(r"\baccept all\b", re.IGNORECASE),
    re.compile(r"\bshare this\b", re.IGNORECASE),
    re.compile(r"\bcontinue reading\b", re.IGNORECASE),
    re.compile(r"\bcomments?\b", re.IGNORECASE),
)

LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2}(?:-[A-Z]{2})?$")


def _document_dict(document: ResourceDocument | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(document, ResourceDocument):
        return document.as_dict()
    return dict(document)


def _clip(text: str, limit: int = 240) -> str:
    clipped = " ".join(text.split())
    return clipped if len(clipped) <= limit else f"{clipped[: limit - 1]}..."


def _count_signal_matches(haystack: str, signals: set[str]) -> int:
    lowered = haystack.lower()
    return sum(1 for signal in signals if signal in lowered)


def _score_source_credibility(provider: str, hostname: str) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 0.45
    trusted_suffixes = (".gov", ".edu", ".org")
    trusted_hosts = ("sec.gov", "fred.stlouisfed.org", "worldbank.org", "cfainstitute.org", "ietf.org", "wikipedia.org")
    official_providers = {"sec_edgar", "fred", "world_bank"}
    if provider in official_providers:
        score = 1.0
        reasons.append(f"structured provider `{provider}` is explicitly trusted")
    elif hostname.endswith(trusted_suffixes):
        score = 0.8
        reasons.append(f"domain `{hostname}` looks institutional")
    elif any(hostname.endswith(item) for item in trusted_hosts):
        score = 0.9
        reasons.append(f"domain `{hostname}` matches allowlisted knowledge source")
    elif hostname:
        reasons.append(f"domain `{hostname}` is public but not specially trusted")
    else:
        score = 0.2
        reasons.append("missing hostname reduces source trust")
    return score, reasons


def _score_shape(title: str, body: str) -> tuple[float, list[str]]:
    reasons: list[str] = []
    title_len = len(title.strip())
    body_len = len(body.strip())
    title_score = 1.0 if 12 <= title_len <= 180 else 0.45 if title_len >= 6 else 0.1
    body_score = 1.0 if body_len >= 800 else 0.8 if body_len >= 300 else 0.45 if body_len >= 120 else 0.1
    if title_score >= 0.8:
        reasons.append("title length looks article-like")
    else:
        reasons.append("title is too short or too long for reliable indexing")
    if body_score >= 0.8:
        reasons.append("body/excerpt length is sufficient for scoring")
    else:
        reasons.append("body/excerpt is too thin, likely just metadata or navigation copy")
    return (title_score * 0.4) + (body_score * 0.6), reasons


def _score_noise(text: str) -> tuple[float, list[str]]:
    matches = [pattern.pattern for pattern in NOISE_PATTERNS if pattern.search(text)]
    if not text.strip():
        return 0.1, ["no body text available for noise screening"]
    if not matches:
        return 1.0, ["no obvious ad, cookie, or signup noise detected"]
    penalty = min(0.85, len(matches) * 0.12)
    return max(0.0, 1.0 - penalty), [f"noise markers detected: {', '.join(matches[:4])}"]


def _score_language_lane_fit(lane: str, language: str, topic: str, text: str) -> tuple[float, list[str]]:
    reasons: list[str] = []
    topic_lower = topic.lower()
    signal_text = f"{topic_lower} {text.lower()}"
    if lane == "language":
        signals = _count_signal_matches(signal_text, LANGUAGE_SIGNAL_TERMS)
        language_ok = bool(language and LANGUAGE_CODE_PATTERN.match(language))
        score = 0.35
        if language_ok:
            score += 0.3
            reasons.append(f"language code `{language}` is well-formed")
        else:
            reasons.append("missing or malformed language code for LanguageOS lane")
        if signals >= 3:
            score += 0.35
            reasons.append("content contains strong language-learning markers")
        elif signals >= 1:
            score += 0.2
            reasons.append("content contains some language-learning markers")
        else:
            reasons.append("weak language-learning signal in title/topic/body")
        return min(score, 1.0), reasons
    signals = _count_signal_matches(signal_text, CFA_SIGNAL_TERMS)
    score = 0.35
    if signals >= 3:
        score += 0.45
        reasons.append("content contains strong CFA/finance markers")
    elif signals >= 1:
        score += 0.25
        reasons.append("content contains some CFA/finance markers")
    else:
        reasons.append("weak CFA/finance signal in title/topic/body")
    if language in {"", "en", "en-US", "en-GB"}:
        score += 0.2
        reasons.append("language is compatible with current CFA study lane")
    else:
        reasons.append(f"language `{language}` may not match current CFA lane expectations")
    return min(score, 1.0), reasons


def _score_answer_topic_signals(answer_bearing: bool, topic: str, text: str) -> tuple[float, list[str]]:
    reasons: list[str] = []
    signals = _count_signal_matches(text.lower(), ANSWER_SIGNAL_TERMS)
    score = 0.25
    if topic.strip():
        score += 0.25
        reasons.append(f"topic is populated as `{topic}`")
    else:
        reasons.append("topic is missing")
    if answer_bearing:
        score += 0.35
        reasons.append("document is explicitly marked answer-bearing")
    elif signals >= 2:
        score += 0.3
        reasons.append("body/title suggests answer-bearing or explanatory material")
    elif signals == 1:
        score += 0.15
        reasons.append("body/title contains a weak answer-bearing hint")
    else:
        reasons.append("no answer-bearing cue detected")
    return min(score, 1.0), reasons


@dataclass(frozen=True, slots=True)
class QualityDimension:
    dimension: str
    score: float
    weight: float
    reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    document_id: str
    lane: str
    overall_score: float
    normalized_score: int
    recommendation: str
    pass_gate: bool
    dimensions: list[QualityDimension]
    strengths: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    summary: str = ""

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["dimensions"] = [dimension.as_dict() for dimension in self.dimensions]
        return payload


def assess_document_quality(
    document: ResourceDocument | Mapping[str, Any],
    *,
    full_text: str = "",
) -> QualityAssessment:
    payload = _document_dict(document)
    metadata = payload.get("metadata", {})
    title = str(payload.get("title", "")).strip()
    excerpt = str(payload.get("excerpt", "")).strip()
    body = full_text.strip() or str(metadata.get("body", "")).strip() or excerpt
    combined = " ".join(part for part in [title, str(payload.get("topic", "")), body] if part).strip()
    hostname = (urlsplit(str(payload.get("url", ""))).hostname or "").lower()

    dimension_specs = [
        ("source_credibility", 0.28, *_score_source_credibility(str(payload.get("provider", "")), hostname)),
        ("content_shape", 0.22, *_score_shape(title, body)),
        ("noise_screen", 0.18, *_score_noise(combined)),
        (
            "lane_fit",
            0.18,
            *_score_language_lane_fit(
                str(payload.get("lane", "")),
                str(payload.get("language", "")),
                str(payload.get("topic", "")),
                combined,
            ),
        ),
        (
            "answer_topic_signals",
            0.14,
            *_score_answer_topic_signals(
                bool(payload.get("answer_bearing", False)),
                str(payload.get("topic", "")),
                combined,
            ),
        ),
    ]

    dimensions = [
        QualityDimension(dimension=name, weight=weight, score=max(0.0, min(score, 1.0)), reasons=reasons)
        for name, weight, score, reasons in dimension_specs
    ]
    overall_score = sum(item.score * item.weight for item in dimensions)
    normalized_score = round(overall_score * 100)
    recommendation = "promote" if overall_score >= 0.78 else "review" if overall_score >= 0.55 else "reject"
    pass_gate = overall_score >= 0.68
    strengths = [
        _clip(reason)
        for item in dimensions
        if item.score >= 0.75
        for reason in item.reasons[:1]
    ]
    concerns = [
        _clip(reason)
        for item in dimensions
        if item.score < 0.55
        for reason in item.reasons[:1]
    ]
    summary = (
        f"score={normalized_score} recommendation={recommendation} "
        f"lane={payload.get('lane', '')} provider={payload.get('provider', '')}"
    )
    return QualityAssessment(
        document_id=str(payload.get("document_id", "")),
        lane=str(payload.get("lane", "")),
        overall_score=round(overall_score, 4),
        normalized_score=normalized_score,
        recommendation=recommendation,
        pass_gate=pass_gate,
        dimensions=dimensions,
        strengths=strengths,
        concerns=concerns,
        summary=summary,
    )
