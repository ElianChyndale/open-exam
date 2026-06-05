# TASK-005

## Goal
Create practice UI API contract before changing frontend screens

## Why This Is Next
- loop_id: ITER-005
- candidate_id: phase-3-practice-ui-contract
- source: plan_doc
- phase: 3-frontend-prototype
- layer: Decision

## Outputs
- Write a compact API contract for project selection, practice configuration, question display, and submission.
- Define frontend states for unanswered, answered, reviewed, noted, and favorited questions.
- Add a smoke-test checklist for browser verification.

## Acceptance
- The contract names every backend field the practice UI needs.
- The checklist can be run before and after frontend work.
- No frontend route is changed before the contract exists.

## Safety Limits
- Do not redesign UI until the API contract is stable.
- Do not introduce Chrome/browser dependency into backend-only tests.
- Preserve existing dashboard routes.

## Evidence
- 系统改革与刷题计划.docx#阶段3
