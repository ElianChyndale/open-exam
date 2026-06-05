"""POST /api/mock/{session_id}/retro — Mock exam session management."""

from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Depends, HTTPException

from deps import get_repo
from schemas import MockRetroResponse, MockSessionCreate

router = APIRouter()


def _recent_mock_focus(repo) -> tuple[list[str], list[str]]:
    wrong_events = [
        event for event in repo.load_events()
        if event.source_layer == "question" and not event.is_correct
    ]
    if not wrong_events:
        return [], []
    recent = sorted(wrong_events, key=lambda item: item.created_at, reverse=True)[:30]
    topic_counts = Counter(event.topic for event in recent if event.topic)
    error_counts = Counter(event.error_type for event in recent if event.error_type)
    return [topic for topic, _ in topic_counts.most_common(3)], [error for error, _ in error_counts.most_common(3)]


@router.post("/create")
async def create_mock_session(req: MockSessionCreate, repo=Depends(get_repo)):
    """Create a new mock exam session record."""
    from datetime import datetime, UTC
    from app.exam_profile import get_profile

    session_data = {
        "session_id": req.session_id,
        "exam_name": req.exam_name or get_profile(repo.root).name,
        "session_label": req.session_label,
        "scheduled_date": req.scheduled_date,
        "total_minutes": req.total_minutes,
        "total_questions": req.total_questions,
        "correct_count": req.correct_count,
        "created_at": datetime.now(UTC).isoformat(),
    }

    import json
    mock_dir = repo.memory_root / "mock_sessions"
    mock_dir.mkdir(parents=True, exist_ok=True)
    session_path = mock_dir / f"{req.session_id}.json"
    session_path.write_text(json.dumps(session_data, ensure_ascii=False, indent=2))

    return {"status": "created", "session_id": req.session_id}


@router.post("/{session_id}/retro", response_model=MockRetroResponse)
async def post_mock_retro(session_id: str, repo=Depends(get_repo)):
    """Generate a post-mock retro analysis.

    Aggregates all events tagged with this session_id and produces:
    - Mistake breakdown by topic/LOS/error_type
    - Bias signal summary
    - Agent failure summary
    - Stop-doing list and next-mock strategy
    """
    from app.workflows import post_mock_retro

    try:
        result_path = post_mock_retro(repo, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    content = result_path.read_text(encoding="utf-8") if result_path.exists() else ""

    # Count events by source layer
    events = [e for e in repo.load_events() if session_id in e.evidence_refs]
    q_count = sum(1 for e in events if e.source_layer == "question")
    b_count = sum(1 for e in events if e.source_layer == "bias")
    a_count = sum(1 for e in events if e.source_layer == "agent")

    # Generate stop-doing and next-strategy
    error_counts = Counter(e.error_type for e in events if e.source_layer == "question")
    focus_topics, focus_error_types = _recent_mock_focus(repo)
    stop_doing = []
    if error_counts.get("careless_reading", 0) >= 3:
        stop_doing.append("别再快速扫题——每题先读最后一句（问什么）再回头看数据。")
    if error_counts.get("formula_misuse", 0) >= 3:
        stop_doing.append("别在不写公式的情况下直接代入计算器——先写出公式再按键。")
    if error_counts.get("time_pressure", 0) >= 1:
        stop_doing.append("别再在前半场过度停留——每 10 题检查一次时间。")
    if b_count > 0:
        stop_doing.append(f"识别到 {b_count} 个可能的认知偏差，下次 mock 前先读纠偏规则。")

    if focus_topics:
        next_strategy = f"下次 mock 前 24 小时：1) 优先复习 {', '.join(focus_topics[:2])} 的高频错题卡 2) 做 10 题定向热身 3) 读 pre-mock brief。"
    else:
        next_strategy = "下次 mock 前 24 小时：1) 复习高频错题卡 2) 做 10 题定向热身 3) 读 pre-mock brief。"

    return MockRetroResponse(
        session_id=session_id,
        question_count=q_count,
        bias_count=b_count,
        agent_count=a_count,
        markdown_content=content,
        stop_doing=stop_doing,
        next_strategy=next_strategy,
    )


@router.get("/{session_id}/brief")
async def get_pre_mock_brief(session_id: str, repo=Depends(get_repo)):
    """Get or generate a pre-mock brief."""
    from app.workflows import pre_mock_brief

    rule = pre_mock_brief(repo)
    focus_topics, focus_error_types = _recent_mock_focus(repo)
    decision = rule.decision
    if focus_topics:
        decision = f"{rule.decision} 本次 mock 前优先关注: {', '.join(focus_topics[:3])}。"
    why_it_works = rule.why_it_works
    if focus_error_types:
        why_it_works = f"{rule.why_it_works} 最近高频错因: {', '.join(focus_error_types[:3])}。"
    return {
        "session_id": session_id,
        "trigger": rule.trigger,
        "decision": decision,
        "why_it_works": why_it_works,
        "focus_topics": focus_topics,
        "focus_error_types": focus_error_types,
    }


@router.get("/history")
async def list_mock_sessions(repo=Depends(get_repo)):
    """List all mock session records."""
    import json
    mock_dir = repo.memory_root / "mock_sessions"
    if not mock_dir.exists():
        return {"sessions": []}

    sessions = []
    for path in sorted(mock_dir.glob("*.json")):
        sessions.append(json.loads(path.read_text(encoding="utf-8")))

    return {"count": len(sessions), "sessions": sessions}
