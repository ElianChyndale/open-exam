"""Knowledge graph, global search, and traceability API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo

router = APIRouter()


def _check_flag(repo, flag_name: str = "knowledge_graph_enabled") -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.knowledge_graph import KnowledgeGraphService

    return KnowledgeGraphService(repo.root)


@router.post("/recompute", response_model=dict[str, Any])
async def recompute_knowledge_graph(req: dict[str, Any] | None = None, repo=Depends(get_repo)):
    """Recompute the read-only local knowledge graph projection."""
    _check_flag(repo, "knowledge_graph_enabled")
    req = req or {}
    return _service(repo).recompute(profile_id=str(req.get("profile_id") or "default"))


@router.get("/summary", response_model=dict[str, Any])
async def knowledge_graph_summary(profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return graph projection summary."""
    _check_flag(repo, "knowledge_graph_enabled")
    return _service(repo).summary(profile_id=profile_id or "default")


@router.get("/nodes", response_model=dict[str, Any])
async def knowledge_graph_nodes(
    profile_id: str = Query(default="default"),
    node_type: str | None = Query(default=None),
    validation_status: str | None = Query(default=None),
    quality_status: str | None = Query(default=None),
    source_ref: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
    repo=Depends(get_repo),
):
    """List graph nodes with filters."""
    _check_flag(repo, "knowledge_graph_enabled")
    return _service(repo).nodes_query(
        profile_id=profile_id or "default",
        node_type=node_type,
        validation_status=validation_status,
        quality_status=quality_status,
        source_ref=source_ref,
        limit=limit,
    )


@router.get("/nodes/{node_id}", response_model=dict[str, Any])
async def knowledge_graph_node(node_id: str, profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return a single graph node."""
    _check_flag(repo, "knowledge_graph_enabled")
    node = _service(repo).get_node(node_id, profile_id=profile_id or "default")
    if node is None:
        raise HTTPException(status_code=404, detail="Knowledge graph node not found")
    return node


@router.get("/nodes/{node_id}/trace", response_model=dict[str, Any])
async def knowledge_graph_trace(node_id: str, profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return upstream, downstream, related, and quality-gate trace for a node."""
    _check_flag(repo, "traceability_map_enabled")
    try:
        return _service(repo).trace(node_id, profile_id=profile_id or "default")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Knowledge graph node not found: {exc.args[0]}") from exc


@router.get("/edges", response_model=dict[str, Any])
async def knowledge_graph_edges(
    profile_id: str = Query(default="default"),
    edge_type: str | None = Query(default=None),
    from_node_id: str | None = Query(default=None),
    to_node_id: str | None = Query(default=None),
    limit: int = Query(default=500, ge=1, le=2000),
    repo=Depends(get_repo),
):
    """List graph edges with filters."""
    _check_flag(repo, "knowledge_graph_enabled")
    return _service(repo).edges_query(
        profile_id=profile_id or "default",
        edge_type=edge_type,
        from_node_id=from_node_id,
        to_node_id=to_node_id,
        limit=limit,
    )


@router.get("/search", response_model=dict[str, Any])
async def knowledge_graph_search(
    profile_id: str = Query(default="default"),
    q: str = Query(default=""),
    node_type: str | None = Query(default=None),
    validation_status: str | None = Query(default=None),
    quality_status: str | None = Query(default=None),
    module: str | None = Query(default=None),
    topic: str | None = Query(default=None),
    source_ref: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=100),
    repo=Depends(get_repo),
):
    """Search across the graph projection."""
    _check_flag(repo, "global_search_enabled")
    return _service(repo).search(
        profile_id=profile_id or "default",
        query=q,
        node_type=node_type,
        validation_status=validation_status,
        quality_status=quality_status,
        module=module,
        topic=topic,
        source_ref=source_ref,
        limit=limit,
    )


@router.get("/impact/{node_id}", response_model=dict[str, Any])
async def knowledge_graph_impact(node_id: str, profile_id: str = Query(default="default"), repo=Depends(get_repo)):
    """Return read-only impact analysis for source/resource/asset/topic changes."""
    _check_flag(repo, "impact_analysis_enabled")
    try:
        return _service(repo).impact(node_id, profile_id=profile_id or "default")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Knowledge graph node not found: {exc.args[0]}") from exc


@router.get("/related/{node_id}", response_model=dict[str, Any])
async def knowledge_graph_related(
    node_id: str,
    profile_id: str = Query(default="default"),
    limit: int = Query(default=50, ge=1, le=200),
    repo=Depends(get_repo),
):
    """Return related graph nodes."""
    _check_flag(repo, "traceability_map_enabled")
    try:
        return _service(repo).related(node_id, profile_id=profile_id or "default", limit=limit)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Knowledge graph node not found: {exc.args[0]}") from exc
