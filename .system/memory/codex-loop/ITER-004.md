---
loop_id: ITER-004
generated_at: 2026-06-05T06:05:05.342349+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-2-answer-wrongbook-contract
- title: Connect answer submission to attempts, wrongbook, notes, and favorites
- phase: 2-question-bank-practice
- layer: Capture
- risk_level: guarded
- task_path: docs/codex_tasks/TASK-004.md

## Expected Outputs
- Persist each answer attempt with correctness, selected answer, time spent, and session ID.
- Update wrongbook records idempotently when answers are incorrect.
- Add note and favorite records that remain attached to a stable question ID.

## Acceptance
- Repeated incorrect answers increment wrongbook counters instead of creating duplicates.
- Correct retries can lower wrongbook priority without deleting history.
- Notes and favorites survive repeated answer submissions.

## Safety Limits
- Do not delete historical attempts when wrongbook priority changes.
- Do not expose hidden correct answers before submission.
- Keep user notes separate from canonical question text.

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
- phase-2-answer-wrongbook-contract | 84 | guarded | Connect answer submission to attempts, wrongbook, notes, and favorites
- phase-3-practice-ui-contract | 76 | safe | Create practice UI API contract before changing frontend screens
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
