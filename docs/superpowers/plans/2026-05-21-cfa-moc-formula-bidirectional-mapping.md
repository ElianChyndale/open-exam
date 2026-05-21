# CFA MOC Formula Bidirectional Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add bidirectional formula mapping between CFA MOC knowledge-tree nodes and formula tables, then update workflows and skills so the agents can classify and patch MOC gaps using the new taxonomy.

**Architecture:** Keep the current four-layer architecture intact. Extend the MOC markdown structure and workflow logic rather than redesigning storage. The implementation is split into three slices: workflow/model behavior, skill and agent instructions, and subject MOC migration.

**Tech Stack:** Python CLI, pytest, markdown MOC files, local skill docs

---

## File Structure

- Modify: `.system/app/models.py`
  - extend workflow-facing types only if needed for the new gap taxonomy output
- Modify: `.system/app/workflows.py`
  - add MOC inspection helpers, new `gap_target` classification, and safer review output
- Modify: `.system/tests/test_workflows.py`
  - cover the new taxonomy and MOC-sensitive classification behavior
- Modify: `docs/moc-auto-patch-workflow.md`
  - align documentation to the new patch target taxonomy
- Modify: `skills/cfa-intent-router/SKILL.md`
  - route “is this formula in my framework?” requests through MOC inspection logic
- Modify: `skills/cfa-question-captor/SKILL.md`
  - specify tree-vs-table-vs-both formula targeting
- Modify: `skills/cfa-pattern-miner/SKILL.md`
  - distinguish missing core formula from misuse
- Modify: `skills/cfa-review-synthesizer/SKILL.md`
  - emit tree-core / table-variant / concept / trap classifications
- Modify: `skills/cfa-validation-guard/SKILL.md`
  - validate formula ownership and target type before patching
- Modify: `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`
  - establish the target MOC pattern first
- Modify: `CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md`
- Modify: `CFA_tier1/Derivatives/00-Derivatives-MOC.md`
- Modify: `CFA_tier1/Equity/00-Equity-MOC.md`
- Modify: `CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md`
- Modify: `CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md`
- Modify: `CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md`
- Modify: `CFA_tier1/Economics/00-Economics-MOC.md`
- Modify: `CFA_tier1/Alternative_Investments/00-Alternative-Investments-MOC.md`
  - add `核心公式` only for genuinely formula-driven nodes
- Modify: `CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md`
  - only normalize formula-table expectations if needed; do not add forced formula nodes

### Task 1: Add workflow tests for the new MOC gap taxonomy

**Files:**
- Modify: `.system/tests/test_workflows.py`
- Modify: `.system/app/workflows.py`

- [ ] **Step 1: Write the failing tests for taxonomy-aware MOC gap review**

```python
def test_moc_gap_review_marks_missing_core_formula_when_tree_lacks_formula(tmp_path: Path) -> None:
    from app.cli import run_cli

    moc = tmp_path / "CFA_tier1" / "Quantitative_Methods"
    moc.mkdir(parents=True, exist_ok=True)
    (moc / "00-Quantitative-Methods-MOC.md").write_text(
        "\n".join(
            [
                "## Quantitative Methods 核心知识树",
                "```text",
                "├── 1.5 Annualization and continuous compounding【考试核心】",
                "│   ├── 定义/直觉",
                "│   │   └── 连续复利和普通复利口径要分开",
                "```",
                "",
                "## 核心公式速查",
                "| 指标 | 公式 | 知识树节点 | 考试说明 |",
                "|------|------|------------|----------|",
                "| Convert CC Return | `e^(r_cc)-1` | `1.5` | 连续复利回到 holding period return |",
            ]
        ),
        encoding="utf-8",
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Quantitative Methods",
        "los": "QM.Rates",
        "prompt_or_question": "Continuous compounding question.",
        "correct_resolution": "Use FV = PVe^(rt).",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 90,
        "evidence_refs": ["mock-cc"],
        "moc_target": "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: knowledge_tree_core_formula" in text


def test_moc_gap_review_marks_formula_table_variant_when_tree_has_core_formula(tmp_path: Path) -> None:
    from app.cli import run_cli

    moc = tmp_path / "CFA_tier1" / "Derivatives"
    moc.mkdir(parents=True, exist_ok=True)
    (moc / "00-Derivatives-MOC.md").write_text(
        "\n".join(
            [
                "## Derivatives 核心知识树",
                "```text",
                "├── M05: Pricing and Valuation of Forwards and Futures【考试核心】",
                "│   ├── 核心公式",
                "│   │   └── F0(T) = S0(1+r)^T",
                "```",
                "",
                "## 核心公式速查",
                "| 指标 | 公式 | 知识树节点 | 考试说明 |",
                "|------|------|------------|----------|",
                "| Forward Price | `S0(1+r)^T` | `M05` | 无收入资产远期价格 |",
            ]
        ),
        encoding="utf-8",
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Derivatives",
        "los": "DER.Forward",
        "prompt_or_question": "Known-yield forward question.",
        "correct_resolution": "Use the yield-adjusted carry variant.",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 100,
        "evidence_refs": ["forward-variant"],
        "moc_target": "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: formula_table_variant" in text
```

- [ ] **Step 2: Run the focused tests to verify they fail for the expected reason**

Run:

```powershell
pytest .system/tests/test_workflows.py -k "gap_review_marks_missing_core_formula or gap_review_marks_formula_table_variant" -v
```

Expected:

- FAIL because `moc-gap-review.md` does not yet contain `gap_target`
- FAIL because workflow logic does not yet inspect MOC content

- [ ] **Step 3: Implement minimal MOC inspection helpers and taxonomy output**

```python
def classify_gap_target(event: MistakeEvent, moc_text: str) -> str:
    if event.error_type != "formula_misuse":
        return "knowledge_tree_concept" if event.error_type == "concept_confusion" else "exam_trap"

    has_core_formula_section = "核心公式" in moc_text
    has_node_mapping_column = "知识树节点" in moc_text

    if not has_core_formula_section:
        return "knowledge_tree_core_formula"
    if has_core_formula_section and has_node_mapping_column:
        return "formula_table_variant"
    return "both"


def render_gap_block(sample: MistakeEvent, grouped: list[MistakeEvent], gap_type: str, gap_target: str) -> list[str]:
    return [
        "",
        f"## {sample.topic} | {sample.los} | {sample.error_type}",
        f"moc_target: {sample.moc_target}",
        f"recurrence: {len(grouped)}",
        f"suggested_gap_type: {gap_type}",
        f"gap_target: {gap_target}",
        f"reason: Repeated {sample.error_type} errors suggest the MOC may need a stronger {gap_target} treatment for this LOS.",
    ]
```

- [ ] **Step 4: Run the focused tests to verify they pass**

Run:

```powershell
pytest .system/tests/test_workflows.py -k "gap_review_marks_missing_core_formula or gap_review_marks_formula_table_variant" -v
```

Expected:

- PASS for both new tests

- [ ] **Step 5: Commit**

```bash
git add .system/tests/test_workflows.py .system/app/workflows.py
git commit -m "feat: classify moc gap targets by tree and formula table"
```

### Task 2: Harden workflow behavior and documentation around the new taxonomy

**Files:**
- Modify: `.system/app/workflows.py`
- Modify: `.system/app/models.py`
- Modify: `docs/moc-auto-patch-workflow.md`
- Test: `.system/tests/test_workflows.py`

- [ ] **Step 1: Write the failing test for concept-only subjects**

```python
def test_moc_gap_review_keeps_ethics_out_of_formula_targeting(tmp_path: Path) -> None:
    from app.cli import run_cli

    moc = tmp_path / "CFA_tier1" / "Ethical_and_Professional_Standards"
    moc.mkdir(parents=True, exist_ok=True)
    (moc / "00-Ethical-and-Professional-Standards-MOC.md").write_text(
        "\n".join(
            [
                "## Ethical and Professional Standards 核心知识树",
                "```text",
                "├── M03: Standard I - Professionalism【考试核心】",
                "│   └── 注意：law answers 'may I'; ethics asks 'should I'",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Ethical and Professional Standards",
        "los": "I.B",
        "prompt_or_question": "Independence and objectivity question.",
        "correct_resolution": "Issuer-paid travel can impair independence.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 70,
        "evidence_refs": ["ethics-1"],
        "moc_target": "CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: knowledge_tree_concept" in text
    assert "knowledge_tree_core_formula" not in text
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run:

```powershell
pytest .system/tests/test_workflows.py -k "keeps_ethics_out_of_formula_targeting" -v
```

Expected:

- FAIL because concept-only subjects are not yet separated from formula taxonomy logic

- [ ] **Step 3: Implement subject-aware gap targeting and doc alignment**

```python
FORMULA_DENSE_SUBJECTS = {
    "Quantitative Methods",
    "Fixed Income",
    "Derivatives",
    "Equity",
    "Financial Statement Analysis",
    "Financial Reporting and Analysis",
    "Corporate Issuers",
    "Portfolio Management",
    "Economics",
}


def subject_supports_formula_nodes(event: MistakeEvent) -> bool:
    return event.topic in FORMULA_DENSE_SUBJECTS or "Alternative_Investments" in (event.moc_target or "")
```

And update `docs/moc-auto-patch-workflow.md` so the patch targets read:

```md
- `knowledge_tree_core_formula`：补知识树节点下的 `核心公式`
- `formula_table_variant`：只补 `核心公式速查`
- `both`：知识树与公式表同时补
- `knowledge_tree_concept`：补知识树概念分支
- `exam_trap`：补考试陷阱或警示说明
```

- [ ] **Step 4: Run the focused test and the existing MOC review tests**

Run:

```powershell
pytest .system/tests/test_workflows.py -k "moc_gap_review" -v
```

Expected:

- PASS for the new Ethics-specific test
- PASS for existing MOC review behavior

- [ ] **Step 5: Commit**

```bash
git add .system/app/workflows.py .system/app/models.py .system/tests/test_workflows.py docs/moc-auto-patch-workflow.md
git commit -m "feat: align moc gap review with formula taxonomy"
```

### Task 3: Update the skill files and agent-facing instructions

**Files:**
- Modify: `skills/cfa-intent-router/SKILL.md`
- Modify: `skills/cfa-question-captor/SKILL.md`
- Modify: `skills/cfa-pattern-miner/SKILL.md`
- Modify: `skills/cfa-review-synthesizer/SKILL.md`
- Modify: `skills/cfa-validation-guard/SKILL.md`

- [ ] **Step 1: Write a failing documentation test via content assertions**

```python
def test_skill_docs_reference_new_gap_target_taxonomy() -> None:
    required = {
        "skills/cfa-intent-router/SKILL.md": "MOC gap inspection",
        "skills/cfa-question-captor/SKILL.md": "knowledge_tree_core_formula",
        "skills/cfa-pattern-miner/SKILL.md": "formula_table_variant",
        "skills/cfa-review-synthesizer/SKILL.md": "knowledge_tree_concept",
        "skills/cfa-validation-guard/SKILL.md": "patch target",
    }

    for path, needle in required.items():
        text = Path(path).read_text(encoding="utf-8")
        assert needle in text
```
```

- [ ] **Step 2: Run the assertions to verify they fail**

Run:

```powershell
@'
from pathlib import Path
required = {
    "skills/cfa-intent-router/SKILL.md": "MOC gap inspection",
    "skills/cfa-question-captor/SKILL.md": "knowledge_tree_core_formula",
    "skills/cfa-pattern-miner/SKILL.md": "formula_table_variant",
    "skills/cfa-review-synthesizer/SKILL.md": "knowledge_tree_concept",
    "skills/cfa-validation-guard/SKILL.md": "patch target",
}
for path, needle in required.items():
    text = Path(path).read_text(encoding="utf-8")
    assert needle in text, f"{path} missing {needle}"
'@ | python -
```

Expected:

- AssertionError for one or more files because the new taxonomy language is not yet present

- [ ] **Step 3: Update each skill with minimal explicit taxonomy language**

```md
## Formula-aware MOC targeting

- `knowledge_tree_core_formula`: 主公式缺在知识树节点
- `formula_table_variant`: 变形/换算公式缺在公式表
- `both`: 两边都缺
- `knowledge_tree_concept`: 缺概念分支或概念区分
- `exam_trap`: 缺考试陷阱提醒
```

And add routing / validation lines such as:

```md
- “我的知识框架里有没有这个公式” -> 先做 MOC gap inspection，再决定是否 patch
- patch 前必须验证公式是否属于该知识树节点
```

- [ ] **Step 4: Re-run the assertions to verify they pass**

Run:

```powershell
@'
from pathlib import Path
required = {
    "skills/cfa-intent-router/SKILL.md": "MOC gap inspection",
    "skills/cfa-question-captor/SKILL.md": "knowledge_tree_core_formula",
    "skills/cfa-pattern-miner/SKILL.md": "formula_table_variant",
    "skills/cfa-review-synthesizer/SKILL.md": "knowledge_tree_concept",
    "skills/cfa-validation-guard/SKILL.md": "patch target",
}
for path, needle in required.items():
    text = Path(path).read_text(encoding="utf-8")
    assert needle in text, f"{path} missing {needle}"
'@ | python -
```

Expected:

- No output
- Exit code 0

- [ ] **Step 5: Commit**

```bash
git add skills/cfa-intent-router/SKILL.md skills/cfa-question-captor/SKILL.md skills/cfa-pattern-miner/SKILL.md skills/cfa-review-synthesizer/SKILL.md skills/cfa-validation-guard/SKILL.md
git commit -m "docs: teach cfa skills the new formula gap taxonomy"
```

### Task 4: Migrate the Quant MOC into the new bidirectional structure

**Files:**
- Modify: `CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md`
- Test: ad hoc content assertions

- [ ] **Step 1: Write a failing assertion for the new Quant structure**

```python
from pathlib import Path

text = Path("CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md").read_text(encoding="utf-8")
assert "│   ├── 核心公式" in text
assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text
assert "FV with Continuous Compounding" in text
```

- [ ] **Step 2: Run the assertion to verify it fails if the structure is still partial**

Run:

```powershell
@'
from pathlib import Path
text = Path("CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md").read_text(encoding="utf-8")
assert "│   ├── 核心公式" in text
assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text
'@ | python -
```

Expected:

- AssertionError because the formula-table header has not been migrated yet

- [ ] **Step 3: Update the Quant knowledge tree and formula tables**

```md
│   └── 1.5 Annualization and continuous compounding【考试核心】
│       ├── 定义/直觉
│       │   └── 连续复利口径和普通复利口径必须先统一
│       ├── 核心公式
│       │   ├── r_cc = ln(1 + HPR)
│       │   └── FV = PVe^(rt), PV = FVe^(-rt)
│       └── continuously compounded returns 可加，普通 returns 不可直接相加
```

And migrate table headers to:

```md
| 指标 | 公式 | 知识树节点 | 考试说明 |
```

- [ ] **Step 4: Re-run the assertion to verify it passes**

Run:

```powershell
@'
from pathlib import Path
text = Path("CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md").read_text(encoding="utf-8")
assert "│       ├── 核心公式" in text
assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text
assert "PVe^(rt)" in text
'@ | python -
```

Expected:

- No output
- Exit code 0

- [ ] **Step 5: Commit**

```bash
git add CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
git commit -m "docs: add bidirectional formula mapping to quant moc"
```

### Task 5: Migrate the remaining formula-heavy MOCs and protect concept-first subjects

**Files:**
- Modify: `CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md`
- Modify: `CFA_tier1/Derivatives/00-Derivatives-MOC.md`
- Modify: `CFA_tier1/Equity/00-Equity-MOC.md`
- Modify: `CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md`
- Modify: `CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md`
- Modify: `CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md`
- Modify: `CFA_tier1/Economics/00-Economics-MOC.md`
- Modify: `CFA_tier1/Alternative_Investments/00-Alternative-Investments-MOC.md`
- Modify: `CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md`

- [ ] **Step 1: Write failing assertions for migrated headers and Ethics protection**

```python
from pathlib import Path

formula_dense = [
    "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    "CFA_tier1/Equity/00-Equity-MOC.md",
]
for path in formula_dense:
    text = Path(path).read_text(encoding="utf-8")
    assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text

ethics = Path("CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md").read_text(encoding="utf-8")
assert "核心公式" not in ethics
```

- [ ] **Step 2: Run the assertions to verify they fail before migration**

Run:

```powershell
@'
from pathlib import Path
formula_dense = [
    "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    "CFA_tier1/Equity/00-Equity-MOC.md",
]
for path in formula_dense:
    text = Path(path).read_text(encoding="utf-8")
    assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text, path
ethics = Path("CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md").read_text(encoding="utf-8")
assert "核心公式" not in ethics
'@ | python -
```

Expected:

- AssertionError for one or more formula-dense MOCs because the new header is not yet present

- [ ] **Step 3: Migrate the remaining MOCs**

```md
│   ├── 核心公式
│   │   └── [main equation for this node]
```

For every formula-dense subject:

- add `核心公式` to formula-driven nodes only
- add `知识树节点` column to each formula table
- map each formula row to its owning node

For `Alternative_Investments`:

- add `核心公式` only where valuation or performance formulas are truly central

For `Ethics`:

- keep concept tree only
- do not add artificial formula nodes

- [ ] **Step 4: Re-run the assertions to verify migration**

Run:

```powershell
@'
from pathlib import Path
formula_dense = [
    "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    "CFA_tier1/Equity/00-Equity-MOC.md",
    "CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md",
    "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
    "CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md",
    "CFA_tier1/Economics/00-Economics-MOC.md",
]
for path in formula_dense:
    text = Path(path).read_text(encoding="utf-8")
    assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text, path
ethics = Path("CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md").read_text(encoding="utf-8")
assert "核心公式" not in ethics
'@ | python -
```

Expected:

- No output
- Exit code 0

- [ ] **Step 5: Commit**

```bash
git add CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md CFA_tier1/Derivatives/00-Derivatives-MOC.md CFA_tier1/Equity/00-Equity-MOC.md CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md CFA_tier1/Economics/00-Economics-MOC.md CFA_tier1/Alternative_Investments/00-Alternative-Investments-MOC.md CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md
git commit -m "docs: migrate cfa mocs to bidirectional formula mapping"
```

### Task 6: Run the full verification suite

**Files:**
- Modify: none
- Test: `.system/tests/test_workflows.py`

- [ ] **Step 1: Run the full workflow test suite**

Run:

```powershell
pytest .system/tests/test_workflows.py -v
```

Expected:

- PASS for all workflow tests

- [ ] **Step 2: Run the targeted content verification script**

Run:

```powershell
@'
from pathlib import Path
paths = list(Path("CFA_tier1").glob("*/00-*-MOC.md"))
for path in paths:
    text = path.read_text(encoding="utf-8")
    if "Ethical-and-Professional-Standards" in path.name:
        assert "核心公式" not in text
        continue
    if "## 核心公式速查" in text:
        assert "| 指标 | 公式 | 知识树节点 | 考试说明 |" in text, str(path)
'@ | python -
```

Expected:

- No output
- Exit code 0

- [ ] **Step 3: Inspect git diff for only intended files**

Run:

```powershell
git diff --stat
```

Expected:

- Only workflow, doc, skill, test, and MOC files related to this feature

- [ ] **Step 4: Commit final verification state**

```bash
git add .
git commit -m "test: verify bidirectional moc formula mapping rollout"
```

## Self-Review

- Spec coverage:
  - knowledge-tree `核心公式` standard -> Tasks 4 and 5
  - formula-table reverse mapping -> Tasks 4 and 5
  - patch target taxonomy -> Tasks 1 and 2
  - agent/skill updates -> Task 3
  - workflow alignment -> Tasks 1 and 2
  - concept-first Ethics protection -> Tasks 2 and 5
- Placeholder scan:
  - each code step includes concrete snippets or assertions
  - each verification step includes exact commands and expected results
- Type consistency:
  - plan consistently uses `gap_target`, `knowledge_tree_core_formula`, `formula_table_variant`, `knowledge_tree_concept`, and `exam_trap`

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-21-cfa-moc-formula-bidirectional-mapping.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
