from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from deps import get_repo
from schemas import TodoReplaceRequest, TodoRevisionRequest, TodoStudyPlanImportRequest, TodoTaskCreate, TodoTaskUpdate

router = APIRouter()


def _raise_workflow_error(exc: Exception) -> None:
    from app.workflows.todo import RevisionConflict

    if isinstance(exc, RevisionConflict):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(exc), "expected_revision": exc.expected, "actual_revision": exc.actual},
        ) from exc
    if isinstance(exc, KeyError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo task not found: {exc.args[0]}") from exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    raise exc


@router.get("/today")
async def get_today(date_str: str = Query(default="", alias="date"), repo=Depends(get_repo)):
    from app.workflows.todo import get_todo

    return get_todo(repo, date_str)


@router.post("/replace")
async def replace(request: TodoReplaceRequest, repo=Depends(get_repo)):
    from app.workflows.todo import replace_todo

    return replace_todo(repo, request.model_dump())


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(request: TodoTaskCreate, repo=Depends(get_repo)):
    from app.workflows.todo import create_todo_task

    try:
        return create_todo_task(
            repo,
            text=request.text,
            deadline=request.deadline,
            progress=request.progress,
            expected_revision=request.expected_revision,
            plan_date=request.date,
        )
    except Exception as exc:
        _raise_workflow_error(exc)


@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, request: TodoTaskUpdate, repo=Depends(get_repo)):
    from app.workflows.todo import update_todo_task

    try:
        return update_todo_task(repo, task_id, request.model_dump(exclude_none=True, exclude={"expected_revision"}), request.expected_revision)
    except Exception as exc:
        _raise_workflow_error(exc)


@router.post("/tasks/{task_id}/toggle")
async def toggle_task(task_id: str, request: TodoRevisionRequest, repo=Depends(get_repo)):
    from app.workflows.todo import toggle_todo_task

    try:
        return toggle_todo_task(repo, task_id, request.expected_revision)
    except Exception as exc:
        _raise_workflow_error(exc)


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, expected_revision: int = Query(..., ge=0), repo=Depends(get_repo)):
    from app.workflows.todo import delete_todo_task

    try:
        return delete_todo_task(repo, task_id, expected_revision)
    except Exception as exc:
        _raise_workflow_error(exc)


@router.post("/import-study-plan")
async def import_study_plan(request: TodoStudyPlanImportRequest, repo=Depends(get_repo)):
    from app.workflows.todo import import_study_plan_tasks

    try:
        return import_study_plan_tasks(repo, request.plan, confirmed=request.confirmed)
    except Exception as exc:
        _raise_workflow_error(exc)


@router.get("/archives")
async def archives(repo=Depends(get_repo)):
    from app.workflows.todo import list_todo_archives

    return {"archives": list_todo_archives(repo)}
