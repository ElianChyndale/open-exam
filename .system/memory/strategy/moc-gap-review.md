---
generated_at: 2026-05-26T02:41:13.954856+00:00
last_updated: 2026-05-26
recommendation_count: 2
resolved_gaps:
  - Quant M09 Tests of Independence — standalone file created, MOC updated
  - Corporate Issuers M02 Investors and Other Stakeholders — file created, modules renumbered
  - Economics restructured 9→8 official modules — retired ARCH01/ARCH02, split ARCH03 Geopolitics/Trade
  - FSA M04 Cash Flow split into M04 (CF I) and M05 (CF II) — modules renumbered M06-M12
  - Ethics M09 Ethics Application — file created, MOC updated
  - Full CFA_tier1 official 2026 module sync — all 10 subjects regenerated from official registry
remaining_gaps: []
---

# MOC Gap Review (Updated)

## Current Generated Recommendations

### Quantitative Methods | QM.Rates and Returns | concept_confusion
moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
recurrence: 4
suggested_gap_type: knowledge_tree
gap_target: knowledge_tree_concept
reason: Repeated concept_confusion errors suggest the MOC may need a stronger knowledge_tree_concept treatment for this LOS.
event_ids: evt-10907b5c267a, evt-0e878b874339, evt-17a43f996f70, evt-9077db629ec2
evidence_refs: screenshot-session-2026-05-21, typed-q-2026-05-21-quant, typed-q-2026-05-21-quant-2, typed-q-2026-05-21-quant-3

### Quantitative Methods | unknown_from_screenshot | concept_confusion
moc_target: CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md
recurrence: 3
suggested_gap_type: knowledge_tree
gap_target: knowledge_tree_concept
reason: Repeated concept_confusion errors suggest the MOC may need a stronger knowledge_tree_concept treatment for this LOS.
event_ids: evt-3e013d8e1a5c, evt-3e64f47fca3a, evt-8a6976859ffb
evidence_refs: chat-screenshot-2026-05-21-q38, chat-screenshot-2026-05-25-bootstrap-standard-error, chat-screenshot-2026-05-25-sampling-error-definition

## Resolved Gaps

### ✅ Full CFA_tier1 — Official 2026 Module Sync
All subject root folders now match the CFA Institute 2026 Level I module count, order, module names, topic weights, and LOS. The official module/LOS source is the CFA Institute 2026 Level I Topic Outlines PDF; the Learning Ecosystem scrape is retained only for page-item navigation.

- Quantitative Methods: 11 modules
- Economics: 8 modules
- Corporate Issuers: 7 modules
- Financial Statement Analysis: 12 modules
- Equity: 8 modules
- Fixed Income: 19 modules
- Derivatives: 10 modules
- Alternative Investments: 7 modules
- Portfolio Management: 6 modules
- Ethical and Professional Standards: 5 modules

Registry: `.system/memory/strategy/cfa-2026-official-module-registry.json`
Report: `.system/memory/strategy/cfa-2026-official-sync-report.md`
Source PDF: `.system/memory/strategy/official-sources/2026-l1-topics-combined.pdf`

### ✅ Quantitative Methods — M09 Tests of Independence
M09-Tests-of-Independence.md created with full LOS coverage. M09-Correlation-and-Regression.md trimmed to pure regression content. MOC module table updated.

### ✅ Corporate Issuers — M02 Investors and Other Stakeholders
M02-Investors-and-Other-Stakeholders.md created. Existing modules renumbered M02→M03 through M08→M09. MOC updated.

### ✅ Economics — 9→8 Module Restructure
Retired ARCH01 (Demand/Supply) and ARCH02 (Aggregate Output) to _archive/. Renumbered M02→M01, M04→M02, M05→M03, M06→M04, M08→M07, M09→M08. Split ARCH03 into M05 (Geopolitics) and M06 (International Trade). MOC completely rewritten with 8-module alignment.

### ✅ FSA — M04 Cash Flow Split
M04 (CF I) and M05 (CF II) created from original M04. Modules M05-M11 renumbered to M06-M12. MOC updated.

### ✅ Ethics — 9→5 Official Module Projection
Legacy Standard I-VII split notes were preserved under `_legacy/2026-05-26-official-sync/` and migrated into official M03 Guidance for Standards I-VII where relevant. Ethics Application is now official M05.

## Mistake-Driven Enrichments Applied

| Module | Error Cards Addressed | Enrichment Type |
|--------|----------------------|-----------------|
| Quant M01 Rates & Returns | 4 cards (CC return, gross/net, MWRR/TWRR, leveraged) | Section 4 traps |
| Quant M03 Statistical Measures | 2 cards (skewness axis, semideviation) | Section 4 traps |
| Quant M05 Portfolio Mathematics | 1 card (Roy safety-first) | Section 4 trap |
| Quant M07 Sampling & Estimation | 3 cards (sampling error, probability sampling, bootstrap) | Section 4 traps + Section 1.3 expansion |
| Quant M10 Big Data & ML | 1 card (overfitting vs blackbox) | Section 4 expansion |

## Knowledge Tree Enrichment

All 10 MOC knowledge trees enriched with concise Chinese node summaries (parenthetical 2-5 char précis) — Quant, Portfolio (done directly); Econ, FSA, CorpIss, Equity, FI, Derivatives, AltInv, Ethics (via background agents).
