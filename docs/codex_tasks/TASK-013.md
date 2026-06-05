# TASK-013

## Goal
Add CSV/XLSX file bridge to the question-bank import console

## Why This Is Next
- loop_id: ITER-020
- candidate_id: gap-import-console-file-bridge
- source: runtime_gap
- phase: 1-environment-data-model
- layer: Projection

## Outputs
- Add a file picker flow for CSV/XLSX import guidance in the admin question-bank console.
- Bridge the frontend to an existing local import path instead of forcing raw JSON paste only.
- Keep the imported-question immutability and admin-session rules intact.

## Acceptance
- Console clearly supports choosing a CSV/XLSX file or shows the exact local import path workflow.
- The UI no longer implies JSON paste is the only realistic admin import route.
- Typecheck or deterministic verification confirms the new flow compiles.

## Safety Limits
- Do not bypass admin auth or question-bank validation rules.
- Do not invent remote upload storage when the repo still uses local-first import.
- Keep the first pass scoped to a bridge, not a full ingestion redesign.

## Evidence
- apps/web/src/components/capture/QuestionBankImportConsole.tsx
- scripts/import_qbank_excel.py
