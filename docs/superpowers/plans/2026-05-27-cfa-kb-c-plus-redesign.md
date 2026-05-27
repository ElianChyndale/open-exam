# CFA Knowledge Base C+ Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a C+ CFA Level I knowledge-base redesign pipeline and first prototype for Quantitative Methods MOC plus M01, with MOC `Formula & Framework Map` as the highest-priority artifact.

**Architecture:** Add a focused Python implementation script that reads existing official registry/index assets, avoids `_legacy/` and `_archive/`, rewrites only approved active files, and produces audit reports before any full-batch rollout. The first implementation milestone creates a reviewable prototype for `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md` and `CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md`.

**Tech Stack:** Python 3.11 standard library, Markdown files, existing `.system/memory/strategy/cfa-2026-epub-textbook-index.json`, existing practice/mock markdown files, `pytest`.

---

## File Structure

Create:

- `scripts/cfa_c_plus_redesign.py`  
  Single entry point for C+ prototype generation, old mechanical-section cleanup, active-file discovery, and audits.

- `.system/tests/test_cfa_c_plus_redesign.py`  
  Unit tests for active-file filtering, old-section cleanup, MOC formula-map rendering, Module knowledge-block rendering, and audit behavior.

- `.system/memory/strategy/cfa-c-plus-prototype-audit.md`  
  Generated audit report after the Quant MOC + M01 prototype is produced.

Modify in Phase 1 prototype only:

- `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`  
  Rebuild MOC around `Formula & Framework Map` first, then Module Atlas, Curriculum Spine, Exam Routes, Evidence Map, Review Routes, and Cross-Subject Interfaces.

- `CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md`  
  Replace mechanical textbook-signal and supplement-table sections with C+ Module structure and textbook-section knowledge blocks.

Do not modify:

- Any path containing `_legacy`
- Any path containing `_archive`
- Any files under `CFA_tier1/mock/` during Phase 1
- Any files under `CFA_tier1/dashboard/` during Phase 1

---

## Task 1: Add C+ Test Harness

**Files:**

- Create: `.system/tests/test_cfa_c_plus_redesign.py`
- Create later in Task 2: `scripts/cfa_c_plus_redesign.py`

- [ ] **Step 1: Write failing tests for active path filtering and old-section cleanup**

Create `.system/tests/test_cfa_c_plus_redesign.py` with:

```python
from pathlib import Path

from scripts.cfa_c_plus_redesign import is_active_knowledge_file, remove_mechanical_sections


def test_is_active_knowledge_file_excludes_legacy_archive_mock_dashboard():
    assert is_active_knowledge_file(Path("CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/Quantitative_Methods/_legacy/M01-Rates-and-Returns.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/Economics/_archive/M01-The-Firm-and-Market-Structures.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/mock/Quant/00-Quant-Mock-Questions.md"))
    assert not is_active_knowledge_file(Path("CFA_tier1/dashboard/Subject-Question-Banks.md"))


def test_remove_mechanical_sections_deletes_previous_patch_blocks():
    source = """# M01

## Textbook Signal Topics

- Textbook volume: `V1`

## 1. 模块定位

Body stays.

### 教材驱动补强（按原版教材回看）

| 教材锚点 | 回看重点 |
|---|---|

## 5. 关键公式与计算框架

Formula stays.

### 教材驱动解题动作

- old action

## 7. 易错点与考试陷阱

Trap stays.

### 教材驱动易错清单

| 易错来源 | 常见误判 |
|---|---|

## 8. 复习安排

End stays.
"""
    cleaned = remove_mechanical_sections(source)
    assert "## Textbook Signal Topics" not in cleaned
    assert "教材驱动补强" not in cleaned
    assert "教材驱动解题动作" not in cleaned
    assert "教材驱动易错清单" not in cleaned
    assert "Body stays." in cleaned
    assert "Formula stays." in cleaned
    assert "Trap stays." in cleaned
    assert "End stays." in cleaned
```

- [ ] **Step 2: Run tests and verify they fail because the script does not exist yet**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py -q
```

Expected:

```text
ModuleNotFoundError: No module named 'scripts.cfa_c_plus_redesign'
```

- [ ] **Step 3: Commit the failing tests**

```powershell
git add -- .system/tests/test_cfa_c_plus_redesign.py
git commit -m "test: define C+ redesign safety behavior"
```

---

## Task 2: Implement Core Safety Helpers

**Files:**

- Create: `scripts/cfa_c_plus_redesign.py`
- Test: `.system/tests/test_cfa_c_plus_redesign.py`

- [ ] **Step 1: Add minimal helper implementation**

Create `scripts/cfa_c_plus_redesign.py` with:

```python
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
    blocked_parts = { "_legacy", "_archive", "mock", "dashboard" }
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
```

- [ ] **Step 2: Run tests and verify helper tests pass**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 3: Commit helper implementation**

```powershell
git add -- scripts/cfa_c_plus_redesign.py .system/tests/test_cfa_c_plus_redesign.py
git commit -m "feat: add C+ redesign safety helpers"
```

---

## Task 3: Add MOC Formula & Framework Renderer

**Files:**

- Modify: `scripts/cfa_c_plus_redesign.py`
- Modify: `.system/tests/test_cfa_c_plus_redesign.py`

- [ ] **Step 1: Add failing renderer test**

Append to `.system/tests/test_cfa_c_plus_redesign.py`:

```python
from scripts.cfa_c_plus_redesign import FormulaFramework, render_formula_framework_map


def test_render_formula_framework_map_prioritizes_use_and_do_not_use_rules():
    entries = [
        FormulaFramework(
            name="Holding Period Return (HPR)",
            module="M01",
            knowledge_node="3.1 Holding Period Return",
            use_when="题干给出期初价格、期末价格和期间收入，要求单一持有期总回报。",
            do_not_use_when="题干要求多期复合增长、经理绩效或投资者现金流体验。",
            inputs="P0, P1, D1；价格和收入必须使用同一货币和同一持有期。",
            output="HPR = (P1 - P0 + D1) / P0。",
            trap_check="确认 D1 没有已经包含在 ending value 中。",
            links="[[M01-Rates-and-Returns]]",
        )
    ]
    rendered = render_formula_framework_map(entries)
    assert rendered.startswith("## 2. Formula & Framework Map 公式与框架地图")
    assert "Do Not Use When" in rendered
    assert "Holding Period Return (HPR)" in rendered
    assert "确认 D1" in rendered
```

- [ ] **Step 2: Run renderer test and verify it fails**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py::test_render_formula_framework_map_prioritizes_use_and_do_not_use_rules -q
```

Expected:

```text
ImportError: cannot import name 'FormulaFramework'
```

- [ ] **Step 3: Implement renderer data model and Markdown output**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
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


def render_formula_framework_map(entries: Iterable[FormulaFramework]) -> str:
    lines = [
        "## 2. Formula & Framework Map 公式与框架地图",
        "",
        "> MOC 的第一核心是公式与框架地图：先知道有什么工具、什么时候用、什么时候不能用，再回到模块正文学习细节。",
        "",
        "| Formula / Framework | Module | Knowledge Node | Use When | Do Not Use When | Inputs | Output | Trap Check | Links |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    entry.name,
                    entry.module,
                    entry.knowledge_node,
                    entry.use_when,
                    entry.do_not_use_when,
                    entry.inputs,
                    entry.output,
                    entry.trap_check,
                    entry.links,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"
```

- [ ] **Step 4: Run tests and verify pass**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commit renderer**

```powershell
git add -- scripts/cfa_c_plus_redesign.py .system/tests/test_cfa_c_plus_redesign.py
git commit -m "feat: render C+ MOC formula framework map"
```

---

## Task 4: Build Quant MOC Prototype Content

**Files:**

- Modify: `scripts/cfa_c_plus_redesign.py`
- Modify: `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`
- Test: `.system/tests/test_cfa_c_plus_redesign.py`

- [ ] **Step 1: Add Quant formula/framework source entries**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
QUANT_FORMULA_FRAMEWORKS = [
    FormulaFramework(
        name="Holding Period Return (HPR)",
        module="M01",
        knowledge_node="3.1 Holding Period Return",
        use_when="题干给出期初价格、期末价格和期间收入，要求单一持有期总回报。",
        do_not_use_when="题干要求多期复合增长、经理绩效或投资者现金流体验。",
        inputs="P0, P1, D1；同一货币、同一持有期。",
        output="HPR = (P1 - P0 + D1) / P0。",
        trap_check="确认 D1 没有已经包含在 ending value 中。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Arithmetic Mean Return",
        module="M01",
        knowledge_node="3.2 Arithmetic or Mean Return",
        use_when="题干要求单期 expected return 或历史收益率的简单平均。",
        do_not_use_when="题干要求多期复合财富增长或 CAGR。",
        inputs="每期 return；各期权重相等，除非题干另给概率。",
        output="Arithmetic mean = sum(Ri) / n。",
        trap_check="算术平均通常高于几何平均，不能代表长期复合增长。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Geometric Mean Return",
        module="M01",
        knowledge_node="3.3 Geometric Mean Return",
        use_when="题干要求多期 compound growth、CAGR 或 historical growth rate。",
        do_not_use_when="题干问下一期 expected return 或概率加权期望。",
        inputs="每期 gross return = 1 + Ri。",
        output="Geometric mean = product(1 + Ri)^(1/n) - 1。",
        trap_check="必须先转 gross return 连乘，不能直接平均净收益率。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Money-Weighted Rate of Return (MWRR)",
        module="M01",
        knowledge_node="4. Money-Weighted and Time-Weighted Return",
        use_when="题干要求 investor experience，且外部现金流时点和金额会影响结果。",
        do_not_use_when="题干要求评价 manager performance 并排除客户现金流影响。",
        inputs="初始投资、追加/赎回现金流、期末价值；现金流符号必须统一。",
        output="Solve r from sum(CFt / (1 + r)^t) = 0。",
        trap_check="差时追加、好时赎回会拖低 MWRR，不等于经理表现差。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Time-Weighted Rate of Return (TWRR)",
        module="M01",
        knowledge_node="4.1.2 Time-Weighted Returns",
        use_when="题干要求 manager performance 或排除外部现金流影响。",
        do_not_use_when="题干要求投资者实际体验或 IRR 口径。",
        inputs="每次外部现金流之间的子期间 HPR。",
        output="TWRR = product(1 + HPi) - 1。",
        trap_check="必须在每次 external cash flow 处切段。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Annualized Return",
        module="M01",
        knowledge_node="5. Annualized Return",
        use_when="题干给非年度收益率，要求转换成年化口径。",
        do_not_use_when="题干给连续复利口径或要求多期总收益。",
        inputs="period return and number of periods per year c。",
        output="Annualized return = (1 + Rperiod)^c - 1。",
        trap_check="c 是一年内期数，不一定等于样本期数。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Continuously Compounded Return",
        module="M01",
        knowledge_node="5.3 Continuously Compounded Returns",
        use_when="题干出现 continuously compounded 或要求收益率可加。",
        do_not_use_when="题干明确使用 ordinary periodic compounding。",
        inputs="HPR 或 continuously compounded rate。",
        output="rcc = ln(1 + HPR); HPR = exp(rcc) - 1。",
        trap_check="不要把 ln(1 + HPR) 和普通年化公式混用。",
        links="[[M01-Rates-and-Returns]]",
    ),
    FormulaFramework(
        name="Gross -> Net -> Leveraged -> After-Tax Return",
        module="M01",
        knowledge_node="6. Other Major Return Measures and Their Applications",
        use_when="题干同时涉及 fees, leverage, taxes 或 return measure definitions。",
        do_not_use_when="题干只问未调整的单期 HPR。",
        inputs="gross return, management/admin fees, borrowing ratio, borrowing cost, tax rate。",
        output="先 gross/net，再 leverage，再 tax。",
        trap_check="Gross return 已含 trading expenses，不要重复扣交易费用。",
        links="[[M01-Rates-and-Returns]]",
    ),
]
```

- [ ] **Step 2: Add Quant MOC renderer**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
def render_quant_moc(current_frontmatter: str = "") -> str:
    formula_map = render_formula_framework_map(QUANT_FORMULA_FRAMEWORKS)
    body = f"""# Quantitative Methods MOC

> **一句话核心**：把投资问题翻译成收益率、现金流、概率、统计推断和模型证据。

---

## 1. Subject Brief 科目定位

- **Exam Weight**: 6-9%
- **Primary output**: choose the right quantitative tool, calculate correctly, and interpret the result in investment language.
- **中文主线**：先识别变量和时间口径，再选择公式或统计框架，最后解释经济含义与限制条件。
- **English trigger role**: return, probability, confidence interval, hypothesis test, regression output, machine learning risk.

{formula_map}
## 3. Module Atlas 模块地图

| Module | Official Module | Core Task | Main Formulas / Frameworks | High-Frequency Question Types | Links |
|---|---|---|---|---|---|
| M01 | Rates and Returns | 选择收益率口径并解释投资含义 | HPR, arithmetic/geometric/harmonic mean, MWRR/TWRR, annualized return, continuous compounding, gross/net/leverage/tax | return measure selection, cash-flow timing, fee/tax/leverage order | [[M01-Rates-and-Returns]] / [[00-Quant-Practice-Questions]] / [[00-Quant-Mock-Questions]] |
| M02 | Time Value of Money in Finance | 把现金流转成 PV/FV 或 implied return | PV/FV, annuity, perpetuity, implied return, cash-flow additivity | discounting, compounding frequency, bond/equity cash flows | [[M02-Time-Value-of-Money-in-Finance]] |
| M03 | Statistical Measures of Asset Returns | 描述收益分布的位置、离散度和形态 | mean, median, variance, standard deviation, skewness, kurtosis, correlation | descriptive statistics, outlier, downside risk | [[M03-Statistical-Measures-of-Asset-Returns]] |
| M04 | Probability Trees and Conditional Expectations | 用概率树和 Bayes 更新期望 | expected value, variance, total probability, Bayes' formula | path probability, conditional expectation, posterior probability | [[M04-Probability-Trees-and-Conditional-Expectations]] |
| M05 | Portfolio Mathematics | 把单资产风险收益组合成 portfolio risk/return | covariance, correlation, portfolio variance, Roy's safety-first | diversification, correlation effects, normal distribution applications | [[M05-Portfolio-Mathematics]] |
| M06 | Simulation Methods | 用模拟生成结果分布 | lognormal distribution, Monte Carlo, bootstrap | simulation use cases, model assumptions, resampling | [[M06-Simulation-Methods]] |
| M07 | Estimation and Inference | 从样本推断总体 | sampling methods, CLT, standard error, confidence interval | sample design, CI choice, inference limits | [[M07-Estimation-and-Inference]] |
| M08 | Hypothesis Testing | 用检验规则作统计判断 | null/alternative, test statistic, p-value, Type I/II error, power | reject/fail to reject, one/two-tailed tests | [[M08-Hypothesis-Testing]] |
| M09 | Parametric and Non-Parametric Tests of Independence | 检验 correlation 或 categorical independence | correlation t-test, Spearman rank, chi-square test | independence tests, contingency table, rank correlation | [[M09-Parametric-and-Non-Parametric-Tests-of-Independence]] |
| M10 | Simple Linear Regression | 解读回归输出和预测限制 | regression equation, ANOVA, R-squared, t-test, F-test, SEE | slope interpretation, model fit, prediction intervals | [[M10-Simple-Linear-Regression]] |
| M11 | Introduction to Big Data Techniques | 判断数据科技工具和模型风险 | supervised/unsupervised learning, overfitting, data visualization | ML type, alternative data, model governance | [[M11-Introduction-to-Big-Data-Techniques]] |

## 4. Curriculum Spine 教材主线

- **Return and discount-rate layer**: M01-M02，建立 required return、discount rate、cash-flow timing 和 compounding language。
- **Distribution and probability layer**: M03-M05，把 return distribution、expected value、variance、covariance 和 portfolio risk 连起来。
- **Inference layer**: M06-M10，从 simulation、sampling、confidence interval、hypothesis test 到 regression output。
- **Model-risk layer**: M11，把 big data 和 machine learning 放回 sample bias、overfitting、validation 和 explainability。

## 5. Exam Routes 做题路线

- **Definition route**: 看到官方术语，先写中文定义边界，再判断适用条件。
- **Calculation route**: 先确认 input units、time period、cash-flow sign、compounding convention，再套公式。
- **Interpretation route**: 数字不是答案终点，必须说明 economic meaning、limitation 和 decision implication。
- **Comparison route**: MWRR vs TWRR、arithmetic vs geometric、parametric vs non-parametric 都先问“题目要衡量什么”。

## 6. Practice & Mock Evidence Map 题库证据地图

- **Practice Questions**: [[00-Quant-Practice-Questions]]
- **Mock Questions**: [[00-Quant-Mock-Questions]]
- **Unclassified Mock Review**: [[00-Mock-Unclassified]]
- **Evidence rule**: 题库证据先回填到 Module，再回填到具体 knowledge block；无法高置信归类的 mock 不强行写入。

## 7. Review Routes 复习路线

- **首轮学习**：M01 -> M02 -> M03 -> M04 -> M05 -> M07 -> M08 -> M09 -> M10 -> M06 -> M11。
- **公式回炉**：优先看本 MOC 的 `Formula & Framework Map`，再进入对应 Module 的 `Formula & Decision Bench`。
- **Mock 前冲刺**：M01/M02 return and TVM，M08/M09 tests，M10 regression output，M11 model risk。
- **错题回炉**：错题先定位到 formula/framework，再回到 Module knowledge block 补定义边界和 trap rule。

## 8. Cross-Subject Interfaces 跨科目接口

- **Fixed Income**: discount rate, yield, spot/forward rates, duration and convexity depend on M01-M02.
- **Equity**: required return, growth, DDM and market efficiency depend on M01-M03.
- **Portfolio Management**: risk-return, correlation, diversification and behavioral evidence depend on M03-M05.
- **FSA / Corporate Issuers**: regression, forecasting, NPV/IRR and working-capital analysis depend on M01-M02 and M10.
"""
    return (current_frontmatter.rstrip() + "\n\n" + body).strip() + "\n" if current_frontmatter else body
```

- [ ] **Step 3: Add frontmatter preservation helper**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---", 4)
    if end == -1:
        return "", text
    frontmatter = text[: end + len("\n---")]
    body = text[end + len("\n---") :].lstrip()
    return frontmatter, body
```

- [ ] **Step 4: Add prototype command for Quant MOC**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
def write_quant_moc_prototype() -> Path:
    path = REPO_ROOT / "CFA_tier1" / "Quantitative_Methods" / "00-Quantitative-Methods-MOC.md"
    original = path.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(original)
    path.write_text(render_quant_moc(frontmatter), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="C+ CFA knowledge-base redesign tools")
    parser.add_argument("--prototype", choices=["quant-moc"], required=True)
    args = parser.parse_args()
    if args.prototype == "quant-moc":
        written = write_quant_moc_prototype()
        print(f"wrote {written.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run Quant MOC prototype**

Run:

```powershell
python scripts/cfa_c_plus_redesign.py --prototype quant-moc
```

Expected:

```text
wrote CFA_tier1\Quantitative_Methods\00-Quantitative-Methods-MOC.md
```

- [ ] **Step 6: Verify Formula & Framework Map comes before Module Atlas**

Run:

```powershell
rg -n "Formula & Framework Map|Module Atlas|Textbook Signal Topics|教材驱动补强" CFA_tier1\Quantitative_Methods\00-Quantitative-Methods-MOC.md
```

Expected:

```text
...:## 2. Formula & Framework Map 公式与框架地图
...:## 3. Module Atlas 模块地图
```

Expected absence:

```text
Textbook Signal Topics
教材驱动补强
```

- [ ] **Step 7: Commit Quant MOC prototype**

```powershell
git add -- scripts/cfa_c_plus_redesign.py CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
git commit -m "feat: prototype C+ Quant formula framework MOC"
```

---

## Task 5: Add Module Knowledge-Block Renderer

**Files:**

- Modify: `scripts/cfa_c_plus_redesign.py`
- Modify: `.system/tests/test_cfa_c_plus_redesign.py`

- [ ] **Step 1: Add failing test for knowledge block rendering**

Append to `.system/tests/test_cfa_c_plus_redesign.py`:

```python
from scripts.cfa_c_plus_redesign import KnowledgeBlock, render_knowledge_block


def test_render_knowledge_block_keeps_bilingual_learning_shape():
    block = KnowledgeBlock(
        heading="2.1 Determinants of Interest Rates / 利率决定因素",
        textbook_position="Module 1, Section 2.1",
        core_meaning="利率是 time value 与 risk premiums 的组合，不是单一风险标签。",
        english_terms="real risk-free rate; expected inflation premium; default risk premium",
        why_it_matters="这决定题目问 required return、discount rate 或 opportunity cost 时如何解释。",
        formula_rule="Nominal rate ≈ real risk-free rate + expected inflation + risk premiums.",
        exam_translation="看到 higher required return，要识别是哪一种 premium 变化。",
        question_triggers="required return; discount rate; opportunity cost; premium",
        practice_mock_evidence="Practice questions often ask which premium changes under a scenario.",
        trap_fix_rule="不要把所有高利率都归因于 default risk；先逐项排 premium。",
    )
    rendered = render_knowledge_block(block)
    assert "Core Meaning 中文解释" in rendered
    assert "English Terms" in rendered
    assert "Trap & Fix Rule" in rendered
    assert "default risk premium" in rendered
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py::test_render_knowledge_block_keeps_bilingual_learning_shape -q
```

Expected:

```text
ImportError: cannot import name 'KnowledgeBlock'
```

- [ ] **Step 3: Implement knowledge block renderer**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify pass**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py -q
```

Expected:

```text
4 passed
```

- [ ] **Step 5: Commit knowledge-block renderer**

```powershell
git add -- scripts/cfa_c_plus_redesign.py .system/tests/test_cfa_c_plus_redesign.py
git commit -m "feat: render C+ module knowledge blocks"
```

---

## Task 6: Build Quant M01 C+ Prototype

**Files:**

- Modify: `scripts/cfa_c_plus_redesign.py`
- Modify: `CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md`

- [ ] **Step 1: Add M01 knowledge blocks**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
QUANT_M01_BLOCKS = [
    KnowledgeBlock(
        heading="2. Interest Rates and Time Value of Money / 利率与货币时间价值",
        textbook_position="V1 Module 1, Section 2",
        core_meaning="利率在本章不是孤立数字，而是 required rate of return、discount rate 和 opportunity cost 的共同语言。它把今天的钱、未来的钱和投资者要求补偿连接起来。",
        english_terms="required rate of return; discount rate; opportunity cost; time value of money",
        why_it_matters="后续 TVM、Fixed Income、Equity valuation 和 Corporate Issuers 的 NPV/IRR 都依赖这套利率语言。",
        formula_rule="先判断利率在题目中扮演的角色：required return 用于投资者要求补偿，discount rate 用于折现现金流，opportunity cost 用于解释放弃的次优选择。",
        exam_translation="如果题干问 interpret an interest rate，不要直接算；先说明它可以被解释为 required return、discount rate 或 opportunity cost。",
        question_triggers="required return; discount rate; opportunity cost; compensate investors; future cash flow",
        practice_mock_evidence="基础题常把三个概念混在一句话里，要求识别利率在当前语境中的角色。",
        trap_fix_rule="看到 interest rate 先问它在题目里是投资者要求、折现工具还是机会成本，再决定是否计算。",
    ),
    KnowledgeBlock(
        heading="2.1 Determinants of Interest Rates / 利率决定因素",
        textbook_position="V1 Module 1, Section 2.1",
        core_meaning="名义利率可以理解为 real risk-free rate 加上 expected inflation 和各类 risk premiums。考试重点不是背一个列表，而是判断题干中的风险变化对应哪一种 premium。",
        english_terms="real risk-free rate; expected inflation premium; default risk premium; liquidity premium; maturity premium",
        why_it_matters="Fixed Income 的 yield spread、Equity 的 required return、Corporate Issuers 的 cost of capital 都会复用这一分解逻辑。",
        formula_rule="Nominal interest rate ≈ real risk-free rate + expected inflation premium + default risk premium + liquidity premium + maturity premium.",
        exam_translation="题干说利率上升时，先判断是 inflation、default risk、liquidity risk 还是 maturity risk 在变化。",
        question_triggers="inflation; default risk; liquidity; maturity; premium; nominal interest rate",
        practice_mock_evidence="Practice/mock 常给发行人信用恶化、期限变长或市场流动性下降，让你判断 required return 为什么上升。",
        trap_fix_rule="不要把所有高利率都归因于 default risk；先按 inflation、default、liquidity、maturity 顺序排查。",
    ),
    KnowledgeBlock(
        heading="3. Rates of Return / 收益率度量总览",
        textbook_position="V1 Module 1, Section 3",
        core_meaning="Return measurement 的核心是选择合适口径：单期总回报、多期平均、复合增长、投资者体验、经理表现、税费杠杆调整都不是同一个问题。",
        english_terms="holding period return; arithmetic mean; geometric mean; harmonic mean; gross return; net return",
        why_it_matters="很多错题不是公式不会，而是题目问的是另一种 return measure。",
        formula_rule="先判断题目要求 single period、one-period expectation、compound growth、cash-flow experience 还是 manager performance。",
        exam_translation="看到 calculate and interpret different approaches to return measurement，先分类，再计算，再解释适用场景。",
        question_triggers="return measure; average return; compound growth; holding period; performance evaluation",
        practice_mock_evidence="基础题常要求在 arithmetic mean 和 geometric mean 之间选择，mock 常把 MWRR/TWRR 与现金流时点混合。",
        trap_fix_rule="先写出题目问的 return purpose，再选公式；不要看到 return 就套 HPR。",
    ),
    KnowledgeBlock(
        heading="3.1 Holding Period Return / 持有期收益率",
        textbook_position="V1 Module 1, Section 3.1",
        core_meaning="HPR 衡量一个持有期内价格变化和期间收入带来的总收益，适用于单一持有期，不自动处理多期复合或现金流时点。",
        english_terms="holding period return; beginning price; ending price; income; dividend",
        why_it_matters="HPR 是 return measurement 的底层积木，TWRR、年化和 gross return 都会用到它。",
        formula_rule="HPR = (P1 - P0 + D1) / P0；Gross return = 1 + HPR。",
        exam_translation="题干给 P0、P1、dividend 或 coupon，并问 holding period return，就直接使用 HPR；算完要解释正负和来源。",
        question_triggers="beginning price; ending price; dividend; income; one holding period; HPR",
        practice_mock_evidence="Practice 题常把 dividend、ending value 和 percentage return 放在同一题里检查你是否重复计入收入。",
        trap_fix_rule="检查 D1 是否已经包含在 ending value 中；如果题干问多期 compound growth，不要停在单期 HPR。",
    ),
    KnowledgeBlock(
        heading="3.2-3.4 Mean Returns / 算术、几何与调和平均",
        textbook_position="V1 Module 1, Sections 3.2-3.4",
        core_meaning="Arithmetic mean 适合单期期望，geometric mean 适合多期复合增长，harmonic mean 常用于 price multiples 的平均。三者回答的问题不同。",
        english_terms="arithmetic mean return; geometric mean return; harmonic mean; expected return; compound growth",
        why_it_matters="CFA 喜欢用同一组 historical returns 问不同平均口径，测试你是否理解用途而不是只会按键。",
        formula_rule="Arithmetic mean = sum(Ri)/n；Geometric mean = product(1 + Ri)^(1/n) - 1；Harmonic mean = n / sum(1/Xi)。",
        exam_translation="问 one-period expected return 用 arithmetic；问 historical compound growth 用 geometric；问平均估值倍数时考虑 harmonic。",
        question_triggers="average return; expected return; compound annual growth; price multiple; P/E average",
        practice_mock_evidence="基础题高频考 arithmetic vs geometric，mock 更容易把 volatility 或 outlier 加进解释。",
        trap_fix_rule="不要用 arithmetic mean 描述长期财富增长；先看题目问 expectation 还是 compounding。",
    ),
    KnowledgeBlock(
        heading="4. Money-Weighted and Time-Weighted Return / 资金加权与时间加权收益率",
        textbook_position="V1 Module 1, Section 4",
        core_meaning="MWRR 是投资者实际现金流体验，TWRR 是剔除外部现金流影响后的经理表现。两者差异来自外部现金流的时点和金额。",
        english_terms="money-weighted rate of return; internal rate of return; time-weighted rate of return; external cash flow; manager performance",
        why_it_matters="考试常用客户在好/坏时点追加或赎回资金来测试你是否能解释 MWRR 与 TWRR 的差异。",
        formula_rule="MWRR solves IRR from dated cash flows；TWRR splits portfolio into subperiods at each external cash flow and geometrically links subperiod returns.",
        exam_translation="题目问 investor experience 用 MWRR；题目问 manager performance 用 TWRR。",
        question_triggers="external cash flow; investor experience; manager performance; contribution; withdrawal; IRR",
        practice_mock_evidence="Mock 题常不要求完整计算，而是要求解释为什么 MWRR 高于或低于 TWRR。",
        trap_fix_rule="客户现金流决策导致的 MWRR 差异不能直接归因于基金经理表现。",
    ),
    KnowledgeBlock(
        heading="5. Annualized and Continuously Compounded Return / 年化与连续复利",
        textbook_position="V1 Module 1, Sections 5.1-5.3",
        core_meaning="Annualized return 把非年度收益率转换成年度口径；continuously compounded return 用自然对数表达，优点是多期可加。",
        english_terms="annualized return; non-annual compounding; continuously compounded return; additivity",
        why_it_matters="同样的 return 在不同 compounding convention 下数值不同，题干口径决定公式。",
        formula_rule="Annualized return = (1 + Rperiod)^c - 1；rcc = ln(1 + HPR)；HPR = exp(rcc) - 1。",
        exam_translation="看到 monthly/quarterly return annualized 用普通复利；看到 continuously compounded 用 ln 或 exp。",
        question_triggers="annualized; monthly return; quarterly return; continuously compounded; natural log",
        practice_mock_evidence="基础题常给月收益率要求年化；mock 常混合 ordinary return 与 continuously compounded return。",
        trap_fix_rule="不要把连续复利和普通年化混用；先圈出 compounding convention。",
    ),
    KnowledgeBlock(
        heading="6. Other Major Return Measures / 其他收益率口径",
        textbook_position="V1 Module 1, Sections 6.1-6.4",
        core_meaning="Gross/net、pre-tax/after-tax、real return 和 leveraged return 是在基础收益率上按费用、税、通胀和融资结构继续调整。",
        english_terms="gross return; net return; pre-tax return; after-tax return; real return; leveraged return",
        why_it_matters="考试常把费用、交易成本、税、通胀和借款成本放在同一题，核心是顺序和口径。",
        formula_rule="Net return subtracts management/admin fees from gross return；real return adjusts for inflation；leveraged return depends on borrowing ratio and borrowing cost。",
        exam_translation="先判断题目要求 gross、net、real、leveraged 还是 after-tax，再按口径顺序调整。",
        question_triggers="gross; net; management fee; administrative fee; trading expense; tax; inflation; borrowed funds",
        practice_mock_evidence="基础题容易考 gross return 已包含 trading expenses；mock 容易考 leverage 和 tax 的顺序。",
        trap_fix_rule="Gross return 已含 trading expenses，不要重复扣；涉及多种调整时先写顺序再算。",
    ),
]
```

- [ ] **Step 2: Add M01 renderer**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
def render_quant_m01(current_frontmatter: str = "") -> str:
    blocks = "\n".join(render_knowledge_block(block) for block in QUANT_M01_BLOCKS)
    formula_bench = render_formula_framework_map(QUANT_FORMULA_FRAMEWORKS).replace(
        "## 2. Formula & Framework Map 公式与框架地图",
        "## 4. Formula & Decision Bench 公式与决策台",
        1,
    )
    body = f"""# M01: Rates and Returns

> **Reading Contract 学习契约**：学完本模块，你必须能区分利率角色、选择正确 return measure、解释现金流时点对收益率的影响，并按费用、税、通胀和杠杆口径调整收益。

---

## 0. Reading Contract 学习契约

- **Explain**: interest rate as required return, discount rate, and opportunity cost.
- **Calculate**: HPR, arithmetic/geometric/harmonic mean, annualized return, continuously compounded return, MWRR/TWRR, gross/net/real/leveraged/after-tax return.
- **Interpret**: what each return measure is designed to measure.
- **Avoid**: using a familiar formula before identifying the return purpose and input convention.

## 1. Module Brief 模块定位

- **Official module**: Module 1: Rates and Returns
- **Textbook source**: CFA Program 2026 Level I Volume 1, Module 1
- **Primary LOS actions**: interpret, calculate, compare, evaluate.
- **Cross-subject links**: TVM, Fixed Income yields, Equity required return, Portfolio performance, Corporate NPV/IRR.

## 2. Curriculum Spine 教材正文主线

{blocks}
## 3. Exam Translation 考试翻译

| Question Type | First Decision | Action | Output |
|---|---|---|---|
| Interest rate interpretation | 利率在题中是 required return、discount rate 还是 opportunity cost | 解释角色和风险补偿来源 | 中文结论 + English term |
| Single-period return | 是否只覆盖一个 holding period | 使用 HPR | 数值 + 收益来源解释 |
| Average return | 题目问 expectation、compound growth 还是 multiple average | 选择 arithmetic/geometric/harmonic | 口径解释 |
| Portfolio performance | 题目问 investor experience 还是 manager performance | 选择 MWRR 或 TWRR | 解释现金流时点影响 |
| Compounding convention | ordinary compounding or continuous compounding | 选择 annualized, ln, or exp | 同一口径下的 return |
| Adjusted return | fees, tax, inflation, leverage 是否出现 | 按 gross/net/real/leverage/tax 口径调整 | 调整后收益率 + 顺序说明 |

{formula_bench}
## 5. Practice & Mock Evidence 题库证据

- **Practice page**: [[00-Quant-Practice-Questions]]
- **Mock page**: [[00-Quant-Mock-Questions]]
- **Evidence placement rule**: 每道题先归入本页的 knowledge block，再记录题干触发词、公式口径和 trap。
- **High-value buckets**:
  - Interest rate roles and premiums
  - HPR and mean return selection
  - MWRR vs TWRR interpretation
  - Annualized vs continuously compounded return
  - Gross/net/real/leveraged/after-tax return order

## 6. Trap Ledger 陷阱账本

| Trap | Corrective Rule | Related Block |
|---|---|---|
| 看到 interest rate 就直接折现 | 先判断它是 required return、discount rate 还是 opportunity cost | 2 / 2.1 |
| 把所有高利率都归因于 default risk | 逐项检查 inflation、default、liquidity、maturity premium | 2.1 |
| 用 arithmetic mean 表示长期复合增长 | expectation 用 arithmetic，compound growth 用 geometric | 3.2-3.4 |
| 用 MWRR 评价经理表现 | manager performance 用 TWRR，investor experience 用 MWRR | 4 |
| 连续复利和普通年化混用 | continuously compounded 用 ln/exp，ordinary compounding 用 power | 5 |
| Gross return 重复扣 trading expenses | Gross 已含 trading expenses，net 再扣 management/admin fees | 6 |

## 7. Final Recall Sheet 最后回忆页

- **90-second recall**: interest rate roles -> premium decomposition -> HPR -> mean returns -> MWRR/TWRR -> annualized/continuous -> gross/net/real/leverage/tax.
- **Formula choice question**: 题目到底要衡量 single period、expected one period、compound growth、investor experience、manager performance，还是 adjusted return？
- **Last trap check**: time period、cash-flow sign、compounding convention、fee/tax/leverage order。
"""
    return (current_frontmatter.rstrip() + "\n\n" + body).strip() + "\n" if current_frontmatter else body
```

- [ ] **Step 3: Add prototype command for M01**

Modify `main()` in `scripts/cfa_c_plus_redesign.py` so it reads:

```python
def write_quant_m01_prototype() -> Path:
    path = REPO_ROOT / "CFA_tier1" / "Quantitative_Methods" / "M01-Rates-and-Returns.md"
    original = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(remove_mechanical_sections(original))
    path.write_text(render_quant_m01(frontmatter), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="C+ CFA knowledge-base redesign tools")
    parser.add_argument("--prototype", choices=["quant-moc", "quant-m01"], required=True)
    args = parser.parse_args()
    if args.prototype == "quant-moc":
        written = write_quant_moc_prototype()
        print(f"wrote {written.relative_to(REPO_ROOT)}")
    if args.prototype == "quant-m01":
        written = write_quant_m01_prototype()
        print(f"wrote {written.relative_to(REPO_ROOT)}")
```

- [ ] **Step 4: Run M01 prototype**

Run:

```powershell
python scripts/cfa_c_plus_redesign.py --prototype quant-m01
```

Expected:

```text
wrote CFA_tier1\Quantitative_Methods\M01-Rates-and-Returns.md
```

- [ ] **Step 5: Verify M01 contains C+ sections and no mechanical patches**

Run:

```powershell
rg -n "Reading Contract|Curriculum Spine|Formula & Decision Bench|Practice & Mock Evidence|Trap Ledger|Textbook Signal Topics|教材驱动补强|教材驱动解题动作|教材驱动易错清单" CFA_tier1\Quantitative_Methods\M01-Rates-and-Returns.md
```

Expected present:

```text
## 0. Reading Contract 学习契约
## 2. Curriculum Spine 教材正文主线
## 4. Formula & Decision Bench 公式与决策台
## 5. Practice & Mock Evidence 题库证据
## 6. Trap Ledger 陷阱账本
```

Expected absent:

```text
Textbook Signal Topics
教材驱动补强
教材驱动解题动作
教材驱动易错清单
```

- [ ] **Step 6: Commit M01 prototype**

```powershell
git add -- scripts/cfa_c_plus_redesign.py CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md
git commit -m "feat: prototype C+ Quant M01 module"
```

---

## Task 7: Add Prototype Audit

**Files:**

- Modify: `scripts/cfa_c_plus_redesign.py`
- Create: `.system/memory/strategy/cfa-c-plus-prototype-audit.md`
- Modify: `.system/tests/test_cfa_c_plus_redesign.py`

- [ ] **Step 1: Add failing audit test**

Append to `.system/tests/test_cfa_c_plus_redesign.py`:

```python
from scripts.cfa_c_plus_redesign import audit_markdown


def test_audit_markdown_reports_required_sections_and_old_patch_absence():
    text = """# Page

## 2. Formula & Framework Map 公式与框架地图

## 3. Module Atlas 模块地图
"""
    result = audit_markdown(
        text,
        required_sections=[
            "## 2. Formula & Framework Map 公式与框架地图",
            "## 3. Module Atlas 模块地图",
        ],
    )
    assert result["missing_required_sections"] == []
    assert result["old_patch_markers"] == []
```

- [ ] **Step 2: Run audit test and verify it fails**

Run:

```powershell
pytest .system/tests/test_cfa_c_plus_redesign.py::test_audit_markdown_reports_required_sections_and_old_patch_absence -q
```

Expected:

```text
ImportError: cannot import name 'audit_markdown'
```

- [ ] **Step 3: Implement audit functions**

Append to `scripts/cfa_c_plus_redesign.py`:

```python
OLD_PATCH_MARKERS = [
    "## Textbook Signal Topics",
    "### 教材驱动补强（按原版教材回看）",
    "### 教材驱动解题动作",
    "### 教材驱动易错清单",
]


def audit_markdown(text: str, required_sections: list[str]) -> dict[str, list[str]]:
    return {
        "missing_required_sections": [section for section in required_sections if section not in text],
        "old_patch_markers": [marker for marker in OLD_PATCH_MARKERS if marker in text],
    }


def write_prototype_audit() -> Path:
    moc_path = REPO_ROOT / "CFA_tier1" / "Quantitative_Methods" / "00-Quantitative-Methods-MOC.md"
    m01_path = REPO_ROOT / "CFA_tier1" / "Quantitative_Methods" / "M01-Rates-and-Returns.md"
    moc_audit = audit_markdown(
        moc_path.read_text(encoding="utf-8"),
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "## 3. Module Atlas 模块地图",
            "## 6. Practice & Mock Evidence Map 题库证据地图",
        ],
    )
    m01_audit = audit_markdown(
        m01_path.read_text(encoding="utf-8"),
        [
            "## 0. Reading Contract 学习契约",
            "## 2. Curriculum Spine 教材正文主线",
            "## 4. Formula & Decision Bench 公式与决策台",
            "## 5. Practice & Mock Evidence 题库证据",
            "## 6. Trap Ledger 陷阱账本",
        ],
    )
    lines = [
        "# C+ Prototype Audit",
        "",
        "- Scope: Quantitative Methods MOC + M01 prototype",
        "- Old files excluded: `_legacy/`, `_archive/`, `mock/`, `dashboard/`",
        "",
        "## Quant MOC",
        "",
        f"- Missing required sections: `{moc_audit['missing_required_sections']}`",
        f"- Old patch markers: `{moc_audit['old_patch_markers']}`",
        "",
        "## Quant M01",
        "",
        f"- Missing required sections: `{m01_audit['missing_required_sections']}`",
        f"- Old patch markers: `{m01_audit['old_patch_markers']}`",
        "",
        "## Review Gate",
        "",
        "- User should review the two prototype pages before any 93-module rollout.",
    ]
    AUDIT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return AUDIT_PATH
```

- [ ] **Step 4: Add audit CLI option**

Modify `main()` in `scripts/cfa_c_plus_redesign.py`:

```python
def main() -> None:
    parser = argparse.ArgumentParser(description="C+ CFA knowledge-base redesign tools")
    parser.add_argument("--prototype", choices=["quant-moc", "quant-m01"], required=False)
    parser.add_argument("--audit-prototype", action="store_true")
    args = parser.parse_args()
    if args.prototype == "quant-moc":
        written = write_quant_moc_prototype()
        print(f"wrote {written.relative_to(REPO_ROOT)}")
    if args.prototype == "quant-m01":
        written = write_quant_m01_prototype()
        print(f"wrote {written.relative_to(REPO_ROOT)}")
    if args.audit_prototype:
        written = write_prototype_audit()
        print(f"wrote {written.relative_to(REPO_ROOT)}")
```

- [ ] **Step 5: Run audit**

Run:

```powershell
python scripts/cfa_c_plus_redesign.py --audit-prototype
```

Expected:

```text
wrote .system\memory\strategy\cfa-c-plus-prototype-audit.md
```

- [ ] **Step 6: Verify audit report has no missing sections or old markers**

Run:

```powershell
rg -n "Missing required sections: `\\[\\]`|Old patch markers: `\\[\\]`" .system\memory\strategy\cfa-c-plus-prototype-audit.md
```

Expected:

```text
...:- Missing required sections: `[]`
...:- Old patch markers: `[]`
...:- Missing required sections: `[]`
...:- Old patch markers: `[]`
```

- [ ] **Step 7: Commit prototype audit**

```powershell
git add -- scripts/cfa_c_plus_redesign.py .system/tests/test_cfa_c_plus_redesign.py .system/memory/strategy/cfa-c-plus-prototype-audit.md
git commit -m "test: audit C+ Quant prototype"
```

---

## Task 8: Prototype Review Checkpoint

**Files:**

- Review: `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`
- Review: `CFA_tier1/Quantitative_Methods/M01-Rates-and-Returns.md`
- Review: `.system/memory/strategy/cfa-c-plus-prototype-audit.md`

- [ ] **Step 1: Stop and present prototype to the user**

Report these exact review points:

```text
Prototype ready for review:
- Quant MOC now starts from Formula & Framework Map.
- Quant M01 is rewritten as a C+ module chapter.
- Mechanical supplement sections are absent from the two prototype files.
- Audit report is available at .system/memory/strategy/cfa-c-plus-prototype-audit.md.
```

- [ ] **Step 2: Ask for review decision before full rollout**

Ask:

```text
请确认：这个 Quant MOC + M01 样板是否可以作为 10 个 MOC 和 93 个现役模块的批量扩散模板？
```

- [ ] **Step 3: Do not proceed to batch rollout until the user approves**

Expected state:

```text
No files outside Quant MOC, Quant M01, the script, tests, and audit report have been changed by this plan phase.
```

---

## Task 9: Full Rollout Plan After Prototype Approval

**Files:**

- Modify later: `scripts/cfa_c_plus_redesign.py`
- Modify later: all active `CFA_tier1/*/00-*-MOC.md`
- Modify later: all active `CFA_tier1/*/M*.md`
- Do not modify later: `_legacy/`, `_archive/`, `mock/`, `dashboard/`

- [ ] **Step 1: Add a second implementation plan after prototype approval**

Create a new plan file only after user approval:

```text
docs/superpowers/plans/2026-05-27-cfa-kb-c-plus-full-rollout.md
```

- [ ] **Step 2: In the rollout plan, require subject-by-subject checkpoints**

The rollout plan must use this order:

```text
1. Quantitative Methods
2. Financial Statement Analysis
3. Fixed Income
4. Equity
5. Economics
6. Corporate Issuers
7. Derivatives
8. Portfolio Management
9. Alternative Investments
10. Ethical and Professional Standards
```

- [ ] **Step 3: In the rollout plan, require audit after each subject**

Each subject checkpoint must verify:

```text
- MOC has Formula & Framework Map.
- All active modules have C+ sections.
- Old mechanical patch markers are absent.
- _legacy and _archive are untouched.
- Practice/mock links remain valid at subject/module level.
```

---

## Self-Review

Spec coverage:

- C+ design is covered by Tasks 4 and 6.
- MOC `Formula & Framework Map` priority is covered by Tasks 3 and 4.
- Module textbook-section knowledge blocks are covered by Tasks 5 and 6.
- Old mechanical patch cleanup is covered by Tasks 1, 2, 6, and 7.
- No `_legacy` / `_archive` modification is covered by Tasks 1, 2, 7, and 9.
- User review before full rollout is covered by Task 8.

Placeholder scan:

- The plan contains no `TBD`, `TODO`, or unspecified implementation step.
- Every code-changing task includes exact file paths, code snippets, commands, and expected output.

Type consistency:

- `FormulaFramework`, `KnowledgeBlock`, `render_formula_framework_map`, `render_knowledge_block`, `audit_markdown`, and prototype functions are introduced before later tasks depend on them.
