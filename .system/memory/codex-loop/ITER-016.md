---
loop_id: ITER-016
generated_at: 2026-06-05T09:50:53.324905+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: gap-auth-ui-session-integration
- title: Expose local auth session and admin entry flow in the frontend
- phase: 3-frontend-prototype
- layer: Projection
- risk_level: safe
- task_path: docs/codex_tasks/TASK-011.md

## Expected Outputs
- Add frontend API helpers for bootstrap-admin, login, logout, and session lookup.
- Create a minimal admin auth entry surface so protected import/review tools have a session path.
- Keep learner practice flow separate from admin import/review flow.

## Acceptance
- Frontend API layer includes auth session helpers.
- Admin-facing UI can create or resume a session without touching learner practice pages.
- Tests or deterministic checks confirm the admin auth surface is wired to the local API.

## Safety Limits
- Do not block anonymous learner practice until a broader auth migration is planned.
- Do not mix admin import controls into learner-only panels.
- Keep the first UI step local-only and explicit about development scope.

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
- gap-auth-ui-session-integration | 82 | safe | Expose local auth session and admin entry flow in the frontend
