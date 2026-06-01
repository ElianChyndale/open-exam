# OpenExam Next-Generation Layered Upgrade

## Summary
Evolve the existing solo-learner CFA system without rewriting its healthy kernel. Preserve current user edits, archive the three reports verbatim, and deliver new capabilities in gated waves. Current baseline: `pytest -q` passes 97 tests; web typecheck and production build pass.

## Architecture Decisions
- Keep `.system/events/*.jsonl` as canonical append-only evidence. Keep SQLite as a rebuildable query projection, not primary storage.
- Preserve the six existing agent roles. Add services and tools, not new agents.
- Keep deterministic local workflows as default. Cloud AI requires explicit opt-in and must return grounded, attributable outputs.
- Add `EventEnvelopeV2`: `event_id`, `schema_version`, `event_type`, `learner_id`, `occurred_at`, `source_layer`, `payload`, `evidence_refs`, `provenance`, `consent_scope`.
- Add PROV-style entities, activities, agents, claims, edges, and replacement history. Use stable taxonomy concept IDs with aliases.
- Maintain backward compatibility by adapting legacy events during replay. Do not rewrite historical JSONL files in place.
- Use feature flags for every new subsystem and preserve Obsidian as a replaceable projection layer.

## Implementation Waves
### Wave 0: Archive And Kernel Hardening
- Copy the reports verbatim into `docs/research/2026-06-01-openexam-next-generation/` as three normalized Markdown files. Add an index mapping original filenames, SHA-256 hashes, and roadmap themes.
- Preserve the dirty worktree. Avoid overwriting generated dashboards or manual Markdown edits during implementation.
- Fix sync preview ID normalization, introduce replay checks, and gradually split the oversized workflow module by subsystem.
- Add topic alias taxonomy, pattern severity ranking, validation expiry and review status, MOC-gap deduplication, mock-result scheduler feedback, and energy-aware daily review shaping.
- Replace fragile frontmatter scalar edits with a formatting-preserving structured metadata helper.

### Wave 1: Learning Record Mesh, Provenance, And Privacy
- Add bounded `learning-records` and `provenance` packages. Normalize current attempt, review, energy, mock, bias, agent-audit, and strategy streams through `EventEnvelopeV2`.
- Materialize rebuildable graph projections for evidence lineage, taxonomy links, prerequisite links, claims, and decision provenance.
- Add consent events, explicit local export, explicit purge with deletion manifest, provider-use records, retention settings, and audit views.
- Add `/api/provenance/{id}`, `/api/privacy/export`, `/api/privacy/purge`, and read-only xAPI export. Keep Caliper as a later adapter.

### Wave 2: Learner Twin, Skill Graph, And Psychometrics
- Add `learner-twin` and `psychometrics` packages with snapshots derived from events: mastery estimate, half-life, recurrence, confidence bias, transfer score, time cost, prerequisite risk, and recent learner state.
- Model each task as a curriculum contract: objective, evidence requirement, due reason, pedagogy policy, and next proof action.
- Start with interpretable HLR/BKT-style scheduling and Rasch-like 1PL estimates. Run 2PL calibration only in shadow mode after sufficient responses.
- Label the existing pass probability as heuristic until data thresholds are met. Add confidence bands instead of false precision.
- Feed mock outcomes, review outcomes, and repeated misconceptions back into scheduling and route recommendations.

### Wave 3: Pedagogy Policy, Human Factors, And Accessibility
- Add `pedagogy-policy` and `human-factors` packages. Convert review packs from Markdown-only output into structured tasks plus Markdown projection.
- Support retrieval probes, self-explanation, contrast pairs, fix-rule recall, worked-example fading, productive failure, teach-back, and transfer mini-mocks.
- Add opt-in sleep, stress, energy, and workload check-ins for non-medical adaptation; allow complete disablement.
- Add accessibility profiles, keyboard-first review flows, reduced motion, semantic landmarks, contrast checks, readable print modes, and mobile review validation against WCAG 2.2 AA.

### Wave 4: Grounded AI, Multimodal Capture, Sync V2, And MCP
- Add a grounded explanation service: claim-level evidence refs, retrieved spans, tool records, model/provider version, confidence, and revoke-or-replace history.
- If evidence is insufficient, return a conservative local fallback instead of an unsupported explanation.
- Extend screenshot capture to structured extraction with field confidence and quarantine review. Add PDF and audio extraction only behind opt-in flags.
- Replace the browser `localStorage` queue with IndexedDB, idempotency keys, cursors, attachment manifests, conflict preview, and retry-safe replay.
- Add a narrow MCP adapter: read-only due reviews, evidence lookup, and provenance inspection first; mutations require explicit confirmation.

### Wave 5: Simulation And Research Runtime
- Add `sim-lab` and `research-runtime` packages behind frontier flags.
- Record policy decisions and outcomes, compare scheduler variants offline, and allow contextual-bandit shadow evaluation without automatic learner-facing promotion.
- Treat inferred misconceptions and prerequisite edges as candidates until evidence thresholds and human review approve them.

### Wave 6: Ecosystem And Trust Adapters
- Add institution-facing aggregate adapters later: Caliper export, roster mapping, privacy-preserving cohort views, opt-in peer pods, discourse coaching, epistemic cards, localization, and optional attention or narrative overlays.
- Add signed local evidence snapshots, then opt-in Open Badges 3.0, CLR, and VC exports with issuer status and revocation.
- Do not put raw learning data on a blockchain. Public-chain or external Merkle anchoring is explicitly deferred.

## Verification And Rollout
- Run legacy replay and SQLite rebuild tests; prove no historical event loss and stable duplicate detection.
- Test provenance coverage, unsupported-claim failure, consent enforcement, export/purge behavior, and feature-flag rollback.
- Validate scheduler changes with deterministic fixtures, mock feedback, sparse-data psychometrics, and disabled human-factor inputs.
- Test IndexedDB offline replay, duplicate retries, attachment conflicts, and MCP authorization boundaries.
- Add Playwright accessibility checks for keyboard use, focus order, reduced motion, mobile layouts, and WCAG 2.2 AA regressions.
- Verify VC/Open Badge export, signature validation, revocation, and absence of raw learning records in trust artifacts.
- Ship each wave only after replay safety, local-first behavior, and projection regeneration pass.

## Assumptions And Standards
- Optimize for the solo learner first; institution features remain adapters.
- Produce one tracked master roadmap and a focused execution spec before each wave.
- Standards anchors: [PROV-O](https://www.w3.org/TR/prov-o/), [SKOS](https://www.w3.org/TR/skos-reference/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [MCP](https://modelcontextprotocol.io/specification/2025-11-25), [xAPI](https://github.com/adlnet/xAPI-Spec), [Open Badges](https://www.1edtech.org/standards/open-badges), [CLR](https://www.1edtech.org/standards/clr), and [VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/).
