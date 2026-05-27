from __future__ import annotations

import json
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


REPO_ROOT = Path(__file__).resolve().parent.parent
EPUB_ROOT = Path(r"D:\BaiduNetdiskDownload\CFA2026一级原版书")
STRATEGY_ROOT = REPO_ROOT / ".system" / "memory" / "strategy"
REGISTRY_PATH = STRATEGY_ROOT / "cfa-2026-official-module-registry.json"

XHTML_NS = {"xhtml": "http://www.w3.org/1999/xhtml"}


@dataclass(frozen=True)
class VolumeSpec:
    volume: int
    subject: str
    epub: str
    moc_path: str


VOLUME_SPECS = [
    VolumeSpec(1, "Quantitative Methods", "cfa-program2026L1V1.ePub", "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"),
    VolumeSpec(2, "Economics", "cfa-program2026L1V2.ePub", "CFA_tier1/Economics/00-Economics-MOC.md"),
    VolumeSpec(3, "Corporate Issuers", "cfa-program2026L1V3.ePub", "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md"),
    VolumeSpec(4, "Financial Statement Analysis", "cfa-program2026L1V4.ePub", "CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md"),
    VolumeSpec(5, "Equity", "cfa-program2026L1V5.ePub", "CFA_tier1/Equity/00-Equity-MOC.md"),
    VolumeSpec(6, "Fixed Income", "cfa-program2026L1V6.ePub", "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md"),
    VolumeSpec(7, "Derivatives", "cfa-program2026L1V7.ePub", "CFA_tier1/Derivatives/00-Derivatives-MOC.md"),
    VolumeSpec(8, "Alternative Investments", "cfa-program2026L1V8.ePub", "CFA_tier1/Alternative_Investments/00-Alternative-Investments-MOC.md"),
    VolumeSpec(9, "Portfolio Management", "cfa-program2026L1V9.ePub", "CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md"),
    VolumeSpec(10, "Ethical and Professional Standards", "cfa-program2026L1V10.ePub", "CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md"),
]

SUBJECT_TITLE_ALIASES = {
    "Quantitative Methods": ("Quantitative Methods",),
    "Economics": ("Economics",),
    "Corporate Issuers": ("Corporate Issuers",),
    "Financial Statement Analysis": ("Financial Statement Analysis",),
    "Equity": ("Equity", "Equity Investments"),
    "Fixed Income": ("Fixed Income",),
    "Derivatives": ("Derivatives",),
    "Alternative Investments": ("Alternative Investments",),
    "Portfolio Management": ("Portfolio Management",),
    "Ethical and Professional Standards": ("Ethical and Professional Standards",),
}

REGISTRY_SUBJECT_ALIASES = {
    "Equity": "Equity Investments",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def parse_list(ol: ET.Element, depth: int = 0) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for li in ol.findall("./xhtml:li", XHTML_NS):
        anchor = li.find("./xhtml:a", XHTML_NS)
        if anchor is None:
            continue
        entry = {
            "title": normalize("".join(anchor.itertext())),
            "href": anchor.get("href", ""),
            "depth": depth,
            "children": [],
        }
        child_ol = li.find("./xhtml:ol", XHTML_NS)
        if child_ol is not None:
            entry["children"] = parse_list(child_ol, depth + 1)
        items.append(entry)
    return items


def flatten(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for entry in entries:
        out.append({k: v for k, v in entry.items() if k != "children"})
        out.extend(flatten(entry["children"]))
    return out


def extract_nav(epub_path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(epub_path) as zf:
        root = ET.fromstring(zf.read("OEBPS/nav.xhtml"))
    navs = root.findall(".//xhtml:nav", XHTML_NS)
    target = navs[0] if navs else None
    if target is None:
        return []
    top_ol = target.find("./xhtml:ol", XHTML_NS)
    if top_ol is None:
        return []
    return parse_list(top_ol)


def is_module_entry(href: str) -> bool:
    return bool(re.search(r"-L_.*-s01\.xhtml$", href))


def is_real_module_title(title: str) -> bool:
    return not title.startswith("Appendices")


def is_signal_title(title: str) -> bool:
    lower = title.lower()
    if title == "Learning Outcomes":
        return False
    if title in {"Practice Problems", "Solutions"}:
        return False
    if lower.startswith("cover") or lower.startswith("title page") or lower.startswith("copyright page"):
        return False
    if lower.startswith("accessibility") or lower.startswith("table of contents") or lower.startswith("how to use"):
        return False
    if lower.startswith("cfa institute learning ecosystem") or lower.startswith("designing your personal study program"):
        return False
    if lower.startswith("errata") or lower.startswith("other feedback"):
        return False
    if title.startswith("1. Introduction"):
        return False
    return True


def collect_signal_items(module_entry: dict[str, Any]) -> list[str]:
    signals: list[str] = []
    for child in flatten(module_entry.get("children", [])):
        title = child["title"]
        if not is_signal_title(title):
            continue
        signals.append(title)
    cleaned: list[str] = []
    seen: set[str] = set()
    for signal in signals:
        key = signal.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(signal)
    return cleaned


def build_subject_index(spec: VolumeSpec, registry_subject: dict[str, Any]) -> dict[str, Any]:
    epub_path = EPUB_ROOT / spec.epub
    nav_entries = extract_nav(epub_path)
    aliases = SUBJECT_TITLE_ALIASES.get(spec.subject, (spec.subject,))
    subject_entry = next((entry for entry in nav_entries if entry["title"] in aliases), None)
    if subject_entry is None:
        raise RuntimeError(f"Could not find subject entry for {spec.subject} in {spec.epub}")

    module_entries = [
        entry
        for entry in subject_entry.get("children", [])
        if is_module_entry(entry["href"]) and is_real_module_title(entry["title"])
    ]
    registry_modules = registry_subject["modules"]
    if len(module_entries) != len(registry_modules):
        raise RuntimeError(
            f"Module count mismatch for {spec.subject}: epub={len(module_entries)} registry={len(registry_modules)}"
        )

    modules: list[dict[str, Any]] = []
    for registry_module, module_entry in zip(registry_modules, module_entries, strict=True):
        signals = collect_signal_items(module_entry)
        modules.append(
            {
                "module": registry_module["module"],
                "official_module": registry_module["official_module"],
                "module_href": module_entry["href"],
                "signal_topics": signals,
                "practice_href": next(
                    (child["href"] for child in module_entry.get("children", []) if child["title"] == "Practice Problems"),
                    "",
                ),
                "solutions_href": next(
                    (child["href"] for child in module_entry.get("children", []) if child["title"] == "Solutions"),
                    "",
                ),
            }
        )

    return {
        "subject": spec.subject,
        "volume": spec.volume,
        "epub": str(epub_path),
        "moc_path": spec.moc_path,
        "modules": modules,
    }


def render_index_markdown(subject_indexes: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        "generated_at: 2026-05-27",
        f"source_root: {EPUB_ROOT}",
        "source_type: official_epub_textbook",
        "---",
        "",
        "# CFA 2026 Level I EPUB Textbook Index",
        "",
        "> 这个索引以原版教材 ePub 目录为准，用于把教材章节结构回填到 MOC 和后续知识治理资产。",
        "",
    ]
    for subject in subject_indexes:
        lines.extend(
            [
                f"## {subject['subject']}",
                "",
                f"- volume: V{subject['volume']}",
                f"- epub: `{subject['epub']}`",
                f"- moc_target: `{subject['moc_path']}`",
                "",
                "| Module | Textbook Chapter | Key Section Anchors | Practice / Solutions |",
                "|---|---|---|---|",
            ]
        )
        for module in subject["modules"]:
            anchors = "; ".join(module["signal_topics"][:8])
            practice = "yes" if module["practice_href"] else "no"
            solutions = "yes" if module["solutions_href"] else "no"
            lines.append(
                f"| {module['module']} | {module['official_module']} | {anchors} | practice={practice}, solutions={solutions} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_moc_textbook_section(subject_index: dict[str, Any]) -> str:
    lines = [
        "## 2.5 原版教材章节锚点",
        "",
        f"- 教材卷册：`V{subject_index['volume']}`",
        f"- 主教材：`{subject_index['epub']}`",
        "- 用法：做题时先按模块定位，再用教材锚点回到具体定义、比较口径、公式应用和例外条件。",
        "",
        "| Module | 教材章节 | 高频细节锚点 |",
        "|---|---|---|",
    ]
    for module in subject_index["modules"]:
        anchors = "；".join(module["signal_topics"][:6])
        lines.append(f"| {module['module']} | {module['official_module']} | {anchors} |")
    lines.append("")
    lines.append("### 教材使用规则")
    lines.append("")
    lines.append("- 先用 MOC 的模块框架回忆，再回到教材锚点补定义边界、步骤顺序和题干触发词。")
    lines.append("- `Practice Problems` 和 `Solutions` 说明每个模块都能直接连到教材内题目与答案层，后续错题可回链到对应模块。")
    lines.append("- 若 MOC、题库页和教材表述有冲突，优先以原版教材和官方 registry 对齐，再决定是否改写长期笔记。")
    return "\n".join(lines)


def update_moc(moc_path: Path, section: str) -> None:
    text = moc_path.read_text(encoding="utf-8")
    pattern = re.compile(r"\n## 2\.5 原版教材章节锚点.*?(?=\n## 3\. )", re.S)
    if pattern.search(text):
        new_text = pattern.sub("\n" + section + "\n\n", text)
    else:
        marker = "\n## 3. 核心知识树"
        if marker not in text:
            raise RuntimeError(f"Could not find insertion marker in {moc_path}")
        new_text = text.replace(marker, "\n" + section + "\n" + marker, 1)
    moc_path.write_text(new_text, encoding="utf-8")


def main() -> None:
    registry = load_registry()
    subject_indexes: list[dict[str, Any]] = []
    for spec in VOLUME_SPECS:
        registry_key = REGISTRY_SUBJECT_ALIASES.get(spec.subject, spec.subject)
        registry_subject = registry["subjects"][registry_key]
        subject_indexes.append(build_subject_index(spec, registry_subject))

    STRATEGY_ROOT.mkdir(parents=True, exist_ok=True)
    json_path = STRATEGY_ROOT / "cfa-2026-epub-textbook-index.json"
    json_path.write_text(json.dumps(subject_indexes, indent=2, ensure_ascii=False), encoding="utf-8")

    md_path = STRATEGY_ROOT / "cfa-2026-epub-textbook-index.md"
    md_path.write_text(render_index_markdown(subject_indexes), encoding="utf-8")

    for subject_index in subject_indexes:
        update_moc(REPO_ROOT / subject_index["moc_path"], render_moc_textbook_section(subject_index))


if __name__ == "__main__":
    main()
