# TASK-006

## Goal
Separate analytics and recommendation extension boundary from core practice

## Why This Is Next
- loop_id: ITER-006
- candidate_id: phase-4-analytics-extension-boundary
- source: plan_doc
- phase: 4-analytics-extensions
- layer: Decision

## Outputs
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

## Evidence
- 系统改革与刷题计划.docx#阶段4
