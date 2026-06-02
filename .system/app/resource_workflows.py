from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
# The executable path and arguments are fixed for a read-only status query.
import subprocess  # nosec B404
from typing import Any
from urllib.parse import urlsplit

import yaml
from app.models import stable_id
from app.resource_storage import ResourceRepository
from app.storage import Repository
from resource_ingestion.audit import audit_documents
from resource_ingestion.discovery import parse_feed_urls, parse_sitemap_urls
from resource_ingestion.fetch import PublicWebFetcher
from resource_ingestion.models import AIEnhancementRecord, PromotionDecision, ResourceSubscription
from resource_ingestion.policy import can_retain_fulltext
from resource_ingestion.providers import build_provider_discovery_url, get_provider_spec, list_provider_specs


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _resources(repo: Repository | ResourceRepository) -> ResourceRepository:
    return repo if isinstance(repo, ResourceRepository) else ResourceRepository(repo)


def load_resource_policy(root: Path) -> dict[str, Any]:
    path = root / ".system" / "config" / "resource-policy.yaml"
    configured = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    return {
        "version": "resource-policy-v1",
        "cfa_official_structured_providers": ["sec_edgar", "fred", "world_bank"],
        "fulltext_allowed_domains": [],
        **(configured or {}),
    }


def list_providers() -> list[dict[str, Any]]:
    return list_provider_specs()


def create_subscription(
    repo: Repository | ResourceRepository,
    *,
    lane: str,
    provider: str,
    target: str,
    schedule: str = "0 */6 * * *",
    budget: int = 50,
    enabled: bool = True,
) -> dict[str, Any]:
    if lane not in {"language", "cfa"}:
        raise ValueError("Resource lane must be language or cfa.")
    get_provider_spec(provider)
    subscription = ResourceSubscription(
        subscription_id=stable_id("resource-subscription", lane, provider, target),
        lane=lane,
        provider=provider,
        target=target,
        schedule=schedule,
        budget=max(1, min(int(budget), 50)),
        enabled=bool(enabled),
        created_at=_now(),
    ).as_dict()
    resources = _resources(repo)
    resources.append("resource.subscription.created", {"subscription": subscription}, evidence_refs=[target])
    return subscription


def list_subscriptions(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    state = _resources(repo).replay()
    return sorted(state["subscriptions"].values(), key=lambda item: item["subscription_id"])


def update_subscription(
    repo: Repository | ResourceRepository,
    *,
    subscription_id: str,
    enabled: bool | None = None,
    schedule: str | None = None,
    budget: int | None = None,
) -> dict[str, Any]:
    resources = _resources(repo)
    subscription = resources.replay()["subscriptions"].get(subscription_id)
    if subscription is None:
        raise KeyError(subscription_id)
    updated = dict(subscription)
    if enabled is not None:
        updated["enabled"] = bool(enabled)
    if schedule is not None:
        updated["schedule"] = schedule
    if budget is not None:
        updated["budget"] = max(1, min(int(budget), 50))
    updated["updated_at"] = _now()
    resources.append(
        "resource.subscription.updated",
        {"subscription": updated},
        evidence_refs=[updated["target"]],
    )
    return updated


def import_resource_document(
    repo: Repository | ResourceRepository,
    *,
    lane: str,
    provider: str,
    url: str,
    title: str,
    text: str = "",
    license_mode: str = "metadata_only",
    language: str = "",
    topic: str = "",
    answer_bearing: bool = False,
    metadata: dict[str, Any] | None = None,
    retrieved_at: str = "",
) -> dict[str, Any]:
    if lane not in {"language", "cfa"}:
        raise ValueError("Resource lane must be language or cfa.")
    get_provider_spec(provider)
    resources = _resources(repo)
    imported = resources.index.ingest(
        lane=lane,
        provider=provider,
        url=url,
        title=title,
        text=text,
        license_mode=license_mode,
        language=language,
        topic=topic,
        answer_bearing=bool(answer_bearing),
        metadata=metadata,
        retrieved_at=retrieved_at,
    )
    if imported["duplicate"]:
        return imported
    document = imported["document"]
    rows = [
        (
            "resource.document.ingested",
            {"document": document, "segments": imported["segments"]},
            [document["url"], document["content_hash"]],
            ["local_storage"],
        ),
        *_promotion_events(document, load_resource_policy(resources.root)),
    ]
    resources.append_many(rows)
    return imported


def _promotion_events(document: dict[str, Any], policy: dict[str, Any]) -> list[tuple[str, dict[str, Any], list[str], list[str]]]:
    evidence_refs = [document["document_id"], document["content_hash"], document["url"]]
    if document["answer_bearing"]:
        return [_inbox_event(document, reason="answer_bearing_content_requires_review")]
    if document["lane"] == "language" and can_retain_fulltext(document["license_mode"]):
        decision = PromotionDecision(
            promotion_id=stable_id("resource-promotion", document["document_id"], "language_private_corpus"),
            lane="language",
            target="language_private_corpus",
            policy_version=str(policy["version"]),
            confidence=1.0,
            evidence_refs=evidence_refs,
            approved=True,
        ).as_dict()
        return [("resource.promotion.decided", {"promotion": decision}, evidence_refs, ["local_storage"])]
    official_providers = set(policy["cfa_official_structured_providers"])
    if (
        document["lane"] == "cfa"
        and document["provider"] in official_providers
        and document["license_mode"] == "official_structured"
    ):
        decision = PromotionDecision(
            promotion_id=stable_id("resource-promotion", document["document_id"], "cfa_registry_fact"),
            lane="cfa",
            target="cfa_registry_fact",
            policy_version=str(policy["version"]),
            confidence=1.0,
            evidence_refs=evidence_refs,
            approved=True,
        ).as_dict()
        return [("resource.promotion.decided", {"promotion": decision}, evidence_refs, ["local_storage"])]
    return [_inbox_event(document, reason="lane_policy_requires_review")]


def _inbox_event(document: dict[str, Any], *, reason: str) -> tuple[str, dict[str, Any], list[str], list[str]]:
    evidence_refs = [document["document_id"], document["content_hash"], document["url"]]
    item = {
        "inbox_id": stable_id("resource-inbox", document["document_id"], reason),
        "document_id": document["document_id"],
        "lane": document["lane"],
        "reason": reason,
        "status": "pending",
        "evidence_refs": evidence_refs,
        "created_at": _now(),
    }
    return ("resource.inbox.queued", {"item": item}, evidence_refs, ["local_storage"])


def list_documents(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    return sorted(_resources(repo).replay()["documents"].values(), key=lambda item: item["retrieved_at"], reverse=True)


def search_resources(
    repo: Repository | ResourceRepository,
    *,
    query: str,
    lane: str = "",
    limit: int = 20,
) -> dict[str, Any]:
    results = _resources(repo).index.search(query, lane=lane, limit=limit)
    return {"query": query, "count": len(results), "results": results}


def run_resource_audit(repo: Repository | ResourceRepository, *, scope: str) -> dict[str, Any]:
    resources = _resources(repo)
    if scope not in {"content", "runtime", "code"}:
        raise ValueError("Audit scope must be content, runtime, or code.")
    if scope == "content":
        findings = audit_documents(list(resources.replay()["documents"].values()))
    elif scope == "runtime":
        findings = []
        if not resources.index.db_path.exists():
            findings.append(
                {
                    "finding_id": stable_id("resource-finding", "resource.index.missing"),
                    "scope": "runtime",
                    "check_id": "resource.index.missing",
                    "severity": "high",
                    "evidence": [resources.index.db_path.relative_to(resources.root).as_posix()],
                    "remediation": "Rebuild the disposable FTS5 resource index.",
                    "status": "open",
                }
            )
    else:
        findings = []
        commands = [
            "python -m ruff check .",
            "python -m mypy",
            "python -m bandit -c pyproject.toml -r .system apps packages scripts",
            "python -m pip_audit -r requirements-audit.txt",
            "pytest -q",
            "cd apps/web && npm run lint && npm run typecheck && npm run build && npm run test:e2e",
            "cd apps/web && npm audit --registry=https://registry.npmjs.org --audit-level=high",
        ]
        report: dict[str, Any] = {
            "scope": "code",
            "generated_at": _now(),
            "commands": commands,
            "automatic_source_edits": False,
            "remediation": "Run the recorded commands, attach their output, and review a proposed patch before editing source code.",
        }
        filename = f"code-audit-{stable_id('resource-audit', report['generated_at'])}.json"
        path = resources.index.audit_root / filename
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {**report, "report_ref": path.relative_to(resources.root).as_posix(), "finding_count": 0, "findings": []}
    rows = [
        ("resource.audit.finding", {"finding": finding}, finding["evidence"], ["local_storage"])
        for finding in findings
    ]
    if rows:
        resources.append_many(rows)
    return {"scope": scope, "finding_count": len(findings), "findings": findings, "checked_at": _now()}


def list_audits(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    return sorted(_resources(repo).replay()["audits"].values(), key=lambda item: item["finding_id"])


def list_inbox(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    return sorted(_resources(repo).replay()["inbox"].values(), key=lambda item: item["inbox_id"])


def resolve_inbox_item(
    repo: Repository | ResourceRepository,
    *,
    inbox_id: str,
    action: str,
) -> dict[str, Any]:
    resources = _resources(repo)
    item = resources.replay()["inbox"].get(inbox_id)
    if item is None:
        raise KeyError(inbox_id)
    if action not in {"approve", "reject"}:
        raise ValueError("Inbox action must be approve or reject.")
    resolution = {**item, "status": action, "resolved_at": _now()}
    resources.append("resource.inbox.resolved", {"inbox_id": inbox_id, "resolution": resolution}, evidence_refs=item["evidence_refs"])
    return resolution


def list_jobs(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    return sorted(_resources(repo).replay()["jobs"].values(), key=lambda item: item["created_at"], reverse=True)


async def crawl_resource_url(
    repo: Repository | ResourceRepository,
    *,
    lane: str,
    provider: str,
    url: str,
    license_mode: str = "metadata_only",
    title: str = "",
    language: str = "",
    topic: str = "",
    answer_bearing: bool = False,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    resources = _resources(repo)
    job_id = stable_id("resource-job", provider, url, _now())
    job = {
        "job_id": job_id,
        "trigger": "crawl",
        "status": "running",
        "budget_usage": 0,
        "retry_state": {},
        "audit_summary": {},
        "created_at": _now(),
    }
    resources.append("resource.job.updated", {"job": job}, evidence_refs=[url])
    web_fetcher = fetcher or PublicWebFetcher()
    try:
        fetched = await web_fetcher.fetch(url)
        policy = load_resource_policy(resources.root)
        hostname = (urlsplit(fetched["url"]).hostname or "").lower()
        effective_license_mode = license_mode
        if license_mode == "metadata_only" and hostname in set(policy["fulltext_allowed_domains"]):
            effective_license_mode = "fulltext_allowed"
        inferred_answer_bearing = answer_bearing or any(
            marker in f"{fetched['url']} {title}".lower()
            for marker in ("practice-problem", "practice_problem", "solution", "answer-key", "answer_key")
        )
        imported = import_resource_document(
            resources,
            lane=lane,
            provider=provider,
            url=fetched["url"],
            title=title or fetched["url"],
            text=fetched["text"],
            license_mode=effective_license_mode,
            language=language,
            topic=topic,
            answer_bearing=inferred_answer_bearing,
            metadata={
                "mime_type": fetched.get("mime_type", ""),
                "etag": fetched.get("etag", ""),
                "last_modified": fetched.get("last_modified", ""),
            },
            retrieved_at=fetched.get("retrieved_at", ""),
        )
        audit = run_resource_audit(resources, scope="content")
        job = {
            **job,
            "status": "completed",
            "budget_usage": 1,
            "audit_summary": {"finding_count": audit["finding_count"]},
        }
        resources.append("resource.job.updated", {"job": job}, evidence_refs=[url, imported["document"]["document_id"]])
        return {"job": job, "document": imported, "audit": audit}
    except Exception as exc:
        failed = {**job, "status": "failed", "retry_state": {"reason": str(exc)}}
        resources.append("resource.job.updated", {"job": failed}, evidence_refs=[url])
        raise


async def discover_resource_urls(provider: str, target: str, *, fetcher: Any | None = None) -> list[str]:
    if provider not in {"rss_atom", "sitemap"}:
        return [target]
    web_fetcher = fetcher or PublicWebFetcher()
    fetched = await web_fetcher.fetch(target)
    if provider == "rss_atom":
        return parse_feed_urls(str(fetched["text"]))
    return parse_sitemap_urls(str(fetched["text"]))


def build_script_discovery_url(provider: str, query: str) -> str:
    return build_provider_discovery_url(provider, query)


async def run_due_subscriptions(
    repo: Repository | ResourceRepository,
    *,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    completed = 0
    skipped_missing_key = 0
    failed = 0
    documents_seen = 0
    for subscription in list_subscriptions(repo):
        if not subscription["enabled"]:
            continue
        provider = get_provider_spec(subscription["provider"])
        if not provider["configured"]:
            skipped_missing_key += 1
            continue
        try:
            urls = await discover_resource_urls(subscription["provider"], subscription["target"], fetcher=fetcher)
            for url in urls[: subscription["budget"]]:
                await crawl_resource_url(
                    repo,
                    lane=subscription["lane"],
                    provider=subscription["provider"],
                    url=url,
                    license_mode=provider["default_license_mode"],
                    fetcher=fetcher,
                )
                documents_seen += 1
            completed += 1
        except Exception:
            failed += 1
    return {
        "completed": completed,
        "skipped_missing_key": skipped_missing_key,
        "failed": failed,
        "documents_seen": documents_seen,
    }


def list_promotions(repo: Repository | ResourceRepository) -> list[dict[str, Any]]:
    return sorted(_resources(repo).replay()["promotions"].values(), key=lambda item: item["promotion_id"])


def discover_resources_ai(
    repo: Repository | ResourceRepository,
    *,
    lane: str,
    query: str,
    max_cost: float = 1.0,
    searcher: Any | None = None,
) -> dict[str, Any]:
    from app.roadmap_waves import provider_is_allowed
    from resource_ingestion.ai_discovery import PROMPT_VERSION, openai_web_search

    resources = _resources(repo)
    if lane not in {"language", "cfa"}:
        raise ValueError("Resource lane must be language or cfa.")
    if not provider_is_allowed(resources.repo, "openai", "resource_ai_discovery"):
        raise PermissionError("AI resource discovery requires recorded consent.")
    payload = (searcher or openai_web_search)(query)
    cost = float(payload.get("cost", 0.0))
    if cost > max_cost:
        raise ValueError("AI resource discovery exceeded its cost budget.")
    candidates = list(payload.get("candidates", []))
    canonical_input = json.dumps({"lane": lane, "query": query}, ensure_ascii=False, sort_keys=True)
    canonical_output = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    citations = sorted(
        {
            str(citation)
            for candidate in candidates
            for citation in candidate.get("citations", [])
            if str(citation)
        }
    )
    confidence = max((float(candidate.get("confidence", 0.0)) for candidate in candidates), default=0.0)
    enhancement = AIEnhancementRecord(
        enhancement_id=stable_id("resource-ai", canonical_input, canonical_output),
        provider="openai_web_search",
        model=str(payload.get("model", "")),
        prompt_version=PROMPT_VERSION,
        input_hash=sha256(canonical_input.encode("utf-8")).hexdigest(),
        output_hash=sha256(canonical_output.encode("utf-8")).hexdigest(),
        citations=citations,
        cost=cost,
        confidence=confidence,
    ).as_dict()
    rows: list[tuple[str, dict[str, Any], list[str], list[str]]] = [
        ("resource.ai.enhanced", {"enhancement": enhancement}, citations, ["local_storage", "resource_ai_discovery"])
    ]
    fetch_ready_count = 0
    for candidate in candidates:
        url = str(candidate.get("url", "")).strip()
        candidate_citations = [str(item) for item in candidate.get("citations", []) if str(item)]
        candidate_confidence = float(candidate.get("confidence", 0.0))
        reason = "ai_discovery_requires_deterministic_fetch"
        if not candidate_citations:
            reason = "ai_discovery_missing_citations"
        elif candidate_confidence >= 0.85:
            fetch_ready_count += 1
        item = {
            "inbox_id": stable_id("resource-inbox", enhancement["enhancement_id"], url, reason),
            "document_id": "",
            "lane": lane,
            "source_url": url,
            "title": str(candidate.get("title", "")),
            "reason": reason,
            "status": "pending",
            "confidence": candidate_confidence,
            "evidence_refs": candidate_citations,
            "created_at": _now(),
        }
        rows.append(("resource.inbox.queued", {"item": item}, candidate_citations, ["local_storage", "resource_ai_discovery"]))
    resources.append_many(rows)
    return {
        "enhancement": enhancement,
        "candidate_count": len(candidates),
        "fetch_ready_count": fetch_ready_count,
        "items": [row[1]["item"] for row in rows[1:]],
    }


def promote_language_extractions(
    repo: Repository | ResourceRepository,
    *,
    document_id: str,
    items: list[dict[str, Any]],
    citations: list[str],
    confidence: float,
    provider: str,
    model: str,
    prompt_version: str = "language-ai-extraction-v1",
    cost: float = 0.0,
    daily_card_budget: int = 50,
) -> dict[str, Any]:
    from app.language_storage import LanguageRepository
    from app.language_workflows import collect_item, generate_cards, import_source

    resources = _resources(repo)
    state = resources.replay()
    document = state["documents"].get(document_id)
    if document is None:
        raise KeyError(document_id)
    canonical_input = json.dumps({"document_id": document_id, "citations": citations}, ensure_ascii=False, sort_keys=True)
    canonical_output = json.dumps(items, ensure_ascii=False, sort_keys=True)
    enhancement = AIEnhancementRecord(
        enhancement_id=stable_id("resource-ai", canonical_input, canonical_output),
        provider=provider,
        model=model,
        prompt_version=prompt_version,
        input_hash=sha256(canonical_input.encode("utf-8")).hexdigest(),
        output_hash=sha256(canonical_output.encode("utf-8")).hexdigest(),
        citations=sorted(set(citations)),
        cost=float(cost),
        confidence=float(confidence),
    ).as_dict()
    evidence_refs = sorted(set([document_id, *citations]))
    base_row = ("resource.ai.enhanced", {"enhancement": enhancement}, evidence_refs, ["local_storage", "resource_ai_extraction"])
    document_segment_ids = {
        segment["segment_id"]
        for segment in state["segments"].values()
        if segment["document_id"] == document_id
    }
    review_reason = ""
    if document["lane"] != "language" or not can_retain_fulltext(document["license_mode"]):
        review_reason = "language_ai_extraction_requires_authorized_fulltext"
    elif document["answer_bearing"]:
        review_reason = "language_ai_extraction_answer_bearing"
    elif confidence < 0.85 or not citations or not set(citations).issubset(document_segment_ids):
        review_reason = "language_ai_extraction_requires_review"
    elif not items:
        review_reason = "language_ai_extraction_empty"
    today = datetime.now(UTC).date().isoformat()
    already_promoted = sum(
        int(event.get("payload", {}).get("new_card_count", 0))
        for event in resources.events()
        if event.get("event_type") == "resource.language.cards.promoted"
        and str(event.get("occurred_at", "")).startswith(today)
    )
    remaining = max(0, min(50, daily_card_budget) - already_promoted)
    if len(items) > remaining:
        review_reason = "language_ai_extraction_daily_budget"
    if review_reason:
        inbox_row = _inbox_event(document, reason=review_reason)
        resources.append_many([base_row, inbox_row])
        return {"promoted": False, "reason": review_reason, "new_card_count": 0, "enhancement": enhancement}

    content_path = (resources.root / document["content_ref"]).resolve()
    private_root = (resources.root / ".system" / "private" / "resources").resolve()
    if private_root not in content_path.parents:
        raise ValueError("Resource content reference must stay inside the private resource store.")
    text = content_path.read_text(encoding="utf-8")
    language_repo = LanguageRepository(resources.repo)
    imported = import_source(
        language_repo,
        source_type="resource",
        title=document["title"],
        language=document.get("language") or "en",
        content=text,
        url=document["url"],
    )
    language_segment_id = imported["segments"][0]["segment_id"]
    card_ids_before = set(language_repo.replay()["cards"])
    for item in items:
        collected = collect_item(
            language_repo,
            item_type=str(item.get("item_type") or "phrase"),
            canonical_form=str(item["canonical_form"]),
            language=document.get("language") or "en",
            segment_id=language_segment_id,
            native_gloss=str(item.get("native_gloss", "")),
            created_from="resource_ai_extraction",
        )
        generate_cards(language_repo, collected["item"]["item_id"], card_types=["recognition"])
    card_ids_after = set(language_repo.replay()["cards"])
    new_card_count = len(card_ids_after - card_ids_before)
    promotion = {
        "document_id": document_id,
        "enhancement_id": enhancement["enhancement_id"],
        "new_card_count": new_card_count,
        "evidence_refs": evidence_refs,
        "promoted_at": _now(),
    }
    resources.append_many(
        [
            base_row,
            ("resource.language.cards.promoted", promotion, evidence_refs, ["local_storage", "resource_ai_extraction"]),
        ]
    )
    return {"promoted": True, "new_card_count": new_card_count, "enhancement": enhancement}


def auto_extract_and_promote(
    repo: Repository | ResourceRepository,
    *,
    document_id: str,
    max_items: int = 15,
) -> dict[str, Any]:
    """Auto-extract vocabulary from a resource document and promote to LanguageOS."""
    from app.feature_flags import FeatureFlags
    from app.language_storage import LanguageRepository
    from app.language_workflows import import_source, collect_item, generate_cards
    from language_science.extraction import full_extract

    if not FeatureFlags.load(_resources(repo).root).enabled("resource_language_pipeline_v2_enabled"):
        return {"promoted": False, "reason": "feature_disabled", "items": []}

    resources = _resources(repo)
    state = resources.replay()
    document = state["documents"].get(document_id)
    if document is None:
        raise KeyError(document_id)
    if document["lane"] != "language":
        return {"promoted": False, "reason": "not_language_lane", "items": []}
    if not document.get("content_ref"):
        return {"promoted": False, "reason": "no_fulltext", "items": []}

    content_path = (resources.root / document["content_ref"]).resolve()
    private_root = (resources.root / ".system" / "private" / "resources").resolve()
    if private_root not in content_path.parents:
        raise ValueError("Content reference outside private store")
    text = content_path.read_text(encoding="utf-8")

    extracted = full_extract(text, max_terms=max_items, max_phrases=max_items // 2)
    language_repo = LanguageRepository(resources.repo)
    imported = import_source(
        language_repo, source_type="resource", title=document["title"],
        language=document.get("language") or "en", content=text, url=document["url"],
    )
    segment_id = imported["segments"][0]["segment_id"] if imported["segments"] else ""

    promoted_count = 0
    for item_data in extracted:
        if item_data["confidence"] < 0.4:
            continue
        try:
            collected = collect_item(
                language_repo,
                item_type=item_data["item_type"],
                canonical_form=item_data["canonical_form"],
                language=document.get("language") or "en",
                segment_id=segment_id,
                created_from="resource_auto_extraction",
            )
            if not collected.get("merged"):
                generate_cards(language_repo, collected["item"]["item_id"], card_types=["recognition"])
                promoted_count += 1
        except Exception:
            continue

    return {"promoted": True, "extracted": len(extracted), "promoted_count": promoted_count}


def revoke_promotion(repo: Repository | ResourceRepository, promotion_id: str) -> dict[str, Any]:
    resources = _resources(repo)
    promotion = resources.replay()["promotions"].get(promotion_id)
    if promotion is None:
        raise KeyError(promotion_id)
    revoked = {**promotion, "revoked": True}
    resources.append("resource.promotion.revoked", {"promotion": revoked}, evidence_refs=revoked["evidence_refs"])
    return revoked


def rebuild_resource_index(repo: Repository | ResourceRepository) -> dict[str, int]:
    return _resources(repo).index.rebuild()


def scheduler_status() -> dict[str, Any]:
    task_name = "OpenExam-ResourceOS"
    if os.name != "nt":
        return {"task_name": task_name, "installed": False, "status": "unsupported_platform"}
    executable = shutil.which("schtasks.exe")
    if executable is None:
        return {"task_name": task_name, "installed": False, "status": "schtasks_unavailable"}
    completed = subprocess.run(
        [executable, "/Query", "/TN", task_name, "/FO", "LIST"],  # nosec B603
        capture_output=True,
        check=False,
        text=True,
        timeout=5,
    )
    return {
        "task_name": task_name,
        "installed": completed.returncode == 0,
        "status": "installed" if completed.returncode == 0 else "not_installed",
    }


def resource_settings() -> dict[str, Any]:
    return {
        "robots_cache_hours": 24,
        "per_domain_concurrency": 2,
        "subscription_resource_limit": 50,
        "max_html_bytes": 5 * 1024 * 1024,
        "max_redirects": 5,
        "ai_discovery_requires_consent": True,
    }
