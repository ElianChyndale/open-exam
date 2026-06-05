---
loop_id: ITER-019
generated_at: 2026-06-05T09:56:35.087104+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: gap-import-console-admin-guidance
- title: Make question-bank import console aware of admin session requirements
- phase: 3-frontend-prototype
- layer: Projection
- risk_level: safe
- task_path: docs/codex_tasks/TASK-012.md

## Expected Outputs
- Show explicit admin-session guidance inside the question-bank import console.
- Surface 401/403 failures as actionable prompts instead of silent loading failures.
- Link import/review operators to the admin auth page without affecting learner practice.

## Acceptance
- Import console displays a clear path to `/review/admin-auth` when no admin session is active.
- Protected API failures produce a readable UI state instead of disappearing silently.
- Learner-facing practice screens remain unchanged.

## Safety Limits
- Do not require admin auth for learner-only screens.
- Do not expose session tokens in the UI.
- Keep the first pass focused on guidance, not a full auth redesign.

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
- gap-import-console-admin-guidance | 74 | safe | Make question-bank import console aware of admin session requirements
