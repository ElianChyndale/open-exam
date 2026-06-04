# TASK-023 Complexity Budget

## Scope

The project is feature-complete for this phase. TASK-023 therefore treats complexity as a budget: improve behavior and tests inside existing modules, do not add new product surface.

## Largest Backend Learning Files

Measured with file byte size in `packages/study-science/src/study_science`:

| File | Size | Budget note |
| --- | ---: | --- |
| `review_lab.py` | 177931 | Largest risk area; contains review flow, import/promotion, scoring, coverage, mock retro, and compatibility behavior. Next refactor should split persistence/adapters from ranking and retro generation. |
| `knowledge_graph.py` | 59177 | Search, node creation, relationship expansion, and ranking are combined. Keep ranking helpers small and covered before any extraction. |
| `learning_analytics.py` | 53581 | Aggregates events, coverage, resources, and adjustments. Risk is wide fixture setup and hidden state coupling. |
| `study_planner.py` | 44726 | Planning, block synthesis, selection, and scoring are tightly coupled. TASK-023 changed selection ordering only. |
| `assessments.py` | 43962 | Assessment generation and retro behavior are coupled to mock evidence. Needs stable fixture builders before extraction. |
| `goals.py` | 43308 | Goal CRUD, derived state, and recommendations live together. |
| `tutor.py` | 42918 | Retrieval, ranking, evidence trust, and answer shaping live together. |
| `interop.py` | 39033 | Export formats, import parsing, duplicate preview, and redaction adapters are combined. |
| `focus_session.py` | 36661 | Session creation, step selection, progression, and fallbacks are together. TASK-023 added a small pure balancing helper. |
| `data_governance.py` | 30119 | Inventory, export, restore, reset, and canonical sanitizer are combined. Keep sanitizer canonical and tested. |
| `review_lab_models.py` | 25189 | Shared model density is high but stable. |
| `mission_control.py` | 24365 | Cross-surface summary logic should stay read-only and small. |

## Largest Frontend Review Pages

Measured with file byte size under `apps/web/src/app/review/**/page.tsx`:

| Page | Size | Budget note |
| --- | ---: | --- |
| `review/interop/page.tsx` | 30592 | Format/export/import UI is large; future work should extract repeated panels. |
| `review/assessments/page.tsx` | 27566 | Assessment setup/results are dense; keep deterministic waits in Playwright. |
| `review/resources/page.tsx` | 22838 | Candidate review and promotion UI are complex. |
| `review/study-planner/page.tsx` | 21849 | Planner UI should stay result-focused and avoid extra cockpit cards. |
| `review/analytics/page.tsx` | 21687 | Dense dashboard; avoid marketing-style sections. |
| `review/focus/page.tsx` | 21151 | Must remain one-task flow; no advanced tools here. |
| `review/data/page.tsx` | 20536 | Data controls must stay explicit and safe. |
| `review/tutor/page.tsx` | 19495 | Tutor answer/evidence UI should keep weak-evidence caveats visible. |
| `review/formulas/page.tsx` | 17225 | Formula practice should not expose wrong answers before reveal. |
| `review/goals/page.tsx` | 16865 | Goal workflows should stay scoped. |
| `review/search/page.tsx` | 15823 | Advanced discovery, not primary cockpit surface. |
| `review/coverage/page.tsx` | 15426 | Coverage detail belongs off the main cockpit. |

## Duplicated Route / Action Maps

- Backend navigation surfaces are centralized in `packages/study-science/src/study_science/navigation.py`.
- Frontend review pages and Playwright tests repeat the same route set for cockpit, focus, tools, and advanced pages.
- API routers and web API clients also repeat endpoint/action names for review, focus, tutor, data, interop, planner, and assessments.
- Budget rule: new route/action entries should be added in one navigation/source map first, then consumed by UI/tests. TASK-023 added no route.

## Services With Too Many Responsibilities

- `review_lab.py`: scoring, import, resource promotion, mock retro, coverage, compatibility, persistence.
- `data_governance.py`: inventory, backup, restore, redaction, reset, export warnings, sanitizer.
- `interop.py`: import preview, duplicate detection, exports, xAPI-ish statements, redaction adapter.
- `tutor.py`: retrieval, ranking, trust scoring, answer shaping.
- `study_planner.py`: goal interpretation, block generation, readiness selection, route recommendation.

Recommended next refactors should be pure-helper first:

1. Extract Review Lab coverage scoring and transfer-gap action synthesis behind tests.
2. Extract Interop duplicate-normalization helpers into a small internal utility only after more duplicate fixtures exist.
3. Extract Tutor ranking into a pure scorer with fixtures for exact formula/headword/source_ref cases.
4. Extract Data Governance sanitizer tests into a table-driven suite before touching export/restore orchestration.

## Test Files With Flakiness Or State-Coupling Risk

| Test file | Size | Risk |
| --- | ---: | --- |
| `apps/web/tests/review-lab.spec.ts` | 103720 | Large end-to-end spec, many workflows and ports; needs strict cleanup and stable network waits. |
| `apps/api/tests/test_api_review_lab.py` | 57912 | Large fixture surface around persisted review memory and compatibility behavior. |
| `apps/api/tests/test_api_tutor.py` | 21292 | Ranking fixtures can become order-sensitive if evidence setup is broad. |
| `apps/api/tests/test_api_knowledge_graph.py` | 17976 | Search rank assertions need isolated graph state. |
| `apps/api/tests/test_api_interop.py` | 17672 | Import/export fixtures need duplicate and sanitizer determinism. |
| `apps/api/tests/test_api_study_planner.py` | 17659 | Planner ordering should use explicit block fixtures for edge cases. |
| `apps/api/tests/test_api_learning_analytics.py` | 17258 | Event aggregation can couple to persisted local state if roots are shared. |
| `apps/api/tests/test_api_data_governance.py` | 13737 | Export/restore path tests must keep temp roots isolated. |

## Anti-Sprawl Guard Enforced

TASK-023 strengthens the backend navigation guard:

- `apps/api/tests/test_api_navigation.py` asserts advanced routes (`/review/data`, `/review/interop`, `/review/knowledge-map`, `/review/search`, `/review/tools`) are not marked `visible_on_main`.
- This keeps `/review` as a premium cockpit instead of a feature directory.
- No new user-facing route was added in TASK-023.

Related existing Playwright coverage still verifies:

- `/review` remains the main cockpit.
- `/review/focus` remains one-task oriented.
- `/review/tools` is accessible as the advanced/tools surface.
- Mobile 390px layouts do not horizontally overflow.

## Complexity Budget Decision For TASK-023

Allowed:

- Small pure helper in an existing module.
- Focused ordering/ranking changes with direct tests.
- Report-only documentation under `.system/reports`.
- Security sanitizer hardening in the canonical sanitizer.

Not allowed:

- New pages, new modules, or cockpit expansion.
- Broad rewrites of Review Lab or Tutor.
- New lint/build dependency.
- Test weakening or skipped validation.

TASK-023 stayed within this budget:

- Added two report files.
- Touched existing algorithm modules only.
- Added deterministic tests using isolated `tmp_path` fixtures or synthetic objects.
- Enforced anti-sprawl through the existing navigation test surface.
