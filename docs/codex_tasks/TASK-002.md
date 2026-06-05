# TASK-002

## Goal
Harden question-bank import contract and immutable published records

## Why This Is Next
- loop_id: ITER-002
- candidate_id: phase-1-import-contract
- source: plan_doc
- phase: 1-environment-data-model
- layer: Capture

## Outputs
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

## Evidence
- 系统改革与刷题计划.docx#阶段1
