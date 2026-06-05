---
loop_id: ITER-003
generated_at: 2026-06-05T06:03:16.960607+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-2-practice-generation
- title: Add governed practice generation with AND/OR tag filters
- phase: 2-question-bank-practice
- layer: Decision
- risk_level: guarded
- task_path: docs/codex_tasks/TASK-003.md

## Expected Outputs
- Create a deterministic practice-session request model with exam, topic, chapter, count, and tag filters.
- Support AND/OR tag semantics without changing the source question bank.
- Persist generated session metadata for answer submission and review.

## Acceptance
- Practice generation can be reproduced in tests with a seeded random source.
- AND filters narrow results and OR filters broaden them as documented.
- The generated session references questions without copying or mutating canonical records.

## Safety Limits
- Do not duplicate canonical question content into mutable session state.
- Do not use random behavior in tests without a fixed seed.
- Do not add recommendation logic inside the core question-bank module.

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
- phase-2-practice-generation | 88 | guarded | Add governed practice generation with AND/OR tag filters
- phase-2-answer-wrongbook-contract | 84 | guarded | Connect answer submission to attempts, wrongbook, notes, and favorites
- phase-3-practice-ui-contract | 76 | safe | Create practice UI API contract before changing frontend screens
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
