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
from routers import attempts, cards, dashboard, diagnosis, energy, export as export_router, institution, mock, privacy, profiles, provenance, question_banks, review, study_plan, todos, transfer, waves


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
app.include_router(energy.router, prefix="/api/energy", tags=["energy"])
app.include_router(study_plan.router, prefix="/api/study-plan", tags=["study-plan"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])
app.include_router(provenance.router, prefix="/api/provenance", tags=["provenance"])
app.include_router(privacy.router, prefix="/api/privacy", tags=["privacy"])
app.include_router(waves.router, prefix="/api", tags=["roadmap-waves"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(institution.router, prefix="/api/institution", tags=["institution"])
app.include_router(export_router.router, prefix="/api/export", tags=["export"])
app.include_router(transfer.router, prefix="/api/import", tags=["transfer"])


@app.get("/api/health")
async def health_check(repo=Depends(get_repo)):
    """Health check endpoint."""
    from app.exam_profile import get_profile
    return {"status": "ok", "version": "0.1.0", "exam": get_profile(repo.root).name}
