---
loop_id: ITER-022
generated_at: 2026-06-05T10:25:08.052627+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: gap-capture-batch-import-ui
- title: Expose batch attempt import in the capture workflow
- phase: 1-environment-data-model
- layer: Projection
- risk_level: safe
- task_path: docs/codex_tasks/TASK-014.md

## Expected Outputs
- Add a batch import surface to Question Capture for multiple attempts or mistake records.
- Bridge the UI to the existing batch-import API instead of keeping it API-only.
- Keep single-question manual capture and screenshot capture intact.

## Acceptance
- Capture UI exposes a clear batch import path.
- The batch import route is no longer hidden behind direct API usage only.
- Typecheck or deterministic verification confirms the added UI compiles.

## Safety Limits
- Do not disrupt the existing manual or screenshot capture flow.
- Do not invent remote file storage if the first pass can use pasted JSON.
- Keep the first version minimal and local-first.

## Stop Conditions
- No eligible non-human candidate remains.
- The same blocker repeats for three consecutive goal turns.
- A task would modify locked question-bank content, secrets, destructive filesystem state, or remote GitHub refs.
- Targeted verification cannot be run or replaced by an explicit verification note.

## Impact Controls
- Prefer Capture/Memory/Decision Layer changes before Projection changes.
- Write plan and completion events before selecting the next task.
- Keep core brushing-question flow stable; put recommendations and analytics behind extension boundaries.
- Use tests or deterministic validation before marking work complete.

## Candidates Considered
- gap-capture-batch-import-ui | 72 | safe | Expose batch attempt import in the capture workflow
