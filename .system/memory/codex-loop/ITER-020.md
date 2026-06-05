---
loop_id: ITER-020
generated_at: 2026-06-05T10:23:30.269911+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: gap-import-console-file-bridge
- title: Add CSV/XLSX file bridge to the question-bank import console
- phase: 1-environment-data-model
- layer: Projection
- risk_level: safe
- task_path: docs/codex_tasks/TASK-013.md

## Expected Outputs
- Add a file picker flow for CSV/XLSX import guidance in the admin question-bank console.
- Bridge the frontend to an existing local import path instead of forcing raw JSON paste only.
- Keep the imported-question immutability and admin-session rules intact.

## Acceptance
- Console clearly supports choosing a CSV/XLSX file or shows the exact local import path workflow.
- The UI no longer implies JSON paste is the only realistic admin import route.
- Typecheck or deterministic verification confirms the new flow compiles.

## Safety Limits
- Do not bypass admin auth or question-bank validation rules.
- Do not invent remote upload storage when the repo still uses local-first import.
- Keep the first pass scoped to a bridge, not a full ingestion redesign.

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
- gap-import-console-file-bridge | 73 | safe | Add CSV/XLSX file bridge to the question-bank import console
