# TASK-011

## Goal
Expose local auth session and admin entry flow in the frontend

## Why This Is Next
- loop_id: ITER-016
- candidate_id: gap-auth-ui-session-integration
- source: runtime_gap
- phase: 3-frontend-prototype
- layer: Projection

## Outputs
- Add frontend API helpers for bootstrap-admin, login, logout, and session lookup.
- Create a minimal admin auth entry surface so protected import/review tools have a session path.
- Keep learner practice flow separate from admin import/review flow.

## Acceptance
- Frontend API layer includes auth session helpers.
- Admin-facing UI can create or resume a session without touching learner practice pages.
- Tests or deterministic checks confirm the admin auth surface is wired to the local API.

## Safety Limits
- Do not block anonymous learner practice until a broader auth migration is planned.
- Do not mix admin import controls into learner-only panels.
- Keep the first UI step local-only and explicit about development scope.

## Evidence
- apps/api/routers/auth.py
- apps/web/src/lib/api.ts
- docs/research/product-audit-report.md#G8
