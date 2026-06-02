"""Mock Question Ingestion Pipeline — parse, index, and register CFA mock questions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from app.cfa_storage import CfaRepository
from app.storage import Repository


SUBJECT_DIR_MAP = {
    "AltInv": "Alternative_Investments",
    "CorpIss": "Corporate_Issuers",
    "Derivatives": "Derivatives",
    "Economics": "Economics",
    "Equity": "Equity",
    "Ethics": "Ethical_and_Professional_Standards",
    "FI": "Fixed_Income",
    "FRA": "Financial_Statement_Analysis",
    "Portfolio": "Portfolio_Management",
    "Quant": "Quantitative_Methods",
}

SUBJECT_EXAM_WEIGHTS = {
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


@dataclass
class MockQuestion:
    question_id: str
    subject_code: str
    subject_name: str
    mock_set: str
    question_number: str
    source_page: str
    question_text: str
    difficulty_guess: str  # "easy", "medium", "hard"
    exam_weight: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


# Regex for mock question line: "- CFA L1 1-1 Q85 | p.19 | Question text..."
LINE_PATTERN = re.compile(
    r"-\s+CFA\s+L1\s+(?P<mock_set>[\d\-]+)\s+Q(?P<qnum>\d+)\s*\|\s*p\.\s*(?P<page>\d+)\s*\|\s*(?P<text>.+)"
)


def parse_mock_line(line: str, subject_code: str) -> MockQuestion | None:
    m = LINE_PATTERN.match(line.strip())
    if not m:
        return None
    subject_name = SUBJECT_DIR_MAP.get(subject_code, subject_code)
    qid = f"mock-{subject_code}-{m.group('mock_set').replace(' ', '-')}-Q{m.group('qnum')}"

    # Heuristic difficulty based on question content
    text = m.group("text").lower()
    if any(w in text for w in ["calculate", "compute", "most likely"]):
        diff = "medium"
    elif any(w in text for w in ["least likely", "except"]):
        diff = "hard"
    else:
        diff = "easy"

    return MockQuestion(
        question_id=qid,
        subject_code=subject_code,
        subject_name=subject_name,
        mock_set=m.group("mock_set"),
        question_number=m.group("qnum"),
        source_page=m.group("page"),
        question_text=m.group("text").strip(),
        difficulty_guess=diff,
        exam_weight=SUBJECT_EXAM_WEIGHTS.get(subject_name, 0.08),
    )


def ingest_all_mock_questions(root: Path) -> dict[str, Any]:
    """Parse all 10 mock question files and build index."""
    mock_root = root / "CFA_tier1" / "mock"
    all_questions: dict[str, MockQuestion] = {}

    for subject_code in SUBJECT_DIR_MAP:
        file_path = mock_root / subject_code / f"00-{subject_code}-Mock-Questions.md"
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            q = parse_mock_line(line, subject_code)
            if q:
                all_questions[q.question_id] = q

    # Build index
    by_subject: dict[str, list[dict[str, Any]]] = {}
    by_mock_set: dict[str, list[dict[str, Any]]] = {}
    for q in all_questions.values():
        d = q.as_dict()
        by_subject.setdefault(q.subject_code, []).append(d)
        by_mock_set.setdefault(q.mock_set, []).append(d)

    index = {
        "total_questions": len(all_questions),
        "by_subject": {k: {"count": len(v), "questions": v} for k, v in by_subject.items()},
        "by_mock_set": {k: {"count": len(v)} for k, v in by_mock_set.items()},
        "subject_weights": SUBJECT_EXAM_WEIGHTS,
    }

    # Write index
    index_path = root / ".system" / "memory" / "mock_question_index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return index


def register_questions_as_cfa_items(repo: CfaRepository, root: Path) -> dict[str, int]:
    """Register mock questions as CFA items in the event store."""
    from app.cfa_workflows import create_cfa_item, create_cfa_card

    index_path = root / ".system" / "memory" / "mock_question_index.json"
    if not index_path.exists():
        return {"registered": 0, "cards": 0}

    index = json.loads(index_path.read_text(encoding="utf-8"))
    registered = 0
    cards_created = 0

    for subject_code, data in index.get("by_subject", {}).items():
        for q_data in data.get("questions", []):
            try:
                item = create_cfa_item(
                    repo,
                    item_type="cfa_concept",
                    canonical_form=q_data["question_text"][:80],
                    topic=q_data["subject_name"],
                    los=f"mock-{subject_code}",
                )
                create_cfa_card(repo, item, card_type="cfa_calculation")
                registered += 1
                cards_created += 1
            except Exception:
                continue

    return {"registered": registered, "cards": cards_created}


def select_proactive_questions(
    root: Path,
    *,
    subject_coverage: dict[str, float] | None = None,
    max_questions: int = 15,
) -> list[dict[str, Any]]:
    """Select questions for proactive review based on coverage gaps."""
    index_path = root / ".system" / "memory" / "mock_question_index.json"
    if not index_path.exists():
        return []

    index = json.loads(index_path.read_text(encoding="utf-8"))
    subject_coverage = subject_coverage or {}

    scored: list[tuple[float, dict[str, Any]]] = []
    for subject_code, data in index.get("by_subject", {}).items():
        weight = SUBJECT_EXAM_WEIGHTS.get(
            SUBJECT_DIR_MAP.get(subject_code, ""), 0.08
        )
        coverage = subject_coverage.get(subject_code, 0.0)
        score = weight * (1.0 - coverage)

        for q in data.get("questions", []):
            scored.append((score, q))

    scored.sort(key=lambda x: -x[0])
    return [q for _, q in scored[:max_questions]]
