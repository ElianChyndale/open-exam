# TASK-007

## Goal
Implement safe practice question display endpoint from UI contract

## Why This Is Next
- loop_id: ITER-008
- candidate_id: phase-3-safe-question-display-endpoint
- source: contract_gap
- phase: 3-frontend-prototype
- layer: Decision

## Outputs
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

## Evidence
- docs/practice_ui_api_contract.md#Question Display
