# OpenExam

OpenExam is a local-first, AI-augmented exam operating system for CFA Level I.
It combines a FastAPI backend, a Next.js cockpit, and cognitive-science study
engines (spaced repetition, retrieval practice, interleaving, self-explanation,
worked-example fading) to turn every question attempt into diagnosis, review
scheduling, daily planning, mock retros, and measurable progress.

This is not a generic flashcards app. It is a full learning evidence kernel —
your mistakes, patterns, calibration, and knowledge states are tracked locally,
analyzed algorithmically, and closed into a feedback loop powered by an
Ebbinghaus graduated knowledge memory model.

## Author

**Elian** — 计算机本科生，正在学习 CFA，目标留学爱尔兰。  
欢迎交流学习经验、备考方法、代码协作。  
这个系统是我边学 CFA 边写出来的，希望能帮到同样在备考的朋友，
也欢迎大佬们提 PR 和 Issue。

## Project Layout

- `apps/api/` — FastAPI backend: attempts, diagnosis, review packs, study plans,
  mock retros, dashboards, institution reports, knowledge memory.
- `apps/web/` — Next.js frontend cockpit (8 pages: today, capture, diagnosis,
  review, mock, dashboard, institution, calendar).
- `packages/study-science/` — retrieval, spacing, interleaving,
  worked-example fading, self-explanation, calibration, energy planning,
  and **knowledge memory** engines.
- `packages/agent-runtime/` — six AI agent role boundaries.
- `.system/` — canonical local event stream, memory overlay, workflow kernel,
  exam profiles, and 40+ tests.
- `CFA_tier1/` — Obsidian/Markdown vault projection layer.

## Quick Start

```powershell
.\start-examos.ps1
```

Starts the API (port 8000) and web app (port 3000), opens
`http://localhost:3000`, and stops both on `Ctrl+C`.

### Manual start

**API:**

```powershell
$env:PYTHONPATH = ".system;apps\api;packages\study-science\src;packages\agent-runtime\src"
python -m uvicorn main:app --app-dir apps\api --host 0.0.0.0 --port 8000
```

**Frontend:**

```powershell
.\start-web.ps1
```

**Health check:**

```powershell
Invoke-RestMethod http://localhost:8000/api/health
# → {"status":"ok","version":"0.1.0","exam":"CFA Level I"}
```

## CLI Still Works

```powershell
# Record a mistake
python scripts/cfa.py record-mistake --payload "{\"source_layer\":\"question\",\"topic\":\"Ethics\",\"los\":\"I.A\",\"prompt_or_question\":\"...\",\"wrong_choice_or_output\":\"A\",\"correct_resolution\":\"B\",\"error_type\":\"concept_confusion\",\"confidence\":2,\"time_spent\":100,\"evidence_refs\":[\"mock-1\"]}"

# Generate daily review (auto-considers knowledge memory state)
python scripts/cfa.py daily-review --focus-topic "Fixed Income"

# Check knowledge point memory states
python scripts/cfa.py knowledge-status

# Run decay sweep on overdue knowledge points
python scripts/cfa.py decay-knowledge

# Complete a daily review and feed back into the knowledge memory loop
python scripts/cfa.py complete-daily-review --review-id daily-review-xxxx
```

## Knowledge Memory Engine

OpenExam's core differentiator: an Ebbinghaus-inspired graduated knowledge
state model.

| State | Interval | Decay | Description |
|-------|----------|-------|-------------|
| New | — | 1d | Never reviewed |
| Reviewed once | 2d | 3d | First exposure, fragile |
| Familiar | 5d | 7d | Can recall with effort |
| Practiced | 12d | 14d | Reliable recall |
| Proficient | 25d | 30d | Quick recall |
| Mastered | 60d | 90d | Automatic, exam-ready |

After every daily review, the KnowledgeMemoryEngine advances or decays each
knowledge point based on outcome, schedules the next review, and feeds back
into daily review generation so overdue points automatically resurface.

## Tests

```powershell
pytest                           # Python tests (workflows, API smoke, models)
```

```powershell
cd apps\web
npm install && npm run typecheck && npm run build   # Frontend checks
```

47 API endpoints tested, all 200 OK. 15 bugs identified and tracked in
`docs/ecosystem-audit-findings.md`.

## Source Of Truth

The frontend is a cockpit, not the source of truth. Canonical learning evidence
lives in `.system/events/` (JSONL event streams) and `.system/memory/`
(markdown cards + knowledge overlay). `CFA_tier1/` is an Obsidian/Markdown
projection layer for reading and review.

## License

MIT — built with ❤️ for the CFA community.
