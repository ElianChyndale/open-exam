"""Official curriculum registry API."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from services.daily_loop_service import curriculum_subject, curriculum_summary

router = APIRouter()


@router.get("")
async def read_curriculum(repo=Depends(get_repo)):
    return curriculum_summary(repo)


@router.get("/{subject_name}")
async def read_curriculum_subject(subject_name: str, repo=Depends(get_repo)):
    subject = curriculum_subject(repo, subject_name)
    if subject is None:
        raise HTTPException(status_code=404, detail=f"Unknown curriculum subject: {subject_name}")
    return subject
