# TASK-023 Algorithm Calibration Report

## Scope

This audit covers the existing learning decisions that determine what the learner should do next, what evidence is trusted, and what data can leave the local system. No new module or user-facing page was added.

## Existing Algorithms Inventoried

| Algorithm | Input signals | Output decision | Current edge cases | Risk if wrong | Calibration target | Coverage status |
| --- | --- | --- | --- | --- | --- | --- |
| Review priority scoring | Asset mastery state, next review date, mistake count, source quality, transfer-gap priority, coverage guidance, validation status. | Ranked review items and due reasons. | All-new queues, many overdue items, weak formula assets, recently reviewed items, draft/unconfirmed assets. | Repeats the same topic, promotes weak/draft content, or misses high-weight overdue knowledge. | Overdue + weak + important confirmed content should win; draft/setup content should stay outside trusted recall. | Existing Review Lab tests cover confirmed/draft promotion, old DailyReview compatibility, wrong-answer non-leakage, coverage and transfer-gap flows. TASK-023 did not alter this scoring directly. |
| Study Planner block selection | Goals, coverage gaps, resource confirmations, asset confirmations, transfer gaps, energy mode, time budget, block type and status. | Ordered plan blocks and recommended next route. | Blocked high-priority work can dominate actionable setup; cleanup/confirmation can crowd out study; low-energy short plans need viable work. | User gets an impossible plan, wastes a short session, or skips required confirmation. | Prefer actionable pending setup over blocked work while preserving cleanup priority and time/energy constraints. | Improved in TASK-023 with actionable-before-blocked sorting and a focused regression test. |
| Focus Session step selection | Today plan blocks, confirmed assets, formulas, lexical items, assessment/focus candidates, source_refs, step status. | One-task-at-a-time step sequence and active step. | Consecutive same-type overload, no today plan, no confirmed content, skipped step idempotence, draft setup-only steps. | Learner gets overloaded or repetitive work and abandons the focus flow. | Stable sequence with no three same-type steps in a row when alternatives exist; source_refs preserved. | Improved in TASK-023 with `_balance_step_sequence` and a deterministic unit test. |
| Tutor context ranking | Query tokens, exact title/headword/formula matches, source_refs, validation/quality status, transfer gaps, evidence trust. | Ranked evidence snippets and answer confidence/warnings. | Exact formula vs metadata noise, draft vs confirmed sources, no evidence, conflicting low-quality resources. | Tutor answers sound authoritative with weak evidence or cite drafts as trusted. | Confirmed/source-backed exact matches win; weak/no evidence caps answer quality and warns. | TASK-022 added evidence trust and no-source cap; TASK-023 preserves this boundary in targeted/full tests. |
| Knowledge Graph search ranking | Query text, structured fields, title/headword/formula fields, source_refs, validation status, node type. | Ranked learner-facing graph nodes and related nodes. | System/action nodes can match query text; generic JSON hits can outrank formula/headword fields; draft nodes can look equivalent. | Search sends learner to implementation/system metadata instead of learnable content. | Structured learner content should outrank advanced/system nodes for the same query. | Improved in TASK-023 with node-type weighting and a regression test. |
| Coverage/readiness scoring | Syllabus topics, confirmed linked assets, draft-only assets, expected asset types, formula/decision-rule expectations, review recency. | Coverage status, coverage score, recommended actions. | Draft-only topics, stale coverage, high-weight missing topics, weak confirmed assets. | Learner believes a topic is ready when only draft or stale content exists. | Confirmed/source-backed coverage should drive readiness; draft-only should trigger confirmation. | Existing coverage tests remain part of Review Lab and analytics validation. |
| Assessment selection / transfer gap generation | Mock evidence, question type, error type, severity, confidence, source_refs, historical performance. | Assessment items, retro summaries, transfer-gap actions. | Formula recall vs procedure gap, time pressure, confidence mismatch, repeated gap families. | Practice does not target the real weakness, or gaps fail to become actions. | Transfer gaps should become source-backed plan/review actions without exposing wrong answers. | Existing assessment and Review Lab tests cover generation, retro, and wrong-answer boundaries. |
| Interop duplicate detection | Incoming openexam_id, normalized front/back/title/trigger text, source_refs, existing asset hashes. | Import preview duplicate warnings and draft assets. | Unicode/case/punctuation variants, title+trigger duplicates, source-derived rows. | Duplicate cards inflate workload and distort retrieval/ranking. | Canonical normalization catches semantic duplicates while keeping new draft imports blocked. | TASK-022 hardened duplicate normalization; TASK-023 keeps it in the required interop suite. |
| Data Governance redaction/safe export | Export mode, category records, forbidden keys, nested strings, local paths, restore paths, include_raw_diagnostics. | Sanitized export payload, redaction report, restore dry-run validation. | Forbidden values hidden in nested strings; absolute local paths in source_refs/text; path traversal on restore. | Wrong answers, internals, or local filesystem details leave the system. | Correct-only sanitizer remains canonical and strips forbidden keys, nested values, and absolute paths. | Improved in TASK-023 with local-path scrubbing and restore traversal checks. |

## Algorithms Improved In TASK-023

1. Study Planner block selection
   - Change: planner ordering now prefers actionable non-blocked matching blocks before blocked blocks, while the cleanup category still favors `file_ingestion_cleanup` and then non-blocked work.
   - Evidence: `packages/study-science/src/study_science/study_planner.py:757`, `packages/study-science/src/study_science/study_planner.py:765`, `apps/api/tests/test_api_study_planner.py:97`.

2. Focus Session step selection
   - Change: `FocusSessionService.start()` now balances the selected step sequence before fitting minutes. The helper preserves step IDs and source_refs while avoiding three same-type steps in a row when an alternative exists.
   - Evidence: `packages/study-science/src/study_science/focus_session.py:176`, `packages/study-science/src/study_science/focus_session.py:750`, `apps/api/tests/test_api_focus.py:129`.

3. Knowledge Graph search ranking
   - Change: ranking now applies a node-type weight so learner content keeps precedence over system/action/analytics nodes for the same query.
   - Evidence: `packages/study-science/src/study_science/knowledge_graph.py:1047`, `packages/study-science/src/study_science/knowledge_graph.py:1184`, `apps/api/tests/test_api_knowledge_graph.py:95`.

## Why These Three Matter Most

- Planner selection is the highest-leverage "what now" decision. A blocked high-priority item should not hide the next actionable confirmation or setup block.
- Focus step ordering is the moment-to-moment learning loop. Preventing repeated same-type overload preserves the premium one-task flow without adding UI noise.
- Graph ranking feeds exploration and retrieval. If system nodes beat formulas/headwords, learners land in implementation detail instead of study material.

## Security and Correctness Calibration

TASK-023 also hardens safe export boundaries:

- The canonical sanitizer now redacts Windows and POSIX absolute local paths from nested string payloads and reports `local_path_redactions_count`.
- Restore dry-run traversal coverage verifies unsafe `../` paths remain rejected.
- The sanitizer tests still assert forbidden safe-payload keys are removed and forbidden values are scrubbed from nested strings.

Evidence:

- `packages/study-science/src/study_science/data_governance.py:33`
- `packages/study-science/src/study_science/data_governance.py:568`
- `packages/study-science/src/study_science/data_governance.py:617`
- `apps/api/tests/test_api_data_governance.py:144`
- `apps/api/tests/test_api_data_governance.py:184`

## Determinism Notes

- Planner regression builds an isolated temporary memory root and calls `_compose_blocks` directly with explicit candidate blocks.
- Focus regression uses synthetic `FocusStep` fixtures rather than persisted local state.
- Graph regression builds an isolated graph service under `tmp_path`.
- Data Governance security regressions use isolated temporary export/restore fixtures.
