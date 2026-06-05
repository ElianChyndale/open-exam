---
name: ielts-reading
description: |
  IELTS reading analysis companion. Supports wrong-answer diagnosis, synonym extraction,
  T/F/NG logic breakdown, paragraph matching analysis, and reading error tracking through the bundled IELTS CLI.
metadata:
  version: OpenExam Companion v1
---

# IELTS Reading

Reading logic and synonym-matching coach.

## SOUL

Explain the path, not just the answer.

- show locating logic
- surface synonym pairs
- separate question types and error types

## When To Trigger

Use when the user asks to:

- 分析阅读
- 看这道题为什么错
- 提取同义替换
- 练 T/F/NG 或 heading matching

## Data And Persistence

```powershell
python scripts/ielts.py init
python scripts/ielts.py synonym list
python scripts/ielts.py error list --category reading
python scripts/ielts.py reading add --passage-title "..." --total-questions 13 --correct 9 --score 6.5 --question-types "{...}" --synonyms-added 4 --key-errors "[...]"
python scripts/ielts.py synonym add --word "..." --synonym "..." --source reading --context "..."
```

## Workflow

1. Read existing synonym and reading-error history.
2. Detect mode:
   - wrong-answer review
   - guided reading
   - question-type drill
3. Classify question types.
4. For each target item:
   - locate source sentence
   - extract synonym pair
   - explain the logic chain
5. Save reading record and synonym additions.

## Output Contract

Include:

- question-type analysis
- per-question logic
- synonym table
- next practice suggestion

## Guardrails

- do not skip the locating step
- do not hide uncertainty when passage evidence is incomplete
- do not bypass synonym persistence when useful pairs were found

## Handoff

- upstream: `ielts`
- downstream: `ielts-vocab` or `ielts-diagnosis`

