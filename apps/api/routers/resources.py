from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from deps import get_repo

router = APIRouter()


class SubscriptionRequest(BaseModel):
    lane: str
    provider: str
    target: str
    schedule: str = "0 */6 * * *"
    budget: int = Field(default=50, ge=1, le=50)
    enabled: bool = True


class SubscriptionUpdateRequest(BaseModel):
    enabled: bool | None = None
    schedule: str | None = None
    budget: int | None = Field(default=None, ge=1, le=50)


class DocumentImportRequest(BaseModel):
    lane: str
    provider: str
    url: str
    title: str
    text: str = ""
    license_mode: str = "metadata_only"
    language: str = ""
    topic: str = ""
    answer_bearing: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditRequest(BaseModel):
    scope: str = "content"


class CrawlRequest(BaseModel):
    lane: str
    url: str
    provider: str = "generic_web"
    license_mode: str = "metadata_only"
    title: str = ""
    language: str = ""
    topic: str = ""
    answer_bearing: bool = False


class DiscoveryRequest(BaseModel):
    lane: str
    mode: str = "script"
    provider: str = "generic_web"
    query: str = ""
    target: str = ""
    max_cost: float = Field(default=1.0, ge=0)


class InboxResolveRequest(BaseModel):
    action: str


class LanguageExtractionRequest(BaseModel):
    document_id: str
    items: list[dict[str, Any]]
    citations: list[str]
    confidence: float = Field(ge=0, le=1)
    provider: str
    model: str
    prompt_version: str = "language-ai-extraction-v1"
    cost: float = Field(default=0, ge=0)


@router.get("/providers")
async def providers():
    from app.resource_workflows import list_providers

    return {"providers": list_providers()}


@router.get("/subscriptions")
async def subscriptions(repo=Depends(get_repo)):
    from app.resource_workflows import list_subscriptions

    return {"subscriptions": list_subscriptions(repo)}


@router.post("/subscriptions", status_code=status.HTTP_201_CREATED)
async def subscribe(request: SubscriptionRequest, repo=Depends(get_repo)):
    from app.resource_workflows import create_subscription

    try:
        return create_subscription(repo, **request.model_dump())
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch("/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: str, request: SubscriptionUpdateRequest, repo=Depends(get_repo)):
    from app.resource_workflows import update_subscription

    try:
        return update_subscription(repo, subscription_id=subscription_id, **request.model_dump())
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/documents")
async def documents(repo=Depends(get_repo)):
    from app.resource_workflows import list_documents

    return {"documents": list_documents(repo)}


@router.get("/documents/{document_id}")
async def document(document_id: str, repo=Depends(get_repo)):
    from app.resource_workflows import list_documents

    for item in list_documents(repo):
        if item["document_id"] == document_id:
            return item
    raise HTTPException(status_code=404, detail=f"Resource document not found: {document_id}")


@router.post("/documents/import", status_code=status.HTTP_201_CREATED)
async def import_document(request: DocumentImportRequest, repo=Depends(get_repo)):
    from app.resource_workflows import import_resource_document

    try:
        return import_resource_document(repo, **request.model_dump())
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/search")
async def search(
    q: str = Query(min_length=1),
    lane: str = "",
    limit: int = Query(default=20, ge=1, le=100),
    repo=Depends(get_repo),
):
    from app.resource_workflows import search_resources

    return search_resources(repo, query=q, lane=lane, limit=limit)


@router.get("/jobs")
async def jobs(repo=Depends(get_repo)):
    from app.resource_workflows import list_jobs

    return {"jobs": list_jobs(repo)}


@router.post("/jobs/crawl", status_code=status.HTTP_201_CREATED)
async def crawl(request: CrawlRequest, repo=Depends(get_repo)):
    from app.resource_workflows import crawl_resource_url

    try:
        return await crawl_resource_url(repo, **request.model_dump())
    except (KeyError, PermissionError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/jobs/run-due")
async def run_due(repo=Depends(get_repo)):
    from app.resource_workflows import run_due_subscriptions

    return await run_due_subscriptions(repo)


@router.post("/discover")
async def discover(request: DiscoveryRequest, repo=Depends(get_repo)):
    from app.resource_workflows import build_script_discovery_url, discover_resource_urls, discover_resources_ai

    try:
        if request.mode == "ai":
            return discover_resources_ai(repo, lane=request.lane, query=request.query, max_cost=request.max_cost)
        target = request.target or build_script_discovery_url(request.provider, request.query)
        return {"mode": "script", "provider": request.provider, "urls": await discover_resource_urls(request.provider, target)}
    except (KeyError, PermissionError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/inbox")
async def inbox(repo=Depends(get_repo)):
    from app.resource_workflows import list_inbox

    return {"items": list_inbox(repo)}


@router.post("/inbox/{inbox_id}/resolve")
async def resolve_inbox(inbox_id: str, request: InboxResolveRequest, repo=Depends(get_repo)):
    from app.resource_workflows import resolve_inbox_item

    try:
        return resolve_inbox_item(repo, inbox_id=inbox_id, action=request.action)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/promotions")
async def promotions(repo=Depends(get_repo)):
    from app.resource_workflows import list_promotions

    return {"promotions": list_promotions(repo)}


@router.post("/promotions/{promotion_id}/revoke")
async def revoke(promotion_id: str, repo=Depends(get_repo)):
    from app.resource_workflows import revoke_promotion

    try:
        return revoke_promotion(repo, promotion_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/promotions/language-items")
async def promote_language_items(request: LanguageExtractionRequest, repo=Depends(get_repo)):
    from app.resource_workflows import promote_language_extractions

    try:
        return promote_language_extractions(repo, **request.model_dump())
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/audits")
async def audits(repo=Depends(get_repo)):
    from app.resource_workflows import list_audits

    return {"findings": list_audits(repo)}


@router.post("/audits/run")
async def audit(request: AuditRequest, repo=Depends(get_repo)):
    from app.resource_workflows import run_resource_audit

    try:
        return run_resource_audit(repo, scope=request.scope)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/index/rebuild")
async def rebuild_index(repo=Depends(get_repo)):
    from app.resource_workflows import rebuild_resource_index

    return rebuild_resource_index(repo)


@router.get("/scheduler/status")
async def get_scheduler_status():
    from app.resource_workflows import scheduler_status

    return scheduler_status()


@router.get("/settings")
async def settings(repo=Depends(get_repo)):
    from app.feature_flags import FeatureFlags
    from app.roadmap_waves import provider_is_allowed
    from app.resource_workflows import load_resource_policy, resource_settings

    return {
        **resource_settings(),
        "policy": load_resource_policy(repo.root),
        "consent": {
            "openai_web_search": provider_is_allowed(repo, "openai", "resource_ai_discovery"),
        },
        "features": {
            key: value
            for key, value in FeatureFlags.load(repo.root).values.items()
            if key.startswith("resource_")
        },
    }
