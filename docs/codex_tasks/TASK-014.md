# TASK-014

## Goal
Expose batch attempt import in the capture workflow

## Why This Is Next
- loop_id: ITER-022
- candidate_id: gap-capture-batch-import-ui
- source: runtime_gap
- phase: 1-environment-data-model
- layer: Projection

## Outputs
- Add a batch import surface to Question Capture for multiple attempts or mistake records.
- Bridge the UI to the existing batch-import API instead of keeping it API-only.
- Keep single-question manual capture and screenshot capture intact.

## Acceptance
- Capture UI exposes a clear batch import path.
- The batch import route is no longer hidden behind direct API usage only.
- Typecheck or deterministic verification confirms the added UI compiles.

## Safety Limits
- Do not disrupt the existing manual or screenshot capture flow.
- Do not invent remote file storage if the first pass can use pasted JSON.
- Keep the first version minimal and local-first.

## Evidence
- apps/web/src/app/capture/page.tsx
- apps/api/routers/attempts.py
- docs/research/product-audit-report.md#G15
