---
name: cfa-validation-guard
description: Convert repeated agent mistakes into validation checklists. Use whenever hallucinations, unsupported rules, or missing root causes start repeating across reviews.
---

# CFA Validation Guard

Each validation rule should include:

- trigger
- check steps
- failure message

## Use this when

- an agent error could mislead future study decisions
- a wrong rule explanation is likely to recur
- the system needs a pre-output checklist rather than another summary
- a proposed MOC formula patch needs validation before writing

## Rule quality bar

- trigger must be specific
- check steps must be executable
- failure message must state the safe correction

## Formula patch validation

Before any MOC writeback, the validation rule must check patch target and formula ownership.

Required checks:

- does the formula really belong to this knowledge tree node
- is it a core formula or only a table-level variant
- does the evidence support `knowledge_tree_core_formula`, `formula_table_variant`, `both`, `knowledge_tree_concept`, or `exam_trap`
- is the patch recommendation anchored to the current `moc_target`

Unsafe pattern:

- seeing a familiar formula and patching it into the first matching topic without node-level validation

Safe correction:

- run the patch target check first
- confirm formula ownership
- only then approve the writeback location
