from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CFA_ROOT = ROOT / "CFA_tier1"
CURRICULUM = CFA_ROOT / "CFA_2026_L1_Complete_Curriculum.md"
SCRAPE_DIR = Path(r"C:\Users\Administrator\AppData\Local\Temp\cfa_courses")
SYNC_DATE = date.today().isoformat()
LEGACY_DIR_NAME = "2026-05-26-official-sync"


SUBJECTS = [
    {
        "number": "01",
        "name": "Quantitative Methods",
        "dir": "Quantitative_Methods",
        "course_id": "1645",
        "weight": "6-9%",
        "moc": "00-Quantitative-Methods-MOC.md",
    },
    {
        "number": "02",
        "name": "Economics",
        "dir": "Economics",
        "course_id": "1646",
        "weight": "6-9%",
        "moc": "00-Economics-MOC.md",
    },
    {
        "number": "03",
        "name": "Corporate Issuers",
        "dir": "Corporate_Issuers",
        "course_id": "1647",
        "weight": "6-9%",
        "moc": "00-Corporate-Issuers-MOC.md",
    },
    {
        "number": "04",
        "name": "Financial Statement Analysis",
        "dir": "Financial_Statement_Analysis",
        "course_id": "1648",
        "weight": "11-14%",
        "moc": "00-Financial-Statement-Analysis-MOC.md",
    },
    {
        "number": "05",
        "name": "Equity Investments",
        "dir": "Equity",
        "course_id": "1649",
        "weight": "11-14%",
        "moc": "00-Equity-MOC.md",
    },
    {
        "number": "06",
        "name": "Fixed Income",
        "dir": "Fixed_Income",
        "course_id": "1650",
        "weight": "11-14%",
        "moc": "00-Fixed-Income-MOC.md",
    },
    {
        "number": "07",
        "name": "Derivatives",
        "dir": "Derivatives",
        "course_id": "1651",
        "weight": "5-8%",
        "moc": "00-Derivatives-MOC.md",
    },
    {
        "number": "08",
        "name": "Alternative Investments",
        "dir": "Alternative_Investments",
        "course_id": "1652",
        "weight": "7-10%",
        "moc": "00-Alternative-Investments-MOC.md",
    },
    {
        "number": "09",
        "name": "Portfolio Management",
        "dir": "Portfolio_Management",
        "course_id": "1653",
        "weight": "8-12%",
        "moc": "00-Portfolio-Management-MOC.md",
    },
    {
        "number": "10",
        "name": "Ethical and Professional Standards",
        "dir": "Ethical_and_Professional_Standards",
        "course_id": "1654",
        "weight": "15-20%",
        "moc": "00-Ethical-and-Professional-Standards-MOC.md",
    },
]


@dataclass
class Module:
    number: int
    name: str
    los: list[str]
    page_items: list[str]


@dataclass
class LegacyNote:
    path: Path
    original_rel: str
    title: str
    official_module: str
    body: str
    tokens: set[str]


def slugify(value: str) -> str:
    value = value.replace("&", "and")
    value = value.replace(":", "")
    value = re.sub(r"\([^)]*\)", "", value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return re.sub(r"-+", "-", value)


def tokenize(value: str) -> set[str]:
    stop = {
        "and",
        "the",
        "of",
        "for",
        "in",
        "to",
        "with",
        "a",
        "an",
        "part",
        "module",
        "m",
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
    }
    raw = re.findall(r"[a-z0-9]+", value.lower().replace("fixed-income", "fixed income"))
    return {t for t in raw if t not in stop and len(t) > 1}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip().splitlines()
    body = text[end + 4 :].lstrip()
    data: dict[str, str] = {}
    for line in raw:
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def parse_curriculum() -> dict[str, list[Module]]:
    text = CURRICULUM.read_text(encoding="utf-8")
    chunks = re.split(r"\n# (\d{2} .+?)\n", text)
    result: dict[str, list[Module]] = {}
    for i in range(1, len(chunks), 2):
        heading = chunks[i].strip()
        subject_name = heading[3:]
        body = chunks[i + 1]
        modules = []
        rows = re.findall(r"^\| (\d+) \| (.+?) \| Content \|$", body, re.MULTILINE)
        for index, name in rows:
            los = []
            pattern = rf"### {re.escape(name)}\n\nThe candidate should be able to:\n\n(.*?)(?=\n### |\n## |\n---|\Z)"
            match = re.search(pattern, body, re.DOTALL)
            if match:
                los = [
                    line[2:].strip()
                    for line in match.group(1).splitlines()
                    if line.startswith("- ")
                ]
            modules.append(Module(int(index), name, los, []))
        result[subject_name] = modules
    return result


def parse_page_items(course_id: str) -> dict[int, list[str]]:
    files = sorted(SCRAPE_DIR.glob(f"course_{course_id}_*_full.txt"))
    if not files:
        return {}
    text = files[0].read_text(encoding="utf-8", errors="replace")
    items: dict[int, list[str]] = {}
    current: int | None = None
    for raw in text.splitlines():
        line = raw.strip()
        module_match = re.match(r"Module (\d+): (.+)$", line)
        if module_match:
            current = int(module_match.group(1))
            items.setdefault(current, [])
            continue
        if not current:
            continue
        if line.startswith("Learning Outcomes:") or re.match(rf"{current}\.\d+\s+\|\s+", line):
            if line not in items[current]:
                items[current].append(line)
    return items


def read_legacy_notes(subject_dir: Path) -> list[LegacyNote]:
    notes: list[LegacyNote] = []
    for path in sorted(subject_dir.glob("M*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = parse_frontmatter(text)
        title = frontmatter.get("title") or body.splitlines()[0].lstrip("# ").strip() if body else path.stem
        official = frontmatter.get("official_module", "")
        token_source = " ".join([path.stem, title, official, body[:2000]])
        notes.append(
            LegacyNote(
                path=path,
                original_rel=path.relative_to(ROOT).as_posix(),
                title=title,
                official_module=official,
                body=body.strip(),
                tokens=tokenize(token_source),
            )
        )
    return notes


def module_context(module: Module) -> str:
    return " ".join([module.name, *module.page_items])


def score_note(note: LegacyNote, module: Module) -> float:
    official = f"module {module.number}: {module.name}".lower()
    if note.official_module.lower() == official:
        return 1.0
    note_module_numbers = {int(n) for n in re.findall(r"\bM0?(\d{1,2})\b", note.path.stem, re.I)}
    target_tokens = tokenize(module_context(module))
    overlap = len(note.tokens & target_tokens) / max(1, len(target_tokens))
    seq = SequenceMatcher(None, " ".join(sorted(note.tokens)), " ".join(sorted(target_tokens))).ratio()
    score = (0.75 * overlap) + (0.25 * seq)
    if module.number in note_module_numbers:
        score += 0.08
    if str(module.number) in note.official_module:
        score += 0.05
    return min(score, 0.99)


def assign_notes(notes: list[LegacyNote], modules: list[Module]) -> dict[int, list[tuple[LegacyNote, float]]]:
    assignments: dict[int, list[tuple[LegacyNote, float]]] = {m.number: [] for m in modules}
    for note in notes:
        scored = sorted(((module, score_note(note, module)) for module in modules), key=lambda pair: pair[1], reverse=True)
        best_module, best_score = scored[0]
        if best_score >= 0.28:
            assignments[best_module.number].append((note, best_score))
        for module, score in scored[1:]:
            if score >= 0.42 and score >= best_score - 0.08:
                assignments[module.number].append((note, score))
    return assignments


def ensure_archived(path: Path, legacy_dir: Path) -> Path:
    target = legacy_dir / path.name
    counter = 2
    while target.exists():
        target = legacy_dir / f"{path.stem}__{counter}{path.suffix}"
        counter += 1
    shutil.move(str(path), str(target))
    return target


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def demote_legacy_headings(body: str) -> str:
    lines = []
    for line in body.splitlines():
        if line.startswith("#"):
            lines.append("###" + line)
        else:
            lines.append(line)
    return "\n".join(lines)


def build_module_markdown(subject: dict[str, str], module: Module, assigned: list[tuple[LegacyNote, float]]) -> str:
    lines = [
        "---",
        f"title: {yaml_quote(f'M{module.number:02d} — {module.name}')}",
        f"description: {yaml_quote(f'CFA Level I 2026 official module: {module.name}')}",
        f"module: M{module.number:02d}",
        f"subject: {yaml_quote(subject['name'])}",
        f"topic_area: {subject['dir']}",
        "curriculum_year: 2026",
        f"official_module: {yaml_quote(f'Module {module.number}: {module.name}')}",
        "official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25",
        "note_type: official_module_projection",
        "status: active",
        "tags:",
        "  - CFA_L1",
        f"  - {subject['dir']}",
        "  - official_2026",
        "---",
        "",
        f"# M{module.number:02d}: {module.name}",
        "",
        "> This file is aligned to the CFA Institute 2026 Level I module name and order. Legacy local notes were migrated below when a reliable match was found.",
        "",
        "## Official Module Structure",
        "",
    ]
    if module.page_items:
        for item in module.page_items:
            lines.append(f"- {item}")
    else:
        lines.append("- Official page item list not captured in local scrape output.")
    lines.extend(["", "## Learning Outcome Statements", ""])
    if module.los:
        lines.append("The candidate should be able to:")
        lines.append("")
        for item in module.los:
            lines.append(f"- {item}")
    else:
        lines.append("- LOS text was not captured in the local consolidated curriculum file for this subject. Use the official module structure above as the projection anchor.")
    lines.extend(["", "## Local Study Notes", ""])
    if assigned:
        for note, score in sorted(assigned, key=lambda pair: pair[0].original_rel):
            lines.append(f"### Migrated from `{note.original_rel}`")
            lines.append("")
            lines.append(f"_Alignment score: {score:.2f}. Original official module field: {note.official_module or 'not set'}._")
            lines.append("")
            if note.body:
                lines.append(demote_legacy_headings(note.body))
            else:
                lines.append("_Original note had no body content._")
            lines.append("")
    else:
        lines.append("_No legacy local note was confidently matched to this official module yet._")
    lines.extend(
        [
            "## Review Hooks",
            "",
            "- Add mistake-driven traps only after they can be traced back to `.system/events/`.",
            "- Keep module naming and order locked to the official 2026 curriculum registry.",
            "",
        ]
    )
    return "\n".join(lines)


def build_moc(subject: dict[str, str], modules: list[Module]) -> str:
    title_slug = subject["name"].replace(" ", "-")
    description = yaml_quote(f"CFA Level I 2026 official module map for {subject['name']}.")
    lines = [
        "---",
        f"title: {yaml_quote(f'00-{title_slug}-MOC')}",
        f"description: {description}",
        f"subject: {yaml_quote(subject['name'])}",
        f"topic_area: {subject['dir']}",
        "level: CFA Level I",
        "curriculum_year: 2026",
        f"exam_weight: {yaml_quote(subject['weight'])}",
        "note_type: master_moc",
        "status: active",
        "official_source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25",
        "tags:",
        "  - CFA_L1",
        "  - MOC",
        f"  - {subject['dir']}",
        "  - official_2026",
        "---",
        "",
        f"# {subject['name']} MOC",
        "",
        "> Official 2026 Level I projection. Module names, numbers, and order are locked to the CFA Institute Learning Ecosystem scrape generated on 2026-05-25.",
        "",
        "## Official Module Table",
        "",
        "| Module | Official Module | Official Page Items | Chapter File |",
        "|---|---|---|---|",
    ]
    for module in modules:
        file_stem = f"M{module.number:02d}-{slugify(module.name)}"
        item_count = len(module.page_items)
        lines.append(
            f"| M{module.number:02d} | Module {module.number}: {module.name} | {item_count} items | [[{file_stem}]] |"
        )
    lines.extend(["", "## Official Knowledge Tree", "", "```text", f"{subject['name']} ({subject['weight']})"])
    for module in modules:
        lines.append(f"├── M{module.number:02d}: {module.name}")
        for item in module.page_items[:8]:
            lines.append(f"│   ├── {item}")
        if len(module.page_items) > 8:
            lines.append(f"│   └── ... {len(module.page_items) - 8} more page items")
    lines.extend(["```", "", "## Governance Rules", ""])
    lines.extend(
        [
            "- Treat this MOC as a projection of the official 2026 module registry, not as the source of truth.",
            "- Add formulas, traps, and mistake-driven notes only when they trace back to `.system/events/` or `.system/memory/`.",
            "- Do not split or merge official modules in the root subject folder; put legacy or custom breakdowns under `_legacy/`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_registry(subject_modules: dict[str, list[Module]]) -> None:
    registry_dir = ROOT / ".system" / "memory" / "strategy"
    registry_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "generated_at": SYNC_DATE,
        "official_source": "CFA Institute Learning Ecosystem scrape generated 2026-05-25",
        "subjects": {},
    }
    for subject in SUBJECTS:
        modules = subject_modules[subject["name"]]
        data["subjects"][subject["name"]] = {
            "directory": subject["dir"],
            "course_id": subject["course_id"],
            "exam_weight": subject["weight"],
            "module_count": len(modules),
            "modules": [
                {
                    "module": f"M{m.number:02d}",
                    "official_module": f"Module {m.number}: {m.name}",
                    "filename": f"M{m.number:02d}-{slugify(m.name)}.md",
                    "page_items": m.page_items,
                    "los": m.los,
                }
                for m in modules
            ],
        }
    (registry_dir / "cfa-2026-official-module-registry.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_report(summary: list[dict[str, object]]) -> None:
    report = ROOT / ".system" / "memory" / "strategy" / "cfa-2026-official-sync-report.md"
    lines = [
        "---",
        f"generated_at: {SYNC_DATE}",
        "source: CFA Institute Learning Ecosystem scrape, generated 2026-05-25",
        "scope: CFA_tier1 official module projection",
        "---",
        "",
        "# CFA 2026 Official Module Sync Report",
        "",
        "| Subject | Official Modules | Root Files Generated | Legacy Files Archived |",
        "|---|---:|---:|---:|",
    ]
    for item in summary:
        lines.append(
            f"| {item['subject']} | {item['official_modules']} | {item['generated_files']} | {item['archived_files']} |"
        )
    lines.extend(
        [
            "",
            "## Result",
            "",
            "- Each subject root now contains only official 2026 module files plus its MOC.",
            "- Previous root-level module files and MOCs were moved to `_legacy/2026-05-26-official-sync/` under the same subject.",
            "- Generated module files include official page-item structures and migrated local notes when matched.",
            "",
        ]
    )
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    curriculum = parse_curriculum()
    subject_modules: dict[str, list[Module]] = {}
    summary: list[dict[str, object]] = []

    for subject in SUBJECTS:
        modules = curriculum[subject["name"]]
        page_items = parse_page_items(subject["course_id"])
        for module in modules:
            module.page_items = page_items.get(module.number, [])
        subject_modules[subject["name"]] = modules

        subject_dir = CFA_ROOT / subject["dir"]
        subject_dir.mkdir(parents=True, exist_ok=True)
        legacy_dir = subject_dir / "_legacy" / LEGACY_DIR_NAME
        legacy_dir.mkdir(parents=True, exist_ok=True)

        legacy_notes = read_legacy_notes(subject_dir)
        archived = []
        for path in sorted(subject_dir.glob("M*.md")):
            archived.append(ensure_archived(path, legacy_dir))
        moc_path = subject_dir / subject["moc"]
        if moc_path.exists():
            archived.append(ensure_archived(moc_path, legacy_dir))

        assignments = assign_notes(legacy_notes, modules)
        generated = 0
        for module in modules:
            filename = f"M{module.number:02d}-{slugify(module.name)}.md"
            (subject_dir / filename).write_text(
                build_module_markdown(subject, module, assignments[module.number]),
                encoding="utf-8",
            )
            generated += 1

        (subject_dir / subject["moc"]).write_text(build_moc(subject, modules), encoding="utf-8")
        summary.append(
            {
                "subject": subject["name"],
                "official_modules": len(modules),
                "generated_files": generated,
                "archived_files": len(archived),
            }
        )

    write_registry(subject_modules)
    write_report(summary)


if __name__ == "__main__":
    main()
