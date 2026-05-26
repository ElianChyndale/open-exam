"""Rewrite CFA_tier1 with the approved rich Markdown study layout.

This pass keeps the official 2026 registry locked while restoring the dense
study material from legacy notes: Chinese explanations, formulas, comparison
tables, trap tables, decision frameworks, and numbered knowledge trees.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import enrich_cfa_tier1_markdown_layout as base


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / ".system" / "memory" / "strategy" / "cfa-2026-official-module-registry.json"
LEGACY_MAP_PATH = ROOT / ".system" / "memory" / "strategy" / "cfa-legacy-to-official-enrichment-map.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def clean_module_name(official_module: str) -> str:
    return re.sub(r"^Module\s+\d+:\s*", "", official_module).strip()


def module_number(module_id: str) -> int:
    match = re.search(r"(\d+)", module_id)
    return int(match.group(1)) if match else 0


def page_topics(module: dict) -> list[str]:
    return base.parse_page_items(module.get("page_items", []))


def wiki_link(filename: str) -> str:
    return f"[[{Path(filename).stem}]]"


def best_legacy(matches: list[base.LegacyMatch]) -> base.LegacyMatch | None:
    useful = [m for m in matches if m.confidence == "high"]
    if useful:
        return useful[0]
    medium = [m for m in matches if m.confidence == "medium"]
    return medium[0] if medium else (matches[0] if matches else None)


def h2_sections(text: str) -> list[tuple[str, str]]:
    body = strip_frontmatter(text)
    starts = list(re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.M))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(starts):
        start = match.end()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(body)
        title = match.group(1).strip()
        sections.append((title, body[start:end].strip()))
    return sections


def section_by_keywords(text: str, keywords: list[str]) -> str:
    for title, content in h2_sections(text):
        hay = title.lower()
        if any(keyword.lower() in hay for keyword in keywords):
            return content.strip()
    return ""


def clean_heading_title(title: str) -> str:
    title = re.sub(r"^[#\s]+", "", title).strip()
    title = re.sub(r"^[⭐🎯📐⚠️✅❌🏆💡🛠️📋🚨🔄]+\s*", "", title).strip()
    title = re.sub(r"^\d+(\.\d+)*[\.、\s:-]*", "", title).strip()
    title = re.sub(r"^知识点\s*\d+[：:]\s*", "", title).strip()
    return title or "核心内容"


def heading_titles(content: str) -> list[str]:
    titles = []
    for match in re.finditer(r"^###\s+(.+?)\s*$", content, flags=re.M):
        title = clean_heading_title(match.group(1))
        if title and title not in titles:
            titles.append(title)
    return titles[:8]


def renumber_h3(content: str, module_idx: int) -> str:
    lines = content.strip().splitlines()
    output: list[str] = []
    h3_count = 0
    h4_count = 0
    saw_h3 = False
    for line in lines:
        h3 = re.match(r"^###\s+(.+)$", line)
        h4 = re.match(r"^####\s+(.+)$", line)
        if h3:
            h3_count += 1
            h4_count = 0
            saw_h3 = True
            output.append(f"### {module_idx}.{h3_count} {clean_heading_title(h3.group(1))}")
        elif h4:
            h4_count += 1
            title = clean_heading_title(h4.group(1))
            output.append(f"#### {module_idx}.{h3_count}.{h4_count} {title}" if h3_count else f"#### {module_idx}.1.{h4_count} {title}")
        elif not line.startswith("# "):
            output.append(line)
    result = "\n".join(output).strip()
    if not saw_h3 and result:
        return f"### {module_idx}.1 核心内容\n\n{result}\n"
    return result + ("\n" if result else "")


def compact_line(value: str, limit: int = 90) -> str:
    value = re.sub(r"^[>\-\*\s]+", "", value).strip()
    value = re.sub(r"\*\*", "", value)
    value = re.sub(r"\s+", " ", value)
    return value[: limit - 1] + "…" if len(value) > limit else value


def formula_lines(content: str) -> list[str]:
    lines = []
    for line in content.splitlines():
        if ("`" in line or "=" in line or "公式" in line or line.startswith("|")) and line.strip():
            lines.append(line)
    return lines[:30]


def legacy_text_for(match: base.LegacyMatch | None) -> str:
    if not match:
        return ""
    return read_text(match.path)


def legacy_moc_text(subject_dir: Path) -> str:
    path = subject_dir / "_legacy" / "2026-05-26-official-sync" / next(iter([p.name for p in (subject_dir / "_legacy" / "2026-05-26-official-sync").glob("00-*-MOC.md")]), "")
    return read_text(path) if path.exists() else ""


def official_frontmatter(subject: str, subject_data: dict, module: dict, difficulty: str) -> str:
    module_name = clean_module_name(module["official_module"])
    return f"""---
title: "{module['module']}: {module_name}"
description: "CFA Level I 2026 {subject} 官方模块笔记：中文主线、英文术语、编号知识树、公式/框架、考点与陷阱"
subject: "{subject}"
topic_area: "{subject_data['directory']}"
level: "CFA Level I"
exam_year: 2026
exam_weight: "{subject_data.get('exam_weight', '')}"
module: "{module['module']}"
official_module: "{module['official_module']}"
los_count: {len(module.get('los', []))}
difficulty: "{difficulty}"
note_type: official_module_note
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - official_2026
  - {subject_data['directory']}
---
"""


def render_los_table(module_idx: int, los: list[str]) -> str:
    rows = ["| LOS | 官方要求 | 中文学习动作 | 做题输出 |", "|---|---|---|---|"]
    for index, los_text in enumerate(los, 1):
        rows.append(f"| {module_idx}.{index} | {los_text} | {base.los_action(los_text)} | 写出结论、依据、公式口径和限制条件。 |")
    return "\n".join(rows)


def render_terms(subject: str, module_name: str, module: dict) -> str:
    terms = base.english_terms(module_name, page_topics(module), subject)
    if not terms:
        return "- 以官方 LOS 和题库高频英文为准，遇到新术语补充到本节。\n"
    return "\n".join(f"- **{term}（{zh}）**：{explanation}" for term, zh, explanation in terms) + "\n"


def render_tree(module_idx: int, module_name: str, module: dict, legacy_core: str) -> str:
    titles = heading_titles(legacy_core)
    if not titles:
        titles = page_topics(module)[:6]
    if not titles:
        titles = [module_name]
    lines = [f"{module_idx}. {module_name}"]
    for index, title in enumerate(titles[:6], 1):
        number = f"{module_idx}.{index}"
        lines.append(f"├─ {number} {clean_heading_title(title)}")
        lines.append(f"│  ├─ {number}.1 定义/识别：先说清概念、公式变量和适用条件")
        lines.append(f"│  └─ {number}.2 应用/判断：再处理计算、比较、解释或情境选择")
    return "```text\n" + "\n".join(lines) + "\n```\n"


def render_formula_section(subject: str, module_name: str, los: list[str], legacy_formula: str, legacy_core: str) -> str:
    if legacy_formula:
        return renumber_h3(legacy_formula, 5)
    lines = formula_lines(legacy_core)
    if lines:
        return "来自 legacy 核心知识点的公式/计算线索：\n\n" + "\n".join(lines) + "\n"
    rows = base.formula_rows(subject, module_name, los)
    if not rows:
        return f"本模块以概念判断为主，无核心计算公式。复习时重点掌握 **{module_name}** 的定义、触发条件、优缺点和例外情形。\n"
    table = ["| 工具 / Formula | 公式或框架 | 中文解释与注意点 |", "|---|---|---|"]
    for name, formula, note in rows:
        table.append(f"| {name} | `{formula}` | {note} |")
    return "\n".join(table) + "\n"


def render_exam_section(module_idx: int, module_name: str, module: dict, legacy_exam: str) -> str:
    topics = heading_titles(legacy_exam)
    if not topics:
        topics = page_topics(module)[:5]
    if not topics:
        topics = [module_name, "官方 LOS 综合应用"]
    stars = ["⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐⭐", "⭐"]
    rows = ["| 重要性 | 考点 | 解题动作 |", "|---|---|---|"]
    for index, topic in enumerate(topics[:5], 1):
        rows.append(f"| {stars[index-1]} | {module_idx}.{index} {clean_heading_title(topic)} | 先定位题干触发词，再写公式/框架，最后解释结果或判断陷阱。 |")
    result = "\n".join(rows) + "\n"
    if legacy_exam:
        result += "\n### 6.9 ⭐⭐ Legacy 考点补充\n\n" + renumber_h3(legacy_exam, 6)
    return result


def trap_rows_from_content(content: str, subject: str, module_name: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in content.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("|---") or raw.startswith("#"):
            continue
        if raw.startswith("|") and raw.count("|") >= 3:
            cells = [compact_line(c) for c in raw.strip("|").split("|")]
            if len(cells) >= 2 and "错误" not in cells[0] and "正确" not in cells[1]:
                rows.append((cells[0], cells[1], cells[2] if len(cells) > 2 else "按官方定义和 LOS 口径核验。"))
        elif raw.startswith(("-", "*")) or "陷阱" in raw or "易错" in raw or "注意" in raw:
            line_clean = compact_line(raw)
            if line_clean:
                rows.append((f"忽略：{line_clean}", line_clean, "题干通常会用口径、顺序、定义边界或例外条件设置干扰。"))
    if rows:
        return rows[:10]
    return [
        (f"只背 {module_name} 的英文名，不解释中文含义", "用中文说清定义、适用条件和考试动作", "术语题和情境题都会考定义边界。"),
        ("看到公式就直接套，不检查口径", "先检查时间、单位、现金流方向、会计口径或统计假设", "CFA 常把错误藏在输入口径里。"),
        ("把显著性、相关性或高分数直接当成好结论", "还要看经济含义、限制条件和跨模块证据", "数量结果必须回到投资解释。"),
    ]


def render_trap_section(subject: str, module_name: str, legacy_traps: str, legacy_core: str) -> str:
    rows = trap_rows_from_content(legacy_traps or legacy_core, subject, module_name)
    table = ["| ❌ 错误理解 | ✅ 正确理解 | 为什么错 / 考试提醒 |", "|---|---|---|"]
    for wrong, right, why in rows:
        table.append(f"| ❌ {wrong} | ✅ {right} | {why} |")
    return "\n".join(table) + "\n"


def render_cross_section(subject_data: dict, module: dict, legacy_cross: str) -> str:
    modules = subject_data["modules"]
    idx = next(i for i, item in enumerate(modules) if item["module"] == module["module"])
    prev_m = modules[idx - 1] if idx > 0 else None
    next_m = modules[idx + 1] if idx + 1 < len(modules) else None
    rows = [
        f"- **上游模块**：{wiki_link(prev_m['filename']) if prev_m else '本科目起点'}。先用它提供定义、变量或基础框架。",
        f"- **下游模块**：{wiki_link(next_m['filename']) if next_m else '本科目收束模块'}。本模块输出会被后续更复杂题型调用。",
    ]
    if legacy_cross:
        rows.append("\n### Legacy 关联补充\n")
        rows.append(legacy_cross)
    return "\n".join(rows).strip() + "\n"


def render_rich_module(subject: str, subject_data: dict, module: dict, matches: list[base.LegacyMatch]) -> str:
    module_idx = module_number(module["module"])
    module_name = clean_module_name(module["official_module"])
    los = module.get("los", [])
    difficulty = base.detect_difficulty(subject, module_name, los)
    match = best_legacy(matches)
    legacy = legacy_text_for(match)
    legacy_core = section_by_keywords(legacy, ["核心知识点", "知识点详解", "local study notes"])
    legacy_formula = section_by_keywords(legacy, ["关键公式", "公式"])
    legacy_exam = section_by_keywords(legacy, ["常见考点", "解题思路", "考点"])
    legacy_traps = section_by_keywords(legacy, ["易错", "考试陷阱", "陷阱"])
    legacy_cross = section_by_keywords(legacy, ["跨模块", "关联"])

    if not legacy_core:
        legacy_core = "\n".join(
            f"### {module_idx}.{index} {topic}\n\n- **中文主线**：围绕 `{topic}` 掌握定义、适用条件、公式/框架和考试判断。\n- **对应动作**：{base.los_action(los[index-1]) if index <= len(los) else '识别概念并应用到题干。'}\n"
            for index, topic in enumerate(page_topics(module)[:5] or [module_name], 1)
        )
    else:
        legacy_core = renumber_h3(legacy_core, module_idx)

    official_structure = base.render_official_structure(module.get("page_items", []))
    los_list = base.render_los(los)
    legacy_source = f"`{match.path.name}` ({match.confidence}, {match.score})" if match else "无可用 legacy 来源"

    return official_frontmatter(subject, subject_data, module, difficulty) + f"""
# {module['module']}: {module_name}

> **模块定位**：{base.SUBJECT_CORE.get(subject, '')} 本模块聚焦 **{module_name}**，要求把官方 LOS 转成可执行的判断、计算或解释动作。

---

## Official Module Structure

{official_structure}
## Learning Outcome Statements

{los_list}
---

## 1. 模块定位

### {module_idx}.1 学习任务
- **核心问题**：考试希望你用 `{module_name}` 解释什么、计算什么、比较什么，或判断什么。
- **输入信息**：题干事实、数据、假设、时间口径、单位、约束条件。
- **输出结果**：中文结论 + 英文关键术语 + 必要公式/框架 + 限制条件。

### {module_idx}.2 考试角色
- **难度类型**：{difficulty}。
- **高频题型**：定义辨析、情境判断、计算解释、表格补数、跨模块比较。
- **答题原则**：先判断 LOS 动词，再选择工具；计算后必须解释结果含义。

### {module_idx}.3 关键英文术语
{render_terms(subject, module_name, module)}
## 2. 官方 LOS 对应学习目标

{render_los_table(module_idx, los)}

## 3. 核心知识树

{render_tree(module_idx, module_name, module, legacy_core)}
## 4. 知识点详解

{legacy_core.strip()}

## 5. 关键公式与计算框架

{render_formula_section(subject, module_name, los, legacy_formula, legacy_core)}
## 6. 常见考点与解题思路

{render_exam_section(module_idx, module_name, module, legacy_exam)}
## 7. 易错点与考试陷阱

{render_trap_section(subject, module_name, legacy_traps, legacy_core)}
## 8. 跨模块关联

{render_cross_section(subject_data, module, legacy_cross)}

## 9. 复习与刷题提示

- 第一轮：按 `Official Module Structure` 逐节过概念，把每个 LOS 改写成中文任务。
- 第二轮：对照 `## 3. 核心知识树` 做主动回忆，能说出每个编号节点的定义、公式/框架和陷阱。
- 第三轮：刷题后记录错因，如果暴露 MOC 缺口，按 `docs/moc-auto-patch-workflow.md` 进入补强流程。
- 考前：只看术语、公式/框架、易错点和本模块错题，避免重新铺开所有正文。

## 10. Legacy Notes Integrated

- **主要 legacy 来源**：{legacy_source}
- **整合规则**：高置信内容已合入 `知识点详解`、`公式与计算框架`、`常见考点`、`易错陷阱` 和 `跨模块关联`。
- **边界**：若 legacy 内容与 2026 官方 LOS 冲突，以官方 module 名称、LOS 和 registry 为准。
""".rstrip() + "\n"


def moc_frontmatter(subject: str, subject_data: dict) -> str:
    return f"""---
title: "00-{subject}-MOC"
description: "CFA Level I 2026 {subject} 官方模块导航、编号知识树、公式/框架、陷阱与学习路径"
subject: "{subject}"
topic_area: "{subject_data['directory']}"
level: CFA Level I
exam_year: 2026
exam_weight: "{subject_data.get('exam_weight', '')}"
module_count: {len(subject_data['modules'])}
note_type: master_moc
status: active
source: "CFA Institute Learning Ecosystem 2026 registry"
tags:
  - CFA_L1
  - MOC
  - official_2026
  - {subject_data['directory']}
---
"""


def render_moc_tree(subject: str, subject_data: dict, matches_by_module: dict[tuple[str, str], list[base.LegacyMatch]]) -> str:
    lines = [f"{subject} ({subject_data.get('exam_weight', '')})"]
    for module in subject_data["modules"]:
        idx = module_number(module["module"])
        module_name = clean_module_name(module["official_module"])
        match = best_legacy(matches_by_module.get((subject, module["module"]), []))
        legacy_core = section_by_keywords(legacy_text_for(match), ["核心知识点", "知识点详解"]) if match else ""
        titles = heading_titles(legacy_core) or page_topics(module)[:3] or [module_name]
        lines.append(f"├─ {idx}. {module_name}")
        for sub_idx, title in enumerate(titles[:3], 1):
            lines.append(f"│  ├─ {idx}.{sub_idx} {clean_heading_title(title)}")
    return "```text\n" + "\n".join(lines) + "\n```\n"


def render_moc_comparison(subject: str) -> str:
    rows = [
        ("⭐⭐⭐", "概念 vs 应用", "definition vs application", "先确认官方定义，再放入题干情境判断。", "概念题也要能说出适用条件和例外。"),
        ("⭐⭐⭐", "计算 vs 解释", "calculation vs interpretation", "数值只是中间结果，答案要解释方向、含义和限制。", "凡是 calculate and interpret 都不能只算。"),
        ("⭐⭐", "静态知识 vs 决策流程", "static knowledge vs decision process", "把每个模块压缩成输入 -> 工具 -> 输出 -> 陷阱。", "流程化比孤立背诵更抗干扰。"),
        ("⭐⭐⭐", "英文识题 vs 中文理解", "English trigger vs Chinese explanation", "英文用于识别题干，中文用于确认真正含义。", "避免看到熟词就按直觉作答。"),
        ("⭐⭐", "本模块 vs 跨模块", "single module vs cross-module use", "同一公式/概念可能在估值、风险、伦理或报表中换场景出现。", "错题要回填到 MOC 节点。"),
    ]
    table = ["| 重要性 | 对比项 | 英文 | 中文解释 | 考试判断 |", "|---|---|---|---|---|"]
    for row in rows:
        table.append("| " + " | ".join(row) + " |")
    return "\n".join(table) + "\n"


def render_moc_formula(subject: str, legacy_moc: str) -> str:
    formula_section = section_by_keywords(legacy_moc, ["公式", "速查"])
    if formula_section:
        return formula_section.strip() + "\n"
    rows = base.FORMULA_BANK.get(subject, [])
    if not rows:
        return "| 编号 | 框架 | 中文用途 |\n|---|---|---|\n| F1 | 概念判断框架 | 本科目以定义、责任、流程和边界判断为主。 |\n"
    table = ["| 编号 | 工具 / Formula | 中文用途 |", "|---|---|---|"]
    for index, (name, formula, note) in enumerate(rows, 1):
        table.append(f"| F{index} | `{name}: {formula}` | {note} |")
    return "\n".join(table) + "\n"


def render_moc_traps(subject: str, legacy_moc: str) -> str:
    trap_section = section_by_keywords(legacy_moc, ["陷阱", "易错"])
    rows = trap_rows_from_content(trap_section, subject, subject)
    table = ["| ❌ 错误理解 | ✅ 正确理解 | 高频场景 |", "|---|---|---|"]
    for wrong, right, why in rows[:12]:
        table.append(f"| ❌ {wrong} | ✅ {right} | {why} |")
    return "\n".join(table) + "\n"


def render_rich_moc(subject: str, subject_data: dict, matches_by_module: dict[tuple[str, str], list[base.LegacyMatch]]) -> str:
    subject_dir = ROOT / "CFA_tier1" / subject_data["directory"]
    legacy_moc = legacy_moc_text(subject_dir)
    nav = ["| 编号 | 官方 Module | 难度 | 必考点 | 模块链接 |", "|---|---|---|---|---|"]
    for module in subject_data["modules"]:
        module_name = clean_module_name(module["official_module"])
        focus = " / ".join(page_topics(module)[:2]) or "LOS 对齐学习"
        nav.append(f"| {module['module']} | {module_name} | {base.detect_difficulty(subject, module_name, module.get('los', []))} | {focus} | {wiki_link(module['filename'])} |")

    deps = []
    modules = subject_data["modules"]
    for index, module in enumerate(modules):
        module_name = clean_module_name(module["official_module"])
        prev_name = clean_module_name(modules[index - 1]["official_module"]) if index > 0 else "本科目入口"
        next_name = clean_module_name(modules[index + 1]["official_module"]) if index + 1 < len(modules) else "本科目总结"
        deps.append(f"- **{module['module']} {module_name}**：承接 `{prev_name}`，输出到 `{next_name}`。")

    path_note = section_by_keywords(legacy_moc, ["学习路径", "通用分析框架"])

    return moc_frontmatter(subject, subject_data) + f"""
# {subject} MOC

> **一句话核心**：{base.SUBJECT_CORE.get(subject, '')}

---

## 1. 科目定位

- **考试权重**：{subject_data.get('exam_weight', '')}
- **官方模块数**：{len(subject_data['modules'])}
- **主线框架**：{base.SUBJECT_FRAMEWORK.get(subject, '识别概念 -> 应用框架 -> 解释结果 -> 检查限制条件')}
- **使用方式**：先从官方模块导航进入，再用编号知识树做主动回忆，最后用公式/陷阱清单做考前压缩。

## 2. 官方模块导航

{chr(10).join(nav)}

## 3. 核心知识树

{render_moc_tree(subject, subject_data, matches_by_module)}
## 4. 跨模块依赖关系

{chr(10).join(deps)}

## 5. 核心对比专题

{render_moc_comparison(subject)}
## 6. 公式与框架速查

{render_moc_formula(subject, legacy_moc)}
## 7. 高频考试陷阱

{render_moc_traps(subject, legacy_moc)}
## 8. 通用分析框架

{path_note.strip() if path_note else '1. **识别任务**：读 LOS 动词和题干问法。\\n2. **定位节点**：回到 `## 3. 核心知识树` 的编号节点。\\n3. **选择工具**：概念框架、公式、表格比较或合规流程。\\n4. **输出结论**：中文结论 + 英文关键词 + 必要限制条件。\\n5. **复盘缺口**：若错因重复出现，进入 `.system/events/` 和 `.system/memory/` 闭环。'}

## 9. 学习路径建议

- **第一轮：结构对齐**。按模块顺序读官方结构和 LOS，不急着刷难题。
- **第二轮：主动回忆**。遮住解释，只看编号知识树说出定义、公式和陷阱。
- **第三轮：题目驱动**。把错题回填到对应模块和 MOC 节点，形成可复用 fix rule。
- **考前压缩**。只保留高频术语、公式/框架、易错点、跨模块依赖和错题触发点。

## 10. Legacy 内容治理

- 本 MOC 已优先吸收 `_legacy/2026-05-26-official-sync/` 中的中文解释、公式、陷阱和框架。
- `_legacy` 只作为补强来源，不作为最终学习入口；若与官方 2026 LOS 冲突，以 registry 和官方 Topic Outline 为准。
""".rstrip() + "\n"


def update_all() -> None:
    registry = json.loads(read_text(REGISTRY_PATH))
    matches_by_module = base.build_legacy_matches(registry)

    for subject, subject_data in registry["subjects"].items():
        subject_dir = ROOT / "CFA_tier1" / subject_data["directory"]
        for module in subject_data["modules"]:
            path = subject_dir / module["filename"]
            rendered = render_rich_module(subject, subject_data, module, matches_by_module.get((subject, module["module"]), []))
            write_text(path, rendered)

        moc_path = base.moc_filename(subject_dir, subject)
        write_text(moc_path, render_rich_moc(subject, subject_data, matches_by_module))

    write_text(LEGACY_MAP_PATH, base.render_legacy_map(registry, matches_by_module))
    module_count = sum(len(subject_data["modules"]) for subject_data in registry["subjects"].values())
    los_count = sum(len(module.get("los", [])) for subject_data in registry["subjects"].values() for module in subject_data["modules"])
    print(f"Updated rich layout: {len(registry['subjects'])} MOCs and {module_count} modules.")
    print(f"Registry check: {module_count} modules / {los_count} LOS.")


if __name__ == "__main__":
    update_all()
