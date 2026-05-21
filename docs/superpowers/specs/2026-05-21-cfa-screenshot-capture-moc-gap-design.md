# CFA Screenshot Capture and MOC Gap Review Design

> Note: This design extends the live `CFA_tier1/ + .system/` learning loop. It does not replace the current CLI-driven workflow; it adds screenshot-aware capture metadata and a controlled path for feeding repeated mistakes back into subject MOCs.

## Goal

Extend the local CFA Level I learning system so Codex can receive a wrong-question screenshot, normalize it into a structured mistake payload, store richer provenance metadata, and generate controlled MOC gap review recommendations when repeated errors suggest the knowledge framework is missing a formula, trap, or tree node.

## Why This Change

The current system already supports:

- subject-first reading through one master `00-*-MOC.md` per topic
- structured event capture for `question`, `bias`, and `agent`
- weekly pattern mining
- pre-mock and post-mock strategy artifacts
- Obsidian projection pages in `CFA_tier1/dashboard/`

What it does not yet support cleanly is the user's actual study behavior:

1. solve official questions or mock questions
2. send a screenshot to Codex
3. have Codex automatically store the mistake without manual payload assembly
4. use repeated mistake evidence to decide whether the corresponding subject MOC should be thickened

Without this extension, the loop is only half closed: storage works, but screenshot ingestion and MOC feedback remain manual and inconsistent.

## User-Facing Outcome

After this change, the intended loop becomes:

1. read the relevant subject MOC in `CFA_tier1/`
2. solve official mock / practice questions
3. send a screenshot to Codex
4. Codex extracts the mistake into a structured payload and calls `record-mistake`
5. the system stores richer source metadata and evidence links
6. repeated `topic + los + error_type` mistakes can generate a `moc-gap-review` recommendation
7. Codex can later use that recommendation to safely update the corresponding subject MOC

## Design Decision

This feature will use a **Codex-native screenshot capture workflow**, not a local OCR pipeline.

That means:

- Codex reads the screenshot in chat and performs the interpretation
- the local system remains responsible for storage, aggregation, and review artifacts
- no OCR engine or image model dependency is added to the CLI

This keeps the first version aligned with the user's real workflow and avoids pulling image extraction complexity into the local runtime.

## Scope

### In scope

- extend `MistakeEvent` with screenshot and MOC-oriented metadata
- preserve backward compatibility for older payloads
- add a new `moc-gap-review` CLI workflow
- persist MOC gap review artifacts under `.system/memory/strategy/`
- add a skill file describing how Codex should capture screenshot mistakes
- update docs so the new closed-loop workflow is explicit

### Out of scope

- local OCR or screenshot parsing inside the CLI
- direct automatic patching of MOCs from pattern mining alone
- new OpenAI agent orchestration beyond the existing scaffold
- redesigning the event store away from JSONL + SQLite

## Data Model Changes

`MistakeEvent` will gain four new fields:

- `question_source`
  - semantic origin of the question
  - examples: `official_mock`, `official_practice_pack`, `official_qbank`, `third_party_qbank`, `custom_drill`
- `source_type`
  - how the evidence reached the system
  - examples: `screenshot`, `typed_question`, `session_note`, `agent_summary`
- `evidence_assets`
  - structured evidence references beyond `evidence_refs`
  - examples: attached image names, local screenshot paths, chat attachment handles
- `moc_target`
  - the exact subject framework file that should be reviewed if this mistake pattern recurs
  - example: `CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md`

These fields must be optional with safe defaults so old payloads continue to parse and existing tests remain valid.

## Storage Changes

The existing storage architecture remains the source of truth:

- `.system/events/` stores raw event logs
- `.system/memory/` stores durable cards, patterns, strategy, and validation artifacts
- `CFA_tier1/dashboard/` remains a projection layer

The new metadata should appear in:

- event JSONL records
- SQLite `mistake_events.payload_json`
- generated `MistakeCard` frontmatter

No new database tables are required for the first version.

## Screenshot Capture Workflow

The screenshot capture workflow is intentionally split across two layers.

### Layer 1: Codex interpretation

When the user sends a screenshot, Codex should:

1. identify the subject, LOS, wrong answer, and correct resolution
2. classify the `error_type`
3. infer `question_source`, `source_type`, `evidence_assets`, and `moc_target`
4. preserve uncertainty conservatively rather than invent details

### Layer 2: local persistence

Codex will call the existing CLI entrypoint:

```powershell
python scripts/cfa.py record-mistake --payload "{...}"
```

The local runtime does not know how to read an image. It only receives a complete payload and stores it.

## MOC Gap Review Workflow

Add a new CLI command:

```powershell
python scripts/cfa.py moc-gap-review
```

This workflow will:

1. load all events
2. focus on `question` events only
3. group by `topic + los + error_type`
4. filter to groups that recur at least 3 times
5. require a non-empty `moc_target`
6. generate a review artifact describing whether the target MOC likely needs:
   - a formula addition
   - an exam trap addition
   - a knowledge-tree node expansion

This step must **not** patch MOCs automatically. It produces a controlled review artifact first.

## MOC Gap Review Artifact

The first version will write one aggregate markdown artifact to:

```text
.system/memory/strategy/moc-gap-review.md
```

Each recommendation block should include:

- `moc_target`
- `topic`
- `los`
- `error_type`
- recurrence count
- suggested gap type
- reason for the recommendation
- linked event IDs or evidence references

The recommendation logic should be heuristic and transparent:

- repeated `formula_misuse` usually suggests `formula`
- repeated `concept_confusion` may suggest `knowledge_tree` or `exam_trap`
- repeated trick-style misunderstandings may suggest `exam_trap`

The artifact is a review queue, not a command to mutate study content.

## CLI Changes

The CLI will gain one new subcommand:

- `moc-gap-review`

The existing commands remain:

- `record-mistake`
- `review-session`
- `audit-agent`
- `mine-patterns`
- `pre-mock-brief`
- `post-mock-retro`

No new top-level script is required; `scripts/cfa.py` remains the standard entrypoint.

## Skill Changes

Add a new local skill:

```text
skills/cfa-screenshot-mistake-captor/SKILL.md
```

This skill will instruct Codex to:

- treat screenshots as raw evidence
- extract the minimum reliable structure
- fill the new provenance fields
- call `record-mistake`
- avoid fabricating LOS or source when uncertain

This keeps screenshot ingestion behavior explicit and reusable.

## Compatibility and Safety

### Backward compatibility

- old payloads without the new fields must still work
- existing tests for question/bias/agent flows must continue to pass
- existing cards and exports remain readable

### Safety constraints

- screenshot interpretation must prefer incomplete truth over confident invention
- pattern mining must not directly edit study content
- MOC updates remain a second step performed by Codex after reading the review artifact

## Verification Strategy

The implementation should prove:

1. old payloads still succeed
2. new fields round-trip through events and cards
3. `moc-gap-review` creates no recommendation before recurrence threshold
4. `moc-gap-review` creates a recommendation after threshold when `moc_target` exists
5. `moc-gap-review` does not fabricate recommendations for events without a `moc_target`
6. screenshot-oriented metadata survives end-to-end storage

## Expected Behavioral Result

After implementation:

- the study system still works exactly as before for manual payload capture
- Codex can reliably turn screenshot conversations into stored question mistakes
- mistake evidence carries richer provenance about official/mock/source context
- repeated errors can surface concrete MOC thickening candidates without directly rewriting the framework
- the user gets a safer and more complete study loop from screenshot -> storage -> pattern -> MOC review
