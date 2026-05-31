"""Locked official/evidence graph with editable personal overlays."""

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import GraphOverlayUpdate
from services.advanced_service import knowledge_graph, update_graph_overlay

router = APIRouter()


@router.get("")
async def read_graph(repo=Depends(get_repo)):
    return knowledge_graph(repo)


@router.put("/overlay")
async def write_overlay(req: GraphOverlayUpdate, repo=Depends(get_repo)):
    try:
        return {"overlay": update_graph_overlay(repo, req.model_dump())}
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
