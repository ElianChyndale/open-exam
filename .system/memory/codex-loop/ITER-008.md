---
loop_id: ITER-008
generated_at: 2026-06-05T06:10:12.568460+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-3-safe-question-display-endpoint
- title: Implement safe practice question display endpoint from UI contract
- phase: 3-frontend-prototype
- layer: Decision
- risk_level: guarded
- task_path: docs/codex_tasks/TASK-007.md

## Expected Outputs
- Add a session-scoped question display endpoint for practice UI use.
- Return prompt, choices, learner state, note count, and favorite state before submission.
- Keep answer, explanation, and correct-answer fields hidden from display payloads.

## Acceptance
- Display endpoint returns 404 or 422 for missing sessions or mismatched question IDs.
- Pre-submission payload includes prompt and choices but excludes answer/explanation fields.
- Post-submission display reflects answered/noted/favorited state without exposing canonical answers.

## Safety Limits
- Do not duplicate display payloads into practice session metadata.
- Do not expose answer, correct_answer, explanation, rationale, or hidden diagnostics.
- Do not change frontend routes until backend contract tests pass.

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
- phase-3-safe-question-display-endpoint | 86 | guarded | Implement safe practice question display endpoint from UI contract
