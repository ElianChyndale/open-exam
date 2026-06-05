# TASK-012

## Goal
Make question-bank import console aware of admin session requirements

## Why This Is Next
- loop_id: ITER-019
- candidate_id: gap-import-console-admin-guidance
- source: runtime_gap
- phase: 3-frontend-prototype
- layer: Projection

## Outputs
- Show explicit admin-session guidance inside the question-bank import console.
- Surface 401/403 failures as actionable prompts instead of silent loading failures.
- Link import/review operators to the admin auth page without affecting learner practice.

## Acceptance
- Import console displays a clear path to `/review/admin-auth` when no admin session is active.
- Protected API failures produce a readable UI state instead of disappearing silently.
- Learner-facing practice screens remain unchanged.

## Safety Limits
- Do not require admin auth for learner-only screens.
- Do not expose session tokens in the UI.
- Keep the first pass focused on guidance, not a full auth redesign.

## Evidence
- apps/web/src/components/capture/QuestionBankImportConsole.tsx
- apps/web/src/app/review/admin-auth/page.tsx
