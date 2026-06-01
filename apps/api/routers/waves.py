from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import get_repo

router = APIRouter()


@router.get("/learner-twin")
async def learner_twin(repo=Depends(get_repo)):
    from app.roadmap_waves import build_learner_twin

    return build_learner_twin(repo)


@router.get("/mcp/tools")
async def mcp_tools(repo=Depends(get_repo)):
    from app.roadmap_waves import ReadOnlyMCPAdapter

    return {"mode": "read-only", "tools": ReadOnlyMCPAdapter(repo).list_tools()}


@router.get("/research/scheduler-comparison")
async def scheduler_comparison(repo=Depends(get_repo)):
    from app.roadmap_waves import compare_scheduler_variants

    return {"variants": compare_scheduler_variants(repo.load_attempt_records())}
