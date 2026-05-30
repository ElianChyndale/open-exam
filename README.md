# ExamOS

ExamOS is a local-first CFA Level I exam operating system: a FastAPI backend, a Next.js cockpit, cognitive-science study engines, and the existing `.system/` evidence kernel in one project.

It is not a generic AI study assistant. The product goal is to turn question attempts into diagnosis, review scheduling, daily planning, mock retros, and measurable progress toward passing.

## Project Layout

- `apps/api/` - FastAPI backend for attempts, diagnosis, review packs, study plans, mock retros, dashboards, and institution reports.
- `apps/web/` - Next.js frontend cockpit.
- `packages/exam-core/` - exam-agnostic domain models.
- `packages/study-science/` - retrieval, spacing, interleaving, worked-example fading, self-explanation, calibration, and energy planning engines.
- `packages/agent-runtime/` - six role boundaries: orchestrator, mistake_recorder, review_coach, pattern_miner, strategy_coach, validator.
- `.system/` - canonical local event, memory, workflow, and test kernel.
- `CFA_tier1/` - Obsidian/Markdown projection layer.

## Start Backend

Simplest option, one command:

```powershell
.\start-examos.ps1
```

This starts the API and web app, opens `http://localhost:3000`, and stops both when you press `Ctrl+C` in that terminal.

## Start Backend Manually

```powershell
.\start-api.ps1
```

Manual equivalent:

```powershell
$env:PYTHONPATH = ".system;apps\api;packages\exam-core\src;packages\study-science\src;packages\agent-runtime\src"
python -m uvicorn main:app --app-dir apps\api --host 0.0.0.0 --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

## Start Frontend Manually

```powershell
.\start-web.ps1
```

The frontend runs at `http://localhost:3000` and uses `NEXT_PUBLIC_API_URL` when set, otherwise `http://localhost:8000`.

## Tests And Builds

Run Python tests:

```powershell
pytest
```

Run frontend checks:

```powershell
cd apps\web
npm install
npm run typecheck
npm run build
```

Current verified Python coverage includes the legacy `.system/tests`, API smoke tests, and package model instantiation tests.

## CLI Still Works

```powershell
python scripts/cfa.py record-mistake --payload "{\"source_layer\":\"question\",\"topic\":\"Ethics\",\"los\":\"I.A\",\"prompt_or_question\":\"...\",\"wrong_choice_or_output\":\"A\",\"correct_resolution\":\"B\",\"error_type\":\"concept_confusion\",\"confidence\":2,\"time_spent\":100,\"evidence_refs\":[\"mock-1\"]}"
python scripts/cfa.py daily-review-pack --focus-topic "Fixed Income"
python scripts/cfa.py post-mock-retro --session-id mock-1
```

## Source Of Truth

The frontend is a cockpit, not the source of truth. Canonical learning evidence remains in `.system/events/` and `.system/memory/`; `CFA_tier1/` is a projection layer for reading and review.
