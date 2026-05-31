"""SQLite FTS5 knowledge search."""

from fastapi import APIRouter, Depends, Query

from deps import get_repo
from services.advanced_service import search_assets

router = APIRouter()


@router.get("")
async def search(q: str = Query(min_length=1), limit: int = Query(default=20, ge=1, le=100), repo=Depends(get_repo)):
    return {"query": q, "results": search_assets(repo, q, limit)}
