---
name: ielts
description: |
  IELTS companion router for this repo. Routes IELTS prep requests into writing, reading, speaking,
  listening, vocab, diagnosis, or dashboard flows through the bundled local `ielts-claude-skills` runtime.
metadata:
  version: OpenExam Companion v1
---

# IELTS Router

Repo-local companion entrypoint for IELTS work.

## SOUL

Route first, coach second.

- use repo-local IELTS tooling
- keep answers action-oriented
- preserve IELTS data in its own local store

## When To Trigger

Use when the user says:

- `/ielts`
- “我要备考雅思”
- “雅思怎么准备”
- “IELTS”

## Data And Persistence

Repo-local CLI wrapper:

```powershell
python scripts/ielts.py init
python scripts/ielts.py config get
python scripts/ielts.py progress show
python scripts/ielts.py memory list --last 15
```

Current companion persistence remains:

- `~/.ielts/config.json`
- `~/.ielts/writing/`
- `~/.ielts/reading/`
- `~/.ielts/listening/`
- `~/.ielts/speaking/`
- `~/.ielts/vocab.json`
- `~/.ielts/synonyms.json`
- `~/.ielts/memories.json`

## Workflow

1. Initialize the IELTS data store through `python scripts/ielts.py init`.
2. Read config, progress, and coaching memory.
3. Ask or infer today’s IELTS target area.
4. Route to:
   - `ielts-writing`
   - `ielts-reading`
   - `ielts-speaking`
   - `ielts-listening`
   - `ielts-vocab`
   - `ielts-diagnosis`
   - `ielts-dashboard`

## Output Contract

Always make clear:

- current IELTS state if data exists
- which subskill is the best next fit
- what command or subflow is being used

## Guardrails

- do not pretend IELTS data lives in `.system/`
- do not merge IELTS records into CFA memory assets
- do not offer unsupported cloud or remote sync

## Handoff

- upstream: user IELTS prep requests
- downstream: all `ielts-*` companion skills

