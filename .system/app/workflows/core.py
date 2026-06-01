from __future__ import annotations

import json
import re
from copy import deepcopy
from collections import Counter, defaultdict
from dataclasses import fields
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from app.models import MistakeCard, MistakeEvent, PatternInsight, StrategyRule, ValidationRule, stable_id
from app.storage import Repository


FIX_RULES = {
    "concept_confusion": "先写出考点定义，再用一句话说明为什么正确选项成立。",
    "formula_misuse": "先画结构或时间轴，再代入公式或计算器。",
    "time_misallocation": "把整场拆成前中后三段，每段设置剩余时间警戒线。",
    "hallucinated_rule": "所有规则性结论都要回到 CFA/IFRS/GAAP 原始约束重新核对。",
    "missed_root_cause": "先列现象，再单独写 root cause，不允许只总结表层现象。",
    "constructed_response_weak_structure": "Essay 先按题干动词搭框架：identify/list 先列对象，discuss 每一点必须补 relationship type、incentive/conflict 或 financial impact。",
    "constraint_miss": "表格题先圈出 governing criterion / hurdle / constraint，再比较 NPV、IRR 或 ROIC；不能只看最显眼的正 NPV。",
    "table_overload_constraint_miss": "图表信息过载时先做 10 秒门槛扫描：minimum、target、required、criterion、constraint、hurdle，再读项目数据。",
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

DAILY_REVIEW_TASK = "完成 Daily Review"
DAILY_REVIEW_TASK_ALIASES = {DAILY_REVIEW_TASK, "完成今日复习资料", "完成每日复习资料"}
DAILY_REVIEW_DEADLINE = "20:00"

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

CARD_DOMAINS = {
    "question-errors": "question",
    "cognitive-bias": "bias",
    "agent-failures": "agent",
}

REVIEW_SOURCE_WEIGHTS = {
    "question": 8,
    "bias": 6,
    "agent": 5,
}

SUBJECT_MOC_PATHS = {
    "Alternative Investments": "CFA_tier1/Alternative_Investments/00-Alternative-Investments-MOC.md",
    "Corporate Issuers": "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
    "Derivatives": "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    "Economics": "CFA_tier1/Economics/00-Economics-MOC.md",
    "Equity": "CFA_tier1/Equity/00-Equity-MOC.md",
    "Ethical and Professional Standards": "CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md",
    "Financial Statement Analysis": "CFA_tier1/Financial_Statement_Analysis/00-Financial-Statement-Analysis-MOC.md",
    "Fixed Income": "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    "Portfolio Management": "CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md",
    "Quantitative Methods": "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md",
}

SUBJECT_ALIASES = {
    "alternative investments": "Alternative Investments",
    "alternative_investments": "Alternative Investments",
    "altinv": "Alternative Investments",
    "corporate issuers": "Corporate Issuers",
    "corporate_issuers": "Corporate Issuers",
    "corpiss": "Corporate Issuers",
    "economics": "Economics",
    "eco": "Economics",
    "quantitative methods": "Quantitative Methods",
    "quantitative_methods": "Quantitative Methods",
    "quant": "Quantitative Methods",
    "fixed income": "Fixed Income",
    "fixed_income": "Fixed Income",
    "fi": "Fixed Income",
    "financial statement analysis": "Financial Statement Analysis",
    "financial_statement_analysis": "Financial Statement Analysis",
    "financial reporting and analysis": "Financial Statement Analysis",
    "fra": "Financial Statement Analysis",
    "portfolio management": "Portfolio Management",
    "portfolio_management": "Portfolio Management",
    "derivatives": "Derivatives",
    "equity": "Equity",
    "equity investments": "Equity",
    "ethical and professional standards": "Ethical and Professional Standards",
    "ethical_and_professional_standards": "Ethical and Professional Standards",
    "ethics": "Ethical and Professional Standards",
}

STOPWORDS = {
    "and",
    "the",
    "with",
    "from",
    "into",
    "under",
    "when",
    "using",
    "based",
    "most",
    "likely",
    "question",
    "screenshot",
    "approx",
    "approximate",
    "exact",
    "shown",
    "does",
    "doesn",
    "level",
    "method",
    "methods",
    "test",
    "tests",
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
    from datetime import date, timedelta

    return ValidationRule(
        rule_id=stable_id("validation", event.event_id or "", event.error_type),
        trigger=f"当 agent 输出涉及 {event.topic} / {event.los} 的规则结论时",
        check_steps=[
            "列出 agent 给出的关键规则结论。",
            "逐条与教材或标准规则核对。",
            "如果结论无法被证据支持，改写为保守表述。",
        ],
        failure_message=event.correct_resolution,
        expiry_date=(date.today() + timedelta(days=90)).isoformat(),
        review_status="active",
        last_reviewed_at=datetime.now(timezone.utc).isoformat(),
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


def mock_bucket_for_event(repo: Repository, event: MistakeEvent) -> str | None:
    from app.exam_profile import get_profile

    profile = get_profile(repo.root)
    if event.moc_target:
        parts = Path(event.moc_target).parts
        if len(parts) >= 2:
            subject_dir = parts[-2]
            bucket = profile.mock_bucket_for(subject_dir)
            if bucket:
                return bucket
            if subject_dir in MOCK_BUCKETS:
                return MOCK_BUCKETS[subject_dir]
    return profile.mock_bucket_for(event.topic) or MOCK_BUCKETS.get(event.topic)


def parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def parse_datetime_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = clean_scalar(value)
    return data


def clean_scalar(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        return cleaned[1:-1]
    return cleaned


def extract_markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return ""
    content_start = start + len(marker)
    next_heading = text.find("\n## ", content_start)
    if next_heading == -1:
        return text[content_start:].strip()
    return text[content_start:next_heading].strip()


def add_review_item(items: dict[str, dict], key: str, candidate: dict) -> None:
    if key not in items:
        stored = deepcopy(candidate)
        stored["reasons"] = list(stored.get("reasons", []))
        items[key] = stored
        return

    current = items[key]
    current["priority"] = max(current.get("priority", 0), candidate.get("priority", 0))
    for reason in candidate.get("reasons", []):
        if reason not in current["reasons"]:
            current["reasons"].append(reason)
    for field in ("next_drill", "fix_rule", "correct_resolution", "evidence_refs", "prompt", "wrong_output"):
        if not current.get(field) and candidate.get(field):
            current[field] = candidate[field]
    for field in ("card_ids",):
        current.setdefault(field, [])
        for value in candidate.get(field, []):
            if value not in current[field]:
                current[field].append(value)
    current["recurrence"] = max(int(current.get("recurrence", 0) or 0), int(candidate.get("recurrence", 0) or 0))


def collect_due_card_items(repo: Repository, review_date: date) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for domain, source_layer in CARD_DOMAINS.items():
        for path in (repo.memory_root / domain).glob("*.md"):
            text = path.read_text(encoding="utf-8")
            frontmatter = parse_frontmatter(text)
            due_at = parse_date(frontmatter.get("review_due_at", ""))
            if not due_at or due_at > review_date:
                continue

            topic = frontmatter.get("topic", "Unknown Topic")
            los = frontmatter.get("los", "Unknown LOS")
            root_cause = frontmatter.get("root_cause", "unknown")
            days_overdue = max((review_date - due_at).days, 0)
            raw_priority = frontmatter.get("spacing_priority", "50")
            scheduler_priority = int(raw_priority) if str(raw_priority).strip() else 50
            key = f"{source_layer}::{topic}::{los}::{root_cause}"
            evidence = extract_markdown_section(text, "Evidence")
            add_review_item(
                items,
                key,
                {
                    "source_layer": source_layer,
                    "topic": topic,
                    "los": los,
                    "error_type": root_cause,
                    "priority": scheduler_priority + days_overdue * 2 + REVIEW_SOURCE_WEIGHTS.get(source_layer, 0),
                    "reasons": [f"review_due_at: {due_at.isoformat()}"],
                    "prompt": extract_markdown_section(text, "Prompt"),
                    "wrong_output": extract_markdown_section(text, "Wrong Output"),
                    "correct_resolution": frontmatter.get("correct_resolution", ""),
                    "question_format": frontmatter.get("question_format", ""),
                    "choices": normalize_choices(extract_markdown_section(text, "Choices")),
                    "fix_rule": frontmatter.get("fix_rule", ""),
                    "next_drill": frontmatter.get("next_drill", ""),
                    "evidence_refs": evidence,
                    "card_ids": [frontmatter.get("card_id", path.stem)],
                },
            )
    return items


def collect_recent_low_confidence_items(
    repo: Repository,
    review_date: date,
    days_back: int,
    events: list[MistakeEvent] | None = None,
) -> dict[str, dict]:
    cutoff = review_date - timedelta(days=days_back)
    items: dict[str, dict] = {}
    for event in events if events is not None else repo.load_events():
        if event.source_layer == "question" and event.is_correct:
            continue
        event_date = parse_datetime_date(event.created_at)
        if not event_date or event_date < cutoff or event_date > review_date:
            continue
        if event.confidence > 2 and event.source_layer == "question":
            continue

        key = f"{event.source_layer}::{event.topic}::{event.los}::{event.error_type}"
        priority = 60 + REVIEW_SOURCE_WEIGHTS.get(event.source_layer, 0)
        if event.confidence <= 1:
            priority += 15
        add_review_item(
            items,
            key,
            {
                "source_layer": event.source_layer,
                "topic": event.topic,
                "los": event.los,
                "error_type": event.error_type,
                "priority": priority,
                "reasons": [f"recent_low_confidence: {event.created_at[:10]}"],
                "prompt": event.prompt_or_question,
                "wrong_output": event.wrong_choice_or_output,
                "correct_resolution": event.correct_resolution,
                "question_format": event.question_format,
                "choices": event.choices,
                "fix_rule": default_fix_rule(event.error_type),
                "next_drill": next_drill_for(event),
                "evidence_refs": ", ".join(event.evidence_refs),
                "card_ids": [stable_id("card", event.event_id or "", event.topic, event.los)]
                if event.source_layer == "question"
                else [],
            },
        )
    return items


def collect_pattern_items(repo: Repository) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for path in (repo.memory_root / "patterns").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        pattern_key = frontmatter.get("pattern_key", "")
        parts = pattern_key.split("::")
        if len(parts) != 3:
            continue
        topic, los, error_type = parts
        recurrence = int(frontmatter.get("recurrence", "0") or 0)
        severity = frontmatter.get("severity", "medium")
        priority = 85 + recurrence * 3 + (10 if severity == "high" else 0)
        key = f"question::{topic}::{los}::{error_type}"
        add_review_item(
            items,
            key,
            {
                "source_layer": "question",
                "topic": topic,
                "los": los,
                "error_type": error_type,
                "priority": priority,
                "reasons": [f"pattern_recurrence: {recurrence}", f"severity: {severity}"],
                "prompt": "先闭卷说出这个 LOS 最容易错的判断边界，再看原错题。",
                "wrong_output": "",
                "correct_resolution": extract_markdown_section(text, "Recommended Intervention"),
                "fix_rule": default_fix_rule(error_type),
                "next_drill": extract_markdown_section(text, "Recommended Intervention"),
                "evidence_refs": frontmatter.get("pattern_id", ""),
                "recurrence": recurrence,
            },
        )
    return items


def merge_review_sources(*sources: dict[str, dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for source in sources:
        for key, item in source.items():
            add_review_item(merged, key, item)
    return sorted(
        merged.values(),
        key=lambda item: (-item.get("priority", 0), item.get("topic", ""), item.get("los", "")),
    )


def interleave_review_items(review_items: list[dict], max_items: int) -> tuple[list[dict], dict[str, int]]:
    """Mix review sources when the cache contains more than one practice bucket."""
    from study_science.interleaving import InterleavingBuilder, InterleavingConfig

    candidates = [deepcopy(item) for item in review_items]
    weak_items = [item for item in candidates if item.get("priority", 0) >= 85]
    old_items = [
        item
        for item in candidates
        if item not in weak_items and any("review_due_at:" in reason for reason in item.get("reasons", []))
    ]
    maintenance_items = [
        item
        for item in candidates
        if item not in weak_items and item not in old_items
    ]
    mix = InterleavingBuilder.build(
        weak_items=weak_items,
        old_mistake_items=old_items,
        maintenance_items=maintenance_items,
        config=InterleavingConfig(max_items=max_items),
    )

    selected = list(mix.items)
    selected_keys = {
        (item.get("source_layer", ""), item.get("topic", ""), item.get("los", ""), item.get("error_type", ""))
        for item in selected
    }
    for item in candidates:
        key = (item.get("source_layer", ""), item.get("topic", ""), item.get("los", ""), item.get("error_type", ""))
        if key not in selected_keys:
            selected.append(item)
            selected_keys.add(key)
        if len(selected) >= max_items:
            break
    return selected[:max_items], mix.composition


def normalize_subject(value: str) -> str:
    normalized = value.replace("_", " ").strip().lower()
    if normalized in SUBJECT_ALIASES:
        return SUBJECT_ALIASES[normalized]
    for alias, subject in SUBJECT_ALIASES.items():
        if alias in normalized:
            return subject
    for subject in SUBJECT_MOC_PATHS:
        if subject.lower() in normalized:
            return subject
    return value.strip()


def subject_moc_path(repo: Repository, subject: str) -> Path | None:
    from app.exam_profile import get_profile

    profile = get_profile(repo.root)
    normalized = profile.normalize_subject(subject)
    relative = profile.moc_path_for(normalized) or SUBJECT_MOC_PATHS.get(normalize_subject(subject))
    if not relative:
        return None
    path = repo.root / relative
    return path if path.exists() else None


def extract_numbered_section(text: str, section_prefix: str) -> str:
    lines = text.splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.startswith(section_prefix):
            start_index = index
            break
    if start_index is None:
        return ""

    collected: list[str] = []
    for line in lines[start_index + 1 :]:
        if line.startswith("## ") and not line.startswith(section_prefix):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def parse_moc_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or "---" in stripped:
        return None
    parts = [part.strip() for part in stripped.strip("|").split("|")]
    if len(parts) < 3:
        return None
    first = parts[0].lower()
    last = parts[-1].lower()
    if first in {
        "trigger",
        "tool",
        "metric",
        "indicator",
        "formula",
        "framework",
        "project type",
        "real option type",
    }:
        return None
    if last in {"exam use", "exam action", "exam decision", "decision", "说明", "应用场景"}:
        return None
    if len(parts) == 3:
        return parts
    return [parts[0], " | ".join(parts[1:-1]), parts[-1]]


def extract_moc_atoms(repo: Repository, subject: str) -> list[dict]:
    path = subject_moc_path(repo, subject)
    if not path:
        return []

    text = path.read_text(encoding="utf-8")
    section = extract_numbered_section(text, "## 2.")
    if not section:
        return []

    atoms: list[dict] = []
    current_heading = "Formula & Framework Map"
    for line in section.splitlines():
        if line.startswith("### "):
            current_heading = line.removeprefix("### ").strip()
            continue
        cells = parse_moc_table_row(line)
        if cells:
            atoms.append(
                {
                    "subject": normalize_subject(subject),
                    "heading": current_heading,
                    "trigger": cells[0],
                    "formula": cells[1],
                    "decision": cells[2],
                    "source": path.relative_to(repo.root).as_posix(),
                    "text": " | ".join(cells),
                }
            )
    return atoms


def subject_module_paths(repo: Repository, subject: str) -> list[Path]:
    from app.exam_profile import get_profile

    profile = get_profile(repo.root)
    normalized = profile.normalize_subject(subject)
    relative = profile.moc_path_for(normalized) or SUBJECT_MOC_PATHS.get(normalize_subject(subject))
    if not relative:
        return []
    subject_dir = (repo.root / relative).parent
    if not subject_dir.exists():
        return []
    return sorted(path for path in subject_dir.glob("M*.md") if path.is_file())


def extract_expanded_module_atoms(repo: Repository, subject: str) -> list[dict]:
    atoms: list[dict] = []
    for path in subject_module_paths(repo, subject):
        text = path.read_text(encoding="utf-8")
        current_heading = path.stem
        include_heading = False
        for line in text.splitlines():
            if line.startswith("### ") or line.startswith("## "):
                current_heading = line.lstrip("#").strip()
                lowered = current_heading.lower()
                include_heading = any(
                    token in lowered
                    for token in (
                        "classifier",
                        "formula",
                        "decision",
                        "trap",
                        "recall",
                    )
                )
                continue
            if not include_heading:
                continue
            cells = parse_moc_table_row(line)
            if cells:
                atoms.append(
                    {
                        "subject": normalize_subject(subject),
                        "heading": current_heading,
                        "trigger": cells[0],
                        "formula": cells[1],
                        "decision": cells[2],
                        "source": path.relative_to(repo.root).as_posix(),
                        "text": " | ".join(cells),
                        "reason": "expanded_module_note",
                        "priority": 75,
                    }
                )
                continue
            stripped = line.strip()
            if stripped.startswith("- "):
                content = stripped.removeprefix("- ").strip()
                if content:
                    atoms.append(
                        {
                            "subject": normalize_subject(subject),
                            "heading": current_heading,
                            "trigger": content.split(":", 1)[0].strip("`* ")[:80],
                            "formula": content,
                            "decision": "module note easy-miss boundary",
                            "source": path.relative_to(repo.root).as_posix(),
                            "text": content,
                            "reason": "expanded_module_note",
                            "priority": 65,
                        }
                    )
    return atoms


def build_expanded_warm_start_items(repo: Repository, review_items: list[dict], focus_topic: str, max_items: int = 40) -> list[dict]:
    focus_subject = normalize_subject(focus_topic) if focus_topic else ""
    if focus_subject:
        subjects = [focus_subject]
    else:
        subjects = []
        for item in review_items:
            subject = normalize_subject(item.get("topic", ""))
            if subject_moc_path(repo, subject) and subject not in subjects:
                subjects.append(subject)

    selected: dict[str, dict] = {}
    for subject in subjects:
        for atom in extract_expanded_module_atoms(repo, subject):
            score = atom.get("priority", 0)
            atom_text = f"{atom['heading']} {atom['text']}".lower()
            if subject == focus_subject:
                score += 15
            for item in review_items:
                if normalize_subject(item.get("topic", "")) != subject:
                    continue
                tokens = tokenize_for_matching(
                    item.get("los", ""),
                    item.get("prompt", ""),
                    item.get("correct_resolution", ""),
                    item.get("error_type", ""),
                )
                score += sum(4 for token in tokens if token in atom_text)
            key = f"{atom['subject']}::{atom['heading']}::{atom['trigger']}"
            selected[key] = {**atom, "priority": score}

    return sorted(
        selected.values(),
        key=lambda item: (-item.get("priority", 0), item.get("subject", ""), item.get("heading", "")),
    )[:max_items]


def merge_warm_start_items(*sources: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for source in sources:
        for item in source:
            key = f"{item.get('subject', '')}::{item.get('heading', '')}::{item.get('trigger', '')}"
            current = merged.get(key)
            if not current or item.get("priority", 0) > current.get("priority", 0):
                merged[key] = item
    return sorted(
        merged.values(),
        key=lambda item: (-item.get("priority", 0), item.get("subject", ""), item.get("heading", "")),
    )


def tokenize_for_matching(*values: str) -> set[str]:
    raw = " ".join(value or "" for value in values).lower()
    tokens = set(re.findall(r"[a-z][a-z0-9-]{2,}", raw))
    tokens.update(token.lower() for token in re.findall(r"\bM\d{2}\b", " ".join(values)))
    return {token for token in tokens if token not in STOPWORDS}


def score_atom(atom: dict, review_item: dict, focus_subject: str) -> int:
    subject = normalize_subject(review_item.get("topic", ""))
    score = 0
    if atom["subject"] == subject:
        score += 30
    if focus_subject and atom["subject"] == focus_subject:
        score += 10

    tokens = tokenize_for_matching(
        review_item.get("topic", ""),
        review_item.get("los", ""),
        review_item.get("prompt", ""),
        review_item.get("correct_resolution", ""),
        review_item.get("fix_rule", ""),
        review_item.get("error_type", ""),
    )
    atom_text = f"{atom['heading']} {atom['text']}".lower()
    score += sum(6 for token in tokens if token in atom_text)

    error_type = review_item.get("error_type", "")
    if error_type == "formula_misuse" and "`" in atom["formula"]:
        score += 12
    if error_type == "concept_confusion" and "`" not in atom["formula"]:
        score += 5
    return score


def build_warm_start_items(repo: Repository, review_items: list[dict], focus_topic: str, max_items: int = 64) -> list[dict]:
    focus_subject = normalize_subject(focus_topic) if focus_topic else ""
    subjects = []
    if focus_subject:
        subjects.append(focus_subject)
    for item in review_items:
        subject = normalize_subject(item.get("topic", ""))
        if subject_moc_path(repo, subject) and subject not in subjects:
            subjects.append(subject)

    atoms_by_subject = {subject: extract_moc_atoms(repo, subject) for subject in subjects}
    selected: dict[str, dict] = {}

    if focus_subject:
        for atom in atoms_by_subject.get(focus_subject, []):
            key = f"{atom['subject']}::{atom['heading']}::{atom['trigger']}"
            selected[key] = {
                **atom,
                "reason": f"today_focus: {focus_subject}",
                "priority": 80,
            }

    for item in review_items:
        subject = normalize_subject(item.get("topic", ""))
        candidates = atoms_by_subject.get(subject, [])
        ranked = sorted(candidates, key=lambda atom: score_atom(atom, item, focus_subject), reverse=True)
        for atom in ranked[:2]:
            atom_score = score_atom(atom, item, focus_subject)
            if atom_score < 30:
                continue
            key = f"{atom['subject']}::{atom['heading']}::{atom['trigger']}"
            reason = "; ".join(item.get("reasons", [])[:2]) or "review_queue"
            current = selected.get(key)
            if current:
                current["priority"] = max(current["priority"], atom_score)
                if reason not in current["reason"]:
                    current["reason"] = f"{current['reason']}; {reason}"
            else:
                selected[key] = {
                    **atom,
                    "reason": reason,
                    "priority": atom_score,
                }

    return sorted(
        selected.values(),
        key=lambda item: (-item.get("priority", 0), item.get("subject", ""), item.get("heading", "")),
    )[:max_items]


def normalize_question_text(text: str) -> str:
    cleaned = (text or "").strip()
    labels = [(match.group(1), match.start()) for match in re.finditer(r"\b([A-E])\.\s", cleaned)]
    positions = {label: position for label, position in labels}
    has_choice_sequence = (
        "A" in positions
        and (("B" in positions and positions["A"] < positions["B"]) or ("C" in positions and positions["A"] < positions["C"]))
    )
    if has_choice_sequence:
        cleaned = re.sub(r"\s+([A-E]\.\s)", r"\n\1", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def quote_block(text: str) -> list[str]:
    cleaned = clean_display_text(normalize_question_text(text))
    if not cleaned:
        return ["> _No text captured._"]
    return [">" if not line.strip() else f"> {line}" for line in cleaned.splitlines()]


def question_display_parts(item: dict) -> tuple[str, list[str], bool]:
    prompt = item.get("prompt") or "先闭卷说出定义、公式或判断边界。"
    explicit_choices = normalize_choices(item.get("choices", []))
    stem, parsed_choices = split_prompt_choices(prompt)
    choices = explicit_choices or parsed_choices
    question_format = infer_question_format(prompt, item.get("wrong_output", ""), choices, item.get("question_format", ""))
    options_missing = question_format == "multiple_choice" and not choices
    return stem or prompt, choices, options_missing


def clean_display_text(text: str) -> str:
    cleaned = re.sub(r"\s*[\ufffd]+\s*", " - ", text or "")
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def human_reason(reason: str) -> str:
    if reason.startswith("review_due_at:"):
        return f"到期复习 {reason.split(':', 1)[1].strip()}"
    if reason.startswith("recent_low_confidence:"):
        return f"近期低信心 {reason.split(':', 1)[1].strip()}"
    if reason.startswith("pattern_recurrence:"):
        return f"重复错误 {reason.split(':', 1)[1].strip()} 次"
    if reason.startswith("severity:"):
        return f"严重度 {reason.split(':', 1)[1].strip()}"
    if reason.startswith("today_focus:"):
        return f"今日主线 {reason.split(':', 1)[1].strip()}"
    return reason


def human_reasons(reasons: list[str]) -> str:
    readable = []
    for reason in reasons:
        text = human_reason(reason)
        if text and text not in readable:
            readable.append(text)
    return "；".join(readable) if readable else "今日复习队列"


def compact_list(values: list[str], limit: int = 5) -> str:
    cleaned = []
    for value in values:
        text = clean_display_text(value)
        if text and text not in cleaned:
            cleaned.append(text)
    if len(cleaned) <= limit:
        return "；".join(cleaned)
    shown = "；".join(cleaned[:limit])
    return f"{shown}；另有 {len(cleaned) - limit} 项"


def boundary_lines_for_group(items: list[dict], limit: int = 3) -> list[str]:
    cues = []
    patterns = (
        "not ",
        "not automatically",
        "unless",
        "but ",
        "can mislead",
        "ignores",
        "excludes",
        "不要",
        "不是",
        "不能",
        "先判",
        "先判断",
        "先定位",
        "only",
    )
    for item in items:
        decision = clean_display_text(item.get("decision", ""))
        if not decision:
            continue
        lowered = decision.lower()
        if any(pattern in lowered or pattern in decision for pattern in patterns):
            trigger = clean_display_text(item.get("trigger", ""))
            cue = f"{trigger}: {decision}" if trigger else decision
            if cue not in cues:
                cues.append(cue)
        if len(cues) >= limit:
            break
    return cues


def grouped_warm_start_items(warm_start_items: list[dict]) -> list[list[dict]]:
    groups: list[list[dict]] = []
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    order: list[tuple[str, str, str]] = []
    for item in warm_start_items:
        key = (item.get("subject", ""), item.get("heading", ""), item.get("source", ""))
        if key not in grouped:
            order.append(key)
        grouped[key].append(item)
    for key in order:
        groups.append(grouped[key])
    return groups


def render_warm_start(lines: list[str], warm_start_items: list[dict]) -> None:
    lines.append("## 一、知识点和公式")
    if not warm_start_items:
        lines.extend(
            [
                "",
                "今天没有从 MOC 中匹配到明确的知识点或公式。先直接做下面的错题复习。",
            ]
        )
        return

    for index, group in enumerate(grouped_warm_start_items(warm_start_items), start=1):
        first = group[0]
        reason_parts = [
            part.strip()
            for item in group
            for part in item.get("reason", "").split(";")
            if part.strip()
        ]
        triggers = [item.get("trigger", "") for item in group]
        boundaries = boundary_lines_for_group(group)
        # Knowledge memory state for the group (from first item that has one)
        decay_info = next((item for item in group if item.get("decay_risk")), None)
        memory_lines: list[str] = []
        if decay_info:
            risk_labels = {"overdue": "超期", "high": "高衰减风险", "medium": "中等衰减风险", "low": "微衰减风险", "none": "状态良好"}
            risk_label = risk_labels.get(decay_info.get("decay_risk", ""), "")
            if risk_label:
                kid_short = str(decay_info.get("knowledge_id", ""))[:24]
                memory_lines = [f"- **记忆状态：** {risk_label}（{kid_short}）", ""]
        lines.extend(
            [
                "",
                f"### {index}. {clean_display_text(first['subject'])} | {clean_display_text(first['heading'])}",
                f"- **先问自己：** 看到这些 trigger，能不能讲出定义、公式、适用条件和例外？{compact_list(triggers)}",
                f"- **今天为什么看：** {human_reasons(reason_parts)}",
                *memory_lines,
                "> [!answer]- Reveal knowledge point",
                "> #### 核心知识点 / 公式",
            ]
        )
        for item in group:
            lines.append(
                f"> - **{clean_display_text(item['trigger'])}:** {clean_display_text(item['formula'])} -> {clean_display_text(item['decision'])}"
            )
        if boundaries:
            lines.extend([">", "> #### 易错边界"])
            lines.extend(f"> - {boundary}" for boundary in boundaries)
        lines.extend([">", f"> **来源：** {first['source']}"])


def render_review_pack(
    review_items: list[dict],
    warm_start_items: list[dict],
    review_date: date,
    days_back: int,
    focus_topic: str,
    source_event_count: int,
    progress_events: list[dict] | None = None,
    energy_warnings: list[str] | None = None,
) -> str:
    from study_science.retrieval import RetrievalEngine
    from study_science.self_explanation import SelfExplanationPrompt
    from study_science.worked_example import WorkedExampleFader

    lines = [
        "---",
        f"generated_for: {review_date.isoformat()}",
        f"days_back: {days_back}",
        f"focus_topic: {focus_topic or 'unspecified'}",
        f"source_event_count: {source_event_count}",
        f"review_item_count: {len(review_items)}",
        "---",
        "",
        "# Daily Review",
        "",
    ]
    if energy_warnings:
        for w in energy_warnings:
            lines.extend(["", w])
        lines.append("")
    lines.extend(progress_summary_lines(progress_events or [], focus_topic))

    render_warm_start(lines, warm_start_items)
    lines.extend(
        [
            "",
            "## 二、错题",
        ]
    )

    if not review_items:
        lines.extend(
            [
                "",
                "今天没有到期错题。用第一部分做主动回忆即可：遮住答案，讲出定义、公式、适用条件和容易混淆的地方。",
            ]
        )
        return "\n".join(lines)

    for index, item in enumerate(review_items, start=1):
        reasons = human_reasons(item.get("reasons", []))
        prompt, choices, options_missing = question_display_parts(item)
        wrong_output = item.get("wrong_output") or "_No previous wrong output captured._"
        correct_resolution = item.get("correct_resolution") or "见原错题卡或模式卡。"
        retrieval_prompts = RetrievalEngine.build_prompts(
            topic=item.get("topic", ""),
            los=item.get("los", ""),
            error_type=item.get("error_type", ""),
            correct_resolution=correct_resolution,
            question_prompt=prompt,
            count=1,
        )
        self_explanation = SelfExplanationPrompt.generate(
            error_type=item.get("error_type", ""),
            topic=item.get("topic", ""),
            los=item.get("los", ""),
            correct_answer=correct_resolution,
            user_answer=wrong_output,
            question_stem=prompt,
        )
        use_fading = WorkedExampleFader.should_use_worked_examples(
            int(item.get("recurrence", 0) or 0),
            item.get("error_type", ""),
        )
        lines.extend(
            [
                "",
                f"### {index}. {clean_display_text(item['topic'])} | {clean_display_text(item['los'])} | {clean_display_text(item['error_type'])}",
                f"- **先遮答案想：** 这题真正考的 trigger 是什么？我上次为什么会错？",
                f"- **今天为什么看：** {reasons}",
                "",
                "#### 主动回忆",
                f"- {clean_display_text(retrieval_prompts[0].prompt_text) if retrieval_prompts else '闭卷讲出核心判断边界。'}",
                "",
                "#### 题目",
                *quote_block(prompt),
                "",
            ]
        )
        if choices:
            lines.extend(["#### 选项", *quote_block("\n".join(choices)), ""])
        elif options_missing:
            lines.extend(
                [
                    "#### 选项",
                    "> _options_missing: 原错题卡未捕获选项，请回到证据截图补全。_",
                    "",
                ]
            )
        lines.extend(
            [
                "#### 我上次错在",
                *quote_block(wrong_output),
                "",
                "#### 正确理解 / 解法",
                "> [!answer]- Reveal correct solution",
                *[
                    ">" if not line.strip() else f"> {line}"
                    for line in clean_display_text(normalize_question_text(correct_resolution)).splitlines()
                ],
                "",
                "#### 下次规则",
                f"- **纠偏规则：** {clean_display_text(item.get('fix_rule') or default_fix_rule(item['error_type']))}",
                f"- **下一步练习：** {clean_display_text(item.get('next_drill') or '做 2 道同类题并记录错因。')}",
                f"- **证据：** {clean_display_text(item.get('evidence_refs') or 'memory cache')}",
                "",
                "#### 自我解释",
                f"- {clean_display_text(self_explanation)}",
            ]
        )
        if use_fading:
            lines.extend(
                [
                    "",
                    "#### Worked example fading",
                    "- **当前阶段：** full solution -> hidden-step completion -> independent solve",
                    "- **动作：** 先复述完整解法，再遮住关键步骤完成一次，最后独立重做。",
                ]
            )

    return "\n".join(lines)


def build_strategy_rule(events: list[MistakeEvent]) -> StrategyRule:
    weak_topics = Counter(event.topic for event in events if event.source_layer == "question")
    topic = weak_topics.most_common(1)[0][0] if weak_topics else "General Review"
    return StrategyRule(
        rule_id="pre-mock-brief",
        trigger="考前 24 小时或下一次 mock 开始前",
        decision=f"优先回看 {topic} 的错题卡，再做 5 题定向热身。",
        why_it_works="先用高频失误考点热启动，能把短期记忆和答题策略一起拉回工作状态。",
    )


def load_exam_date(repo: Repository) -> str:
    path = repo.root / ".system" / "exam_date.txt"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()[:10]


def record_event(repo: Repository, payload: dict, mode: str) -> MistakeEvent:
    payload = dict(payload)
    if mode == "record-mistake":
        payload = hydrate_question_fields(payload)
    expected = {"record-mistake": "question", "review-session": "bias", "audit-agent": "agent"}[mode]
    for field_name in ("event_id", "event_type", "learner_id", "schema_version"):
        payload.pop(field_name, None)
    payload["source_layer"] = expected
    event = MistakeEvent.from_payload(payload)

    # Replay guard: skip if event_id already exists in the catalog index
    if repo.has_event(event.event_id):
        return event

    repo.append_event(event)

    if event.source_layer == "question" and event.is_correct:
        return event

    # Compute personalized calibration adjustment for dynamic expansion
    from study_science.spacing import SpacingScheduler
    cal_warnings = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
    cal_adjustment = SpacingScheduler.compute_calibration_adjustment(cal_warnings)

    card = MistakeCard.from_event(
        event,
        default_fix_rule(event.error_type),
        next_drill_for(event),
        exam_date=load_exam_date(repo),
        calibration_adjustment=cal_adjustment,
    )
    domain = target_domain(event.source_layer)
    repo.save_card(domain, card, event.event_id or "")

    if event.source_layer == "agent":
        repo.save_validation_rule(build_validation_rule(event), event.event_id or "")

    # Calibration check — write warning artifact for high-confidence errors
    if event.source_layer == "question" and not event.is_correct:
        from study_science.calibration import ConfidenceCalibration
        if ConfidenceCalibration.is_dangerous(event.confidence, is_correct=False):
            bump = ConfidenceCalibration.priority_bump(event.confidence, is_correct=False)
            warning_path = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
            warning = {
                "event_id": event.event_id,
                "topic": event.topic,
                "los": event.los,
                "confidence": event.confidence,
                "priority_bump": bump,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            with open(warning_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(warning, ensure_ascii=False) + "\n")

    return event


def record_question_attempt(repo: Repository, payload: dict) -> dict:
    """Persist one question attempt and create a mistake card only when wrong."""
    payload = dict(payload)
    payload.setdefault("source_layer", "question")
    payload.setdefault("confidence", 2)
    payload.setdefault("time_spent", 60)
    payload.setdefault("evidence_refs", [])
    payload.setdefault("error_type", "concept_confusion")
    payload.setdefault("wrong_choice_or_output", "")
    payload.setdefault("correct_resolution", "")
    created_at = str(payload.get("created_at") or datetime.now(timezone.utc).isoformat())
    payload["created_at"] = created_at

    attempt_id = stable_id(
        "attempt",
        str(payload.get("topic", "")),
        str(payload.get("los", "")),
        str(payload.get("prompt_or_question", "")),
        str(payload.get("wrong_choice_or_output", "")),
        ",".join(str(ref) for ref in payload.get("evidence_refs", [])),
        created_at,
    )
    is_correct = bool(payload.get("is_correct", False))
    event = None
    if not is_correct:
        capture_fields = {field.name for field in fields(MistakeEvent)}
        mistake_payload = {
            key: value
            for key, value in payload.items()
            if key in capture_fields
        }
        event = record_event(repo, mistake_payload, mode="record-mistake")

    repo.append_attempt_record(
        {
            **payload,
            "schema_version": 1,
            "event_id": attempt_id,
            "event_type": "attempt.recorded",
            "learner_id": "local",
            "occurred_at": created_at,
            "source_refs": payload.get("evidence_refs", []),
            "payload": payload,
            "attempt_id": attempt_id,
            "mistake_event_id": event.event_id if event else "",
            "is_correct": is_correct,
        }
    )
    if is_correct:
        return {"attempt_id": attempt_id, "event": None, "card_id": ""}

    return {
        "attempt_id": attempt_id,
        "event": event,
        "card_id": stable_id("card", event.event_id or "", event.topic, event.los),
    }


def batch_import_attempts(repo: Repository, events_payload: list[dict], source_label: str = "batch-import") -> dict:
    """Import question attempts through the same correctness-aware pipeline."""
    attempt_ids: list[str] = []
    event_ids: list[str] = []
    for payload in events_payload:
        payload = dict(payload)
        payload.setdefault("evidence_refs", [source_label])
        result = record_question_attempt(repo, payload)
        attempt_ids.append(result["attempt_id"])
        if result["event"] is not None:
            event_ids.append(result["event"].event_id or "")
    return {"attempt_ids": attempt_ids, "event_ids": event_ids}


def batch_import_events(repo: Repository, events_payload: list[dict], source_label: str = "batch-import") -> list[str]:
    """Import multiple question attempts at once.

    Args:
        repo: Repository instance
        events_payload: List of MistakeEvent-compatible dicts
        source_label: Label for evidence_refs

    Returns:
        List of created event IDs.
    """
    return batch_import_attempts(repo, events_payload, source_label)["event_ids"]


def mark_card_reviewed(repo: Repository, card_id: str, outcome: str, confidence_after: int = 0) -> dict:
    """Record a card review and reschedule using SpacingScheduler."""
    from datetime import date
    from study_science.spacing import SpacingInput, SpacingScheduler

    card_path = None
    card_domain = None
    for domain in ("question-errors", "cognitive-bias", "agent-failures"):
        p = repo.memory_root / domain / f"{card_id}.md"
        if p.exists():
            card_path = p
            card_domain = domain
            break

    if not card_path:
        raise FileNotFoundError(f"Card {card_id} not found in any domain")

    text = card_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    topic = frontmatter.get("topic", "Unknown")
    los = frontmatter.get("los", "Unknown")
    error_type = frontmatter.get("root_cause", "unknown")
    prev_reviews = int(frontmatter.get("previous_reviews", "0") or "0")
    confidence_before = int(frontmatter.get("confidence_before", "0") or "0")
    exam_date = frontmatter.get("exam_date", "") or load_exam_date(repo)

    is_correct = outcome == "recalled"
    confidence = confidence_after if confidence_after > 0 else (
        3 if outcome == "recalled" else 1 if outcome == "struggled" else 0
    )

    # Compute personalized calibration adjustment for dynamic expansion
    cal_warnings = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
    cal_adjustment = SpacingScheduler.compute_calibration_adjustment(cal_warnings)

    input_data = SpacingInput(
        topic=topic,
        los=los,
        error_type=error_type,
        confidence=confidence,
        is_correct=is_correct,
        time_spent_seconds=60,
        previous_reviews=prev_reviews + 1,
        last_reviewed_at=date.today().isoformat(),
        exam_date=exam_date,
        calibration_adjustment=cal_adjustment,
    )
    decision = SpacingScheduler.schedule(input_data)

    repo.update_card_review(
        domain=card_domain,
        card_id=card_id,
        previous_reviews=prev_reviews + 1,
        review_due_at=decision.next_review_date,
        spacing_interval_days=decision.interval_days,
        spacing_priority=decision.priority,
        last_reviewed_at=date.today().isoformat(),
        spacing_reasoning=decision.reasoning,
        confidence_before=confidence,
        exam_date=exam_date,
    )

    progress = {
        "record_type": "card_review",
        "card_id": card_id,
        "outcome": outcome,
        "is_correct": is_correct,
        "confidence_after": confidence,
        "confidence_before": confidence_before,
        "confidence_delta": confidence - confidence_before,
        "topic": topic,
        "los": los,
        "next_review_date": decision.next_review_date,
        "interval_days": decision.interval_days,
        "spacing_reasoning": decision.reasoning,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    repo.append_jsonl_event("progress", progress)

    # ── Feedback loop: feed card outcome to linked knowledge points ──────
    _feed_card_outcome_to_knowledge(repo, card_id, topic, los, outcome, confidence)

    return progress


def _feed_card_outcome_to_knowledge(
    repo: Repository, card_id: str, topic: str, los: str,
    outcome: str, confidence_after: int,
) -> None:
    """Feed a card review outcome back into the knowledge-status overlay.

    Knowledge points whose (subject, heading) match this card's (topic, los)
    get their state updated based on the recall outcome.
    """
    from study_science.knowledge_memory import KnowledgeMemoryEngine, KnowledgeFeedbackInput, KnowledgeState

    overlay_path = repo.memory_root / "review" / "knowledge-status.json"
    if not overlay_path.exists():
        return
    try:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    kp_map = overlay.get("knowledge_points", {})
    if not kp_map:
        return

    # Normalize topic for matching
    topic_lower = topic.strip().lower()
    los_lower = los.strip().lower()

    km_engine = KnowledgeMemoryEngine()
    updated = False

    for kid, entry in kp_map.items():
        subj = entry.get("subject", "").strip().lower()
        head = entry.get("heading", "").strip().lower()
        trig = entry.get("trigger", "").strip().lower()
        linked_card_ids = entry.get("linked_card_ids", [])

        if linked_card_ids:
            if card_id not in linked_card_ids:
                continue
        else:
            # Historical overlays do not have explicit links, so retain the
            # conservative topic/LOS fallback until their next snapshot.
            if subj != topic_lower:
                continue
            if los_lower not in head and los_lower not in trig:
                los_prefix = los_lower.split(" ")[0].split("/")[0] if los_lower else ""
                if not los_prefix or (
                    los_prefix not in head and los_prefix not in trig
                ):
                    continue

        # Match found — feed outcome back
        feedback = KnowledgeFeedbackInput(
            knowledge_id=kid,
            subject=entry.get("subject", ""),
            heading=entry.get("heading", ""),
            trigger=entry.get("trigger", ""),
            source_refs=entry.get("source_refs", []),
            outcome={"recalled": "reviewed", "struggled": "struggled", "forgot": "forgot"}.get(outcome, "reviewed"),
            confidence_after=confidence_after,
        )
        new_entry, decision = km_engine.update_knowledge_point(
            entry, feedback,
            exam_date=load_exam_date(repo),
        )
        kp_map[kid] = new_entry
        updated = True

    if updated:
        overlay["knowledge_points"] = kp_map
        overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")


def record_fix_rule_feedback(repo: Repository, card_id: str, helpful: bool, note: str = "") -> dict:
    """Append learner feedback for a card's correction rule."""
    domain = _card_domain_for(repo, card_id)
    if not domain:
        raise FileNotFoundError(f"Card {card_id} not found in any domain")
    event = _review_event(
        "card.fix_rule.feedback",
        card_id,
        datetime.now(timezone.utc).isoformat(),
        source_refs=[card_id],
        payload={"card_id": card_id, "helpful": helpful, "note": note},
    )
    repo.append_jsonl_event("review", event)
    return event


def mine_patterns(repo: Repository, events: list[MistakeEvent] | None = None) -> list[PatternInsight]:
    events = events if events is not None else repo.load_events()
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
    seen_event_ids: set[str] = set()
    buckets: dict[str, list[MistakeEvent]] = defaultdict(list)
    for event in events:
        if event.source_layer != "question":
            continue
        if not event.moc_target:
            continue
        # Deduplicate by event_id
        if event.event_id and event.event_id in seen_event_ids:
            continue
        if event.event_id:
            seen_event_ids.add(event.event_id)
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
        f"generated_at: {events[-1].created_at if events else ''}",
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
        bucket = mock_bucket_for_event(repo, event)
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


def progress_log_path(repo: Repository) -> Path:
    return repo.memory_root / "progress" / "progress-events.jsonl"


def record_progress(repo: Repository, payload: dict) -> Path:
    payload = dict(payload)
    payload.setdefault("created_at", datetime.now().isoformat())
    payload.setdefault("record_type", "module_progress")
    payload.setdefault("status", "recorded")
    path = progress_log_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def load_progress_events(repo: Repository) -> list[dict]:
    path = progress_log_path(repo)
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def progress_summary_lines(progress_events: list[dict], focus_topic: str) -> list[str]:
    if not progress_events:
        return []

    focus_subject = normalize_subject(focus_topic) if focus_topic else ""
    completed = []
    for event in progress_events:
        if event.get("record_type") != "daily_review_completed":
            continue
        if event.get("status") not in {"completed", "done"}:
            continue
        event_focus = normalize_subject(str(event.get("focus_topic", "")))
        if focus_subject and event_focus and event_focus != focus_subject:
            continue
        date_text = str(event.get("date") or event.get("created_at", "")[:10])
        if date_text and date_text not in completed:
            completed.append(date_text)
    if not completed:
        return []
    return ["## 复习进度", "", f"- 已完成复习: {', '.join(completed[-3:])}", ""]


def _review_snapshot_root(repo: Repository) -> Path:
    path = repo.memory_root / "review" / "daily"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _review_event(
    event_type: str,
    *identity_parts: str,
    source_refs: list[str] | None = None,
    payload: dict | None = None,
) -> dict:
    return {
        "schema_version": 1,
        "event_id": stable_id("review-event", event_type, *identity_parts),
        "event_type": event_type,
        "learner_id": "local",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "source_refs": source_refs or [],
        "payload": payload or {},
    }


def _append_review_event_once(repo: Repository, event: dict) -> bool:
    existing_ids = {
        row.get("event_id")
        for row in repo.load_jsonl_events("review")
    }
    if event["event_id"] in existing_ids:
        return False
    repo.append_jsonl_event("review", event)
    return True


def _as_source_refs(value: object) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value if str(item).strip()]
    if not value:
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _knowledge_point_snapshot(item: dict) -> dict:
    knowledge_id = stable_id(
        "knowledge",
        str(item.get("source", "")),
        str(item.get("heading", "")),
        str(item.get("trigger", "")),
    )
    return {
        "knowledge_id": knowledge_id,
        "subject": item.get("subject", ""),
        "heading": item.get("heading", ""),
        "trigger": item.get("trigger", ""),
        "source_refs": [str(item.get("source", ""))] if item.get("source") else [],
    }


def write_daily_review_snapshot(
    repo: Repository,
    review_date: date,
    days_back: int,
    max_items: int,
    focus_topic: str,
    knowledge_depth: str,
    review_items: list[dict],
    warm_start_items: list[dict],
    source_event_count: int = 0,
    interleaving_composition: dict[str, int] | None = None,
) -> dict:
    knowledge_points: list[dict] = []
    seen_knowledge: set[str] = set()
    for item in warm_start_items:
        point = _knowledge_point_snapshot(item)
        if point["knowledge_id"] not in seen_knowledge:
            knowledge_points.append(point)
            seen_knowledge.add(point["knowledge_id"])

    mistake_cards: list[dict] = []
    seen_cards: set[str] = set()
    for item in review_items:
        for card_id in item.get("card_ids", []):
            if not card_id or card_id in seen_cards:
                continue
            mistake_cards.append(
                {
                    "card_id": card_id,
                    "topic": item.get("topic", ""),
                    "los": item.get("los", ""),
                    "source_refs": _as_source_refs(item.get("evidence_refs")),
                }
            )
            seen_cards.add(card_id)

    item_ids = [
        *[item["knowledge_id"] for item in knowledge_points],
        *[item["card_id"] for item in mistake_cards],
    ]
    knowledge_card_map: dict[str, list[str]] = {}
    for point in knowledge_points:
        searchable = f"{point.get('heading', '')} {point.get('trigger', '')}".lower()
        linked_cards = [
            card["card_id"]
            for card in mistake_cards
            if normalize_subject(card.get("topic", "")) == normalize_subject(point.get("subject", ""))
            and card.get("los", "").strip()
            and card.get("los", "").strip().lower() in searchable
        ]
        if linked_cards:
            knowledge_card_map[point["knowledge_id"]] = linked_cards

    review_id = stable_id(
        "daily-review",
        review_date.isoformat(),
        str(days_back),
        str(max_items),
        focus_topic,
        knowledge_depth,
        ",".join(sorted(item_ids)),
    )
    snapshot = {
        "schema_version": 1,
        "review_id": review_id,
        "generated_for": review_date.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_event_count": source_event_count,
        "generation": {
            "days_back": days_back,
            "max_items": max_items,
            "focus_topic": focus_topic,
            "knowledge_depth": knowledge_depth,
        },
        "knowledge_points": knowledge_points,
        "mistake_cards": mistake_cards,
        "knowledge_card_map": knowledge_card_map,
        "interleaving_composition": interleaving_composition or {},
    }
    snapshot_root = _review_snapshot_root(repo)
    body = json.dumps(snapshot, ensure_ascii=False, indent=2)
    (snapshot_root / f"{review_id}.json").write_text(body, encoding="utf-8")
    (snapshot_root / "latest.json").write_text(body, encoding="utf-8")

    _append_review_event_once(
        repo,
        _review_event(
            "daily_review.generated",
            review_id,
            source_refs=item_ids,
            payload={
                "review_id": review_id,
                "generated_for": review_date.isoformat(),
                "knowledge_point_count": len(knowledge_points),
                "mistake_card_count": len(mistake_cards),
                "generation": snapshot["generation"],
            },
        ),
    )
    return snapshot


def load_daily_review_snapshot(repo: Repository, review_id: str = "") -> dict:
    name = f"{review_id}.json" if review_id else "latest.json"
    path = _review_snapshot_root(repo) / name
    if not path.exists():
        raise FileNotFoundError(f"Daily Review snapshot not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _card_domain_for(repo: Repository, card_id: str) -> str | None:
    for domain in CARD_DOMAINS:
        if (repo.memory_root / domain / f"{card_id}.md").exists():
            return domain
    return None


def complete_daily_review(repo: Repository, review_id: str) -> dict:
    from study_science.knowledge_memory import KnowledgeMemoryEngine

    snapshot = load_daily_review_snapshot(repo, review_id)
    occurred_at = datetime.now(timezone.utc).isoformat()
    km_engine = KnowledgeMemoryEngine()
    overlay_path = repo.memory_root / "review" / "knowledge-status.json"
    if overlay_path.exists():
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    else:
        overlay = {"schema_version": 1, "knowledge_points": {}}

    reviewed_items = 0
    knowledge_decisions: list[dict] = []

    for point in snapshot.get("knowledge_points", []):
        item_id = point["knowledge_id"]
        event = _review_event(
            "daily_review.item.reviewed",
            review_id,
            item_id,
            source_refs=point.get("source_refs", []),
            payload={"review_id": review_id, "item_id": item_id, "item_type": "knowledge_point", "status": "Reviewed once"},
        )
        newly_reviewed = _append_review_event_once(repo, event)
        if newly_reviewed:
            reviewed_items += 1
        else:
            continue

        # Feedback loop: feed review exposure into KnowledgeMemoryEngine
        from study_science.knowledge_memory import KnowledgeFeedbackInput
        current_entry = overlay["knowledge_points"].get(item_id)
        linked_card_ids = snapshot.get("knowledge_card_map", {}).get(item_id, [])
        if linked_card_ids:
            current_entry = {
                **(current_entry or {}),
                "linked_card_ids": sorted(
                    set((current_entry or {}).get("linked_card_ids", [])) | set(linked_card_ids)
                ),
            }
        feedback = KnowledgeFeedbackInput(
            knowledge_id=item_id,
            subject=point.get("subject", ""),
            heading=point.get("heading", ""),
            trigger=point.get("trigger", ""),
            source_refs=point.get("source_refs", []),
            outcome="reviewed",
            confidence_after=2,
        )
        entry, decision = km_engine.update_knowledge_point(
            current_entry, feedback,
            exam_date=load_exam_date(repo),
        )
        overlay["knowledge_points"][item_id] = entry
        knowledge_decisions.append({
            "knowledge_id": decision.knowledge_id,
            "state": decision.status_label,
            "state_value": int(decision.state),
            "next_review_at": decision.next_review_date,
            "review_interval_days": decision.review_interval_days,
            "decay_risk": decision.decay_risk,
        })

    overlay_path.parent.mkdir(parents=True, exist_ok=True)
    overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")

    for card in snapshot.get("mistake_cards", []):
        item_id = card["card_id"]
        event = _review_event(
            "daily_review.item.reviewed",
            review_id,
            item_id,
            source_refs=card.get("source_refs", []),
            payload={"review_id": review_id, "item_id": item_id, "item_type": "mistake_card", "status": "Reviewed once"},
        )
        if _append_review_event_once(repo, event):
            reviewed_items += 1
        domain = _card_domain_for(repo, item_id)
        if domain:
            repo.update_card_status(domain, item_id, "Reviewed once")

    completed = _append_review_event_once(
        repo,
        _review_event(
            "daily_review.completed",
            review_id,
            source_refs=[
                *[item["knowledge_id"] for item in snapshot.get("knowledge_points", [])],
                *[item["card_id"] for item in snapshot.get("mistake_cards", [])],
            ],
            payload={
                "review_id": review_id,
                "status": "completed",
                "reviewed_item_count": len(snapshot.get("knowledge_points", [])) + len(snapshot.get("mistake_cards", [])),
            },
        ),
    )
    if completed:
        record_progress(
            repo,
            {
                "date": snapshot.get("generated_for", ""),
                "record_type": "daily_review_completed",
                "status": "completed",
                "focus_topic": snapshot.get("generation", {}).get("focus_topic", ""),
                "review_id": review_id,
            },
        )
    return {
        "review_id": review_id,
        "completed": completed,
        "newly_reviewed_items": reviewed_items,
        "knowledge_decisions": knowledge_decisions,
    }


def collect_due_knowledge_points(repo: Repository, target_date: date) -> list[dict]:
    """Collect knowledge points due for review from the KnowledgeMemoryEngine overlay.

    Reads knowledge-status.json and returns entries whose next_review_at
    has arrived or is past, enriched with decay priority for scheduling.
    """
    from study_science.knowledge_memory import KnowledgeMemoryEngine

    overlay_path = repo.memory_root / "review" / "knowledge-status.json"
    if not overlay_path.exists():
        return []

    try:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    kp_map = overlay.get("knowledge_points", {})
    if not kp_map:
        return []

    # Run decay sweep first so states are current
    engine = KnowledgeMemoryEngine()
    overlay, _decayed = engine.decay_sweep(overlay, target_date)
    overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")

    today_str = target_date.isoformat()
    due: list[dict] = []

    for kid, entry in kp_map.items():
        next_review = entry.get("next_review_at", "")[:10]
        if not next_review:
            continue

        # Due if next_review_at <= target_date
        if next_review > today_str:
            continue

        decay_risk = entry.get("decay_risk", "none")
        state_value = int(entry.get("state_value", 0) or 0)
        consecutive = int(entry.get("consecutive_successes", 0) or 0)

        # Priority boost from decay risk and state
        risk_boost = {
            "overdue": 50,
            "high": 40,
            "medium": 25,
            "low": 10,
            "none": 0,
        }.get(decay_risk, 0)

        scheduling_priority = 100 + risk_boost + (5 - state_value) * 3

        due.append({
            "subject": entry.get("subject", ""),
            "heading": entry.get("heading", ""),
            "trigger": entry.get("trigger", ""),
            "reason": (
                f"Memory review due; state={entry.get('status', '?')}, "
                f"decay_risk={decay_risk}, consecutive_successes={consecutive}"
            ),
            "priority": scheduling_priority,
            "knowledge_id": kid,
            "state": entry.get("status", ""),
            "state_value": state_value,
            "decay_risk": decay_risk,
            "next_review_at": next_review,
            "source": "; ".join(entry.get("source_refs", [])),
        })

    return sorted(due, key=lambda x: -x["priority"])[:20]


def daily_review_pack(
    repo: Repository,
    review_date: date | None = None,
    days_back: int = 7,
    max_items: int = 20,
    focus_topic: str = "",
    knowledge_depth: str = "standard",
    energy_level: int | None = None,
) -> Path:
    target_date = review_date or datetime.now().date()
    days_back = max(days_back, 1)
    max_items = max(max_items, 1)

    # ── Energy-aware shaping ──────────────────────────────────────────
    # Auto-detect energy from the latest check-in if not provided
    if energy_level is None:
        energy_events = repo.load_energy_events()
        if energy_events:
            latest = max(energy_events, key=lambda e: e.get("created_at", ""))
            energy_level = latest.get("energy_level")
    energy_warnings: list[str] = []
    if energy_level is not None:
        if energy_level <= 1:
            # Low energy: fewer items, mistakes only (no new material)
            max_items = min(max_items, 8)
            energy_warnings.append(
                "⚠️ 当前精力偏低，已减少复习量至核心错题。建议优先完成后再休息。"
            )
        elif energy_level == 2:
            # Moderate energy: standard but no expansion
            max_items = min(max_items, 14)
            energy_warnings.append(
                "⚡ 精力适中，复习量已适度缩减。聚焦高优先级错题。"
            )
        else:
            energy_warnings.append(
                "🧠 精力充沛，适合完整复习和深入理解。"
            )
    # ──────────────────────────────────────────────────────────────────

    events = repo.load_events()
    mine_patterns(repo, events)
    due_items = collect_due_card_items(repo, target_date)
    recent_items = collect_recent_low_confidence_items(repo, target_date, days_back, events)
    pattern_items = collect_pattern_items(repo)
    review_items, interleaving_composition = interleave_review_items(
        merge_review_sources(due_items, pattern_items, recent_items),
        max_items,
    )
    warm_start_items = build_warm_start_items(repo, review_items, focus_topic)
    if knowledge_depth == "expanded":
        warm_start_items = merge_warm_start_items(
            warm_start_items,
            build_expanded_warm_start_items(repo, review_items, focus_topic),
        )

    # ── Knowledge Memory Loop: inject due knowledge points ──────────────
    # Due KPs are knowledge points whose next_review_at has arrived,
    # as computed by the KnowledgeMemoryEngine. They need consolidation
    # to prevent forgetting-curve decay. Inject them into warm-start items
    # so they appear in the "知识点和公式" section of the daily review.
    due_knowledge_points = collect_due_knowledge_points(repo, target_date)
    if due_knowledge_points:
        # Build a set of existing (subject, heading, trigger) keys from warm_start_items
        existing_keys = {
            (i.get("subject", ""), i.get("heading", ""), i.get("trigger", ""))
            for i in warm_start_items
        }
        for kp in due_knowledge_points:
            key = (kp["subject"], kp["heading"], kp["trigger"])
            if key not in existing_keys:
                # Look up formula/decision from MOC if available, otherwise use defaults
                try:
                    atoms = extract_moc_atoms(repo, kp["subject"])
                    matching = [a for a in atoms if a.get("heading") == kp["heading"] and a.get("trigger") == kp["trigger"]]
                    atom = matching[0] if matching else {}
                except Exception:
                    atom = {}
                warm_start_items.append({
                    "subject": kp["subject"],
                    "heading": kp["heading"],
                    "trigger": kp["trigger"],
                    "formula": atom.get("formula", kp.get("state", "Reviewed once")),
                    "decision": atom.get("decision", f"Decay risk: {kp.get('decay_risk', 'none')}"),
                    "boundaries": atom.get("boundaries", []),
                    "reason": kp.get("reason", "Memory review due"),
                    "source": kp.get("source", "knowledge-status"),
                    "priority": kp.get("priority", 50),
                    "knowledge_id": kp.get("knowledge_id", ""),
                    "decay_risk": kp.get("decay_risk", ""),
                })
                existing_keys.add(key)
        # Re-sort by priority, then subject, then heading
        warm_start_items.sort(key=lambda x: (-x.get("priority", 0), x.get("subject", ""), x.get("heading", "")))

    progress_events = load_progress_events(repo)

    body = render_review_pack(
        review_items=review_items,
        warm_start_items=warm_start_items,
        source_event_count=len(events),
        review_date=target_date,
        days_back=days_back,
        focus_topic=focus_topic,
        progress_events=progress_events,
        energy_warnings=energy_warnings,
    )
    write_daily_review_snapshot(
        repo,
        review_date=target_date,
        days_back=days_back,
        max_items=max_items,
        focus_topic=focus_topic,
        knowledge_depth=knowledge_depth,
        review_items=review_items,
        warm_start_items=warm_start_items,
        source_event_count=len(events),
        interleaving_composition=interleaving_composition,
    )
    strategy_path = repo.memory_root / "strategy" / "daily-review.md"
    repo.write_markdown(strategy_path, body, "daily_review", "daily-review")
    repo.write_markdown(
        repo.memory_root / "strategy" / "daily-review-pack.md",
        "# Daily Review Pack\n\n已迁移至 [[daily-review]]。\n",
        "daily_review_compatibility",
        "daily-review-pack",
    )
    repo.write_obsidian_page("Daily Review.md", body.splitlines())
    repo.write_obsidian_page("今日复习资料.md", ["# 今日复习资料", "", "已迁移至 [[Daily Review]]。"])
    return strategy_path


def coerce_task_list(value: object) -> list[str]:
    if isinstance(value, list):
        raw_items = [str(item) for item in value]
    elif isinstance(value, str):
        raw_items = re.split(r"[\n;；]+", value)
    else:
        raw_items = []

    tasks: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        task = re.sub(r"^\s*[-*]\s*\[[ xX]\]\s*", "", item).strip()
        task = re.sub(r"^\s*[-*]\s*", "", task).strip()
        if not task:
            continue
        key = task.lower()
        if key in seen:
            continue
        seen.add(key)
        tasks.append(task)
    return tasks


def normalize_deadline(value: object) -> str:
    if value is None:
        return ""

    raw = str(value).strip()
    if not raw:
        return ""

    match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*([aApP][mM])?", raw)
    if not match:
        return raw

    hour = int(match.group(1))
    minute = int(match.group(2) or "00")
    meridiem = match.group(3)
    if meridiem:
        if meridiem.lower() == "pm" and hour != 12:
            hour += 12
        if meridiem.lower() == "am" and hour == 12:
            hour = 0
    return f"{hour:02d}:{minute:02d}"


def normalize_todo_tasks(value: object) -> list[dict[str, str]]:
    if isinstance(value, list):
        raw_items = value
    elif isinstance(value, str):
        raw_items = re.split(r"[\n;；]+", value)
    else:
        raw_items = []

    tasks: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw_items:
        deadline = ""
        if isinstance(item, dict):
            task_text = str(item.get("task") or item.get("title") or item.get("text") or item.get("name") or "").strip()
            deadline = normalize_deadline(item.get("deadline") or item.get("due") or item.get("time"))
        else:
            task_text = str(item).strip()

        task_text = re.sub(r"^\s*[-*]\s*\[[ xX]\]\s*", "", task_text).strip()
        task_text = re.sub(r"^\s*[-*]\s*", "", task_text).strip()
        if not task_text:
            continue

        key = task_text.lower()
        if key in seen:
            continue
        seen.add(key)
        tasks.append({"task": task_text, "deadline": deadline})
    return tasks


def ensure_daily_review_task(tasks: list[dict[str, str]]) -> list[dict[str, str]]:
    for task in tasks:
        if task["task"].strip().lower() in {alias.lower() for alias in DAILY_REVIEW_TASK_ALIASES}:
            task["task"] = DAILY_REVIEW_TASK
            task["deadline"] = DAILY_REVIEW_DEADLINE
            return tasks

    daily_review = {"task": DAILY_REVIEW_TASK, "deadline": DAILY_REVIEW_DEADLINE}
    for index, task in enumerate(tasks):
        deadline = task.get("deadline", "")
        if deadline and deadline > DAILY_REVIEW_DEADLINE:
            return [*tasks[:index], daily_review, *tasks[index:]]
    return [*tasks, daily_review]


def archive_today_todo(repo: Repository, archive_date: str) -> Path | None:
    dashboard_path = repo.obsidian_root / "today_todo.md"
    today_path = dashboard_path if dashboard_path.exists() else repo.root / "today_todo.md"
    if not today_path.exists():
        return None

    text = today_path.read_text(encoding="utf-8")
    if not text.strip():
        return None

    archive_root = repo.schedule_root / "todo_archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    base_path = archive_root / f"{archive_date}-todo.md"
    archive_path = base_path
    counter = 2
    while archive_path.exists():
        archive_path = archive_root / f"{archive_date}-todo-{counter}.md"
        counter += 1
    archive_path.write_text(text, encoding="utf-8")
    return archive_path


def render_todo(payload: dict, plan_date: str, tasks: list[dict[str, str]]) -> str:
    title = payload.get("title") or "今日 Todo"
    focus = payload.get("focus") or payload.get("theme") or "完成今天最重要的任务"
    time_blocks = coerce_task_list(payload.get("time_blocks", []))

    lines = [
        "---",
        f"date: {plan_date}",
        f"focus: {focus}",
        "status: active",
        "---",
        "",
        f"# {title}",
        "",
        f"> Focus: {focus}",
        "",
        "## Tasks",
    ]
    if tasks:
        for task in tasks:
            deadline = task.get("deadline", "")
            suffix = f"（deadline: {deadline}）" if deadline else ""
            lines.append(f"- [ ] {task['task']}{suffix}")
    else:
        lines.append("- [ ] 明确今天最重要的 3-5 个任务")

    if time_blocks:
        lines.extend(["", "## Time Blocks"])
        lines.extend(f"- {block}" for block in time_blocks)

    lines.extend(
        [
            "",
            "## Review",
            "- 完成了什么：",
            "- 卡住或调整：",
            "- 明天保留：",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def write_todo(repo: Repository, payload: dict) -> Path:
    plan_date = str(payload.get("date") or datetime.now().date().isoformat())
    tasks = ensure_daily_review_task(normalize_todo_tasks(payload.get("tasks", [])))
    archive_today_todo(repo, plan_date)

    path = repo.obsidian_root / "today_todo.md"
    body = render_todo(payload, plan_date, tasks)
    path.write_text(body, encoding="utf-8")
    return path


def _feed_mock_to_spacing(repo: Repository, incorrect_events: list[MistakeEvent]) -> None:
    """Feed mock incorrect results back into spacing intervals.

    For each incorrect mock event, find the corresponding card and compress
    its spacing interval (force review soon) and boost priority.
    """
    from datetime import date as date_type
    from app.models import stable_id as sid

    tomorrow = (date_type.today() + timedelta(days=1)).isoformat()
    for event in incorrect_events:
        card_id = sid("card", event.event_id or "", event.topic, event.los)
        # Try both question-errors and cognitive-bias domains
        for domain in ("question-errors", "cognitive-bias"):
            card_path = repo.memory_root / domain / f"{card_id}.md"
            if not card_path.exists():
                continue
            try:
                repo.update_card_review(
                    domain=domain,
                    card_id=card_id,
                    previous_reviews=0,  # don't increment — this is a reset
                    review_due_at=tomorrow,
                    spacing_interval_days=1,
                    spacing_priority=95,  # mock error = highest priority
                    last_reviewed_at=datetime.now(timezone.utc).isoformat(),
                    spacing_reasoning="Mock feedback: incorrect → forced review tomorrow",
                )
            except (FileNotFoundError, OSError):
                continue
            break  # found and updated in this domain


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

    # ── Feed mock results back into spacing and knowledge memory ──────
    incorrect_questions = [e for e in grouped.get("question", []) if not e.is_correct]
    if incorrect_questions:
        _feed_mock_to_spacing(repo, incorrect_questions)

        # Write mock accuracy signal
        total = len(grouped.get("question", []))
        accuracy = round((total - len(incorrect_questions)) / total * 100) if total > 0 else 100
        signal = {
            "session_id": session_id,
            "total_questions": total,
            "incorrect_count": len(incorrect_questions),
            "accuracy_pct": accuracy,
            "topics": list({e.topic for e in incorrect_questions}),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        signal_path = repo.memory_root / "strategy" / "mock-feedback-signals.jsonl"
        with open(signal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(signal, ensure_ascii=False) + "\n")

    refresh_learning_outputs(repo)
    return path


def load_payload(raw: str) -> dict:
    return json.loads(raw)


def normalize_choice_line(label: str, text: str) -> str:
    return f"{label.upper()}. {clean_display_text(text)}".strip()


def split_prompt_choices(text: str) -> tuple[str, list[str]]:
    cleaned = (text or "").strip()
    matches = list(re.finditer(r"(?:^|\s)([A-E])\.\s+", cleaned))
    if len(matches) < 2:
        return cleaned, []
    labels = [match.group(1) for match in matches]
    positions = {match.group(1): match.start() for match in matches}
    has_choice_sequence = (
        "A" in positions
        and (
            ("B" in positions and positions["A"] < positions["B"])
            or ("C" in positions and positions["A"] < positions["C"])
        )
    )
    if not has_choice_sequence or labels[0] != "A":
        return cleaned, []

    stem = cleaned[: matches[0].start()].strip()
    choices: list[str] = []
    for index, match in enumerate(matches):
        label = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
        choice_text = cleaned[start:end].strip()
        if choice_text:
            choices.append(normalize_choice_line(label, choice_text))
    return stem, choices


def normalize_choices(value: object) -> list[str]:
    if isinstance(value, list):
        raw_items = value
    elif isinstance(value, str):
        raw_items = [line for line in value.splitlines() if line.strip()]
    else:
        raw_items = []

    choices: list[str] = []
    for index, item in enumerate(raw_items):
        text = clean_display_text(str(item))
        if not text:
            continue
        match = re.match(r"^([A-E])\.\s*(.*)$", text)
        if match:
            choices.append(normalize_choice_line(match.group(1), match.group(2)))
        else:
            label = chr(ord("A") + index)
            choices.append(normalize_choice_line(label, text))
    return choices


def infer_question_format(prompt: str, wrong_output: str, choices: list[str], explicit: str = "") -> str:
    if explicit:
        return explicit
    if choices:
        return "multiple_choice"
    if re.match(r"^\s*[A-E](?:\.|\b)", wrong_output or ""):
        return "multiple_choice"
    if len(re.findall(r"\b[A-E]\.\s", prompt or "")) >= 2:
        return "multiple_choice"
    return ""


def hydrate_question_fields(payload: dict) -> dict:
    prompt = str(payload.get("prompt_or_question") or "")
    stem, parsed_choices = split_prompt_choices(prompt)
    choices = normalize_choices(payload.get("choices") or parsed_choices)
    question_format = infer_question_format(
        prompt,
        str(payload.get("wrong_choice_or_output") or ""),
        choices,
        str(payload.get("question_format") or ""),
    )
    if choices:
        payload = dict(payload)
        payload["prompt_or_question"] = stem or prompt
        payload["choices"] = choices
    if question_format:
        payload = dict(payload)
        payload["question_format"] = question_format
    return payload


def weekly_focus_recommendation(repo: Repository) -> str:
    """Generate a weekly focus recommendation based on last 7 days of data.

    Returns the markdown content written to strategy/weekly-focus-*.md
    """
    from collections import Counter, defaultdict
    from datetime import date, timedelta

    today = date.today()
    week_ago = today - timedelta(days=7)

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question" and not e.is_correct]
    recent = [e for e in question_events if e.created_at[:10] >= week_ago.isoformat()]

    if not recent:
        return "过去 7 天没有记录错题。建议先做一套练习题再安排本周重点。"

    # Most problematic topics
    topic_errors: dict[str, list] = defaultdict(list)
    for e in recent:
        topic_errors[e.topic].append(e)

    # Score each topic: errors + high-confidence errors + recurrence
    topic_scores: dict[str, float] = {}
    for topic, errs in topic_errors.items():
        score = len(errs) * 2  # error count
        score += sum(3 for e in errs if e.confidence >= 3 and not e.is_correct)  # high-conf penalty
        # LOS variety
        los_set = set(e.los for e in errs)
        score += len(los_set) * 1.5
        topic_scores[topic] = score

    ranked = sorted(topic_scores.items(), key=lambda x: -x[1])

    lines = [
        "---",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        f"period: {week_ago.isoformat()} to {today.isoformat()}",
        "---",
        "",
        "# 本周学习重点建议",
        "",
        f"**分析周期:** {week_ago.isoformat()} ~ {today.isoformat()}",
        f"**本周错误总数:** {len(recent)}",
        "",
    ]

    if ranked:
        top = ranked[0]
        lines.extend([
            "## 最需关注的 Topic",
            "",
            f"**{top[0]}** (得分 {top[1]:.0f}) — 过去 7 天出现 {len(topic_errors[top[0]])} 次错误",
            "",
        ])

        # List high-confidence errors in top topic
        high_conf = [e for e in topic_errors[top[0]] if e.confidence >= 3 and not e.is_correct]
        if high_conf:
            lines.extend([
                "### 高信心错误（最危险）",
                "",
                *[f"- {e.los}: 信心 {e.confidence}/4 但做错 → {e.correct_resolution[:80]}..." for e in high_conf[:3]],
                "",
            ])

        # Top 3 topics to focus
        lines.append("## 本周推荐优先级")
        lines.append("")
        for i, (topic, score) in enumerate(ranked[:3], 1):
            err_count = len(topic_errors[topic])
            pct = int(score / max(topic_scores.values(), default=1) * 100)
            lines.append(f"{i}. **{topic}** — {err_count} 次错误，建议分配 {pct}% 的复习时间")
        lines.append("")

        # Review completion
        from app.workflows import load_progress_events
        progress = load_progress_events(repo)
        week_reviews = sum(1 for p in progress if p.get("record_type") == "daily_review_completed"
                          and p.get("status") in {"completed", "done"}
                          and p.get("date", "")[:10] >= week_ago.isoformat())
        lines.extend([
            "## 本周复习情况",
            "",
            f"- 完成复习包: {week_reviews} 次",
            f"- {'✅ 继续保持' if week_reviews >= 3 else '⚠️ 建议增加复习频率，目标每周至少 5 次'}",
            "",
        ])

    output = "\n".join(lines)
    path = repo.memory_root / "strategy" / f"weekly-focus-{today.isoformat()}.md"
    repo.write_markdown(path, output, "weekly_focus", f"weekly-focus-{today.isoformat()}")
    return output
