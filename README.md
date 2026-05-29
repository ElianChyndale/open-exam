# CFA Tier 1 Local Agent Mistake System

This repository implements a local-first CFA Tier 1 mistake workflow.

The Obsidian-facing vault is organized by subject folders such as `Quantitative_Methods/`, `Ethical_and_Professional_Standards/`, and `Financial_Statement_Analysis/`, with generated review pages written into `CFA_tier1/dashboard/`. Each subject folder keeps one master `00-*-MOC.md` knowledge framework as its reading entrypoint.

Core layout:

- `CFA_tier1/` stores Obsidian-readable study notes and exported projection pages.
- `.obsidian/` stores Obsidian vault configuration only.
- `.system/events/` stores raw question, bias, and agent event logs.
- `.system/memory/` stores durable markdown cards and strategy artifacts.
- `skills/` stores reusable local agent skills.
- `.system/evals/` stores local evaluation fixtures.
- `.system/app/` contains the CLI, workflows, storage layer, and Agents SDK scaffolding.
- `scripts/` stores runnable entrypoint helpers for the hidden system layer.

## Quick start

Run the local tests:

```powershell
pytest
```

Record a question mistake:

```powershell
python scripts/cfa.py record-mistake --payload "{\"source_layer\":\"question\",\"topic\":\"Ethics\",\"los\":\"I.A\",\"prompt_or_question\":\"...\",\"wrong_choice_or_output\":\"A\",\"correct_resolution\":\"B\",\"error_type\":\"concept_confusion\",\"confidence\":2,\"time_spent\":100,\"evidence_refs\":[\"mock-1\"]}"
```

Screenshot-based capture works through Codex rather than local OCR. When you send a wrong-question screenshot, Codex can normalize it into a structured `record-mistake` payload and preserve richer provenance fields such as `question_source`, `source_type`, `evidence_assets`, and `moc_target`.

Generate a mock review summary:

```powershell
python scripts/cfa.py post-mock-retro --session-id mock-1
```

Generate a framework feedback review from repeated question mistakes:

```powershell
python scripts/cfa.py moc-gap-review
```

This produces a controlled review artifact under `.system/memory/strategy/` so repeated mistakes can suggest MOC improvements without automatically rewriting the subject framework.

Generate a daily spaced-review pack from recent learning cache and due cards:

```powershell
python scripts/cfa.py daily-review-pack --focus-topic "Corporate Issuers"
```

This writes `.system/memory/strategy/daily-review-pack.md` and projects `CFA_tier1/dashboard/今日复习资料.md`.

Write a concise task-level daily todo and archive the previous one:

```powershell
python scripts/cfa.py write-todo --payload "{\"date\":\"2026-05-28\",\"focus\":\"完成 Corporate Issuers 学习\",\"tasks\":[\"完成 Corporate Issuers 主学习\",\"做练习题\",\"处理新增错题\"]}"
```

## OpenAI API note

The repository contains an OpenAI Agents SDK integration scaffold. Live agent runs require a valid `OPENAI_API_KEY`. The local file, memory, export, and eval workflows work without live API access.
