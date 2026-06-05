# TASK-008

## Goal
Replace screenshot placeholder flow with structured extraction handoff

## Why This Is Next
- loop_id: ITER-010
- candidate_id: gap-screenshot-structured-extraction
- source: runtime_gap
- phase: capture-screenshot
- layer: Capture

## Outputs
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

## Evidence
- apps/api/routers/attempts.py
- docs/research/product-audit-report.md#G1
- AGENTS.md
