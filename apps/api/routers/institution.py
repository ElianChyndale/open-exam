"""GET /api/institution/cohorts/{id}/risk-report — Institution console."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import CohortCreate, CohortRiskResponse

router = APIRouter()


@router.post("/cohorts")
async def create_cohort(req: CohortCreate, repo=Depends(get_repo)):
    """Create a new institution cohort."""
    import json
    from datetime import datetime, UTC

    cohort_dir = repo.memory_root / "institution" / "cohorts"
    cohort_dir.mkdir(parents=True, exist_ok=True)

    cohort_data = {
        "cohort_id": f"cohort-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
        "institution_id": req.institution_id,
        "cohort_name": req.cohort_name,
        "exam_target": req.exam_target,
        "exam_date": req.exam_date,
        "learner_ids": req.learner_ids,
        "instructor_ids": [],
        "created_at": datetime.now(UTC).isoformat(),
    }

    path = cohort_dir / f"{cohort_data['cohort_id']}.json"
    path.write_text(json.dumps(cohort_data, ensure_ascii=False, indent=2))

    return {"status": "created", **cohort_data}


@router.get("/cohorts/{cohort_id}/risk-report", response_model=CohortRiskResponse)
async def get_cohort_risk_report(cohort_id: str, repo=Depends(get_repo)):
    """Generate an institutional risk report for a cohort.

    Returns:
    - At-risk learner rankings
    - Dropout warnings (inactive learners)
    - Aggregate metrics
    - Instructor intervention recommendations
    """
    import json

    cohort_dir = repo.memory_root / "institution" / "cohorts"
    cohort_path = cohort_dir / f"{cohort_id}.json"

    if not cohort_path.exists():
        raise HTTPException(status_code=404, detail=f"Cohort {cohort_id} not found")

    cohort = json.loads(cohort_path.read_text(encoding="utf-8"))

    # For each learner, check their progress
    at_risk: list[dict] = []
    dropout_warnings: list[dict] = []
    learner_metrics: list[dict] = []

    for learner_id in cohort.get("learner_ids", []):
        # Each learner has their own repo/state
        # In production, this queries learner-specific data
        # For MVP, we check the events directory for learner-tagged events
        events = repo.load_events()

        learner_events = [
            e for e in events
            if learner_id in e.evidence_refs or learner_id in str(e.event_id)
        ]

        from datetime import date, datetime
        today = date.today()

        # Check inactivity (no events in 7 days)
        recent_dates = set()
        for e in learner_events:
            try:
                event_date = datetime.fromisoformat(e.created_at.replace("Z", "+00:00")).date()
                recent_dates.add(event_date)
            except (ValueError, TypeError):
                pass

        days_since_last = 999
        if recent_dates:
            last_date = max(recent_dates)
            days_since_last = (today - last_date).days

        total_errors = len(learner_events)

        # Risk assessment
        risk_score = 0.0
        if days_since_last >= 7:
            risk_score += 0.4
            dropout_warnings.append({
                "learner_id": learner_id,
                "days_inactive": days_since_last,
                "warning": f"Learner {learner_id} has been inactive for {days_since_last} days",
            })
        if days_since_last >= 3:
            risk_score += 0.2
        if total_errors == 0:
            risk_score += 0.1  # no data = can't assess

        if risk_score > 0.3:
            at_risk.append({
                "learner_id": learner_id,
                "risk_score": round(risk_score, 2),
                "total_errors": total_errors,
                "days_inactive": days_since_last,
            })

        learner_metrics.append({
            "learner_id": learner_id,
            "total_events": total_errors,
            "days_inactive": days_since_last,
            "risk_score": round(risk_score, 2),
        })

    # Aggregate metrics
    if learner_metrics:
        avg_events = sum(m["total_events"] for m in learner_metrics) / len(learner_metrics)
        avg_inactive = sum(m["days_inactive"] for m in learner_metrics) / len(learner_metrics)
    else:
        avg_events = 0
        avg_inactive = 0

    # Sort at-risk by risk score descending
    at_risk.sort(key=lambda x: -x["risk_score"])

    # Instructor recommendations
    recommendations: list[str] = []
    if dropout_warnings:
        recommendations.append(f"有 {len(dropout_warnings)} 名学员超过 7 天未活跃，建议班主任逐一跟进。")
    if len(at_risk) > len(learner_metrics) * 0.3:
        recommendations.append("超过 30% 学员处于风险状态，建议检查课程难度和时间安排是否合理。")
    if at_risk:
        top_risk = at_risk[0]
        recommendations.append(f"最高风险学员: {top_risk['learner_id']} (风险分 {top_risk['risk_score']})，建议安排一对一诊断。")

    return CohortRiskResponse(
        report_id=f"risk-{cohort_id}-{date.today().isoformat()}",
        cohort_id=cohort_id,
        cohort_name=cohort.get("cohort_name", ""),
        total_learners=len(cohort.get("learner_ids", [])),
        at_risk_count=len(at_risk),
        dropout_warning_count=len(dropout_warnings),
        avg_review_completion=round(max(0, 1.0 - avg_inactive / 7), 3),  # approximation
        avg_accuracy=0.0,  # requires correct/incorrect data
        at_risk_learners=at_risk[:20],
        dropout_warnings=dropout_warnings[:20],
        instructor_recommendations=recommendations,
        generated_at=date.today().isoformat(),
    )


@router.get("/cohorts")
async def list_cohorts(repo=Depends(get_repo)):
    """List all institution cohorts."""
    import json
    cohort_dir = repo.memory_root / "institution" / "cohorts"
    if not cohort_dir.exists():
        return {"cohorts": []}

    cohorts = []
    for path in sorted(cohort_dir.glob("*.json")):
        cohorts.append(json.loads(path.read_text(encoding="utf-8")))

    return {"count": len(cohorts), "cohorts": cohorts}
