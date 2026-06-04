"""OpenExam API — FastAPI backend.

Wraps existing .system/app/ workflows as REST API endpoints.
Provides the full user cockpit API per PLAN.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure .system/app is importable
_SYSTEM = Path(__file__).resolve().parents[2] / ".system"
if str(_SYSTEM) not in sys.path:
    sys.path.insert(0, str(_SYSTEM))

# Ensure apps/api is importable (for deps, schemas, routers, services)
_API = Path(__file__).resolve().parent
if str(_API) not in sys.path:
    sys.path.insert(0, str(_API))

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deps import get_repo
from routers import attempts, assessments, cards, dashboard, data_governance, diagnosis, energy, export as export_router, focus, goals, institution, interop, knowledge_graph, language, learning_analytics, mock, navigation, onboarding, privacy, profiles, provenance, question_banks, resource_candidates, resources, review, study_plan, study_planner, todos, transfer, tutor, waves
from routers import review_lab

# New wave routers (feature-flag gated)
try:
    from routers import knowledge_sources
except ImportError:
    knowledge_sources = None

try:
    from routers import language_dictionaries
except ImportError:
    language_dictionaries = None

try:
    from routers import language_os
except ImportError:
    language_os = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown."""
    # Ensure directories exist
    from deps import get_repo
    repo = get_repo()
    repo.ensure_layout()
    yield


app = FastAPI(
    title="OpenExam API",
    description="考试通过率操作系统 — CFA/FRM/CPA Exam Operating System API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(attempts.router, prefix="/api/attempts", tags=["attempts"])
app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
app.include_router(question_banks.router, prefix="/api/question-banks", tags=["question-banks"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(diagnosis.router, prefix="/api/diagnose", tags=["diagnosis"])
app.include_router(review.router, prefix="/api/review-pack", tags=["review"])
app.include_router(review.router, prefix="/api/daily-review", tags=["daily-review"])
app.include_router(review_lab.router, prefix="/api/review-lab", tags=["review-lab"])
app.include_router(energy.router, prefix="/api/energy", tags=["energy"])
app.include_router(study_plan.router, prefix="/api/study-plan", tags=["study-plan"])
app.include_router(study_planner.router, prefix="/api/study-planner", tags=["study-planner"])
app.include_router(learning_analytics.router, prefix="/api/learning-analytics", tags=["learning-analytics"])
app.include_router(assessments.router, prefix="/api/assessments", tags=["assessments"])
app.include_router(knowledge_graph.router, prefix="/api/knowledge-graph", tags=["knowledge-graph"])
app.include_router(data_governance.router, prefix="/api/data-governance", tags=["data-governance"])
app.include_router(tutor.router, prefix="/api/tutor", tags=["tutor"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["onboarding"])
app.include_router(interop.router, prefix="/api/interop", tags=["interop"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["navigation"])
app.include_router(focus.router, prefix="/api/focus", tags=["focus"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])
app.include_router(provenance.router, prefix="/api/provenance", tags=["provenance"])
app.include_router(privacy.router, prefix="/api/privacy", tags=["privacy"])
app.include_router(waves.router, prefix="/api", tags=["roadmap-waves"])
app.include_router(language.router, prefix="/api/language", tags=["language"])
app.include_router(resources.router, prefix="/api/resources", tags=["resources"])
app.include_router(resource_candidates.router, prefix="/api/resources/candidates", tags=["resource-candidates"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(institution.router, prefix="/api/institution", tags=["institution"])
app.include_router(export_router.router, prefix="/api/export", tags=["export"])
app.include_router(transfer.router, prefix="/api/import", tags=["transfer"])

if knowledge_sources is not None:
    app.include_router(knowledge_sources.router, prefix="/api/knowledge", tags=["knowledge"])

if language_dictionaries is not None:
    app.include_router(language_dictionaries.router, prefix="/api/language/dictionaries", tags=["language-dictionaries"])

if language_os is not None:
    app.include_router(language_os.router, prefix="/api/language-os", tags=["language-os"])


@app.get("/api/health")
async def health_check(repo=Depends(get_repo)):
    """Health check endpoint."""
    from app.exam_profile import get_profile
    return {"status": "ok", "version": "0.1.0", "exam": get_profile(repo.root).name}
