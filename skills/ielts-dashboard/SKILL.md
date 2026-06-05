---
name: ielts-dashboard
description: |
  IELTS dashboard companion. Generates and opens the local IELTS HTML dashboard
  through the bundled CLI, surfacing trends, radar views, error summaries, and vocab status.
metadata:
  version: OpenExam Companion v1
---

# IELTS Dashboard

Generate and open the IELTS local dashboard, not interpret every learning decision.

## SOUL

Fast, visual, local-first.

- build the view
- open the file
- tell the user what they can inspect next

## When To Trigger

Use when the user asks for:

- dashboard
- 看数据
- 打开 IELTS 面板
- progress visualization

## Data And Persistence

```powershell
python scripts/ielts.py init
python scripts/ielts.py dashboard
```

Current output remains the original companion location:

- `~/.ielts/dashboard.html`

## Workflow

1. Initialize the IELTS local store if needed.
2. Generate the dashboard through the CLI wrapper.
3. Tell the user where the output lives and what it shows.
4. If there is no data yet, redirect them to a practice skill first.

## Output Contract

Include:

- success/failure state
- dashboard path
- the most relevant next use step

## Guardrails

- do not pretend this is the same as the OpenExam CFA dashboard
- do not analyze deeply here if `ielts-diagnosis` is the better next tool
- do not require a server; this is local static output

## Handoff

- upstream: `ielts`
- downstream: `ielts-diagnosis` or a practice subskill when data is missing

