# Codex Self-Cycle Workflow

This workflow turns the plan in `系统改革与刷题计划.docx` into a local, governed
AI-coding loop. It is intentionally not a blind infinite runner. Each iteration
must leave a plan, a task file, a completion event, and a verification note.

## Commands

Generate the next autonomous task:

```powershell
python scripts/cfa.py codex-loop-plan --mode unattended
```

Mark a task complete after implementation and verification:

```powershell
python scripts/cfa.py codex-loop-complete `
  --candidate-id "phase-1-import-contract" `
  --summary "Implemented import immutability guard." `
  --artifact ".system/app/question_banks.py" `
  --verification "pytest -q .system/tests/test_question_banks.py"
```

Then generate the next plan again.

## Artifacts

- `.system/events/codex_loop/codex_loop-events.jsonl` records planned and completed loop events.
- `.system/memory/codex-loop/ITER-xxx.json` stores machine-readable iteration plans.
- `.system/memory/codex-loop/ITER-xxx.md` stores human-readable iteration plans.
- `.system/memory/codex-loop/completions/*.json` records completed candidates.
- `docs/codex_tasks/TASK-xxx.md` stores the selected implementation task.

## Candidate Sources

The planner currently considers:

- The self-cycle bootstrap task.
- Skill upgrade proposals generated from repeated validator failures.
- Phase backlog items extracted from the brushing-system reform plan:
  environment/data model, practice generation, answer submission and wrongbook,
  frontend API contract, analytics/extension boundary.

Completed candidates are skipped on later iterations.

## Safety Model

Unattended mode skips candidates that require human approval and stops on blocked
risk. Every task carries safety limits. The standing limits are:

- Do not auto-edit published question prompts, answer keys, explanations, secrets,
  destructive filesystem state, or remote GitHub refs.
- Do not make analytics, recommendations, or AI outputs part of the canonical
  question bank.
- Do not mark a task complete without targeted tests or an explicit deterministic
  verification note.

## Layer Placement

This workflow belongs to the Decision Layer. It chooses what Codex should do next
based on local evidence and plans, but it does not replace `.system/events/` or
`.system/memory/` as source of truth.
