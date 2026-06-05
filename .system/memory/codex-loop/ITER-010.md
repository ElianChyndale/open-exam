---
loop_id: ITER-010
generated_at: 2026-06-05T09:40:46.074181+00:00
mode: unattended
status: planned
---

# Codex Self-Cycle Plan

## Selected Next Work
- candidate_id: gap-screenshot-structured-extraction
- title: Replace screenshot placeholder flow with structured extraction handoff
- phase: capture-screenshot
- layer: Capture
- risk_level: guarded
- task_path: docs/codex_tasks/TASK-008.md

## Expected Outputs
- Create a local structured extraction artifact for screenshot uploads instead of returning only a placeholder payload.
- Preserve raw image evidence and mark uncertain fields explicitly instead of guessing LOS or conclusions.
- Keep the extraction handoff traceable so a later agent step can complete record-mistake safely.

## Acceptance
- Screenshot upload returns a durable extraction draft reference, not only a generic saved status.
- Draft output stores evidence path plus clearly empty or uncertain fields when the image cannot support them.
- Tests cover safe filename handling and the structured handoff contract.

## Safety Limits
- Do not hallucinate LOS, source, choices, or correct answers from unclear screenshots.
- Do not delete or rewrite the original screenshot evidence asset.
- Do not claim full AI extraction unless the workflow persists an explicit draft artifact.

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
- gap-screenshot-structured-extraction | 96 | guarded | Replace screenshot placeholder flow with structured extraction handoff
