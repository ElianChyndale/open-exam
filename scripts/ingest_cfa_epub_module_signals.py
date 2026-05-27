from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / ".system" / "memory" / "strategy" / "cfa-2026-epub-textbook-index.json"

SUBJECT_DIRS = {
    "Quantitative Methods": "Quantitative_Methods",
    "Economics": "Economics",
    "Corporate Issuers": "Corporate_Issuers",
    "Financial Statement Analysis": "Financial_Statement_Analysis",
    "Equity": "Equity",
    "Fixed Income": "Fixed_Income",
    "Derivatives": "Derivatives",
    "Alternative Investments": "Alternative_Investments",
    "Portfolio Management": "Portfolio_Management",
    "Ethical and Professional Standards": "Ethical_and_Professional_Standards",
}

INDEX_SUBJECT_TO_REGISTRY = {
    "Equity": "Equity Investments",
}


def load_index() -> list[dict]:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def load_registry_map() -> dict[tuple[str, str], str]:
    registry_path = REPO_ROOT / ".system" / "memory" / "strategy" / "cfa-2026-official-module-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    mapping: dict[tuple[str, str], str] = {}
    for subject_name, subject in registry["subjects"].items():
        normalized_subject = subject_name
        for module in subject["modules"]:
            mapping[(normalized_subject, module["module"])] = module["filename"]
    return mapping


def render_section(subject: dict, module: dict) -> str:
    anchors = module["signal_topics"][:8]
    practice = "available" if module.get("practice_href") else "not listed"
    solutions = "available" if module.get("solutions_href") else "not listed"
    lines = [
        "## Textbook Signal Topics",
        "",
        f"- Textbook volume: `V{subject['volume']}`",
        f"- Source ePub: `{subject['epub']}`",
        f"- Textbook chapter: `{module['official_module']}`",
        f"- Practice / Solutions: `{practice}` / `{solutions}`",
        "",
        "### High-Signal Anchors",
        "",
    ]
    for anchor in anchors:
        lines.append(f"- {anchor}")
    lines.extend(
        [
            "",
            "### How To Use These Anchors",
            "",
            "- 先用题干关键词匹配到最接近的教材锚点，再回到正文确认定义边界、顺序条件和例外。",
            "- 计算题优先看公式触发段；概念题优先看对比、分类和限制条件段。",
            "- 若一道题同时触发多个锚点，先处理 LOS 主动作对应的那个，再补其余支持细节。",
        ]
    )
    return "\n".join(lines)


def update_module_note(path: Path, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"\n## Textbook Signal Topics.*?(?=\n---\n\n## 1\. 模块定位)", re.S)
    if pattern.search(text):
        new_text = pattern.sub(lambda _: "\n" + section, text)
    else:
        marker = "\n---\n\n## 1. 模块定位"
        if marker not in text:
            raise RuntimeError(f"Could not find insertion marker in {path}")
        new_text = text.replace(marker, "\n\n" + section + marker, 1)
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    index = load_index()
    registry_map = load_registry_map()

    for subject in index:
        subject_name = subject["subject"]
        registry_subject = INDEX_SUBJECT_TO_REGISTRY.get(subject_name, subject_name)
        subject_dir = SUBJECT_DIRS[subject_name]
        for module in subject["modules"]:
            filename = registry_map[(registry_subject, module["module"])]
            note_path = REPO_ROOT / "CFA_tier1" / subject_dir / filename
            section = render_section(subject, module)
            update_module_note(note_path, section)


if __name__ == "__main__":
    main()
