# OpenExam Recovery Execution Plan

> Date: 2026-06-03  
> Inputs: `2.md`, `docs/OPENEXAM_UPGRADE_PLAN.md`, recovered ClaudeCode task state, current workspace state

## 1. Purpose

This plan is the execution contract for the current recovery run.

It does three things at once:

1. Continues the interrupted ClaudeCode implementation instead of restarting from scratch.
2. Preserves the core product direction from `2.md`.
3. Forces quality gates so the repo does not accumulate half-connected waves.

This document supersedes any assumption that `docs/OPENEXAM_UPGRADE_PLAN.md` reflects real implementation progress. That file remains the target architecture. This file is the current execution truth.

## 2. Current State

### 2.1 Real Progress

| Area | State | Notes |
|---|---|---|
| Wave 1: Knowledge ingestion | Partial implementation | Core files, models, and router exist; not yet proven to feed downstream review. |
| Wave 2: Knowledge coverage | Mostly planned | Coverage workflow, router, and dashboard are not fully present. |
| Wave 3: Review Lab | Implemented but not fully stabilized | Engine, API, page, and hooks exist; recovery/history bug required follow-up fix. |
| Wave 4: DictionaryOS | Implemented skeleton | Dictionary models, importers, index, router, API client, and pages exist. |
| Wave 5: Language card quality | Partial | `cards_v2.py`, `spanish_morphology.py`, `false_friends.py`, `lexical_graph.py` exist; workflow adoption was incomplete. |
| Wave 6: Resource quality | New minimal implementation in progress | Quality scoring, candidate queue, promotion helper, router, and page now exist as additive modules. |
| Wave 7: Unified dashboard | Planned | Not part of this immediate recovery batch. |

### 2.2 Recovered ClaudeCode Task Truth

Recovered task state shows:

- Task `7`: KnowledgeOS PDF pipeline completed
- Task `8`: DailyReview Lab completed
- Task `9`: DictionaryOS completed
- Task `10`: Wave 4-5 LanguageOS core files were still in progress
- Task `11`: Language dictionary router/API integration completed
- Task `12`: Wave 6 ResourceOS quality engine was pending

That means the current recovery batch must finish Task `10`, Task `12`, and the quality/stability work they exposed.

### 2.3 Immediate Baseline Risks

- `review_lab` and `dictionary_os` were gated by flags without clear UX fallback.
- `cards_v2` existed but did not fully own the language card generation path.
- Review Lab history did not support restoring active or paused sessions.
- ResourceOS promotion was still lane/license driven without a quality gate layer.
- Existing repo regression: `update_knowledge_from_diagnosis` was referenced by the diagnosis router but not exported from `app.workflows`.
- Working tree mixed source changes with runtime artifacts under `.system/events`, `.system/memory`, logs, and dashboard projections.

## 3. Recovery Strategy

We do not expand horizontally first. We close the current batch.

### Batch 1: Stabilize the Existing New Core

Goal: turn the already-started waves into a coherent, testable update.

Scope:

- Wave 1 ingestion remains in place and must at least keep its event/projection path intact.
- Wave 3 Review Lab must be usable and restorable.
- Wave 4 DictionaryOS must be reachable, searchable, and test-backed.
- Wave 5 language card quality must affect real generation behavior, not just exist in isolated modules.
- Wave 6 Resource quality must exist as a real candidate/review workflow, even if introduced as a sidecar rather than a full replacement.
- Baseline regressions that block trust in the repo must be fixed now.

Definition of done:

- All new surfaces are behind explicit flags or have a deliberate fallback path.
- Language cards no longer regress into `front == answer` when the new path is enabled.
- Review Lab history supports `active`, `paused`, and `completed` recovery.
- Resource candidates can be scored, reviewed, and promoted with a quality record.
- API and targeted tests for the touched paths pass.

### Batch 2: Connect Knowledge Coverage to Review

Goal: implement the highest-value part of `2.md` after Batch 1 is stable.

Scope:

- `knowledge_coverage` workflow
- coverage router
- coverage projections for subject/module/LOS/formula
- orphan knowledge / orphan mistakes / decay risk signals
- minimal connection from knowledge atoms into review planning

Definition of done:

- Coverage is computed from structured atoms, not only MOC heuristics.
- Coverage produces a consumable API/projection.
- At least one downstream review surface consumes the new coverage signal.

### Batch 3: Unified UX and Deeper Quality

Goal: only after Batch 1 and 2 are green.

Scope:

- Wave 7 dashboard consolidation
- PWA/onboarding work
- broader ResourceOS automatic gating
- stronger recall-first answer redaction and projection cleanup

## 4. Hard Quality Gates

These are not optional.

### 4.1 Event Gate

- No new capability is considered complete unless it writes replayable events or an equivalent durable projection.
- New models without runtime consumers do not count as progress.

### 4.2 Projection Gate

- A wave is not complete until it is visible through at least one of:
  - API
  - UI/page
  - review snapshot
  - Obsidian/dashboard projection

### 4.3 Flag Gate

- Every new feature must either:
  - sit behind a feature flag with a safe fallback, or
  - intentionally replace the old path with explicit regression coverage.
- `403` alone is not an acceptable fallback story.

### 4.4 Review Gate

- `Review Lab` must not coexist with old bulk review completion in a way that pollutes memory state.
- Unit-level scoring is the quality bar for the new review path.

### 4.5 Card Quality Gate

- `front != answer` is mandatory for all v2 language card flows.
- It is not enough for `cards_v2.py` to exist; the generation entrypoint must actually use it when enabled.

### 4.6 Resource Gate

- Resources cannot enter a promoted learning path without:
  - license compatibility
  - quality scoring
  - reviewable decision trail

### 4.7 Baseline Gate

- Existing regressions that cause targeted test failures must be fixed before claiming the update is complete.

### 4.8 Change Hygiene Gate

- Runtime artifacts are not treated as implementation progress.
- Code changes and generated state should be separated in review and verification.

## 5. Concrete Workstreams For This Run

### Workstream A: LanguageOS Completion

Must include:

- Dictionary browsing UI with rich result presentation
- Spanish conjugation rendering
- dictionary navigation entry
- v2 card invariant test coverage
- workflow-level adoption of higher-quality card generation

### Workstream B: Review Lab Stabilization

Must include:

- session history support for restore
- API regression coverage for `active` / `paused` / `completed`
- no breakage to report generation on the normal path

### Workstream C: Resource Quality Engine

Must include:

- quality scoring module
- candidate queue
- review and promotion helper
- resource candidate API
- resource candidate UI
- feature-gated exposure where appropriate

### Workstream D: Baseline and Integration

Must include:

- fix current diagnosis/workflow export regression
- ensure shared routers and API clients stay coherent
- run targeted Python and web validation after integration

## 6. Verification Order

1. Fix baseline regressions first.
2. Validate Python imports and targeted unit/API tests.
3. Validate feature-flagged API behavior.
4. Validate primary pages:
   - `/language/dictionary`
   - `/language/dictionary/import`
   - `/review/lab`
   - `/resources/candidates`
5. Re-run focused regression suite for touched areas.

## 7. Non-Goals For This Recovery Run

These are important but not part of this immediate closure batch:

- full Wave 7 unified dashboard completion
- PWA/offline rollout
- fully replacing existing review pack generation with knowledge coverage
- deep refactor of giant workflow modules
- broad event schema migration beyond what this batch touches

## 8. Completion Standard

This recovery run is complete only when:

- the current Batch 1 implementation is integrated,
- the targeted regressions are fixed,
- the touched flows are covered by tests,
- the plan and the code agree on what is actually done.
