# ChatGPT × Codex Collaboration Workflow

This document adapts the external file `Codex ChatGPT 协同工作流.docx` to the
current OpenExam repository.

## Purpose

Use ChatGPT as a planning and review partner, while Codex remains the local
execution agent inside this repository. The collaboration goal is not remote
computer control. The goal is a stable loop:

1. ChatGPT critiques or narrows the next bounded task.
2. Codex implements inside the repo and verifies with tests.
3. Codex exports a new brief back to ChatGPT.
4. The cycle repeats without losing source-of-truth discipline.

## Hard Constraints

- `.system/events/` and `.system/memory/` stay above summaries and chat output.
- Core question-bank prompts, answers, explanations, and published ordering are
  treated as locked unless there is an explicit guarded path.
- Recommendation, analytics, and AI output belong to extension boundaries, not
  canonical evidence.
- Every planning suggestion must end in a bounded task with acceptance criteria
  and verification.

## Role Split

### ChatGPT

- Refine the next task.
- Shrink risky scope.
- Tighten acceptance criteria.
- Point out evidence gaps or test gaps.

### Codex

- Read local truth first.
- Modify code and docs locally.
- Run targeted verification.
- Export the next collaboration brief.

## Repo Workflow

1. Generate or inspect the latest local plan.
   `python scripts/cfa.py codex-loop-plan --mode unattended`
2. Export a ChatGPT brief.
   `python scripts/cfa.py chatgpt-brief`
3. Paste `.system/memory/collaboration/chatgpt/CURRENT_BRIEF.md` into the
   ChatGPT chat named `Codex ChatGPT 协同工作流`.
4. Bring ChatGPT's reply back as planning input for the next bounded change.
5. After implementation, mark the loop step complete if appropriate and export
   a fresh brief again.

## Phase Mapping From The Original Workflow

- Phase 1: environment and data model
- Phase 2: practice generation and answer capture
- Phase 3: frontend contract and interaction
- Phase 4: analytics and extension modules

In this repository, those phases must still respect the Capture / Memory /
Decision / Projection layering defined in `AGENTS.md`.
