from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from app.models import MistakeCard, MistakeEvent, PatternInsight, StrategyRule, ValidationRule, stable_id
from app.storage import Repository


FIX_RULES = {
    "concept_confusion": "先写出考点定义，再用一句话说明为什么正确选项成立。",
    "formula_misuse": "先画结构或时间轴，再代入公式或计算器。",
    "time_misallocation": "把整场拆成前中后三段，每段设置剩余时间警戒线。",
    "hallucinated_rule": "所有规则性结论都要回到 CFA/IFRS/GAAP 原始约束重新核对。",
    "missed_root_cause": "先列现象，再单独写 root cause，不允许只总结表层现象。",
}

FORMULA_DENSE_SUBJECTS = {
    "Alternative Investments",
    "Alternative_Investments",
    "Corporate Issuers",
    "Corporate_Issuers",
    "Derivatives",
    "Economics",
    "Equity",
    "Equity Investments",
    "Financial Reporting and Analysis",
    "Financial Statement Analysis",
    "Financial_Statement_Analysis",
    "Fixed Income",
    "Fixed_Income",
    "Portfolio Management",
    "Portfolio_Management",
    "Quantitative Methods",
    "Quantitative_Methods",
}

CONCEPT_FIRST_SUBJECTS = {
    "Ethical and Professional Standards",
    "Ethical_and_Professional_Standards",
}

MOCK_BUCKETS = {
    "Alternative Investments": "AltInv",
    "Alternative_Investments": "AltInv",
    "Corporate Issuers": "CorpIss",
    "Corporate_Issuers": "CorpIss",
    "Derivatives": "Derivatives",
    "Economics": "Economics",
    "Equity": "Equity",
    "Equity Investments": "Equity",
    "Ethical and Professional Standards": "Ethics",
    "Ethical_and_Professional_Standards": "Ethics",
    "Financial Statement Analysis": "FRA",
    "Financial Reporting and Analysis": "FRA",
    "Financial_Statement_Analysis": "FRA",
    "Fixed Income": "FI",
    "Fixed_Income": "FI",
    "Portfolio Management": "Portfolio",
    "Portfolio_Management": "Portfolio",
    "Quantitative Methods": "Quant",
    "Quantitative_Methods": "Quant",
}


def default_fix_rule(error_type: str) -> str:
    return FIX_RULES.get(error_type, "把错误转成一句可重复执行的纠偏规则。")


def next_drill_for(event: MistakeEvent) -> str:
    if event.source_layer == "question":
        return f"24 小时内重做 2 道 {event.topic} / {event.los} 同类题。"
    if event.source_layer == "bias":
        return f"下次学习 {event.topic} 前先口述纠偏规则，再开始做题。"
    return f"下次 agent 复盘前执行一轮 {event.error_type} 校验清单。"


def target_domain(source_layer: str) -> str:
    return {
        "question": "question-errors",
        "bias": "cognitive-bias",
        "agent": "agent-failures",
    }[source_layer]


def build_validation_rule(event: MistakeEvent) -> ValidationRule:
    return ValidationRule(
        rule_id=stable_id("validation", event.event_id or "", event.error_type),
        trigger=f"当 agent 输出涉及 {event.topic} / {event.los} 的规则结论时",
        check_steps=[
            "列出 agent 给出的关键规则结论。",
            "逐条与教材或标准规则核对。",
            "如果结论无法被证据支持，改写为保守表述。",
        ],
        failure_message=event.correct_resolution,
    )


def classify_moc_gap_type(error_type: str) -> str:
    if error_type == "formula_misuse":
        return "formula"
    if error_type == "concept_confusion":
        return "knowledge_tree"
    return "exam_trap"


def resolve_moc_target_path(repo: Repository, moc_target: str) -> Path | None:
    if not moc_target:
        return None
    path = Path(moc_target)
    if not path.is_absolute():
        path = repo.root / path
    return path


def read_moc_text(repo: Repository, moc_target: str) -> str:
    path = resolve_moc_target_path(repo, moc_target)
    if not path or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def subject_supports_formula_nodes(event: MistakeEvent) -> bool:
    if event.topic in CONCEPT_FIRST_SUBJECTS:
        return False
    if event.topic in FORMULA_DENSE_SUBJECTS:
        return True
    return "Alternative_Investments" in (event.moc_target or "")


def classify_gap_target(event: MistakeEvent, moc_text: str) -> str:
    if event.error_type == "concept_confusion":
        return "knowledge_tree_concept"
    if event.error_type != "formula_misuse":
        return "exam_trap"
    if not subject_supports_formula_nodes(event):
        return "knowledge_tree_concept"

    has_core_formula_section = "核心公式" in moc_text
    has_node_mapping_column = "知识树节点" in moc_text

    if not has_core_formula_section and not has_node_mapping_column:
        return "both"
    if not has_core_formula_section:
        return "knowledge_tree_core_formula"
    return "formula_table_variant"


def gap_type_for_target(gap_target: str) -> str:
    if gap_target in {"knowledge_tree_concept", "knowledge_tree_core_formula"}:
        return "knowledge_tree"
    if gap_target == "exam_trap":
        return "exam_trap"
    return "formula"


def mock_bucket_for_event(event: MistakeEvent) -> str | None:
    if event.moc_target:
        parts = Path(event.moc_target).parts
        if len(parts) >= 2:
            subject_dir = parts[-2]
            if subject_dir in MOCK_BUCKETS:
                return MOCK_BUCKETS[subject_dir]
    return MOCK_BUCKETS.get(event.topic)


def build_strategy_rule(events: list[MistakeEvent]) -> StrategyRule:
    weak_topics = Counter(event.topic for event in events if event.source_layer == "question")
    topic = weak_topics.most_common(1)[0][0] if weak_topics else "General Review"
    return StrategyRule(
        rule_id="pre-mock-brief",
        trigger="考前 24 小时或下一次 mock 开始前",
        decision=f"优先回看 {topic} 的错题卡，再做 5 题定向热身。",
        why_it_works="先用高频失误考点热启动，能把短期记忆和答题策略一起拉回工作状态。",
    )


def record_event(repo: Repository, payload: dict, mode: str) -> MistakeEvent:
    event = MistakeEvent.from_payload(payload)
    expected = {"record-mistake": "question", "review-session": "bias", "audit-agent": "agent"}[mode]
    event.source_layer = expected
    repo.append_event(event)

    card = MistakeCard.from_event(event, default_fix_rule(event.error_type), next_drill_for(event))
    domain = target_domain(event.source_layer)
    repo.save_card(domain, card, event.event_id or "")

    if event.source_layer == "agent":
        repo.save_validation_rule(build_validation_rule(event), event.event_id or "")

    return event


def mine_patterns(repo: Repository) -> list[PatternInsight]:
    events = repo.load_events()
    buckets: dict[str, list[MistakeEvent]] = defaultdict(list)
    for event in events:
        if event.source_layer != "question":
            continue
        key = f"{event.topic}::{event.los}::{event.error_type}"
        buckets[key].append(event)

    insights: list[PatternInsight] = []
    for key, grouped in buckets.items():
        if len(grouped) < 3:
            continue
        insight = PatternInsight(
            pattern_id=stable_id("pattern", key),
            pattern_key=key,
            recurrence=len(grouped),
            severity="high" if len(grouped) >= 4 else "medium",
            affected_topics=sorted({event.topic for event in grouped}),
            recommended_intervention=f"连续 3 次以上出错，安排 {grouped[0].topic} 的 LOS 定向复盘和 5 题短练。",
        )
        repo.save_pattern(insight)
        insights.append(insight)
    return insights


def moc_gap_review(repo: Repository) -> Path | None:
    events = repo.load_events()
    buckets: dict[str, list[MistakeEvent]] = defaultdict(list)
    for event in events:
        if event.source_layer != "question":
            continue
        if not event.moc_target:
            continue
        key = f"{event.topic}::{event.los}::{event.error_type}::{event.moc_target}"
        buckets[key].append(event)

    recommendations: list[tuple[list[MistakeEvent], str, str]] = []
    for grouped in buckets.values():
        if len(grouped) < 3:
            continue
        sample = grouped[0]
        gap_target = classify_gap_target(sample, read_moc_text(repo, sample.moc_target))
        recommendations.append((grouped, gap_type_for_target(gap_target), gap_target))

    if not recommendations:
        return None

    lines = [
        "---",
        f"generated_at: {repo.load_events()[-1].created_at if events else ''}",
        f"recommendation_count: {len(recommendations)}",
        "---",
        "",
        "# MOC Gap Review",
    ]
    for grouped, gap_type, gap_target in sorted(
        recommendations,
        key=lambda item: (-len(item[0]), item[0][0].topic, item[0][0].los, item[2]),
    ):
        sample = grouped[0]
        evidence_refs = sorted({ref for event in grouped for ref in event.evidence_refs})
        event_ids = [event.event_id for event in grouped if event.event_id]
        lines.extend(
            [
                "",
                f"## {sample.topic} | {sample.los} | {sample.error_type}",
                f"moc_target: {sample.moc_target}",
                f"recurrence: {len(grouped)}",
                f"suggested_gap_type: {gap_type}",
                f"gap_target: {gap_target}",
                f"reason: Repeated {sample.error_type} errors suggest the MOC may need a stronger {gap_target} treatment for this LOS.",
                f"event_ids: {', '.join(event_ids)}",
                f"evidence_refs: {', '.join(evidence_refs)}",
            ]
        )

    path = repo.memory_root / "strategy" / "moc-gap-review.md"
    repo.write_markdown(path, "\n".join(lines), "moc_gap_review", "moc-gap-review")
    return path


def export_mock_pages(repo: Repository) -> None:
    events = [event for event in repo.load_events() if event.source_layer == "question"]
    grouped: dict[str, list[MistakeEvent]] = defaultdict(list)
    for event in events:
        bucket = mock_bucket_for_event(event)
        if bucket:
            grouped[bucket].append(event)

    for bucket, bucket_events in grouped.items():
        lines = [
            "---",
            f"bucket: {bucket}",
            f"question_count: {len(bucket_events)}",
            "---",
            "",
            f"# {bucket} Mock Mistakes",
        ]
        for event in bucket_events:
            evidence_assets = ", ".join(event.evidence_assets) if event.evidence_assets else ""
            lines.extend(
                [
                    "",
                    f"## {event.topic} | {event.los}",
                    f"- error_type: {event.error_type}",
                    f"- question_source: {event.question_source or 'unknown'}",
                    f"- source_type: {event.source_type or 'unknown'}",
                    f"- wrong_choice_or_output: {event.wrong_choice_or_output}",
                    f"- correct_resolution: {event.correct_resolution}",
                    f"- evidence_refs: {', '.join(event.evidence_refs)}",
                    f"- evidence_assets: {evidence_assets}",
                    f"- moc_target: {event.moc_target}",
                ]
            )
        path = repo.vault_root / "mock" / bucket / f"00-{bucket}-Mistakes.md"
        repo.write_markdown(path, "\n".join(lines), "mock_projection", f"mock-{bucket}-mistakes")


def export_obsidian(repo: Repository) -> None:
    events = repo.load_events()
    question_events = [event for event in events if event.source_layer == "question"]
    bias_events = [event for event in events if event.source_layer == "bias"]
    agent_events = [event for event in events if event.source_layer == "agent"]

    repo.write_obsidian_page(
        "今日新增错题.md",
        [
            "# 今日新增错题",
            *[
                f"- {event.topic} | {event.los} | {event.error_type} | {event.correct_resolution}"
                for event in question_events
            ],
        ],
    )

    error_counts = Counter(event.error_type for event in events)
    repo.write_obsidian_page(
        "高频错因榜.md",
        [
            "# 高频错因榜",
            *[f"- {error_type}: {count}" for error_type, count in error_counts.most_common()],
        ],
    )

    topic_counts = Counter(event.topic for event in question_events)
    repo.write_obsidian_page(
        "Topic弱点页.md",
        [
            "# Topic 弱点页",
            *[f"- {topic}: {count}" for topic, count in topic_counts.most_common()],
        ],
    )

    repo.write_obsidian_page(
        "Agent失误页.md",
        [
            "# Agent 失误页",
            *[
                f"- {event.topic} | {event.error_type} | {event.correct_resolution}"
                for event in agent_events
            ],
        ],
    )

    repo.write_obsidian_page(
        "策略手册页.md",
        [
            "# 策略手册页",
            f"- 题目错题数: {len(question_events)}",
            f"- 认知偏差数: {len(bias_events)}",
            f"- Agent 失误数: {len(agent_events)}",
        ],
    )


def refresh_learning_outputs(repo: Repository) -> None:
    export_obsidian(repo)
    export_mock_pages(repo)


def pre_mock_brief(repo: Repository) -> StrategyRule:
    events = repo.load_events()
    mine_patterns(repo)
    rule = build_strategy_rule(events)
    repo.save_strategy_rule(rule)
    moc_gap_review(repo)
    refresh_learning_outputs(repo)
    return rule


def post_mock_retro(repo: Repository, session_id: str) -> Path:
    events = [
        event
        for event in repo.load_events()
        if session_id in event.evidence_refs
    ]
    grouped = defaultdict(list)
    for event in events:
        grouped[event.source_layer].append(event)

    lines = [
        "---",
        f"session_id: {session_id}",
        f"question_count: {len(grouped['question'])}",
        f"bias_count: {len(grouped['bias'])}",
        f"agent_count: {len(grouped['agent'])}",
        "---",
        "",
        "# Post Mock Retro",
    ]
    for source_layer, title in [("question", "Question Mistakes"), ("bias", "Bias Signals"), ("agent", "Agent Failures")]:
        lines.append("")
        lines.append(f"## {title}")
        for event in grouped[source_layer]:
            lines.append(
                f"- {event.topic} | {event.los} | {event.error_type} | {event.correct_resolution}"
            )

    path = repo.memory_root / "strategy" / f"{session_id}-retro.md"
    repo.write_markdown(path, "\n".join(lines), "mock_retro", f"{session_id}-retro")
    refresh_learning_outputs(repo)
    return path


def load_payload(raw: str) -> dict:
    return json.loads(raw)
