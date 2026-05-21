# CFA_tier1 Vault Restructure Implementation Plan

> Note: This plan documents the original restructuring sequence. The current live vault has since been refined into subject-based directories such as `Quantitative_Methods/`, `Ethical_and_Professional_Standards/`, and `dashboard/`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the repository into an Obsidian-friendly `CFA_tier1` vault with `.obsidian` config and move the agent system paths under `.system/` without breaking CLI exports.

**Architecture:** The repository keeps its current data model and CLI behavior, but path resolution moves into a new vault-oriented filesystem layout. Generated pages are isolated under `CFA_tier1/90-Exports/`, curated notes live in topic folders, and the internal workflow storage moves under `.system/`.

**Tech Stack:** Python, pathlib, pytest, markdown files, Obsidian vault conventions

---

## File Map

- Modify: `app/storage.py`
- Modify: `app/workflows.py`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `tests/test_workflows.py`
- Create: `.obsidian/.gitkeep`
- Create: `CFA_tier1/00-Index.md`
- Create: `CFA_tier1/00-Overview/.gitkeep`
- Create: `CFA_tier1/90-Exports/.gitkeep`
- Move: `CFA_L1_备考指南.md` -> `CFA_tier1/00-Overview/CFA_L1_备考指南.md`
- Move: `数量_Quantitative_Methods_知识框架.md` -> `CFA_tier1/01-Quantitative/数量_Quantitative_Methods_知识框架.md`
- Create: `.system/app/.gitkeep`
- Create: `.system/events/.gitkeep`
- Create: `.system/memory/.gitkeep`
- Create: `.system/evals/.gitkeep`
- Create: `.system/tests/.gitkeep`
- Move: `app/`, `events/`, `memory/`, `evals/`, `tests/` into `.system/`

### Task 1: Update tests first for the new repository paths

**Files:**
- Modify: `tests/test_workflows.py`

- [ ] **Step 1: Write the failing path assertions**

```python
question_events = list((tmp_path / ".system" / "events" / "question").glob("*.jsonl"))
cards = list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
daily = tmp_path / "CFA_tier1" / "90-Exports" / "今日新增错题.md"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_workflows.py -q`
Expected: FAIL because `Repository` still points to `events/`, `memory/`, and `obsidian/`

### Task 2: Implement the new path resolution

**Files:**
- Modify: `app/storage.py`

- [ ] **Step 1: Change repository roots**

```python
self.system_root = root / ".system"
self.events_root = self.system_root / "events"
self.memory_root = self.system_root / "memory"
self.obsidian_root = root / "CFA_tier1" / "90-Exports"
self.vault_root = root / "CFA_tier1"
self.app_root = self.system_root / "app"
self.skills_root = root / "skills"
self.evals_root = self.system_root / "evals"
```

- [ ] **Step 2: Ensure the new directories are created**

```python
directories = [
    self.events_root / "question",
    self.events_root / "bias",
    self.events_root / "agent",
    self.memory_root / "question-errors",
    self.memory_root / "cognitive-bias",
    self.memory_root / "agent-failures",
    self.memory_root / "patterns",
    self.memory_root / "strategy",
    self.memory_root / "validation",
    self.vault_root / "00-Overview",
    self.vault_root / "01-Quantitative",
    self.vault_root / "90-Exports",
    self.root / ".obsidian",
    self.skills_root,
    self.evals_root / "results",
]
```

- [ ] **Step 3: Run tests to verify path behavior passes**

Run: `pytest tests/test_workflows.py -q`
Expected: fewer or no path failures

### Task 3: Keep workflow exports aligned with the vault

**Files:**
- Modify: `app/workflows.py`

- [ ] **Step 1: Keep export names stable but rely on the new vault export root**

```python
repo.write_obsidian_page("今日新增错题.md", [...])
repo.write_obsidian_page("高频错因榜.md", [...])
repo.write_obsidian_page("Topic弱点页.md", [...])
repo.write_obsidian_page("Agent失误页.md", [...])
repo.write_obsidian_page("策略手册页.md", [...])
```

- [ ] **Step 2: Run the full workflow tests**

Run: `pytest tests/test_workflows.py -q`
Expected: PASS

### Task 4: Update docs for the new structure

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Rewrite structure references**

```text
- `CFA_tier1/` stores Obsidian-readable study content and exported projection pages.
- `.system/events/` stores raw question, bias, and agent event logs.
- `.system/memory/` stores durable markdown cards and strategy artifacts.
- `.obsidian/` stores Obsidian vault configuration only.
```

- [ ] **Step 2: Re-run targeted tests to confirm docs changes did not touch runtime**

Run: `pytest tests/test_workflows.py -q`
Expected: PASS

### Task 5: Move vault-facing content and create scaffolding

**Files:**
- Create: `.obsidian/.gitkeep`
- Create: `CFA_tier1/00-Index.md`
- Move: `CFA_L1_备考指南.md`
- Move: `数量_Quantitative_Methods_知识框架.md`
- Move: `app/`, `events/`, `memory/`, `evals/`, `tests/`

- [ ] **Step 1: Create the vault scaffold**

```text
CFA_tier1/00-Overview/
CFA_tier1/01-Quantitative/
CFA_tier1/90-Exports/
.obsidian/
.system/
```

- [ ] **Step 2: Move the content and system directories into place**

Run:

```powershell
Move-Item app .system/app
Move-Item events .system/events
Move-Item memory .system/memory
Move-Item evals .system/evals
Move-Item tests .system/tests
Move-Item CFA_L1_备考指南.md CFA_tier1/00-Overview/CFA_L1_备考指南.md
Move-Item 数量_Quantitative_Methods_知识框架.md CFA_tier1/01-Quantitative/数量_Quantitative_Methods_知识框架.md
```

- [ ] **Step 3: Run workflow tests from the repository root**

Run: `pytest .system/tests/test_workflows.py -q`
Expected: PASS

### Task 6: Final verification

**Files:**
- Verify only

- [ ] **Step 1: Run the full focused test suite**

Run: `pytest .system/tests/test_workflows.py -q`
Expected: all tests pass

- [ ] **Step 2: Smoke test the CLI**

Run:

```powershell
python -m .system.app.main pre-mock-brief
```

Expected: command invocation path may need adjustment if package execution through `.system` is not valid; if so, document the package/module constraint and retain root-level importability via Python path assumptions.
