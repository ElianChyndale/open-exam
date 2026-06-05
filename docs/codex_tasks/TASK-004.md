# TASK-004

## Goal
Connect answer submission to attempts, wrongbook, notes, and favorites

## Why This Is Next
- loop_id: ITER-004
- candidate_id: phase-2-answer-wrongbook-contract
- source: plan_doc
- phase: 2-question-bank-practice
- layer: Capture

## Outputs
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

## Evidence
- 系统改革与刷题计划.docx#阶段2
