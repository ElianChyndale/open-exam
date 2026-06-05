---
loop_id: ITER-001
generated_at: 2026-06-05T05:59:51.557713+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: self-cycle-skill-governance
- title: Bootstrap governed Codex self-cycle workflow
- phase: self-cycle
- layer: Decision
- risk_level: safe
- task_path: docs/codex_tasks/TASK-001.md

## Expected Outputs
- Create a governed Codex loop planner that can choose the next safe task from local evidence.
- Add CLI commands for planning and completing autonomous loop steps.
- Document safety gates so unattended work cannot mutate core question-bank truth silently.

## Acceptance
- A local command writes a traceable next-step plan and task artifact.
- Completed candidates are not selected again.
- Tests cover planning, completion, and proposal-driven task selection.

## Safety Limits
- Do not auto-edit published question content, locked answer keys, secrets, or remote branches.
- Do not mark a task complete without tests or an explicit verification note.
- Do not bypass AGENTS Source of Truth ordering.

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
- self-cycle-skill-governance | 100 | safe | Bootstrap governed Codex self-cycle workflow
- phase-1-import-contract | 92 | guarded | Harden question-bank import contract and immutable published records
- phase-2-practice-generation | 88 | guarded | Add governed practice generation with AND/OR tag filters
- phase-2-answer-wrongbook-contract | 84 | guarded | Connect answer submission to attempts, wrongbook, notes, and favorites
- phase-3-practice-ui-contract | 76 | safe | Create practice UI API contract before changing frontend screens
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
