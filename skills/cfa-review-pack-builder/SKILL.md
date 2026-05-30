---
name: cfa-review-pack-builder
description: Build and audit CFA daily review packs from recent events, due mistake cards, patterns, and MOC notes. Use this whenever the user asks for daily review material, spaced review, recent-learning cache summaries, readable question formatting, formula/knowledge previews, or fixes to the daily-review-pack workflow.
---

# CFA Review Pack Builder

Use this skill when generating or auditing `daily-review-pack` outputs.

The review pack is a Decision Layer artifact. It should decide what the learner reviews next, while keeping every item traceable to `.system/events/`, `.system/memory/`, or active `CFA_tier1/*/00-*-MOC.md` pages.

Standard CLI:

- `python scripts/cfa.py record-progress --payload "{...}"`
- `python scripts/cfa.py daily-review-pack --date YYYY-MM-DD --focus-topic "<topic>" --max-items 30 --knowledge-depth expanded`

## Output Standard

A good review pack must be readable as one human study file, not as an agent work log. Its visible content has this order:

1. Metadata/frontmatter.
2. `# 今日复习资料`.
3. `## 一、知识点和公式` with formulas, concepts, and decision rules selected from recent due items, repeated patterns, and today's focus topic.
4. `## 二、错题` with readable question cards.

Avoid visible scheduling or system-control sections unless the user explicitly asks for them. Memory logic can still determine selection, but the learner should see study material, not a process report.

## Selection Logic

Prefer items in this order:

1. Due or overdue mistake cards by `review_due_at`.
2. Repeated patterns with recurrence >= 3.
3. Recent low-confidence events.
4. Today's focus topic MOC, so new learning has a preview scaffold.
5. Progress ledger entries from `.system/memory/progress/`, especially completed daily review and focus overrides.

Use memory theory directly:

- Start with active recall prompts before answers.
- Interleave old weak topics with today's main topic.
- Prioritize high-friction items: low confidence, overdue, repeated error type.
- Keep bedtime as mental replay only unless the user explicitly asks for a serious night session.

## Formatting Rules

Questions must be readable as questions, not as metadata.

- Put the question under `#### 题目`.
- Render the prompt as a blockquote or fenced block so option lines stay aligned.
- Preserve blank lines between stem and choices.
- Keep choices on separate lines.
- Render choices under a separate `#### 选项` section when available.
- If a multiple-choice card lacks choices, show `options_missing` rather than inventing options.
- Put answer/explanation under `#### 正确理解 / 解法`.
- Put the old wrong answer under `#### 我上次错在` when available.
- Keep `fix_rule`, `next_drill`, and evidence as short bullets under `#### 下次规则`.
- Do not emit fields like `retrieval_prompt:` as long single-line bullets when the prompt contains options.

## Knowledge Warm Start Rules

The warm start should not be generic. It should include:

- Formula rows from active MOC Formula & Framework Map sections when the review queue includes formula errors.
- Concept distinctions from active MOCs when the review queue includes concept confusion.
- Today's focus topic core formulas or frameworks, even if the user has not yet made mistakes in that topic today.
- A short `Why this is here` reason for each item, tied to due review, repeated pattern, recent low-confidence event, or focus topic.
- Group related rows by MOC heading so the learner sees the full local framework, not isolated one-line fragments.
- Keep English terms and formula notation intact. Add Chinese only where it clarifies the decision rule or common trap.
- Each grouped warm-start block should include concise core rows and the most important easy-miss boundaries; avoid replacing the source MOC with a long essay.
- In `expanded` mode, include active module-note classifier/trap/recall sections for the focus topic only; non-focus subjects may still appear from due cards or MOCs but should not dominate the warm start.

When exact MOC matching is imperfect, prefer conservative broad subject-level rows rather than inventing formulas.

## Audit Checklist

Before finishing:

- The pack contains `## 一、知识点和公式` before `## 二、错题`.
- At least one warm-start item is connected to the focus topic when a focus topic was supplied.
- Multiple-choice options render on separate lines.
- No question stem is hidden inside a long metadata bullet.
- Every review queue item has a source reason and evidence reference.
- The output can be regenerated without manually editing the dashboard page.
