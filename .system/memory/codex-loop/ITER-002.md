---
loop_id: ITER-002
generated_at: 2026-06-05T06:00:33.911096+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-1-import-contract
- title: Harden question-bank import contract and immutable published records
- phase: 1-environment-data-model
- layer: Capture
- risk_level: guarded
- task_path: docs/codex_tasks/TASK-002.md

## Expected Outputs
- Define import payload validation for exam, subject, chapter, knowledge tags, difficulty, and answer fields.
- Add a published-question immutability guard for prompts, choices, answers, and explanations.
- Emit an import report that separates accepted, rejected, duplicate, and locked records.

## Acceptance
- Invalid imports are rejected with actionable errors.
- Published core question content cannot be changed without an explicit override path.
- Tests prove import order and explanation text stay stable after publish.

## Safety Limits
- Do not rewrite existing core question text or answer explanations.
- Do not infer missing official answers from ambiguous source files.
- Keep import changes behind tests and local data only.

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
- phase-1-import-contract | 92 | guarded | Harden question-bank import contract and immutable published records
- phase-2-practice-generation | 88 | guarded | Add governed practice generation with AND/OR tag filters
- phase-2-answer-wrongbook-contract | 84 | guarded | Connect answer submission to attempts, wrongbook, notes, and favorites
- phase-3-practice-ui-contract | 76 | safe | Create practice UI API contract before changing frontend screens
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
