---
name: cfa-pattern-miner
description: Mine repeated CFA mistake patterns by Topic, LOS, and error type. Use whenever the user asks what they keep getting wrong, what topics are weak, or what patterns emerged across sessions.
---

# CFA Pattern Miner

Only promote a pattern when recurrence is high enough to justify intervention.

## Required checks

- group by `topic + los + error_type`
- separate question patterns from bias and agent problems
- do not upgrade one-off pain into long-term doctrine

## Promotion path

1. event
2. card
3. pattern
4. strategy or validation
5. if relevant, `moc-gap-review`

## Formula-aware pattern splits

Repeated formula-related errors must stay separated by what is actually wrong:

- missing `knowledge_tree_core_formula`
- missing `formula_table_variant`
- formula exists but the learner misapplies it
- concept confusion that really belongs to `knowledge_tree_concept`
- misuse that should become `exam_trap`

Do not promote every repeated formula error into the same “formula missing” conclusion.

## Output standard

Every promoted pattern should answer:

- what repeats
- how often it repeats
- what action should change next
- whether the MOC may need strengthening
- which `gap_target` is most likely, if the evidence is strong enough

If evidence is weak, say that MOC patch direction is still unproven rather than guessing.
