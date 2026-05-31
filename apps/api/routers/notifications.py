"""In-app notification center."""

from fastapi import APIRouter, Depends

from deps import get_repo
from services.daily_loop_service import notifications

router = APIRouter()


@router.get("")
async def read_notifications(repo=Depends(get_repo)):
    return {"notifications": notifications(repo)}
