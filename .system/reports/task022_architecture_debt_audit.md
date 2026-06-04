# TASK-022 Architecture Debt Audit

## Scope

Focused audit of Focus Session, Study Planner, Review Lab, Tutor, Knowledge Graph, Data Governance, Interop, Navigation, frontend review surfaces, and Playwright validation hygiene after the rapid OpenExam buildout.

## Top 10 Debt Items

| # | Severity | Affected files/services | Evidence | Root cause | User/product risk | Recommended fix | TASK-022 status |
|---|---|---|---|---|---|---|---|
| 1 | High | `data_governance.py`, `interop.py`, `tutor.py`, `knowledge_graph.py`, `assessments.py`, `learning_analytics.py`, `focus_session.py` | Separate forbidden-key sets existed as `RAW_DIAGNOSTIC_KEYS`, `FORBIDDEN_FIELDS`, `RAW_KEYS`, `WRONG_KEYS`, plus local recursive strip functions. Lists did not cover `wrong_answer`, `wrong_output`, `selected_answer`, `raw_response`, `diagnostics`, or `common_wrong_path` consistently. | Correct-only safeguards were added feature by feature instead of from one registry. | Wrong-answer or raw diagnostic fields could leak differently across backup, graph, tutor, analytics, and interop payloads. | Use one canonical registry and sanitizer from `study_science.data_governance`; make services reuse it. | Fixed. |
| 2 | High | `knowledge_graph.py` search ranking | `_rank()` treated exact `plain_formula`/`headword` metadata matches the same as weak free-form metadata hits. | Ranking flattened all metadata through JSON string search. | Search could surface broad metadata notes above the exact formula or lexical item the user asked for. | Add structured-field ranking for formula, lexical, asset, and assessment question fields. | Fixed. |
| 3 | High | `interop.py` import preview duplicate detection | `_content_hash()` normalized case/spacing but not punctuation, and existing duplicate hashes used only `trigger + correct_rule`, missing `title + correct_rule`. | Import/export card identity was tied to one Anki front convention. | Same card imported with title wording or hyphen differences could create duplicate draft assets. | Normalize NFKC/case/punctuation/spacing and index both title and trigger against the correct rule. | Fixed. |
| 4 | Medium | `tutor.py` retrieval ranking | `_context_score()` used validation/source dimensions but did not explicitly encode confirmed source-backed trust versus generated no-source evidence. | Scoring mixed quality and relevance without a named trust term. | Generated local summaries with high text match could compete too closely with confirmed cited evidence. | Add explicit `evidence_trust` and cap no-source quality contribution. | Fixed. |
| 5 | Medium | `focus_session.py` step orchestration | `_steps_from_plan()` maps several plan block types into fewer focus step types; repeated confirmation-style steps can cluster when the planner emits many blockers. | Focus consumes planner order directly with only minute fitting. | Focus can feel repetitive and less calm when several blocked confirmation tasks appear consecutively. | Add a small diversity pass that avoids excessive repeated step types while preserving blocked work. | Deferred; lower risk after planner category caps, but should be next. |
| 6 | Medium | `study_planner.py` scheduling | `_compose_blocks()` category mix is table-driven but blocked candidates can still consume budget when they are the highest priority in a category. | Planner does not separate executable work from blocked hygiene tasks before budget allocation. | A time-boxed plan may over-allocate to tasks the learner cannot complete immediately. | Prefer pending/actionable candidates first, then include one blocked cleanup item as a visible blocker. | Deferred; needs focused planner tests. |
| 7 | Medium | `review_lab.py` | File size is about 178KB and combines resource ingestion, asset extraction, formula lab, mock retro, coverage, route registry, and scoring. | Rapid feature accumulation in one engine class. | Future changes have high blast radius and are harder to review. | Extract shared scoring/sanitizer helpers first, then split domain services only with tests. | Deferred; broad split would exceed this task's no-rewrite constraint. |
| 8 | Medium | `apps/web/src/app/review/interop/page.tsx`, `assessments/page.tsx`, `resources/page.tsx`, `study-planner/page.tsx`, `focus/page.tsx`, `data/page.tsx` | Several review pages are 20-30KB and define local repeated fact/metric/redaction helpers. | UI grew page-by-page without shared review primitives. | Repeated copy and helper drift can reintroduce jargon or unsafe field previews. | Extract small shared primitives only when touching each page; keep primary cockpit/focus minimal. | Partially fixed via TASK-022 Playwright guard; extraction deferred. |
| 9 | Low | `apps/web/tests/review-lab.spec.ts` | Full review-lab spec covers many flows in one file, and many tests seed shared local stores. | End-to-end coverage grew with product surface. | More risk of order coupling and stale local state surprises. | Keep network waits for mutations, add targeted helpers and surface guards, continue port cleanup. | Partially fixed with TASK-022 surface/mobile guard. |
| 10 | Low | `scripts/dev/cleanup-validation-processes.ps1` validation workflow | Cleanup is safe and port-scoped, but evidence is manual per report and not embedded in Playwright teardown. | Validation process management lives outside test runner lifecycle. | A future validation run could leave listeners if the operator forgets cleanup. | Keep script port-scoped; optionally wrap manual browser validation in a helper that always records port state. | Deferred; script remains safe and will be used in this report. |

## Fixed In TASK-022

- Canonical correct-only registry and sanitizer in `study_science.data_governance`.
- Reused sanitizer in Focus, Tutor, Data Governance, Interop, Knowledge Graph, Assessment, and Learning Analytics public payload paths.
- Knowledge Graph structured-field ranking for exact formulas/headwords and other high-signal fields.
- Tutor evidence trust scoring and no-source quality cap.
- Interop duplicate normalization across case, spacing, punctuation, title, trigger, and correct rule variants.
- Playwright surface guard for minimal primary cockpit/Focus and accessible advanced tools hub.

## Deferred With Rationale

- Splitting `review_lab.py` and large frontend pages is valid debt but too broad for a no-rewrite hardening pass.
- Focus step diversity and planner blocked-work budgeting deserve a separate small TDD pass because they can subtly affect plan ordering.
- Full validation cleanup automation can be improved later; TASK-021's port-scoped cleanup script is safe and sufficient for this run.
