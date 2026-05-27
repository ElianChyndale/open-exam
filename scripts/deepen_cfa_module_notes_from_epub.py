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

STOPWORDS = {
    "and",
    "of",
    "the",
    "to",
    "for",
    "in",
    "with",
    "using",
    "part",
    "an",
    "other",
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


def clean_anchor(anchor: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.\s*", "", anchor).strip()


def anchor_depth(anchor: str) -> int:
    match = re.match(r"^(\d+(?:\.\d+)*)\.", anchor)
    if not match:
        return 1
    return match.group(1).count(".") + 1


def anchor_acronym(title: str) -> str:
    words = re.findall(r"[A-Za-z]+", title)
    useful = [word for word in words if word.lower() not in STOPWORDS]
    if not useful:
        return ""
    acronym = "".join(word[0].upper() for word in useful if word)
    return acronym if 2 <= len(acronym) <= 6 else ""


def anchor_focus(anchor: str) -> str:
    title = clean_anchor(anchor)
    depth = anchor_depth(anchor)
    lower = title.lower()
    if "introduction" in lower or "overview" in lower or "summary" in lower:
        return "先确认本节对象、变量口径和它与整章主线的关系，再进入后续细节。"
    if "practice problems" in lower or "solutions" in lower:
        return "把这部分当作教材内 drill 入口，优先验证自己是否能独立复原判断步骤。"
    if depth >= 3:
        return "重点回看分类边界、步骤顺序、输入输出变量，以及容易被题目改口径的细节。"
    if depth == 2:
        return "重点回看这一层的主干结论、比较口径和公式适用条件，再往下接次级细节。"
    return "重点回看定义、核心结论和它在本模块中的用途，避免只记标题不记动作。"


def anchor_triggers(anchor: str) -> str:
    title = clean_anchor(anchor)
    acronym = anchor_acronym(title)
    parts = [f"`{title}`"]
    if acronym:
        parts.append(f"`{acronym}`")
    parts.append("题干里出现同义词、定义反问、比较口径或一步计算时回到这一节。")
    return "；".join(parts)


def build_detail_section(module: dict) -> str:
    lines = [
        "### 教材驱动补强（按原版教材回看）",
        "",
        "| 教材锚点 | 回看重点 | 题干触发词 |",
        "|---|---|---|",
    ]
    for anchor in module["signal_topics"][:8]:
        lines.append(f"| {clean_anchor(anchor)} | {anchor_focus(anchor)} | {anchor_triggers(anchor)} |")
    return "\n".join(lines)


def build_action_section(module: dict) -> str:
    lines = [
        "### 教材驱动解题动作",
        "",
        "- 先按 `Textbook Signal Topics` 找最接近的教材小节，不要直接凭熟词下结论。",
    ]
    for anchor in module["signal_topics"][:5]:
        title = clean_anchor(anchor)
        lines.append(f"- 遇到 `{title}`` 相关题型时，先复原该小节的定义边界，再决定是套公式、做比较还是判断例外。")
    if module.get("practice_href"):
        lines.append("- 做完一轮后，回到教材内 `Practice Problems / Solutions` 检查自己是否漏掉了变量口径、顺序条件或例外。")
    return "\n".join(lines)


def build_trap_section(module: dict) -> str:
    lines = [
        "### 教材驱动易错清单",
        "",
        "| 易错来源 | 常见误判 | 回正动作 |",
        "|---|---|---|",
    ]
    for anchor in module["signal_topics"][:5]:
        title = clean_anchor(anchor)
        depth = anchor_depth(anchor)
        misread = "把标题当成会做题，忽略定义边界和相邻概念差异。"
        if depth >= 3:
            misread = "记住了主标题，却忽略该细分小节真正考的是步骤顺序、分类条件或变量口径。"
        lines.append(
            f"| {title} | {misread} | 看到相关题干先回到 `{title}`，用一句话说清“它是什么、什么时候用、最容易和什么混”。 |"
        )
    return "\n".join(lines)


def replace_or_insert(text: str, start_heading: str, end_heading: str, section_title: str, content: str) -> str:
    pattern = re.compile(rf"\n### {re.escape(section_title)}.*?(?=\n### |\n{re.escape(end_heading)})", re.S)
    start_index = text.find(start_heading)
    end_index = text.find(end_heading, start_index + 1)
    if start_index == -1 or end_index == -1:
        return text
    block = text[start_index:end_index]
    if pattern.search(block):
        block = pattern.sub("\n" + content + "\n", block)
    else:
        block = block.rstrip() + "\n\n" + content + "\n"
    return text[:start_index] + block + text[end_index:]


def update_note(path: Path, module: dict) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_or_insert(text, "\n## 4. 知识点详解", "\n## 5.", "教材驱动补强（按原版教材回看）", build_detail_section(module))
    text = replace_or_insert(text, "\n## 6. 常见考点与解题思路", "\n## 7.", "教材驱动解题动作", build_action_section(module))
    text = replace_or_insert(text, "\n## 7. 易错点与考试陷阱", "\n## 8.", "教材驱动易错清单", build_trap_section(module))
    path.write_text(text, encoding="utf-8")


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
            update_note(note_path, module)


if __name__ == "__main__":
    main()
