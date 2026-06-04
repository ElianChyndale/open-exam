"""Learning Analytics API.

Correct-only projections over Review Lab, Formula Lab, LanguageOS, Study
Planner, coverage, resources, mock retro, and ingestion signals.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_repo
from schemas import LearningAnalyticsRecomputeRequest

router = APIRouter()


def _flags(repo):
    from app.feature_flags import FeatureFlags

    return FeatureFlags.load(repo.root)


def _check_flag(repo, flag_name: str = "learning_analytics_enabled") -> None:
    flags = _flags(repo)
    if not flags.enabled(flag_name):
        raise HTTPException(status_code=403, detail=f"{flag_name} feature flag is disabled")


def _service(repo):
    from study_science.learning_analytics import LearningAnalyticsService

    return LearningAnalyticsService(repo.root)


def _range_query(value: str) -> str:
    return value or "30d"


@router.get("/summary", response_model=dict[str, Any])
async def get_learning_analytics_summary(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return an aggregate correct-only learning outcome summary."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "correct_only_analytics_enabled")
    return _service(repo).summary(profile_id=profile_id, range_key=_range_query(range_key))


@router.get("/events", response_model=dict[str, Any])
async def get_learning_analytics_events(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return normalized correct-only learning analytics events."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "correct_only_analytics_enabled")
    events = _service(repo).events(profile_id=profile_id, range_key=_range_query(range_key))
    return {"profile_id": profile_id or "default", "count": len(events), "events": events}


@router.post("/recompute", response_model=dict[str, Any])
async def recompute_learning_analytics(req: LearningAnalyticsRecomputeRequest, repo=Depends(get_repo)):
    """Rebuild persisted analytics projections from local source state."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "correct_only_analytics_enabled")
    return _service(repo).recompute(profile_id=req.profile_id, range_key=req.range)


@router.get("/calibration", response_model=dict[str, Any])
async def get_learning_analytics_calibration(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return mastery calibration records across global/topic/asset scopes."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "mastery_calibration_enabled")
    records = _service(repo).calibration_records(profile_id=profile_id, range_key=_range_query(range_key))
    return {"profile_id": profile_id or "default", "count": len(records), "records": records}


@router.get("/mastery-trends", response_model=dict[str, Any])
async def get_learning_analytics_mastery_trends(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return scoped mastery trend records excluding the global aggregate."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "mastery_calibration_enabled")
    records = _service(repo).mastery_trends(profile_id=profile_id, range_key=_range_query(range_key))
    return {"profile_id": profile_id or "default", "count": len(records), "records": records}


@router.get("/plan-effectiveness", response_model=dict[str, Any])
async def get_learning_analytics_plan_effectiveness(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return Study Planner adherence and block completion metrics."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "plan_effectiveness_enabled")
    return _service(repo).plan_effectiveness(profile_id=profile_id, range_key=_range_query(range_key))


@router.get("/resource-usefulness", response_model=dict[str, Any])
async def get_learning_analytics_resource_usefulness(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return resource quality, promotion, and reviewed-asset usefulness metrics."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "resource_usefulness_enabled")
    return _service(repo).resource_usefulness(profile_id=profile_id, range_key=_range_query(range_key))


@router.get("/coverage-momentum", response_model=dict[str, Any])
async def get_learning_analytics_coverage_momentum(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return syllabus coverage momentum and high-weight gap metrics."""
    _check_flag(repo, "learning_analytics_enabled")
    _check_flag(repo, "coverage_momentum_enabled")
    return _service(repo).coverage_momentum(profile_id=profile_id, range_key=_range_query(range_key))


@router.get("/formula-outcomes", response_model=dict[str, Any])
async def get_learning_analytics_formula_outcomes(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return Formula Lab recall, procedure, and transfer-gap outcome metrics."""
    _check_flag(repo, "learning_analytics_enabled")
    return _service(repo).formula_outcomes(profile_id=profile_id, range_key=_range_query(range_key))


@router.get("/language-outcomes", response_model=dict[str, Any])
async def get_learning_analytics_language_outcomes(
    profile_id: str = Query(default="default"),
    range_key: str = Query(default="30d", alias="range"),
    repo=Depends(get_repo),
):
    """Return LanguageOS lexical recognition and production outcome metrics."""
    _check_flag(repo, "learning_analytics_enabled")
    return _service(repo).language_outcomes(profile_id=profile_id, range_key=_range_query(range_key))
