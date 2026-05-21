# CFA MOC Formula Bidirectional Mapping and Agent Update Design

> Note: This design extends the current CFA Level I local-agent study system. It does not replace the four-layer architecture or the CLI-first workflow. It formalizes how formulas should live inside subject MOCs, how formula tables should point back to knowledge-tree nodes, and how the existing agents and skills should adapt to this new standard.

## Goal

Upgrade the CFA Level I MOC system so formulas are no longer isolated in formula tables. After this change:

- users can see the core formula directly inside the relevant knowledge-tree node
- formula tables continue to serve as compact lookup sheets
- formula tables explicitly point back to the knowledge-tree node they belong to
- Codex can decide whether a mistake requires patching the tree, the formula table, or both
- the local agents and skills share one stable MOC patching rule

## Why This Change

The current subject MOCs already provide:

- one master `00-*-MOC.md` per subject
- a knowledge tree for conceptual navigation
- a `核心公式速查` section for compact formula review
- mistake capture, pattern mining, and MOC gap review workflows

What is still weak is the connection between structure and formulas:

1. some knowledge-tree nodes include formulas, but many do not
2. formulas are discoverable in tables, but not consistently visible at the point of understanding
3. repeated mistake evidence can suggest “formula missing,” but there is no uniform place inside the tree to patch it
4. agents can detect a gap, but they do not yet share a formal target taxonomy for where that gap belongs

This produces a fragile loop: formulas exist, but the framework is not yet detailed enough to support stable, repeatable patching.

## User-Facing Outcome

After this change, the intended study experience becomes:

1. open a subject MOC
2. read the knowledge tree as the main understanding scaffold
3. see the core formula directly under the relevant knowledge point
4. use the formula table for variants, conversions, and compact review
5. when a repeated mistake appears, let Codex decide whether the missing piece is:
   - a core formula missing from the tree
   - a variant formula missing from the formula table
   - both
6. let the corresponding workflow patch the correct location instead of guessing

## Core Design Decision

This design adopts a **bidirectional mapping standard** between:

- knowledge-tree nodes
- formula-table rows

The standard is:

1. formula-driven knowledge-tree nodes gain a `核心公式` subsection
2. `核心公式` contains only the main formula or formulas that the learner should recall at the concept node itself
3. `核心公式速查` keeps the broader formula inventory, including variants and conversions
4. every formula-table row gets a `知识树节点` column that points back to the owning node

This preserves both learning modes:

- tree-first understanding
- table-first review

## Scope

### In scope

- define a uniform node structure for formula-bearing MOC knowledge-tree entries
- define a uniform formula-table schema with reverse node mapping
- classify which subjects should be formula-dense by default
- update MOC patching logic so gap recommendations can target tree, table, or both
- update the relevant local agents, skills, and workflows to use the new targeting language

### Out of scope

- redesigning the entire MOC prose style
- changing the raw event store architecture
- forcing formulas into concept-only subjects or concept-only nodes
- replacing the current `核心公式速查` sections with generated content

## Subject Applicability

The system should not force one density rule on all subjects.

### Formula-dense by default

These subjects should generally use `核心公式` nodes wherever the concept is formula-driven:

- `Quantitative_Methods`
- `Fixed_Income`
- `Derivatives`
- `Equity`
- `Financial_Statement_Analysis`
- `Corporate_Issuers`
- `Portfolio_Management`
- `Economics`

### Selective formula usage

- `Alternative_Investments`
  - add `核心公式` only where the topic is genuinely calculation-driven

### Concept-first subject

- `Ethical_and_Professional_Standards`
  - do not force `核心公式` subsections into the tree
  - retain concept structure only

## Knowledge-Tree Standard

Formula-bearing nodes will follow this structure:

```text
├── 2.3 Implied quantities【考试核心】
│   ├── 定义/直觉
│   │   └── 用价格、现金流和增长关系反推隐含变量
│   ├── 核心公式
│   │   ├── r = D1/P0 + g
│   │   └── PV = Σ CFt/(1+r)^t
│   └── 注意：先识别已知项，再反推未知项【考试陷阱】
```

### Rules

- only formula-bearing nodes gain `核心公式`
- `核心公式` should contain the main exam-facing formula, not every algebraic rearrangement
- if a node has no meaningful main formula, do not add a fake placeholder
- where useful, `定义/直觉` should be used to anchor the formula semantically rather than dropping equations without context

## Formula Table Standard

Each `核心公式速查` table should gain a reverse mapping column:

```md
| 指标 | 公式 | 知识树节点 | 考试说明 |
|------|------|------------|----------|
| Gordon Link | `r=D1/P0+g` | `2.3` | 用价格、股利和增长反推 required return |
```

### Rules

- `知识树节点` should use the local node number already visible in the MOC
- if one formula supports more than one node, prefer the most direct owning node rather than duplicating ownership everywhere
- variants, conversions, and boundary forms remain in the table even if they are not repeated in the tree
- concept-only formula tables are not required for subjects like Ethics

## Patch Target Taxonomy

The system needs a clearer way to say what is missing.

The new target taxonomy should be:

- `knowledge_tree_core_formula`
- `formula_table_variant`
- `both`
- `exam_trap`
- `knowledge_tree_concept`

### Interpretation

- `knowledge_tree_core_formula`
  - the main formula is missing from the concept node in the tree
- `formula_table_variant`
  - the node already has the core formula, but a conversion, rearrangement, or comparison formula is missing from the formula table
- `both`
  - the concept node lacks the core formula and the formula table also lacks the supporting formula row
- `exam_trap`
  - the issue is conceptual confusion or misuse, not formula absence
- `knowledge_tree_concept`
  - the tree itself lacks a concept branch or distinction, even if the formula table is complete

## Workflow Changes

### `record-mistake`

No change to the CLI shape is required, but the downstream MOC patch logic should assume that a formula gap may now target the tree, the table, or both.

### `mine-patterns`

No structural change is required, but pattern interpretation should preserve enough evidence for later MOC targeting.

### `moc-gap-review`

This workflow becomes the decision point for MOC patch direction.

It should:

1. detect repeated `topic + los + error_type` patterns
2. inspect the corresponding MOC target
3. determine whether the observed gap is:
   - missing core formula in the tree
   - missing variant formula in the table
   - both
   - concept/tree weakness
   - exam trap weakness
4. output `gap_target` using the new taxonomy

### `moc-auto-patch`

This workflow must be aligned to the new patch targets:

- `knowledge_tree_core_formula` -> patch the node’s `核心公式`
- `formula_table_variant` -> patch the `核心公式速查` table only
- `both` -> patch both locations
- `exam_trap` -> patch the trap section or tree warning line only
- `knowledge_tree_concept` -> expand the tree node or add a concept branch

The workflow must continue to avoid deleting user-authored content and must patch only the local relevant section.

## Agent and Skill Updates

The existing system should keep the current role boundaries. No new top-level agent role is needed.

### `orchestrator`

Update responsibility:

- route MOC-related requests using the new patch target taxonomy
- ensure the flow stays `event -> pattern -> gap review -> patch`
- avoid jumping directly to a tree rewrite without evidence

### `mistake_recorder`

Update responsibility:

- capture enough structured evidence so later formula-gap decisions are possible
- when the user explicitly says “this formula is missing from my framework,” mark the mistake/MOC context conservatively rather than converting it straight into a strategy-level summary

### `review_coach`

Update responsibility:

- explain whether the weakness is formula recall, formula selection, or concept structure
- recommend whether the user should reinforce the tree node or just drill variants

### `pattern_miner`

Update responsibility:

- surface repeated formula-related errors with clearer separation:
  - missing core formula
  - formula misuse despite formula existing
  - concept confusion not solved by adding a formula

### `strategy_coach`

Update responsibility:

- use the richer MOC structure when generating pre-mock and post-mock guidance
- direct the user to specific node numbers, not only broad subjects

### `validator`

Update responsibility:

- guard against unsafe MOC edits by checking:
  - the formula really belongs to that node
  - the formula is core vs variant as labeled
  - the patch target matches the evidence

## Skill File Updates

### `skills/cfa-question-captor/SKILL.md`

Update to state:

- formula-driven gaps may require patching the knowledge tree, formula table, or both
- `核心公式` is the preferred destination for the main formula of a node
- formula variants should remain in the formula table

### `skills/cfa-review-synthesizer/`

Update to state:

- review output should explicitly identify whether the gap is tree-core, table-variant, concept, or trap

### `skills/cfa-pattern-miner/`

Update to state:

- repeated formula errors should not all collapse into one “formula missing” conclusion
- the skill should help distinguish structural formula absence from misuse

### `skills/cfa-validation-guard/`

Update to state:

- formula patch validation must check ownership and target type before writing

### `skills/cfa-intent-router/`

Update to state:

- “我的知识框架里有没有这个公式” and similar requests should route through MOC gap inspection rather than being treated as a generic study explanation

## File-Level Implementation Targets

The following files are expected to change during implementation:

- `CFA_tier1/*/00-*-MOC.md`
- `docs/moc-auto-patch-workflow.md`
- `.system/app/workflows.py`
- `skills/cfa-question-captor/SKILL.md`
- `skills/cfa-intent-router/SKILL.md`
- `skills/cfa-pattern-miner/SKILL.md`
- `skills/cfa-review-synthesizer/SKILL.md`
- `skills/cfa-validation-guard/SKILL.md`

Depending on current code organization, the CLI entry layer and related tests may also need updates.

## Verification Strategy

The implementation should prove:

1. formula-bearing nodes can be patched without damaging surrounding tree text
2. formula tables retain readability after adding the `知识树节点` column
3. the system can distinguish:
   - missing core formula
   - missing variant formula
   - concept-only gap
4. Ethics is not polluted with forced formula nodes
5. MOC gap recommendations remain evidence-backed and conservative
6. the updated skills and workflows agree on the same patch target taxonomy

## Expected Behavioral Result

After implementation:

- each formula-heavy subject MOC becomes a stronger study scaffold instead of a loose mix of tree and formula sheet
- users can see the main formula at the knowledge point where it matters
- formula tables remain compact but now point back to the knowledge tree
- repeated mistakes can trigger more precise MOC reinforcement
- the agents become more accountable because they share a single explicit rule for deciding what kind of MOC patch is justified
