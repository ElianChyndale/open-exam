---
name: codex-self-cycle
description: Use this skill whenever the user asks Codex to work autonomously, keep planning after finishing work, run a no-human-interaction coding loop, continue a /goal without waiting for the user, or turn a product plan into iterative AI & AI-coding work. This skill routes the agent through the local `codex-loop-plan` and `codex-loop-complete` workflow so autonomous work stays traceable, test-gated, and safe.
---

# Codex Self-Cycle

Use this skill to turn an open-ended autonomous coding request into a governed local loop.
The goal is not to create an infinite runaway process; it is to make each autonomous step
traceable, verifiable, and able to select the next step without extra human prompting.

## Operating Loop

1. Read the local source of truth first: `AGENTS.md`, `.system/events/`, `.system/memory/`,
   existing plans, and any plan file the user provided.
2. Generate the next loop plan:
   ```powershell
   python scripts/cfa.py codex-loop-plan --mode unattended
   ```
3. Open the generated plan under `.system/memory/codex-loop/` and the task under
   `docs/codex_tasks/`.
4. Execute the selected task while respecting the safety limits in the task file.
5. Verify with targeted tests, lint, API checks, or an explicit deterministic inspection.
6. Mark the task complete:
   ```powershell
   python scripts/cfa.py codex-loop-complete --candidate-id "<id>" --summary "<what changed>" --artifact "<path>" --verification "<tests/checks>"
   ```
7. Immediately generate the next plan again. Continue while there is a meaningful eligible
   candidate and the goal remains active.

## Safety Gates

Stop instead of inventing work when:

- No eligible non-human candidate remains.
- The same blocker repeats for three consecutive goal turns.
- The next task would modify locked question-bank prompts, answer keys, explanations,
  secrets, destructive filesystem state, or remote GitHub refs.
- Verification cannot be run and no explicit deterministic inspection can replace it.

Escalate to the user when:

- The task requires admin approval under the question-bank immutability rule.
- Remote GitHub branch, PR, or issue changes are required.
- The task changes published core brushing-question behavior instead of an extension boundary.

## Project-Specific Boundaries

- Keep the core question-bank flow stable.
- Put recommendation, analytics, adaptive practice, and self-improvement logic in extension
  or Decision Layer modules.
- Treat Obsidian pages as projections, not canonical data.
- Preserve the six agent roles in `.system/app/agents_runtime.py`; do not add new agent roles
  just to make the loop feel more autonomous.

## Completion Note Pattern

Use a concise completion summary:

```text
Implemented <capability>. Artifacts: <files>. Verification: <commands/results>. Next plan generated.
```
