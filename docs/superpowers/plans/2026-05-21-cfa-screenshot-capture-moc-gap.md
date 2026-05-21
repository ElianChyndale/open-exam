# CFA Screenshot Capture and MOC Gap Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Codex-native screenshot mistake capture metadata, a new `moc-gap-review` workflow, and the documentation needed to close the CFA mistake-to-MOC learning loop.

**Architecture:** The local runtime remains a storage and review engine, not an OCR system. Screenshot interpretation happens in Codex via a new skill contract, while Python code receives richer payloads, preserves provenance metadata, and generates controlled MOC gap review artifacts instead of mutating MOCs directly.

**Tech Stack:** Python, dataclasses, pathlib, argparse, pytest, markdown, JSONL, SQLite-backed artifact indexing

---

## File Map

- Modify: `.system/app/models.py`
- Modify: `.system/app/workflows.py`
- Modify: `.system/app/cli.py`
- Modify: `.system/app/storage.py`
- Modify: `.system/tests/test_workflows.py`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Create: `skills/cfa-screenshot-mistake-captor/SKILL.md`
- Create: `docs/superpowers/specs/2026-05-21-cfa-screenshot-capture-moc-gap-design.md`

### Task 1: Add regression tests for richer event metadata

**Files:**
- Modify: `.system/tests/test_workflows.py`

- [ ] **Step 1: Write a failing test for optional screenshot metadata on question events**

The new test should prove that `record-mistake` accepts and stores:

- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

It should assert both:

- the event JSONL contains those fields
- the generated card markdown contains those fields in frontmatter or body

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `pytest .system/tests/test_workflows.py::test_record_question_mistake_preserves_screenshot_metadata -q`

Expected: FAIL because `MistakeEvent` does not yet accept the new fields.

### Task 2: Extend the event and card data models

**Files:**
- Modify: `.system/app/models.py`

- [ ] **Step 1: Add optional fields to `MistakeEvent`**

Add these optional fields with safe defaults:

- `question_source: str = ""`
- `source_type: str = ""`
- `evidence_assets: list[str] = field(default_factory=list)`
- `moc_target: str = ""`

The implementation must keep older payloads valid.

- [ ] **Step 2: Extend `MistakeCard` so the new metadata survives projection**

Add matching fields where useful so the generated card can preserve provenance:

- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

Update `MistakeCard.from_event(...)` accordingly.

- [ ] **Step 3: Run the focused metadata test**

Run: `pytest .system/tests/test_workflows.py::test_record_question_mistake_preserves_screenshot_metadata -q`

Expected: PASS

### Task 3: Persist the new metadata in stored cards

**Files:**
- Modify: `.system/app/storage.py`

- [ ] **Step 1: Update `save_card(...)` markdown output**

Add the new fields to card frontmatter when present:

- `question_source`
- `source_type`
- `evidence_assets`
- `moc_target`

`evidence_assets` can be serialized as a comma-joined line in the first version.

- [ ] **Step 2: Keep the storage format backward compatible**

Do not require these fields for older cards and do not change the directory layout.

- [ ] **Step 3: Re-run the focused metadata test**

Run: `pytest .system/tests/test_workflows.py::test_record_question_mistake_preserves_screenshot_metadata -q`

Expected: PASS with card assertions green.

### Task 4: Add the `moc-gap-review` behavior test first

**Files:**
- Modify: `.system/tests/test_workflows.py`

- [ ] **Step 1: Write a failing test for recurring mistakes that should produce a MOC gap review**

The test should:

1. record at least 3 `question` events with the same `topic`, `los`, and `error_type`
2. include a valid `moc_target`
3. run the new `moc-gap-review` command
4. assert that `.system/memory/strategy/moc-gap-review.md` exists
5. assert that the artifact contains:
   - the `moc_target`
   - recurrence count
   - a suggested gap type

- [ ] **Step 2: Write a second failing test for recurring mistakes without `moc_target`**

This should prove the review does not invent framework update targets when the source data is incomplete.

- [ ] **Step 3: Run the focused review tests to verify they fail**

Run:

```powershell
pytest .system/tests/test_workflows.py::test_moc_gap_review_creates_recommendation_for_repeated_targeted_errors -q
pytest .system/tests/test_workflows.py::test_moc_gap_review_skips_repeated_errors_without_moc_target -q
```

Expected: FAIL because the CLI and workflow do not exist yet.

### Task 5: Implement the `moc-gap-review` workflow

**Files:**
- Modify: `.system/app/workflows.py`

- [ ] **Step 1: Add a helper that classifies the likely MOC gap type**

Recommended first-pass mapping:

- `formula_misuse` -> `formula`
- `concept_confusion` -> `knowledge_tree`
- fallback -> `exam_trap`

Keep this simple and explicit.

- [ ] **Step 2: Add a workflow function such as `moc_gap_review(repo: Repository) -> Path | None`**

The function should:

1. load events
2. filter to `source_layer == "question"`
3. group by `topic + los + error_type + moc_target`
4. require recurrence `>= 3`
5. skip entries with empty `moc_target`
6. write a markdown artifact to `.system/memory/strategy/moc-gap-review.md`

- [ ] **Step 3: Make the artifact readable and review-oriented**

Include:

- title
- generated timestamp
- one section per recommendation
- evidence refs or event IDs
- human-readable reason

- [ ] **Step 4: Run the focused review tests**

Run:

```powershell
pytest .system/tests/test_workflows.py::test_moc_gap_review_creates_recommendation_for_repeated_targeted_errors -q
pytest .system/tests/test_workflows.py::test_moc_gap_review_skips_repeated_errors_without_moc_target -q
```

Expected: PASS

### Task 6: Wire the new CLI command

**Files:**
- Modify: `.system/app/cli.py`

- [ ] **Step 1: Add the `moc-gap-review` subparser**

Match the style of the existing command registration.

- [ ] **Step 2: Route the command in `run_cli(...)`**

It should call the new workflow and return `0` on success.

- [ ] **Step 3: Run a focused CLI test or the review tests again**

Run:

```powershell
pytest .system/tests/test_workflows.py::test_moc_gap_review_creates_recommendation_for_repeated_targeted_errors -q
```

Expected: PASS with command parsing included.

### Task 7: Add the screenshot capture skill contract

**Files:**
- Create: `skills/cfa-screenshot-mistake-captor/SKILL.md`

- [ ] **Step 1: Write the skill file**

The skill should instruct Codex to:

- treat screenshots as raw evidence
- extract only reliable information
- fill the new provenance fields
- map to the existing `record-mistake` workflow
- avoid guessing LOS or question source when uncertain

- [ ] **Step 2: Keep the skill aligned with AGENTS rules**

The skill should preserve the project’s evidence-first rule and the `question -> pattern -> strategy` promotion order.

### Task 8: Update repository docs

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Update `README.md` quick-start guidance**

Add a short explanation that:

- Codex can capture screenshot mistakes into structured events
- richer source metadata is stored
- `moc-gap-review` exists as a controlled MOC feedback stage

- [ ] **Step 2: Update `AGENTS.md` workflow guidance**

Document:

- the new provenance fields in `MistakeEvent`
- screenshot-based question capture as a valid evidence path
- the role of `moc-gap-review`
- the fact that MOC updates are review-driven rather than automatic

- [ ] **Step 3: Re-run the full test suite**

Run: `pytest -q`

Expected: PASS

### Task 9: Final verification

**Files:**
- Verify only

- [ ] **Step 1: Run the full workflow test suite**

Run: `pytest -q`

Expected: all tests pass

- [ ] **Step 2: Smoke test the new CLI surface**

Run:

```powershell
python scripts/cfa.py --help
python scripts/cfa.py moc-gap-review
```

Expected:

- help output includes `moc-gap-review`
- command completes without parser error in an initialized repo

- [ ] **Step 3: Optional isolated smoke test**

In a temporary repo root:

1. write 3 screenshot-style `record-mistake` events with the same `moc_target`
2. run `moc-gap-review`
3. verify the review file is generated under `.system/memory/strategy/`
