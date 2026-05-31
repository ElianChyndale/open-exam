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
from fastapi.responses import JSONResponse

from routers import advanced_mock, attempts, coach, curriculum, dashboard, diagnosis, energy, institution, knowledge_graph, mock, notifications, practice, profile, question_banks, reports, retrieval, review, search, study_plan, tasks, transfer


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


@app.middleware("http")
async def require_saas_bearer(request, call_next):
    from auth import AuthError, bearer_token, verify_supabase_token
    from deps import get_openexam_mode

    if get_openexam_mode() == "supabase" and request.url.path.startswith("/api/") and request.url.path != "/api/health":
        try:
            token = bearer_token(request.headers.get("Authorization", ""))
            request.state.auth_claims = verify_supabase_token(token)
        except (AuthError, RuntimeError) as error:
            return JSONResponse(status_code=401, content={"detail": str(error)})
    return await call_next(request)


# Mount routers
app.include_router(attempts.router, prefix="/api/attempts", tags=["attempts"])
app.include_router(diagnosis.router, prefix="/api/diagnose", tags=["diagnosis"])
app.include_router(review.router, prefix="/api/review-pack", tags=["review"])
app.include_router(energy.router, prefix="/api/energy", tags=["energy"])
app.include_router(study_plan.router, prefix="/api/study-plan", tags=["study-plan"])
app.include_router(mock.router, prefix="/api/mock", tags=["mock"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(institution.router, prefix="/api/institution", tags=["institution"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["curriculum"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(retrieval.router, prefix="/api/review-sessions", tags=["retrieval"])
app.include_router(question_banks.router, prefix="/api/question-banks", tags=["question-banks"])
app.include_router(practice.router, prefix="/api/practice-sessions", tags=["practice"])
app.include_router(advanced_mock.router, prefix="/api/mock", tags=["mock-runs"])
app.include_router(coach.router, prefix="/api/coach", tags=["coach"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(knowledge_graph.router, prefix="/api/knowledge-graph", tags=["knowledge-graph"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(transfer.router, prefix="/api", tags=["transfer"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0", "exam": "CFA Level I"}
