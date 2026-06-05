---
loop_id: ITER-005
generated_at: 2026-06-05T06:07:13.226280+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-3-practice-ui-contract
- title: Create practice UI API contract before changing frontend screens
- phase: 3-frontend-prototype
- layer: Decision
- risk_level: safe
- task_path: docs/codex_tasks/TASK-005.md

## Expected Outputs
- Write a compact API contract for project selection, practice configuration, question display, and submission.
- Define frontend states for unanswered, answered, reviewed, noted, and favorited questions.
- Add a smoke-test checklist for browser verification.

## Acceptance
- The contract names every backend field the practice UI needs.
- The checklist can be run before and after frontend work.
- No frontend route is changed before the contract exists.

## Safety Limits
- Do not redesign UI until the API contract is stable.
- Do not introduce Chrome/browser dependency into backend-only tests.
- Preserve existing dashboard routes.

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
- phase-3-practice-ui-contract | 76 | safe | Create practice UI API contract before changing frontend screens
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
