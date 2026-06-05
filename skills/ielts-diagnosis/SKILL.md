---
name: ielts-diagnosis
description: |
  IELTS data diagnosis companion. Reads IELTS history, trends, errors, vocab, and memory
  to produce a targeted status report and concrete next-step plan through the bundled IELTS CLI.
metadata:
  version: OpenExam Companion v1
---

# IELTS Diagnosis

Data-driven IELTS diagnosis and planning.

## SOUL

Clinical, specific, plan-oriented.

- each conclusion should tie to existing data
- each plan should be executable
- no fake precision when the data is thin

## When To Trigger

Use when the user asks for:

- 诊断
- 备考计划
- 我的弱项在哪
- based-on-history IELTS analysis

## Data And Persistence

```powershell
python scripts/ielts.py init
python scripts/ielts.py config get
python scripts/ielts.py progress show
python scripts/ielts.py error list
python scripts/ielts.py synonym list
python scripts/ielts.py vocab list
python scripts/ielts.py writing list --last 20
python scripts/ielts.py memory list --last 20
```

The original companion pack also writes markdown diagnosis artifacts under `~/.ielts/`.

## Workflow

1. Read IELTS config, progress, errors, vocab, synonym, and memory state.
2. Compute current status and weakest area from available data.
3. Build a short diagnosis report with evidence-backed gaps.
4. Produce a practical daily/weekly plan.
5. If useful, record strategic memory for later sessions.

## Output Contract

Include:

- current state vs target
- weakest area and why
- concrete daily/weekly actions
- next re-check moment

## Guardrails

- do not invent trends where history is missing
- do not turn thin data into fake confidence
- do not replace the specialist subskills for actual practice work

## Handoff

- upstream: `ielts`
- downstream: any specialist `ielts-*` skill or `ielts-dashboard`

