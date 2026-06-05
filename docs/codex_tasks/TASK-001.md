# TASK-001

## Goal
Bootstrap governed Codex self-cycle workflow

## Why This Is Next
- loop_id: ITER-001
- candidate_id: self-cycle-skill-governance
- source: plan_doc
- phase: self-cycle
- layer: Decision

## Outputs
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

## Evidence
- 系统改革与刷题计划.docx
- AGENTS.md
