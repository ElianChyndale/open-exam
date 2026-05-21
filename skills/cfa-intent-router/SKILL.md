---
name: cfa-intent-router
description: Route CFA Tier 1 local-agent tasks into record-mistake, review-session, mine-patterns, pre-mock-brief, post-mock-retro, or audit-agent flows. Use this whenever the user mentions wrong questions, weak topics, mock review, study bottlenecks, or agent audit work.
---

# CFA Intent Router

Classify the incoming request into one of six workflow intents:

- `record-mistake`
- `review-session`
- `mine-patterns`
- `pre-mock-brief`
- `post-mock-retro`
- `audit-agent`

Prefer the smallest workflow that preserves the evidence trail.

## Formula-aware MOC routing

When the user is really asking whether their framework contains a formula, route through MOC inspection before giving a study explanation or patch suggestion.

- “我的知识框架里有没有这个公式”
- “这个公式在我的 MOC 里吗”
- “如果没有就帮我补进知识树”

These requests should first trigger MOC gap inspection anchored to the relevant `moc_target`, then decide whether the user needs:

- formula ownership validation
- `record-mistake` evidence capture
- later `mine-patterns`
- or a conservative patch recommendation

Do not treat formula-presence requests as generic tutoring.

## Routing rules

- Wrong answer or screenshot of a wrong question -> `record-mistake`
- Process issue, timing issue, repeated confusion without a single question focus -> `review-session`
- Repeated weak area analysis -> `mine-patterns`
- Mock coming up soon -> `pre-mock-brief`
- Finished a mock and want synthesis -> `post-mock-retro`
- Agent explanation was wrong or unsafe -> `audit-agent`
- Formula presence / framework completeness question -> MOC gap inspection first, usually through `record-mistake` or `mine-patterns` depending on whether event evidence already exists

If a request spans multiple layers, preserve the system order:

1. capture event
2. mine pattern
3. generate strategy

Do not jump to strategy if the evidence layer is still missing.

## Gap target taxonomy

Use the same MOC gap taxonomy as the rest of the system:

- `knowledge_tree_core_formula`: the node is missing its main formula
- `formula_table_variant`: the node has the core formula but the formula table misses a variant or conversion
- `both`: both the tree node and formula table are incomplete
- `knowledge_tree_concept`: the tree lacks the concept branch or distinction
- `exam_trap`: the weakness is misuse, confusion, or a missing warning rather than formula absence

Route patch requests conservatively. Validate formula ownership before recommending any writeback.
