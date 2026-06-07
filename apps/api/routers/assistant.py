"""Assistant Drawer Router — routes drawer messages to the intent service."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from deps import get_repo

router = APIRouter()


@router.post("/messages", response_model=dict[str, Any])
async def assistant_message(req: dict[str, Any], repo=Depends(get_repo)):
    from services.assistant_drawer import AssistantDrawerService

    return AssistantDrawerService(repo).handle_message(req)
