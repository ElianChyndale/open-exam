---
loop_id: ITER-006
generated_at: 2026-06-05T06:08:16.912830+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: phase-4-analytics-extension-boundary
- title: Separate analytics and recommendation extension boundary from core practice
- phase: 4-analytics-extensions
- layer: Decision
- risk_level: safe
- task_path: docs/codex_tasks/TASK-006.md

## Expected Outputs
- Document which statistics are core and which recommendations are extension-layer outputs.
- Add a local feature flag boundary for recommendation and adaptive-practice modules.
- Define rollback behavior when analytics extension code fails.

## Acceptance
- Core answer submission works when recommendation flags are disabled.
- Analytics failures do not corrupt canonical attempts or question-bank records.
- Tests cover at least one disabled-extension path.

## Safety Limits
- Do not make core practice depend on AI recommendation availability.
- Do not store generated strategy as canonical evidence.
- Keep extension outputs traceable to attempt and wrongbook events.

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
- phase-4-analytics-extension-boundary | 72 | safe | Separate analytics and recommendation extension boundary from core practice
