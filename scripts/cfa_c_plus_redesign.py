from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / ".system" / "memory" / "strategy" / "cfa-2026-epub-textbook-index.json"
AUDIT_PATH = REPO_ROOT / ".system" / "memory" / "strategy" / "cfa-c-plus-prototype-audit.md"

MECHANICAL_SECTION_PATTERNS = [
    re.compile(r"\n## Textbook Signal Topics\n.*?(?=\n## \d+\.|\n## [^\n]+|\Z)", re.S),
    re.compile(r"\n### 教材驱动补强（按原版教材回看）\n.*?(?=\n## |\n### |\Z)", re.S),
    re.compile(r"\n### 教材驱动解题动作\n.*?(?=\n## |\n### |\Z)", re.S),
    re.compile(r"\n### 教材驱动易错清单\n.*?(?=\n## |\n### |\Z)", re.S),
]


def is_active_knowledge_file(path: Path) -> bool:
    normalized = path.as_posix()
    if not normalized.endswith(".md"):
        return False
    blocked_parts = {"_legacy", "_archive", "mock", "dashboard"}
    return not any(part in blocked_parts for part in path.parts)


def remove_mechanical_sections(text: str) -> str:
    cleaned = text
    for pattern in MECHANICAL_SECTION_PATTERNS:
        cleaned = pattern.sub("\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + "\n"


def load_textbook_index() -> list[dict]:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def find_subject(index: list[dict], subject: str) -> dict:
    for item in index:
        if item["subject"] == subject:
            return item
    raise ValueError(f"Subject not found in textbook index: {subject}")
