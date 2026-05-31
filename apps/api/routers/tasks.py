"""Executable daily tasks and in-app notifications."""

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo
from schemas import TaskStatusUpdate
from services.daily_loop_service import notifications, set_task_status, today_tasks

router = APIRouter()


@router.get("/today")
async def read_today_tasks(focus_topic: str = Query(default=""), repo=Depends(get_repo)):
    return {"tasks": today_tasks(repo, focus_topic)}


@router.post("/{task_id}/status")
async def update_task_status(task_id: str, req: TaskStatusUpdate, repo=Depends(get_repo)):
    task = set_task_status(repo, task_id, req.status)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Unknown task: {task_id}")
    return {"task": task}


@router.get("/notifications/list")
async def read_task_notifications(repo=Depends(get_repo)):
    return {"notifications": notifications(repo)}
