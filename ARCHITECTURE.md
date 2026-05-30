# ExamOS Architecture

考试通过率操作系统 — CFA/FRM/CPA Exam Operating System

## Directory Structure

```
ExamOS/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py             # App entry point, router mounting
│   │   ├── schemas.py          # Pydantic request/response models
│   │   ├── deps.py             # Dependency injection (Repository, AgentRuntime)
│   │   ├── requirements.txt    # Python dependencies
│   │   ├── routers/            # API route modules
│   │   │   ├── attempts.py     # POST /api/attempts — question capture
│   │   │   ├── diagnosis.py    # POST /api/diagnose — error diagnosis
│   │   │   ├── review.py       # GET /api/review-pack/today
│   │   │   ├── study_plan.py   # GET /api/study-plan/today
│   │   │   ├── energy.py       # POST /api/energy/check-in
│   │   │   ├── mock.py         # POST /api/mock/{id}/retro
│   │   │   ├── dashboard.py    # GET /api/dashboard/effectiveness
│   │   │   └── institution.py  # GET /api/institution/cohorts/{id}/risk-report
│   │   └── services/           # Business logic layer
│   │       ├── diagnosis_service.py
│   │       └── study_plan_service.py
│   │
│   └── web/                    # Next.js frontend
│       ├── src/
│       │   ├── app/            # App Router pages
│       │   │   ├── today/      # Today Cockpit
│       │   │   ├── capture/    # Question Capture
│       │   │   ├── diagnosis/  # Error Diagnosis
│       │   │   ├── review/     # Review Pack
│       │   │   ├── mock/       # Mock Center
│       │   │   ├── dashboard/  # Effectiveness Dashboard
│       │   │   └── institution/ # Institution Console
│       │   ├── components/     # Shared UI components
│       │   └── lib/            # API client, utilities
│       ├── package.json
│       ├── tailwind.config.ts
│       └── next.config.js
│
├── packages/
│   ├── exam-core/              # Abstract exam engine (exam-agnostic)
│   │   └── src/exam_core/
│   │       └── models.py       # QuestionAttempt, ErrorDiagnosis, EnergyCheckIn,
│   │                           # ReviewTask, StudyPlan, MockSession,
│   │                           # LearnerProgressReport, CohortRiskReport, etc.
│   │
│   ├── study-science/          # Cognitive science engines
│   │   └── src/study_science/
│   │       ├── retrieval.py    # Retrieval Engine (testing effect)
│   │       ├── spacing.py      # Spacing Scheduler (spaced practice)
│   │       ├── interleaving.py # Interleaving Builder (mixed practice)
│   │       ├── worked_example.py # Worked Example Fader (cognitive load)
│   │       ├── self_explanation.py # Self-Explanation Prompt
│   │       ├── calibration.py  # Confidence Calibration
│   │       └── energy_planner.py # Energy-Aware Planner
│   │
│   └── agent-runtime/          # Agent orchestration
│       └── src/agent_runtime/
│           └── runtime.py      # 6 agent roles: orchestrator,
│                               # mistake_recorder, review_coach,
│                               # pattern_miner, strategy_coach, validator
│
├── .system/                    # Local-first source of truth (existing)
│   ├── app/                    # CLI kernel (models, workflows, storage, agents)
│   ├── events/                 # JSONL event logs (question, bias, agent, energy)
│   ├── memory/                 # Long-term cognitive assets (cards, patterns, strategy)
│   └── tests/                  # legacy kernel tests
│
├── CFA_tier1/                  # Obsidian / Markdown projection (existing)
├── skills/                     # Agent skill definitions (existing 15+ skills)
├── scripts/                    # Python scripts (existing)
│
├── start-api.ps1               # Start FastAPI server
├── start-web.ps1               # Start Next.js dev server
└── PLAN.md                     # Full product plan
```

## Architecture Principles

1. **Frontend is NOT source of truth** — `.system/events/` and `.system/memory/` are the canonical data
2. **AI doesn't give strategy without event evidence** — every recommendation traces to an attempt, event, card, or mock record
3. **Obsidian is projection, not primary storage** — CFA_tier1/ is a read-only projection layer
4. **All conclusions traceable** — attempt → event → memory card → pattern → strategy

## Data Flow

```
User Action (web UI or CLI)
    ↓
API Endpoint (FastAPI router)
    ↓
Service Layer (diagnosis_service, study_plan_service)
    ├──→ Cognitive Science Engines (study-science package)
    └──→ Workflow Functions (.system/app/workflows.py)
            ↓
        Repository (.system/app/storage.py)
            ├── JSONL event logs (.system/events/)
            ├── SQLite catalog (.system/events/catalog.sqlite3)
            ├── Markdown memory cards (.system/memory/)
            └── Obsidian projection (CFA_tier1/dashboard/)
```

## Cognitive Science Engines (7)

| Engine | Module | Key Mechanism |
|--------|--------|--------------|
| Retrieval | `retrieval.py` | Active recall before passive review |
| Spacing | `spacing.py` | Optimal intervals by confidence + exam date |
| Interleaving | `interleaving.py` | 60% weak / 20% old / 10% adjacent / 10% maintenance |
| Worked Example | `worked_example.py` | Full → completion → independent fading |
| Self-Explanation | `self_explanation.py` | One-question post-error reflection |
| Calibration | `calibration.py` | High-confidence errors = highest priority |
| Energy Planning | `energy_planner.py` | Align task difficulty with energy level |

## API Endpoints

The business API exposes 20 product endpoints below. FastAPI also registers OpenAPI/docs routes, so route introspection reports 24 total routes.

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/attempts` | Record a question attempt |
| POST | `/api/attempts/screenshot` | Upload screenshot for AI extraction |
| GET | `/api/attempts/recent` | List recent attempts |
| POST | `/api/diagnose` | Diagnose an error |
| GET | `/api/diagnose/patterns` | List detected patterns |
| GET | `/api/review-pack/today` | Generate daily review pack |
| GET | `/api/review-pack/due` | List due review items |
| GET | `/api/study-plan/today` | Generate daily study plan |
| POST | `/api/energy/check-in` | Record energy check-in |
| GET | `/api/energy/history` | Energy check-in history |
| POST | `/api/mock/create` | Create mock session |
| POST | `/api/mock/{id}/retro` | Post-mock retro |
| GET | `/api/mock/{id}/brief` | Pre-mock brief |
| GET | `/api/mock/history` | Mock session history |
| GET | `/api/dashboard/effectiveness` | Effectiveness dashboard |
| GET | `/api/dashboard/summary` | Quick summary |
| POST | `/api/institution/cohorts` | Create cohort |
| GET | `/api/institution/cohorts/{id}/risk-report` | Risk report |
| GET | `/api/institution/cohorts` | List cohorts |
| GET | `/api/health` | Health check |

## Getting Started

### Backend

```powershell
.\start-api.ps1
# or manually:
$env:PYTHONPATH = ".system\app;packages\exam-core\src;packages\study-science\src;packages\agent-runtime\src"
uvicorn main:app --app-dir apps\api --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```powershell
.\start-web.ps1
# or manually:
cd apps\web && npm install && npm run dev
```

### CLI (existing)

```powershell
python scripts/cfa.py record-mistake --payload "{...}"
python scripts/cfa.py daily-review-pack --focus-topic "Fixed Income"
python scripts/cfa.py write-todo --payload "{...}"
```

### Tests

```powershell
pytest
cd apps\web
npm run typecheck
npm run build
```
