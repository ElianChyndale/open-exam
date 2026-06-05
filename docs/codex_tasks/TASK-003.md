# TASK-003

## Goal
Add governed practice generation with AND/OR tag filters

## Why This Is Next
- loop_id: ITER-003
- candidate_id: phase-2-practice-generation
- source: plan_doc
- phase: 2-question-bank-practice
- layer: Decision

## Outputs
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

## Evidence
- 系统改革与刷题计划.docx#阶段2
