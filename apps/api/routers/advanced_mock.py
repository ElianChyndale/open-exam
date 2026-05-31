"""Typed append-only mock run API."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import ExternalMockImport, MockRunAnswer, MockRunCreate, MockRunStateUpdate
from services.advanced_service import create_mock_run, get_mock_run, import_mock_results, list_mock_runs, submit_mock_answer, update_mock_run_state

router = APIRouter()


@router.post("/runs")
async def start_run(req: MockRunCreate, repo=Depends(get_repo)):
    return {"run": create_mock_run(repo, req.model_dump())}


@router.get("/runs")
async def list_runs(repo=Depends(get_repo)):
    return {"runs": list_mock_runs(repo)}


@router.get("/runs/{run_id}")
async def read_run(run_id: str, repo=Depends(get_repo)):
    run = get_mock_run(repo, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Mock run not found")
    return {"run": run}


@router.post("/runs/{run_id}/state")
async def set_run_state(run_id: str, req: MockRunStateUpdate, repo=Depends(get_repo)):
    run = update_mock_run_state(repo, run_id, req.action, req.elapsed_seconds)
    if run is None:
        raise HTTPException(status_code=404, detail="Mock run not found")
    return {"run": run}


@router.post("/runs/{run_id}/answers")
async def answer_run(run_id: str, req: MockRunAnswer, repo=Depends(get_repo)):
    answer = submit_mock_answer(repo, run_id, req.model_dump())
    if answer is None:
        raise HTTPException(status_code=404, detail="Mock run not found")
    return answer


@router.post("/import-results")
async def import_results(req: ExternalMockImport, repo=Depends(get_repo)):
    return {"run": import_mock_results(repo, req.model_dump())}
