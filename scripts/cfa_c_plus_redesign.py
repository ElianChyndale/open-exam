from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = REPO_ROOT / "CFA_tier1"
STRATEGY_ROOT = REPO_ROOT / ".system" / "memory" / "strategy"
INDEX_PATH = STRATEGY_ROOT / "cfa-2026-epub-textbook-index.json"
REGISTRY_PATH = STRATEGY_ROOT / "cfa-2026-official-module-registry.json"
AUDIT_PATH = STRATEGY_ROOT / "cfa-c-plus-rollout-audit.md"

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

REGISTRY_SUBJECT_ALIASES = {
    "Equity": "Equity Investments",
}

MOCK_DIR_BY_SUBJECT_DIR = {
    "Alternative_Investments": "AltInv",
    "Corporate_Issuers": "CorpIss",
    "Derivatives": "Derivatives",
    "Economics": "Economics",
    "Equity": "Equity",
    "Ethical_and_Professional_Standards": "Ethics",
    "Financial_Statement_Analysis": "FRA",
    "Fixed_Income": "FI",
    "Portfolio_Management": "Portfolio",
    "Quantitative_Methods": "Quant",
}

MECHANICAL_SECTION_PATTERNS = [
    re.compile(r"(?ms)(?:^|\n)## Textbook Signal Topics\n.*?(?=\n## \d+\.|\n## [^\n]+|\Z)"),
    re.compile(r"(?ms)(?:^|\n)### 教材驱动补强（按原版教材回看）\n.*?(?=\n## |\n### |\Z)"),
    re.compile(r"(?ms)(?:^|\n)### 教材驱动解题动作\n.*?(?=\n## |\n### |\Z)"),
    re.compile(r"(?ms)(?:^|\n)### 教材驱动易错清单\n.*?(?=\n## |\n### |\Z)"),
]

OLD_PATCH_MARKERS = [
    "## Textbook Signal Topics",
    "### 教材驱动补强（按原版教材回看）",
    "### 教材驱动解题动作",
    "### 教材驱动易错清单",
]

MODULE_REQUIRED_SECTIONS = [
    "## 0. Reading Contract 学习契约",
    "## 1. Module Brief 模块定位",
    "## 2. Curriculum Spine 教材正文主线",
    "## 3. Exam Translation 考试翻译",
    "## 4. Formula & Decision Bench 公式与决策台",
    "## 5. Practice & Mock Evidence 题库证据",
    "## 6. Trap Ledger 陷阱账本",
    "## 7. Final Recall Sheet 最后回忆页",
]

MOC_REQUIRED_SECTIONS = [
    "## 1. Subject Brief 科目定位",
    "## 2. Formula & Framework Map 公式与框架地图",
    "## 3. Module Atlas 模块地图",
    "## 4. Curriculum Spine 教材主线",
    "## 5. Exam Routes 做题路线",
    "## 6. Practice & Mock Evidence Map 题库证据地图",
    "## 7. Review Routes 复习路线",
    "## 8. Cross-Subject Interfaces 跨科目接口",
]


@dataclass(frozen=True)
class FormulaFramework:
    name: str
    module: str
    knowledge_node: str
    use_when: str
    do_not_use_when: str
    inputs: str
    output: str
    trap_check: str
    links: str


@dataclass(frozen=True)
class KnowledgeBlock:
    heading: str
    textbook_position: str
    core_meaning: str
    english_terms: str
    why_it_matters: str
    formula_rule: str
    exam_translation: str
    question_triggers: str
    practice_mock_evidence: str
    trap_fix_rule: str


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def load_textbook_index() -> list[dict]:
    return load_json(INDEX_PATH)  # type: ignore[return-value]


def load_registry() -> dict:
    return load_json(REGISTRY_PATH)  # type: ignore[return-value]


def find_subject(index: list[dict], subject: str) -> dict:
    for item in index:
        if item["subject"] == subject:
            return item
    raise ValueError(f"Subject not found in textbook index: {subject}")


def registry_subject_name(subject: str) -> str:
    return REGISTRY_SUBJECT_ALIASES.get(subject, subject)


def is_active_knowledge_file(path: Path) -> bool:
    parts = path.parts
    if len(parts) < 3 or parts[0] != "CFA_tier1":
        return False
    if any(part in {"_legacy", "_archive", "mock", "dashboard"} for part in parts):
        return False
    if parts[1] not in set(SUBJECT_DIRS.values()):
        return False
    filename = path.name
    return bool(re.match(r"00-.*-MOC\.md$", filename) or re.match(r"M\d{2}-.+\.md$", filename))


def remove_mechanical_sections(text: str) -> str:
    cleaned = text
    for pattern in MECHANICAL_SECTION_PATTERNS:
        cleaned = pattern.sub("\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + "\n"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---", 4)
    if end == -1:
        return "", text
    frontmatter = text[: end + len("\n---")]
    body = text[end + len("\n---") :].lstrip()
    return frontmatter, body


def clean_anchor(anchor: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.\s*", "", anchor).strip()


def anchor_number(anchor: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+)*)\.", anchor)
    return match.group(1) if match else ""


def anchor_depth(anchor: str) -> int:
    number = anchor_number(anchor)
    return number.count(".") + 1 if number else 1


def english_terms(title: str) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", title)
    seen: list[str] = []
    for word in words:
        key = word.lower()
        if key not in {item.lower() for item in seen}:
            seen.append(word)
    return "; ".join(seen[:10]) if seen else title


def markdown_link(path: Path) -> str:
    return f"[[{path.stem}]]"


def subject_tagline(subject: str) -> str:
    taglines = {
        "Quantitative Methods": "把投资问题翻译成收益率、现金流、概率、统计推断和模型证据。",
        "Economics": "把企业、经济周期、政策、贸易和汇率转成投资环境判断。",
        "Corporate Issuers": "把公司组织、治理、营运资本、资本配置和融资结构转成企业决策证据。",
        "Financial Statement Analysis": "把财务报表转成可比较、可预测、可质疑的经营证据。",
        "Equity": "把市场结构、行业公司分析和估值工具转成权益投资判断。",
        "Fixed Income": "把债券现金流、收益率、利率风险、信用风险和证券化结构转成定价与风险判断。",
        "Derivatives": "把远期、期货、互换和期权转成无套利、复制和估值语言。",
        "Alternative Investments": "把私募、实物资产、对冲基金和数字资产转成结构、回报和风险判断。",
        "Portfolio Management": "把资产风险收益、组合构建、行为偏差和风险管理转成投资流程。",
        "Ethical and Professional Standards": "把职业标准、客户义务、市场诚信和 GIPS 转成情境判断规则。",
    }
    return taglines.get(subject, "把官方教材结构转成可执行的考试知识地图。")


def practice_file_for_subject(subject_dir: str) -> Path | None:
    directory = VAULT_ROOT / subject_dir
    matches = sorted(directory.glob("00-*-Practice-Questions.md"))
    return matches[0] if matches else None


def mock_file_for_subject(subject_dir: str) -> Path | None:
    mock_dir = MOCK_DIR_BY_SUBJECT_DIR.get(subject_dir)
    if not mock_dir:
        return None
    directory = VAULT_ROOT / "mock" / mock_dir
    matches = sorted(directory.glob("00-*-Mock-Questions.md"))
    return matches[0] if matches else None


def table_cells(line: str) -> list[str]:
    if not line.strip().startswith("|") or "---" in line:
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_formula_section(text: str) -> str:
    match = re.search(r"(?ms)^## 5\..*?(?=^## \d+\.|\Z)", text)
    return match.group(0) if match else ""


def formula_entries_from_module(path: Path, module: dict, signal_topics: list[str]) -> list[FormulaFramework]:
    text = path.read_text(encoding="utf-8")
    formula_section = extract_formula_section(text)
    entries: list[FormulaFramework] = []
    seen: set[str] = set()
    for line in formula_section.splitlines():
        cells = table_cells(line)
        if len(cells) < 2:
            continue
        first = cells[0]
        if first.lower() in {"公式", "指标", "formula", "metric", "题干触发"}:
            continue
        if len(first) > 90:
            continue
        formula = cells[1]
        context = cells[2] if len(cells) >= 3 else module["official_module"]
        key = (first + formula).lower()
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            FormulaFramework(
                name=first,
                module=module["module"],
                knowledge_node=nearest_signal(first, signal_topics),
                use_when=f"题干要求 `{first}` 对应的计算、比较或解释，并且输入口径与本模块一致。",
                do_not_use_when="题干目标、时间口径、现金流方向、会计口径或统计假设不匹配时，先回到对应教材小节重新选工具。",
                inputs=context,
                output=formula,
                trap_check="先检查变量定义、单位、方向、时间口径和题目是否要求解释结果。",
                links=markdown_link(path),
            )
        )
    if entries:
        return entries[:14]
    return framework_entries_from_signals(path, module, signal_topics)


def nearest_signal(name: str, signal_topics: list[str]) -> str:
    lowered = name.lower()
    for signal in signal_topics:
        clean = clean_anchor(signal)
        if clean.lower() in lowered or any(word.lower() in clean.lower() for word in re.findall(r"[A-Za-z]{4,}", name)[:2]):
            return signal
    return signal_topics[0] if signal_topics else "Module framework"


def framework_entries_from_signals(path: Path, module: dict, signal_topics: list[str]) -> list[FormulaFramework]:
    selected = signal_topics[:8] or [module["official_module"]]
    entries: list[FormulaFramework] = []
    for signal in selected:
        title = clean_anchor(signal)
        entries.append(
            FormulaFramework(
                name=f"{title} framework",
                module=module["module"],
                knowledge_node=signal,
                use_when=f"题干围绕 `{title}` 的定义、分类、流程、比较或情境判断展开。",
                do_not_use_when="题干已经转向另一个教材小节、跨模块公式或更具体的例外条件。",
                inputs="题干事实、官方术语、LOS 动词、相关限制条件。",
                output="中文判断结论 + English term + 必要的比较口径或流程步骤。",
                trap_check="不要只认熟词；先说清定义边界、适用条件和容易混淆的相邻概念。",
                links=markdown_link(path),
            )
        )
    return entries


def render_formula_framework_map(entries: Iterable[FormulaFramework]) -> str:
    grouped: dict[str, list[FormulaFramework]] = {}
    for entry in entries:
        grouped.setdefault(entry.module, []).append(entry)
    lines = [
        "## 2. Formula & Framework Map 公式与框架地图",
        "",
        "> MOC 的第一核心是公式与框架地图：先知道有什么工具、什么时候用、什么时候不能用，再回到模块正文学习细节。",
        "",
    ]
    for module in sorted(grouped):
        lines.extend(
            [
                f"### {module}",
                "",
                "| Formula / Framework | Knowledge Node | Use When | Do Not Use When | Inputs | Output | Trap Check | Links |",
                "|---|---|---|---|---|---|---|---|",
            ]
        )
        for entry in grouped[module]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        sanitize_cell(entry.name),
                        sanitize_cell(entry.knowledge_node),
                        sanitize_cell(entry.use_when),
                        sanitize_cell(entry.do_not_use_when),
                        sanitize_cell(entry.inputs),
                        sanitize_cell(entry.output),
                        sanitize_cell(entry.trap_check),
                        sanitize_cell(entry.links),
                    ]
                )
                + " |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def sanitize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("|", "/")).strip()


def render_knowledge_block(block: KnowledgeBlock) -> str:
    return f"""### {block.heading}

**Textbook Position**: {block.textbook_position}

**Core Meaning 中文解释**: {block.core_meaning}

**English Terms**: {block.english_terms}

**Why It Matters**: {block.why_it_matters}

**Formula / Rule**: {block.formula_rule}

**Exam Translation**: {block.exam_translation}

**Question Triggers**: {block.question_triggers}

**Practice / Mock Evidence**: {block.practice_mock_evidence}

**Trap & Fix Rule**: {block.trap_fix_rule}
"""


def build_knowledge_block(subject: str, module: dict, signal: str, formulas: list[FormulaFramework]) -> KnowledgeBlock:
    title = clean_anchor(signal)
    number = anchor_number(signal)
    matching_formula = next((entry for entry in formulas if clean_anchor(entry.knowledge_node).lower() == title.lower()), None)
    depth_note = "主干框架" if anchor_depth(signal) <= 2 else "细节口径"
    formula_rule = matching_formula.output if matching_formula else "先确认定义边界、输入条件、比较对象和例外条件；若涉及计算，再进入本模块 Formula & Decision Bench。"
    return KnowledgeBlock(
        heading=f"{number + ' ' if number else ''}{title} / 教材小节精讲",
        textbook_position=f"{subject} {module['official_module']} | {signal}",
        core_meaning=f"本节把 `{title}` 放在 `{module['official_module']}` 的 {depth_note} 中理解。学习时先用中文说清它解决什么问题，再保留 English terms 用于识别题干。",
        english_terms=english_terms(title),
        why_it_matters=f"它连接本模块 LOS 与考试输出：题目不会只考标题，而会要求你解释、计算、比较、评价或在情境中选择正确框架。",
        formula_rule=formula_rule,
        exam_translation=f"看到 `{title}` 或同义表述时，先定位本小节，再判断题目要 definition、calculation、comparison、interpretation 还是 exception。",
        question_triggers=f"`{title}`；{english_terms(title)}；LOS 动词；题干里的时间口径、条件限制、比较对象或情境变化。",
        practice_mock_evidence="基础题用于检验定义和单点口径；mock 更常把本节与相邻知识点组合，要求先定位本小节再排除干扰。",
        trap_fix_rule=f"不要把 `{title}` 当成孤立术语背诵；下次做题先写一句“它是什么、什么时候用、和什么容易混”。",
    )


def render_module(
    subject: str,
    subject_index: dict,
    registry_subject: dict,
    module: dict,
    module_index: dict,
    path: Path,
    formulas: list[FormulaFramework],
) -> str:
    original = remove_mechanical_sections(path.read_text(encoding="utf-8"))
    frontmatter, _ = split_frontmatter(original)
    practice_file = practice_file_for_subject(registry_subject["directory"])
    mock_file = mock_file_for_subject(registry_subject["directory"])
    signals = module_index.get("signal_topics", [])
    blocks = "\n".join(build_knowledge_block(subject, module, signal, formulas) for signal in signals)
    los_lines = "\n".join(f"{idx}. {los}" for idx, los in enumerate(module.get("los", []), start=1))
    formula_bench = render_module_formula_bench(formulas, signals)
    title = f"{module['module']}: {module['official_module'].replace('Module ' + str(int(module['module'][1:])) + ': ', '')}"
    body = f"""# {title}

> **Reading Contract 学习契约**：本页按原版教材小节重写，再把每个知识点翻译成考试动作。中文负责理解，English terms 负责识题、公式和官方概念。

---

## 0. Reading Contract 学习契约

- **Official module**: {module['official_module']}
- **Textbook source**: V{subject_index['volume']} `{Path(subject_index['epub']).name}`
- **Practice / Solutions**: {"available" if module_index.get("practice_href") else "not listed"} / {"available" if module_index.get("solutions_href") else "not listed"}
- **Learning output**: 读完本页后，要能把教材小节转成 definition、calculation、comparison、interpretation、trap check 五类考试动作。

## 1. Module Brief 模块定位

- **Subject**: {subject}
- **Module**: {module['module']}
- **中文定位**：{subject_tagline(subject)}
- **Cross-link rule**: 先用本模块定位题干，再回到 MOC 的 `Formula & Framework Map` 检查工具选择是否正确。

### Learning Outcome Statements

{los_lines if los_lines else "- Registry did not list LOS for this module."}

## 2. Curriculum Spine 教材正文主线

{blocks if blocks else "### Module Framework / 教材主线\n\n本模块没有从 ePub index 抽到细分小节；复习时以官方 LOS、模块标题和题库证据为主。"}

## 3. Exam Translation 考试翻译

| Exam Input | First Decision | Action | Output |
|---|---|---|---|
| 官方术语或教材小节标题 | 它对应哪个 textbook section 和 LOS 动词 | 回到 `Curriculum Spine` 的知识块 | 中文解释 + English term |
| 计算数据、表格或比率 | 是否满足公式输入条件 | 到 `Formula & Decision Bench` 选工具 | 数值 + 口径说明 |
| 两个相似概念 | 比较对象、适用条件、例外是否不同 | 写出 definition boundary 和 decision rule | 对比结论 |
| 情境判断题 | 题干事实触发哪个限制条件 | 先定位小节，再排除相邻概念 | 判断 + 原因 |
| mock 组合题 | 是否跨模块或跨科目 | 先处理本模块核心动作，再补 supporting detail | 分步答案 |

## 4. Formula & Decision Bench 公式与决策台

{formula_bench}

## 5. Practice & Mock Evidence 题库证据

- **Practice page**: {markdown_link(practice_file) if practice_file else "No practice page found yet."}
- **Mock page**: {markdown_link(mock_file) if mock_file else "No mock page found yet."}
- **Evidence rule**: 题库证据先归入本页某个 textbook section；无法高置信归类时保留在 mock unclassified，不硬塞。
- **Reflection rule**: 如果题目暴露的是知识缺口，回到本页知识块补定义和公式；如果暴露的是过程偏差，进入 `.system/events/bias/` 或相关 review。

## 6. Trap Ledger 陷阱账本

| Trap Source | Common Misread | Fix Rule |
|---|---|---|
| Textbook title familiarity | 看到熟悉 English term 就直接选答案 | 先用中文说清定义边界，再看题干条件 |
| Formula memory | 只记公式，不检查输入口径 | 检查单位、时间、现金流方向、会计口径或统计假设 |
| Adjacent concepts | 把相邻小节的规则混用 | 回到 `Textbook Position`，确认题目真正问哪一节 |
| Mock pressure | 组合题里先处理了 supporting detail | 先处理 LOS 主动作，再补其他细节 |

## 7. Final Recall Sheet 最后回忆页

- **One-minute map**: {", ".join(clean_anchor(signal) for signal in signals[:8])}
- **Before calculation**: 写出输入、口径、单位、时点和限制条件。
- **Before selection**: 判断题目要 definition、calculation、comparison、interpretation 还是 exception。
- **After answer**: 用一句中文解释结果，再保留关键 English term 方便回链。
"""
    return (frontmatter.rstrip() + "\n\n" + body).strip() + "\n" if frontmatter else body.strip() + "\n"


def render_module_formula_bench(formulas: list[FormulaFramework], signals: list[str]) -> str:
    if not formulas:
        formulas = framework_entries_from_signals(Path("module.md"), {"module": "", "official_module": "Module"}, signals)
    lines = [
        "| Formula / Framework | Use When | Do Not Use When | Inputs | Output | Trap Check |",
        "|---|---|---|---|---|---|",
    ]
    for entry in formulas:
        lines.append(
            "| "
            + " | ".join(
                [
                    sanitize_cell(entry.name),
                    sanitize_cell(entry.use_when),
                    sanitize_cell(entry.do_not_use_when),
                    sanitize_cell(entry.inputs),
                    sanitize_cell(entry.output),
                    sanitize_cell(entry.trap_check),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_moc(subject: str, subject_index: dict, registry_subject: dict, formula_entries: list[FormulaFramework]) -> str:
    moc_path = REPO_ROOT / subject_index["moc_path"]
    frontmatter, _ = split_frontmatter(moc_path.read_text(encoding="utf-8"))
    subject_dir = registry_subject["directory"]
    practice_file = practice_file_for_subject(subject_dir)
    mock_file = mock_file_for_subject(subject_dir)
    modules_by_id = {item["module"]: item for item in subject_index["modules"]}
    formula_map = render_formula_framework_map(formula_entries)
    atlas_lines = [
        "| Module | Official Module | Textbook Chapter | Core Task | Main Formulas / Frameworks | Practice / Mock / Module |",
        "|---|---|---|---|---|---|",
    ]
    for module in registry_subject["modules"]:
        module_index = modules_by_id[module["module"]]
        module_path = VAULT_ROOT / subject_dir / module["filename"]
        module_formulas = [entry.name for entry in formula_entries if entry.module == module["module"]]
        anchors = "；".join(clean_anchor(anchor) for anchor in module_index.get("signal_topics", [])[:4])
        links = f"{markdown_link(module_path)}"
        if practice_file:
            links += f" / {markdown_link(practice_file)}"
        if mock_file:
            links += f" / {markdown_link(mock_file)}"
        atlas_lines.append(
            "| "
            + " | ".join(
                [
                    module["module"],
                    sanitize_cell(module["official_module"]),
                    sanitize_cell(module_index["official_module"]),
                    sanitize_cell(anchors),
                    sanitize_cell("；".join(module_formulas[:5]) if module_formulas else anchors),
                    links,
                ]
            )
            + " |"
        )
    body = f"""# {subject} MOC

> **一句话核心**：{subject_tagline(subject)}

---

## 1. Subject Brief 科目定位

- **Exam weight**: {registry_subject.get("exam_weight", "See official registry")}
- **Official modules**: {len(registry_subject["modules"])}
- **Textbook volume**: V{subject_index['volume']} `{Path(subject_index['epub']).name}`
- **Primary use**: 先用 `Formula & Framework Map` 选工具，再进入 Module 页学习教材小节和题库证据。
- **Bilingual rule**: 中文负责理解和判断；English terms 负责识题、LOS、公式和官方概念。

{formula_map}
## 3. Module Atlas 模块地图

{chr(10).join(atlas_lines)}

## 4. Curriculum Spine 教材主线

{render_curriculum_spine(subject_index)}

## 5. Exam Routes 做题路线

- **Definition route**: 看到官方术语，先定位 textbook section，再用中文说清 definition boundary。
- **Calculation route**: 先检查输入、单位、时点、现金流方向、会计口径或统计假设，再选公式。
- **Comparison route**: 先问比较对象和适用条件，再写出差异、例外和考试判断。
- **Interpretation route**: 数值只是中间结果，答案必须回到 economic meaning、reporting implication、risk or decision implication。
- **Mock route**: 组合题先处理 LOS 主动作，再补 supporting detail；不确定归类的题保留在 unclassified。

## 6. Practice & Mock Evidence Map 题库证据地图

- **Practice page**: {markdown_link(practice_file) if practice_file else "No practice page found yet."}
- **Mock page**: {markdown_link(mock_file) if mock_file else "No mock page found yet."}
- **Unclassified mock**: [[00-Mock-Unclassified]]
- **Evidence rule**: 题库证据优先回填到 Module 的 textbook knowledge block，再进入错题/偏差/agent 事件层。

## 7. Review Routes 复习路线

- **First pass**: 按 Module Atlas 顺序进入正文，确保每个教材小节都能用中文讲清。
- **Formula pass**: 只看本页 `Formula & Framework Map`，逐条回答 use / do not use / inputs / trap。
- **Mock prep**: 先看高密度公式和框架模块，再看 Practice & Mock Evidence。
- **Mistake repair**: 错题先定位 formula/framework，再进入对应 Module 的 Trap Ledger 和 Final Recall Sheet。

## 8. Cross-Subject Interfaces 跨科目接口

- **Quantitative Methods**: return, probability, inference, regression and model-risk language feed valuation, portfolio and reporting analysis.
- **Financial Statement Analysis / Corporate Issuers**: reporting choices, ratios, cash flow and capital allocation connect to equity and credit analysis.
- **Equity / Fixed Income / Derivatives**: valuation and risk tools connect through discount rates, cash flows, arbitrage and replication.
- **Portfolio / Alternatives / Ethics**: investment process, product structure, client duty and governance constraints shape final decisions.
"""
    return (frontmatter.rstrip() + "\n\n" + body).strip() + "\n" if frontmatter else body.strip() + "\n"


def render_curriculum_spine(subject_index: dict) -> str:
    lines: list[str] = []
    for module in subject_index["modules"]:
        anchors = "；".join(clean_anchor(anchor) for anchor in module.get("signal_topics", [])[:8])
        lines.append(f"- **{module['module']} {module['official_module']}**: {anchors}")
    return "\n".join(lines)


def module_indexes_by_id(subject_index: dict) -> dict[str, dict]:
    return {module["module"]: module for module in subject_index["modules"]}


def build_subject_formula_entries(subject: str, subject_index: dict, registry_subject: dict) -> dict[str, list[FormulaFramework]]:
    entries_by_module: dict[str, list[FormulaFramework]] = {}
    index_by_id = module_indexes_by_id(subject_index)
    for module in registry_subject["modules"]:
        module_path = VAULT_ROOT / registry_subject["directory"] / module["filename"]
        module_index = index_by_id[module["module"]]
        entries_by_module[module["module"]] = formula_entries_from_module(
            module_path,
            module,
            module_index.get("signal_topics", []),
        )
    return entries_by_module


def rollout_all() -> list[Path]:
    index = load_textbook_index()
    registry = load_registry()
    written: list[Path] = []
    for subject_index in index:
        subject = subject_index["subject"]
        registry_subject = registry["subjects"][registry_subject_name(subject)]
        entries_by_module = build_subject_formula_entries(subject, subject_index, registry_subject)
        all_entries = [entry for entries in entries_by_module.values() for entry in entries]
        moc_path = REPO_ROOT / subject_index["moc_path"]
        assert is_active_knowledge_file(moc_path.relative_to(REPO_ROOT))
        moc_path.write_text(render_moc(subject, subject_index, registry_subject, all_entries), encoding="utf-8")
        written.append(moc_path)
        index_by_id = module_indexes_by_id(subject_index)
        for module in registry_subject["modules"]:
            module_path = VAULT_ROOT / registry_subject["directory"] / module["filename"]
            relative = module_path.relative_to(REPO_ROOT)
            assert is_active_knowledge_file(relative), f"Refusing to write inactive path: {relative}"
            module_text = render_module(
                subject,
                subject_index,
                registry_subject,
                module,
                index_by_id[module["module"]],
                module_path,
                entries_by_module[module["module"]],
            )
            module_path.write_text(module_text, encoding="utf-8")
            written.append(module_path)
    write_rollout_audit(written)
    return written


def audit_markdown(text: str, required_sections: list[str]) -> dict[str, list[str]]:
    return {
        "missing_required_sections": [section for section in required_sections if section not in text],
        "old_patch_markers": [marker for marker in OLD_PATCH_MARKERS if marker in text],
    }


def write_rollout_audit(written: list[Path]) -> Path:
    moc_missing: list[str] = []
    module_missing: list[str] = []
    old_markers: list[str] = []
    inactive_written = [str(path.relative_to(REPO_ROOT)) for path in written if not is_active_knowledge_file(path.relative_to(REPO_ROOT))]
    for path in written:
        text = path.read_text(encoding="utf-8")
        required = MOC_REQUIRED_SECTIONS if path.name.startswith("00-") else MODULE_REQUIRED_SECTIONS
        result = audit_markdown(text, required)
        relative = str(path.relative_to(REPO_ROOT))
        if result["missing_required_sections"]:
            target = moc_missing if path.name.startswith("00-") else module_missing
            target.append(f"{relative}: {result['missing_required_sections']}")
        if result["old_patch_markers"]:
            old_markers.append(f"{relative}: {result['old_patch_markers']}")
    lines = [
        "# C+ Rollout Audit",
        "",
        "- Scope: all active CFA_tier1 subject MOCs and Module pages",
        "- Excluded: `_legacy/`, `_archive/`, `mock/`, `dashboard/`, practice question pages",
        f"- Written files: {len(written)}",
        f"- MOC files: {sum(1 for path in written if path.name.startswith('00-'))}",
        f"- Module files: {sum(1 for path in written if re.match(r'M\\d{{2}}-', path.name))}",
        "",
        "## Results",
        "",
        f"- Inactive paths written: `{inactive_written}`",
        f"- MOC missing required sections: `{moc_missing}`",
        f"- Module missing required sections: `{module_missing}`",
        f"- Old patch markers: `{old_markers}`",
        "",
        "## Review Focus",
        "",
        "- Open each subject MOC and inspect `Formula & Framework Map` first.",
        "- Open representative modules and confirm textbook sections now live inside `Curriculum Spine` rather than as a tail table.",
        "- Keep unclassified mock items separate until high-confidence mapping is available.",
    ]
    AUDIT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return AUDIT_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="C+ CFA knowledge-base redesign tools")
    parser.add_argument("--rollout-all", action="store_true")
    parser.add_argument("--audit-all", action="store_true")
    args = parser.parse_args()
    if args.rollout_all:
        written = rollout_all()
        print(f"wrote {len(written)} active MOC/module files")
        print(f"audit {AUDIT_PATH.relative_to(REPO_ROOT)}")
    elif args.audit_all:
        index = load_textbook_index()
        registry = load_registry()
        paths: list[Path] = []
        for subject_index in index:
            registry_subject = registry["subjects"][registry_subject_name(subject_index["subject"])]
            paths.append(REPO_ROOT / subject_index["moc_path"])
            for module in registry_subject["modules"]:
                paths.append(VAULT_ROOT / registry_subject["directory"] / module["filename"])
        write_rollout_audit(paths)
        print(f"audit {AUDIT_PATH.relative_to(REPO_ROOT)}")
    else:
        parser.error("Use --rollout-all or --audit-all")


if __name__ == "__main__":
    main()
