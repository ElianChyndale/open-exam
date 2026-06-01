# OpenExam LanguageOS Implementation Basis

> Frozen: 2026-06-02
> Source: `docs/superpowers/specs/languangePlan.md`
> Delivery rule: LanguageOS extends OpenExam. It is not a separate application.

## 1. Architecture Boundaries

LanguageOS reuses the existing OpenExam four-layer architecture:

| Layer | LanguageOS responsibility | Canonical paths |
|---|---|---|
| Capture | Immutable language events and local attachments | `.system/events/language/`, `.system/private/language-assets/` |
| Memory | Rebuildable snapshots, caches, graph and exports | `.system/memory/language/` |
| Decision | Deterministic scheduling, grammar, graph and transfer logic | `packages/language-science/`, `.system/app/language_workflows.py` |
| Projection | API responses, cockpit pages, Markdown and Obsidian exports | `apps/api/routers/language.py`, `apps/web/src/app/language/`, `CFA_tier1/dashboard/language/` |

Rules:

1. JSONL events are canonical. Snapshots, caches and projections are disposable and rebuildable.
2. Exam and language event families remain separate. Cross-domain bridges write explicit bridge events.
3. Local-first adapters ship first. Cloud providers are disabled until a matching consent event exists.
4. DeepSeek is the first optional cloud adapter, behind a provider-neutral interface.
5. No new agent role is added. Existing orchestrator and validator boundaries remain authoritative.

## 2. Repository Protocols

Add:

```text
packages/language-science/src/language_science/
  __init__.py
  models.py
  scheduler.py
  grammar.py
  intuition_graph.py
  importers.py

.system/app/
  language_storage.py
  language_workflows.py

apps/api/routers/
  language.py

apps/web/src/
  app/language/*
  components/language/*
  components/motion/*
  lib/motion/*
```

`LanguageRepository` owns the language JSONL stream and rebuildable snapshot file. It must not mutate historical events.

## 3. Event Schema

All language writes use `EventEnvelopeV2`:

```json
{
  "event_id": "evt2-*",
  "schema_version": 2,
  "event_type": "language.*",
  "learner_id": "local-default",
  "occurred_at": "ISO-8601",
  "source_layer": "language",
  "payload": {},
  "evidence_refs": [],
  "provenance": {},
  "consent_scope": ["local_storage"],
  "idempotency_key": ""
}
```

Frozen event types:

```text
language.profile.selected
language.source.imported
language.source.duplicate_detected
language.segment.created
language.item.collected
language.item.merged
language.card.created
language.review.completed
language.grammar.analyzed
language.grammar.edited
language.intuition.rebuilt
language.session.completed
language.export.created
language.cloud_transcription.requested
exam.language_gap.detected
```

## 4. Core Models

Implement immutable dataclasses:

```text
LanguageProfile
CorpusSource
CorpusSegment
LanguageItem
LanguageCard
GrammarAnalysis
IntuitionEdge
LanguageSession
ScheduleDecision
```

Required profiles:

```text
en-general
en-finance
es-general
es-business
```

Required item types:

```text
word
phrase
sentence
grammar_pattern
idiom
collocation
```

Required card types:

```text
recognition
production
cloze
dictation
shadowing
grammar_parse
translation_reverse
free_recall
```

## 5. API Contracts

All routes live under `/api/language`.

```text
GET  /profiles
POST /profiles/select
GET  /sources
POST /sources
GET  /sources/{source_id}
GET  /segments?source_id=
POST /segments
GET  /items
POST /items
POST /items/{item_id}/merge
GET  /cards/due
POST /cards/generate
POST /cards/{card_id}/review
POST /grammar/analyze
GET  /grammar/{segment_id}
PATCH /grammar/{segment_id}
GET  /intuition/graph
GET  /intuition/search?q=
POST /intuition/rebuild
POST /sessions
GET  /stats
POST /imports
POST /transcriptions
GET  /exports/{format}
```

Errors:

| Case | Status |
|---|---|
| Unknown resource | `404` |
| Duplicate source | `200`, existing source plus `duplicate: true` |
| Invalid import format | `422` |
| Missing transcription consent | `403` |
| Revision or merge conflict | `409` |
| Unsupported optional extractor | `422` with local fallback guidance |

## 6. Import Formats

Local imports:

| Format | Behavior |
|---|---|
| `manual`, `text` | Split into sentence segments and preserve character locators |
| `srt`, `vtt` | Preserve timestamp start/end locators |
| `epub` | Preserve chapter-style locator; baseline accepts extracted text |
| `pdf` | Preserve page locator; baseline accepts extracted text |
| `audio` | Persist attachment manifest before any transcription |
| `youtube`, `bilibili`, `podcast`, `web` | Store source metadata through provider adapters |

Every source stores a SHA-256 content hash. Duplicate source import returns the historical source. Audio is always stored locally before transcription. Cloud transcription remains disabled unless `language_cloud_transcription` is enabled and consent exists.

## 7. Scheduling

Expose `MemorySchedulerProtocol` with:

```python
preview(card) -> dict[str, ScheduleDecision]
schedule(card, rating) -> ScheduleDecision
```

Language ratings:

```text
again
hard
good
easy
```

The first implementation is deterministic and FSRS-compatible in interface. It stores difficulty, stability, retrievability, state, repetitions and due time in each card snapshot. Sparse-data behavior must not depend on a cloud optimizer.

## 8. Grammar Lens

Baseline analyzers are deterministic and editable:

1. English: clause split, phrase detection, collocations and CEFR heuristic.
2. Spanish: the English baseline plus gender, number, tense, mood, person and irregularity features.
3. Analysis is cached by segment text hash.
4. Edits append `language.grammar.edited`; history is never rewritten.
5. A grammar pattern can be collected as a `LanguageItem`.

## 9. Intuition Graph

Deterministic graph edges ship first:

```text
synonym
antonym
collocation
idiom_variant
register_variant
false_friend
translation_confusion
grammar_pattern
co_occurrence
exam_domain_link
```

Embedding search is optional behind `language_embedding_search`. Disabled mode must still support exact and token-overlap search.

## 10. Skill Transfer

Sessions:

```text
listening
dictation
shadowing
translation
writing
reading_speed
```

Track recognition and output gaps separately. Cross-domain bridges include CFA/FRM stems, finance phrases, Ethics wording distinctions and concept-expression review.

## 11. Frontend Routes

```text
/language
/language/import
/language/corpus
/language/review
/language/listening
/language/grammar
/language/intuition
/language/stats
/language/settings
```

The main cockpit may show language metrics, but it must not merge exam and language event streams.

## 12. Motion And Accessibility

Install:

```text
gsap
@gsap/react
```

Official `@gsap/react` guidance is frozen as follows:

1. Register `useGSAP` once with `gsap.registerPlugin(useGSAP)`.
2. Place GSAP code in client components.
3. Use `scope` for selectors and automatic context cleanup.
4. Use `contextSafe()` for callbacks that create animations after hook execution.
5. Respect `prefers-reduced-motion`; skip nonessential movement and preserve content.

Required motion:

```text
card flip
number transition
grammar tree timeline
intuition graph stagger
restrained completion feedback
```

Accessibility rules:

1. All actions remain keyboard accessible.
2. Every form control has a label or `aria-label`.
3. Reduced-motion mode disables nonessential transforms.
4. Color is never the only state indicator.
5. Loading and error messages use status semantics.

## 13. Feature Flags

```yaml
language_os_enabled: false
language_fsrs_enabled: false
language_grammar_lens: false
language_intuition_graph: false
language_content_import: false
language_cloud_transcription: false
language_embedding_search: false
gsap_motion_enabled: false
reduced_motion_safe: true
```

## 14. Exports

Implement:

```text
anki
csv
markdown
obsidian
```

Exports are projections. They append `language.export.created` and never become source of truth.

## 15. Test And Rollout Gates

Required backend tests:

```text
event replay and projection rebuild
source hash deduplication and segment locators
English and Spanish profile switching
item merge and card generation
FSRS-compatible rating updates
grammar cache and editable analysis
intuition graph rebuild and search
importers and attachment manifests
consent-gated transcription
session output gaps and exports
```

Required frontend gates:

```text
npm run typecheck
npm run build
/language/* Playwright flows
prefers-reduced-motion behavior
```

Milestone gate:

```powershell
pytest -q
cd apps/web
npm run typecheck
npm run build
```

## 16. Rollout Order

1. `L0` kernel, repository, profiles and replay.
2. `L1` source, segment and item context capture.
3. `L2` cards, deterministic FSRS-compatible scheduler and review.
4. `L3` local importers, metadata adapters and consent-gated transcription.
5. `L4` English/Spanish Grammar Lens.
6. `L5` deterministic Intuition Graph; optional embeddings remain off.
7. `L6` skill-transfer sessions and exam-language bridges.
8. `L7` GSAP motion system with reduced-motion fallback.
9. `L8` cockpit pages and exports.

## 17. Documentation Sources

- Source blueprint: `docs/superpowers/specs/languangePlan.md`
- GSAP React official repository: https://github.com/greensock/react
- GSAP React documentation: https://gsap.com/resources/React/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Reduced motion media query: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- FSRS reference implementation: https://github.com/open-spaced-repetition/fsrs4anki
