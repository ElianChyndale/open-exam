"""ExamOS API — FastAPI backend.

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

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import attempts, dashboard, diagnosis, energy, export as export_router, institution, mock, review, study_plan


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown."""
    # Ensure directories exist
    from deps import get_repo
    repo = get_repo()
    repo.ensure_layout()
    yield


app = FastAPI(
    title="ExamOS API",
    description="考试通过率操作系统 — CFA/FRM/CPA Exam Operating System API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(attempts.router, prefix="/api/attempts", tags=["attempts"])
app.include_router(diagnosis.router, prefix="/api/diagnose", tags=["diagnosis"])
app.include_router(review.router, prefix="/api/review-pack", tags=["review"])
app.include_router(energy.router, prefix="/api/energy", tags=["energy"])
app.include_router(study_plan.router, prefix="/api/study-plan", tags=["study-plan"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(institution.router, prefix="/api/institution", tags=["institution"])
app.include_router(export_router.router, prefix="/api/export", tags=["export"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0", "exam": "CFA Level I"}
