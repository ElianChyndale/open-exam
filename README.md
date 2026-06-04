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
- `apps/web/` — Next.js frontend cockpit, including LanguageOS and ResourceOS.
- `packages/study-science/` — retrieval, spacing, interleaving,
  worked-example fading, self-explanation, calibration, energy planning,
  and **knowledge memory** engines.
- `packages/agent-runtime/` — six AI agent role boundaries.
- `packages/resource-ingestion/` — policy-guarded public resource ingestion,
  deterministic fetching, discovery providers, and private FTS5 indexing.
- `.system/` — canonical local event stream, memory overlay, workflow kernel,
  exam profiles, and 40+ tests.
- `CFA_tier1/` — Obsidian/Markdown vault projection layer.

## Quick Start

```powershell
.\start-examos.ps1
```

Starts the API (port 8000), web app (port 3000), imports the 613 CFA mock
question bank, checks all dependencies, and opens `http://localhost:3000`.
Press `Ctrl+C` in the terminal to stop all services.

### What's included

| Service | URL | Description |
|---------|-----|-------------|
| **Web Cockpit** | `http://localhost:3000` | Today, review, mock, LanguageOS |
| **API** | `http://localhost:8000` | FastAPI with 47+ endpoints |
| **Mock Bank** | auto-imported | 613 CFA L1 questions across 10 subjects |
| **Logs** | `.system/logs/` | stdout/stderr for both processes |

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

## ResourceOS

ResourceOS ingests public internet resources through robots, SSRF, redirect,
license, hash-manifest, and audit checks. Unknown copyright defaults to
metadata and a short excerpt. Licensed full text stays under
`.system/private/resources/`, is excluded from Git, and is searchable through
the local FTS5 index.

```powershell
python scripts/resources.py providers
python scripts/resources.py crawl --lane language --url https://example.com/article
python scripts/resources.py subscribe --provider rss_atom --lane cfa --url https://example.com/feed.xml
python scripts/resources.py run-due --scheduled
python scripts/resources.py audit --scope content
python scripts/resources.py rebuild-index
```

The Windows scheduler is always an explicit user operation:

```powershell
.\scripts\install-resource-scheduler.ps1
.\scripts\remove-resource-scheduler.ps1
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
python -m ruff check .
python -m mypy
python -m bandit -c pyproject.toml -r .system apps packages scripts
python -m pip_audit -r requirements-audit.txt
pytest -q
```

```powershell
cd apps\web
npm install
npm run lint
npm run typecheck
npm run build
npm run test:e2e
npm run audit:deps
```

`python -m mypy` is the strict ResourceOS gate. The older modules remain
covered by Ruff, Bandit, tests, and incremental typing work.

## Source Of Truth

The frontend is a cockpit, not the source of truth. Canonical learning evidence
lives in `.system/events/` (JSONL event streams) and `.system/memory/`
(markdown cards + knowledge overlay). `CFA_tier1/` is an Obsidian/Markdown
projection layer for reading and review.

## License

MIT — built with ❤️ for the CFA community.
