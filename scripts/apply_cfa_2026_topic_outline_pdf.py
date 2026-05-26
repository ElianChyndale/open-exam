from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
CFA_ROOT = ROOT / "CFA_tier1"
REGISTRY = ROOT / ".system" / "memory" / "strategy" / "cfa-2026-official-module-registry.json"
PDF = ROOT / ".system" / "memory" / "strategy" / "official-sources" / "2026-l1-topics-combined.pdf"

PAGE_RANGES = {
    "Quantitative Methods": range(0, 3),
    "Economics": range(4, 7),
    "Corporate Issuers": range(8, 10),
    "Financial Statement Analysis": range(10, 14),
    "Equity Investments": range(14, 17),
    "Fixed Income": range(18, 22),
    "Derivatives": range(22, 24),
    "Alternative Investments": range(24, 26),
    "Portfolio Management": range(26, 29),
    "Ethical and Professional Standards": range(30, 32),
}

OFFICIAL_WEIGHTS = {
    "Quantitative Methods": "6-9%",
    "Economics": "6-9%",
    "Corporate Issuers": "6-9%",
    "Financial Statement Analysis": "11-14%",
    "Equity Investments": "11-14%",
    "Fixed Income": "11-14%",
    "Derivatives": "5-8%",
    "Alternative Investments": "7-10%",
    "Portfolio Management": "8-12%",
    "Ethical and Professional Standards": "15-20%",
}


def normalize_text(value: str) -> str:
    value = value.replace("–", "-").replace("—", "-").replace("\t", " ")
    return re.sub(r"\s+", " ", value).strip()


def clean_pdf_line(value: str) -> str:
    line = normalize_text(value)
    line = re.sub(r"^(\d+)?([A-Za-z].*?)(\d+)$", r"\2", line)
    line = re.sub(r"^\d+(?=[A-Za-z])", "", line)
    return line.strip()


def extract_subject_lines(reader: PdfReader, subject: str) -> list[str]:
    lines: list[str] = []
    ignored = {
        "2026 Level I Topic Outlines",
        "LEARNING OUTCOMES",
        "The candidate should be able to:",
        subject,
        "Financial Statement",
        "Analysis",
        "Ethical and Professional",
        "Standards",
    }
    for page_index in PAGE_RANGES[subject]:
        text = reader.pages[page_index].extract_text() or ""
        for raw_line in text.splitlines():
            line = clean_pdf_line(raw_line)
            if not line:
                continue
            if line.startswith("© CFA Institute"):
                continue
            if line in ignored:
                continue
            lines.append(line)
    return lines


def extract_los(reader: PdfReader, subject: str, module_names: list[str]) -> dict[str, list[str]]:
    lines = extract_subject_lines(reader, subject)
    los_by_module = {name: [] for name in module_names}
    name_lookup = {normalize_text(name): name for name in module_names}
    current_module: str | None = None
    current_bullet: str | None = None
    index = 0

    while index < len(lines):
        matched_module = None
        matched_line_count = 0
        for line_count in range(1, 5):
            candidate = normalize_text(" ".join(lines[index : index + line_count]))
            if candidate in name_lookup:
                matched_module = name_lookup[candidate]
                matched_line_count = line_count
                break

        if matched_module:
            if current_module and current_bullet:
                los_by_module[current_module].append(normalize_text(current_bullet))
                current_bullet = None
            current_module = matched_module
            index += matched_line_count
            continue

        line = lines[index]
        if line.startswith("□"):
            if current_module and current_bullet:
                los_by_module[current_module].append(normalize_text(current_bullet))
            current_bullet = line.lstrip("□").strip()
        elif current_module and current_bullet:
            current_bullet += " " + line
        index += 1

    if current_module and current_bullet:
        los_by_module[current_module].append(normalize_text(current_bullet))

    return los_by_module


def replace_los_section(text: str, los: list[str]) -> str:
    start = text.index("## Learning Outcome Statements")
    end_marker = "\n## Local Study Notes"
    end = text.index(end_marker, start)
    lines = ["## Learning Outcome Statements", "", "The candidate should be able to:", ""]
    for item in los:
        lines.append(f"- {item}")
    lines.append("")
    return text[:start] + "\n".join(lines) + text[end:]


def rebuild_curriculum_markdown(registry: dict) -> str:
    lines = [
        "# CFA 2026 Level I Complete Official Curriculum",
        "",
        "*Generated from CFA Institute 2026 Level I Topic Outlines and local Learning Ecosystem page-item scrape.*",
        "",
        "This document contains the official CFA 2026 Level I topic areas, learning modules, and Learning Outcome Statements (LOS).",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
    ]
    for idx, (subject, data) in enumerate(registry["subjects"].items(), start=1):
        anchor = subject.lower().replace(" ", "-")
        lines.append(f"- [{idx:02d} {subject}](#{idx:02d}-{anchor}) — {data['module_count']} content modules")
    lines.append("")
    lines.append("---")
    for idx, (subject, data) in enumerate(registry["subjects"].items(), start=1):
        lines.extend(
            [
                "",
                f"# {idx:02d} {subject}",
                "",
                f"**Exam Weight:** {data['exam_weight']}",
                "",
                "## Module Overview",
                "",
                "| # | Module | Type |",
                "|---|--------|------|",
            ]
        )
        for module in data["modules"]:
            lines.append(f"| {int(module['module'][1:])} | {module['official_module'].split(': ', 1)[1]} | Content |")
        lines.extend(["", "## Learning Outcome Statements", ""])
        for module in data["modules"]:
            module_name = module["official_module"].split(": ", 1)[1]
            lines.extend([f"### {module_name}", "", "The candidate should be able to:", ""])
            for los in module["los"]:
                lines.append(f"- {los}")
            lines.append("")
        lines.append("---")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    reader = PdfReader(str(PDF))
    total_los = 0

    registry["official_outline_source"] = "CFA Institute 2026 Level I Topic Outlines combined PDF"
    registry["official_outline_url"] = "https://www.cfainstitute.org/sites/default/files/docs/programs/cfa-program/2026-l1-topics-combined.pdf"

    for subject, data in registry["subjects"].items():
        module_names = [module["official_module"].split(": ", 1)[1] for module in data["modules"]]
        los_by_module = extract_los(reader, subject, module_names)
        data["exam_weight"] = OFFICIAL_WEIGHTS[subject]

        for module in data["modules"]:
            module_name = module["official_module"].split(": ", 1)[1]
            los = los_by_module[module_name]
            if not los:
                raise RuntimeError(f"No LOS parsed for {subject} / {module_name}")
            module["los"] = los
            total_los += len(los)

            path = CFA_ROOT / data["directory"] / module["filename"]
            text = path.read_text(encoding="utf-8")
            path.write_text(replace_los_section(text, los), encoding="utf-8")

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (CFA_ROOT / "CFA_2026_L1_Complete_Curriculum.md").write_text(
        rebuild_curriculum_markdown(registry), encoding="utf-8"
    )
    print(f"Applied official 2026 topic outline LOS: {total_los}")


if __name__ == "__main__":
    main()
