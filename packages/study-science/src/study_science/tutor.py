from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, is_forbidden_key, sanitize_payload
from study_science.knowledge_graph import KnowledgeGraphService


TutorMode = Literal[
    "explain",
    "hint",
    "compare",
    "formula_help",
    "study_strategy",
    "language_help",
    "trace_source",
    "assessment_retro",
    "general",
]

ContextType = Literal[
    "asset",
    "formula",
    "syllabus_topic",
    "coverage",
    "transfer_gap",
    "resource",
    "source_segment",
    "lexical_asset",
    "assessment",
    "study_plan",
    "analytics",
    "mission_action",
]

ActionType = Literal[
    "review",
    "formula_practice",
    "assessment",
    "confirm_asset",
    "confirm_resource",
    "coverage_gap",
    "language_review",
    "study_plan",
    "analytics",
    "search",
    "data_backup",
]

TRUSTED_STATUSES = {"confirmed", "validated", "derived", "generated", "active", "completed", "open", "ready", "extracted"}
BLOCKED_STATUSES = {"draft", "needs_review", "rejected", "blocked"}
RAW_KEYS = FORBIDDEN_SAFE_PAYLOAD_KEYS

MODE_NODE_TYPES: dict[str, set[str]] = {
    "formula_help": {"formula", "asset", "transfer_gap", "assessment_question", "coverage_record"},
    "language_help": {"lexical_asset", "source_document", "study_plan_block"},
    "study_strategy": {"mission_action", "study_plan", "study_plan_block", "transfer_gap", "coverage_record", "analytics_record"},
    "trace_source": {"formula", "asset", "source_segment", "source_document", "resource", "assessment_question"},
    "assessment_retro": {"assessment", "assessment_question", "transfer_gap", "analytics_record"},
    "hint": {"formula", "asset", "lexical_asset", "syllabus_topic", "transfer_gap"},
    "explain": {"asset", "formula", "syllabus_topic", "coverage_record", "source_segment"},
    "compare": {"asset", "formula", "syllabus_topic", "lexical_asset"},
    "general": {"asset", "formula", "syllabus_topic", "mission_action", "study_plan_block"},
}


@dataclass(slots=True)
class TutorRecommendedAction:
    title: str
    reason: str
    launch_route: str
    action_type: ActionType

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TutorSourceContext:
    context_id: str
    node_id: str | None
    source_ref: str | None
    context_type: ContextType
    title: str
    excerpt: str
    validation_status: str | None
    quality_status: str | None
    relevance_score: float
    launch_route: str | None
    source_refs: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return sanitize_public(asdict(self))


@dataclass(slots=True)
class TutorMessage:
    message_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str
    cited_source_refs: list[str] = field(default_factory=list)
    linked_node_ids: list[str] = field(default_factory=list)
    linked_asset_ids: list[str] = field(default_factory=list)
    linked_topic_ids: list[str] = field(default_factory=list)
    linked_routes: list[str] = field(default_factory=list)
    safety_flags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return sanitize_public(asdict(self))


@dataclass(slots=True)
class TutorConversation:
    conversation_id: str
    profile_id: str
    title: str
    created_at: str
    updated_at: str
    mode: TutorMode
    messages: list[TutorMessage] = field(default_factory=list)
    source_context: list[TutorSourceContext] = field(default_factory=list)
    status: Literal["active", "archived"] = "active"

    def as_dict(self) -> dict[str, Any]:
        return sanitize_public(
            {
                "conversation_id": self.conversation_id,
                "profile_id": self.profile_id,
                "title": self.title,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "mode": self.mode,
                "messages": [message.as_dict() for message in self.messages],
                "source_context": [context.as_dict() for context in self.source_context],
                "status": self.status,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> TutorConversation:
        return cls(
            conversation_id=str(payload.get("conversation_id") or ""),
            profile_id=str(payload.get("profile_id") or "default"),
            title=str(payload.get("title") or "Tutor conversation"),
            created_at=str(payload.get("created_at") or _now()),
            updated_at=str(payload.get("updated_at") or _now()),
            mode=payload.get("mode") or "general",
            messages=[TutorMessage(**message) for message in payload.get("messages", [])],
            source_context=[TutorSourceContext(**context) for context in payload.get("source_context", [])],
            status=payload.get("status") or "active",
        )


class TutorService:
    """Deterministic, local-first study tutor over verified OpenExam memory."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.memory_root = self.repo_root / ".system" / "memory"
        self.review_root = self.memory_root / "review"
        self.language_root = self.memory_root / "language" / "dictionary-kernel"
        self.planner_root = self.memory_root / "study-planner" / "plans"
        self.conversation_root = self.memory_root / "tutor" / "conversations"
        self.conversation_root.mkdir(parents=True, exist_ok=True)

    def ask(
        self,
        *,
        profile_id: str = "default",
        mode: TutorMode = "general",
        query: str,
        context_node_id: str | None = None,
    ) -> dict[str, Any]:
        mode = _mode(mode)
        profile_id = profile_id or "default"
        contexts = self.search_context(profile_id=profile_id, query=query, mode=mode, context_node_id=context_node_id, limit=8)
        missing_evidence = not contexts
        answer = self._compose_answer(profile_id=profile_id, mode=mode, query=query, contexts=contexts, missing_evidence=missing_evidence)
        actions = self._recommended_actions(mode=mode, contexts=contexts, missing_evidence=missing_evidence)
        cited_refs = _unique([ref for context in contexts for ref in context.source_refs])
        payload = {
            "profile_id": profile_id,
            "mode": mode,
            "query": query,
            "answer": answer,
            "missing_evidence": missing_evidence,
            "source_context": [context.as_dict() for context in contexts],
            "recommended_actions": [action.as_dict() for action in actions],
            "cited_source_refs": cited_refs,
            "linked_node_ids": _unique([context.node_id for context in contexts if context.node_id]),
            "linked_asset_ids": _unique([str(context.details.get("asset_id")) for context in contexts if context.details.get("asset_id")]),
            "linked_topic_ids": _unique([str(context.details.get("topic_id") or context.details.get("syllabus_topic_id")) for context in contexts if context.details.get("topic_id") or context.details.get("syllabus_topic_id")]),
            "linked_routes": _unique([context.launch_route for context in contexts if context.launch_route] + [action.launch_route for action in actions]),
            "safety_flags": self._safety_flags(missing_evidence=missing_evidence),
            "llm_provider": {"enabled": False, "fallback": "deterministic_templates"},
        }
        return sanitize_public(payload)

    def search_context(
        self,
        *,
        profile_id: str = "default",
        query: str = "",
        mode: TutorMode = "general",
        context_node_id: str | None = None,
        limit: int = 8,
    ) -> list[TutorSourceContext]:
        profile_id = profile_id or "default"
        mode = _mode(mode)
        graph = KnowledgeGraphService(self.repo_root).project(profile_id=profile_id)
        nodes = [sanitize_public(item) for item in graph.get("nodes", [])]
        edges = [sanitize_public(item) for item in graph.get("edges", [])]
        degree = _degree_map(edges)
        query_terms = _terms(query)
        contexts: list[TutorSourceContext] = []
        for node in nodes:
            if context_node_id and node.get("node_id") != context_node_id:
                continue
            if not self._node_allowed(node):
                continue
            score = self._context_score(node, query=query, query_terms=query_terms, mode=mode, degree=degree.get(node.get("node_id"), 0))
            if context_node_id:
                score = max(score, 0.95)
            if score <= 0.08:
                continue
            contexts.append(self._context_from_node(node, score=score))
        if mode == "formula_help":
            contexts.sort(
                key=lambda item: (
                    1 if item.details.get("ba_ii_plus_steps") else 0,
                    1 if item.context_type == "formula" else 0,
                    item.relevance_score,
                ),
                reverse=True,
            )
        else:
            contexts.sort(key=lambda item: item.relevance_score, reverse=True)
        if not contexts and mode == "study_strategy":
            contexts = self._fallback_strategy_contexts(profile_id=profile_id)
        return contexts[: max(1, min(limit, 20))]

    def search_context_payload(self, *, profile_id: str = "default", query: str = "", mode: TutorMode = "general", limit: int = 8) -> dict[str, Any]:
        contexts = self.search_context(profile_id=profile_id, query=query, mode=mode, limit=limit)
        return {
            "profile_id": profile_id or "default",
            "query": query,
            "mode": _mode(mode),
            "count": len(contexts),
            "source_context": [context.as_dict() for context in contexts],
        }

    def suggestions(self, *, profile_id: str = "default") -> dict[str, Any]:
        summary = self.ask(profile_id=profile_id, mode="study_strategy", query="What should I do next?", context_node_id=None)
        suggestions = [
            {"mode": "formula_help", "title": "Explain WACC with calculator steps", "query": "Explain WACC and the calculator steps", "launch_route": "/review/tutor"},
            {"mode": "hint", "title": "Give me a hint before the answer", "query": "Give me a hint for WACC", "launch_route": "/review/tutor"},
            {"mode": "language_help", "title": "Explain a Spanish word in context", "query": "Explain repasar in context", "launch_route": "/review/tutor"},
            {"mode": "trace_source", "title": "Show the source chain for a rule", "query": "Show me the source for WACC", "launch_route": "/review/tutor"},
            {"mode": "study_strategy", "title": "Choose a 20 minute study action", "query": "What should I do next if I only have 20 minutes?", "launch_route": "/review/tutor"},
        ]
        return sanitize_public(
            {
                "profile_id": profile_id or "default",
                "suggestions": suggestions,
                "recommended_actions": summary.get("recommended_actions", []),
            }
        )

    def create_conversation(self, *, profile_id: str = "default", mode: TutorMode = "general", title: str | None = None) -> dict[str, Any]:
        now = _now()
        profile_id = profile_id or "default"
        title = title or "Tutor conversation"
        conversation = TutorConversation(
            conversation_id=_stable_id("tutor-conv", profile_id, title, now),
            profile_id=profile_id,
            title=title,
            created_at=now,
            updated_at=now,
            mode=_mode(mode),
        )
        self._write_conversation(conversation)
        return {"conversation": conversation.as_dict()}

    def list_conversations(self, *, profile_id: str = "default", include_archived: bool = False) -> dict[str, Any]:
        conversations = [
            conversation
            for conversation in self._read_conversations()
            if conversation.profile_id == (profile_id or "default") and (include_archived or conversation.status == "active")
        ]
        conversations.sort(key=lambda item: item.updated_at, reverse=True)
        return {"profile_id": profile_id or "default", "count": len(conversations), "conversations": [item.as_dict() for item in conversations]}

    def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        conversation = self._read_conversation(conversation_id)
        return conversation.as_dict() if conversation else None

    def add_message(self, conversation_id: str, *, content: str) -> dict[str, Any]:
        conversation = self._read_conversation(conversation_id)
        if conversation is None:
            raise KeyError(conversation_id)
        user_message = TutorMessage(
            message_id=_stable_id("tutor-msg", conversation_id, "user", content, _now()),
            role="user",
            content=content,
            created_at=_now(),
            safety_flags=["user_question"],
        )
        answer = self.ask(profile_id=conversation.profile_id, mode=conversation.mode, query=content)
        assistant_message = TutorMessage(
            message_id=_stable_id("tutor-msg", conversation_id, "assistant", content, _now()),
            role="assistant",
            content=str(answer["answer"]),
            created_at=_now(),
            cited_source_refs=list(answer.get("cited_source_refs") or []),
            linked_node_ids=list(answer.get("linked_node_ids") or []),
            linked_asset_ids=list(answer.get("linked_asset_ids") or []),
            linked_topic_ids=list(answer.get("linked_topic_ids") or []),
            linked_routes=list(answer.get("linked_routes") or []),
            safety_flags=list(answer.get("safety_flags") or []),
        )
        conversation.messages.extend([user_message, assistant_message])
        conversation.source_context = [TutorSourceContext(**context) for context in answer.get("source_context", [])]
        conversation.updated_at = _now()
        self._write_conversation(conversation)
        return {"conversation": conversation.as_dict(), "answer": answer}

    def archive_conversation(self, conversation_id: str) -> dict[str, Any]:
        conversation = self._read_conversation(conversation_id)
        if conversation is None:
            raise KeyError(conversation_id)
        conversation.status = "archived"
        conversation.updated_at = _now()
        self._write_conversation(conversation)
        return {"conversation": conversation.as_dict()}

    def governance_summary(self, *, profile_id: str = "default") -> dict[str, Any]:
        conversations = self.list_conversations(profile_id=profile_id, include_archived=True)["conversations"]
        return {
            "profile_id": profile_id or "default",
            "conversation_count": len(conversations),
            "active_conversation_count": sum(1 for item in conversations if item.get("status") == "active"),
            "last_conversation_at": conversations[0]["updated_at"] if conversations else None,
            "snapshot_route": "/review/tutor",
        }

    def _compose_answer(
        self,
        *,
        profile_id: str,
        mode: TutorMode,
        query: str,
        contexts: list[TutorSourceContext],
        missing_evidence: bool,
    ) -> str:
        if missing_evidence:
            return (
                "Local evidence is missing for this question. Import or confirm a source-backed asset, then search the graph again. "
                "Start with /review/resources, /review/assets, or /review/search."
            )
        if mode == "hint":
            return self._compose_hint(contexts)
        if mode == "formula_help":
            return self._compose_formula(contexts)
        if mode == "language_help":
            return self._compose_language(contexts)
        if mode == "study_strategy":
            return self._compose_strategy(query=query, contexts=contexts)
        if mode == "trace_source":
            return self._compose_trace(profile_id=profile_id, contexts=contexts)
        if mode == "assessment_retro":
            return self._compose_assessment_retro(contexts)
        if mode == "compare":
            return self._compose_compare(contexts)
        return self._compose_explain(contexts)

    def _compose_formula(self, contexts: list[TutorSourceContext]) -> str:
        primary = (
            next((context for context in contexts if context.context_type in {"formula", "asset"} and context.details.get("ba_ii_plus_steps")), None)
            or _first_context(contexts, {"formula", "asset"})
            or contexts[0]
        )
        details = primary.details
        formula = details.get("plain_formula") or details.get("formula_latex") or primary.title
        variables = details.get("variables") or []
        variable_text = "; ".join(
            f"{item.get('symbol')}: {item.get('meaning') or item.get('label')}"
            for item in variables
            if isinstance(item, dict) and item.get("symbol")
        )
        applies = "; ".join(details.get("applies_when") or [])
        boundaries = "; ".join(details.get("common_correct_boundary_rules") or details.get("boundary_rules") or [])
        steps = details.get("ba_ii_plus_steps") or []
        step_text = "; ".join(str(step) for step in steps)
        refs = ", ".join(primary.source_refs)
        parts = [
            f"Formula help: {details.get('correct_rule') or primary.excerpt}",
            f"Formula: {formula}.",
        ]
        if variable_text:
            parts.append(f"Variables: {variable_text}.")
        if applies:
            parts.append(f"When to apply: {applies}.")
        if boundaries:
            parts.append(f"Boundary: {boundaries}.")
        if step_text:
            parts.append(f"BA II Plus steps: {step_text}.")
        parts.append(f"Evidence: {refs or 'local source context'}." )
        parts.append("Next action: open Formula Lab for a recall-first practice pass.")
        return " ".join(parts)

    def _compose_hint(self, contexts: list[TutorSourceContext]) -> str:
        primary = _first_context(contexts, {"formula", "asset", "lexical_asset"}) or contexts[0]
        if primary.context_type == "lexical_asset":
            return (
                f"Hint 1: Look at how '{primary.title}' behaves in the example sentence. "
                "Hint 2: Decide whether it names an action, object, or quality. "
                f"Evidence: {', '.join(primary.source_refs) or 'local lexical context'}."
            )
        return (
            "Hint 1: Identify the component weights before computing anything. "
            "Hint 2: Check whether debt cost should be before-tax or after-tax. "
            "Hint 3: Match the calculator input to the valuation task, then stop before revealing the full setup. "
            f"Evidence: {', '.join(primary.source_refs) or 'local formula context'}."
        )

    def _compose_language(self, contexts: list[TutorSourceContext]) -> str:
        primary = _first_context(contexts, {"lexical_asset"}) or contexts[0]
        details = primary.details
        example = details.get("example_sentence")
        collocations = ", ".join(details.get("collocations") or [])
        usage = f" Example: {example}." if example else ""
        collocation_text = f" Collocations: {collocations}." if collocations else ""
        return (
            f"Language help: {primary.title} means {details.get('translation') or primary.excerpt}. "
            f"Definition: {details.get('definition') or primary.excerpt}.{usage}{collocation_text} "
            f"Evidence: {', '.join(primary.source_refs) or 'local dictionary context'}. "
            "Next action: review it in Language Review."
        )

    def _compose_strategy(self, *, query: str, contexts: list[TutorSourceContext]) -> str:
        minutes = _minutes(query)
        actionable = [context for context in contexts if context.launch_route]
        top = actionable[:3] or contexts[:3]
        intro = f"With {minutes} minutes, " if minutes else "For the next session, "
        lines = [
            intro + "pick the highest-actionability local signal instead of browsing for new material.",
        ]
        for index, context in enumerate(top, start=1):
            reason = context.details.get("due_reason") or context.excerpt
            lines.append(f"{index}. {context.title}: {reason} ({context.launch_route or '/review/search'}).")
        refs = _unique([ref for context in top for ref in context.source_refs])
        if refs:
            lines.append(f"Evidence: {', '.join(refs)}.")
        return " ".join(lines)

    def _compose_trace(self, *, profile_id: str, contexts: list[TutorSourceContext]) -> str:
        primary = contexts[0]
        refs = ", ".join(primary.source_refs)
        try:
            trace = KnowledgeGraphService(self.repo_root).trace(primary.node_id or "", profile_id=profile_id)
        except Exception:
            trace = {"upstream_lineage": [], "downstream_usage": [], "quality_gates": {}}
        upstream = trace.get("upstream_lineage") or []
        downstream = trace.get("downstream_usage") or []
        quality = trace.get("quality_gates") or {}
        return (
            f"Trace source: {primary.title}. Source refs: {refs or 'none recorded'}. "
            f"Upstream sources: {len(upstream)}; downstream usages: {len(downstream)}. "
            f"Quality gate: status={quality.get('status') or primary.validation_status or 'unknown'}, "
            f"quality={quality.get('quality_status') or primary.quality_status or 'unknown'}. "
            "Use the Search or Knowledge Map route to inspect the full chain."
        )

    def _compose_assessment_retro(self, contexts: list[TutorSourceContext]) -> str:
        top = _first_context(contexts, {"assessment", "transfer_gap"}) or contexts[0]
        return (
            f"Assessment retro: {top.title}. The grounded signal is {top.excerpt}. "
            "Use an assessment or mock-retro route to practice the linked gap without reusing raw wrong answers."
        )

    def _compose_compare(self, contexts: list[TutorSourceContext]) -> str:
        left = contexts[0]
        right = contexts[1] if len(contexts) > 1 else None
        if not right:
            return f"Comparison needs another grounded concept. Current evidence: {left.title} from {', '.join(left.source_refs)}."
        return (
            f"Compare: {left.title} is grounded by {left.excerpt}. "
            f"{right.title} is grounded by {right.excerpt}. "
            "Review the shared source refs before memorizing differences."
        )

    def _compose_explain(self, contexts: list[TutorSourceContext]) -> str:
        primary = contexts[0]
        related = [context.title for context in contexts[1:4]]
        related_text = f" Related concepts: {', '.join(related)}." if related else ""
        return (
            f"Explanation: {primary.excerpt}. Evidence: {', '.join(primary.source_refs) or 'local context'}. "
            f"Suggested route: {primary.launch_route or '/review/search'}.{related_text}"
        )

    def _recommended_actions(
        self,
        *,
        mode: TutorMode,
        contexts: list[TutorSourceContext],
        missing_evidence: bool,
    ) -> list[TutorRecommendedAction]:
        if missing_evidence:
            return [
                TutorRecommendedAction("Search local knowledge", "Check whether the rule exists under another title.", "/review/search", "search"),
                TutorRecommendedAction("Import or confirm assets", "Tutor cannot cite unconfirmed or missing evidence.", "/review/assets", "confirm_asset"),
                TutorRecommendedAction("Review resources", "Add source-backed notes before asking again.", "/review/resources", "confirm_resource"),
            ]
        actions: list[TutorRecommendedAction] = []
        for context in contexts:
            route = context.launch_route or "/review/search"
            if context.context_type == "formula":
                actions.append(TutorRecommendedAction("Practice in Formula Lab", f"Rehearse {context.title} with calculator steps.", "/review/formulas", "formula_practice"))
            elif context.context_type == "lexical_asset":
                actions.append(TutorRecommendedAction("Review lexical item", f"Schedule {context.title} in LanguageOS.", "/language/review", "language_review"))
            elif context.context_type == "transfer_gap":
                actions.append(TutorRecommendedAction("Resolve transfer gap", context.excerpt, "/review/mock-retro", "review"))
            elif context.context_type == "coverage":
                actions.append(TutorRecommendedAction("Close coverage gap", context.excerpt, "/review/coverage", "coverage_gap"))
            elif context.context_type == "study_plan":
                actions.append(TutorRecommendedAction("Open study plan block", context.excerpt, "/review/study-planner", "study_plan"))
            elif context.context_type == "analytics":
                actions.append(TutorRecommendedAction("Inspect analytics signal", context.excerpt, "/review/analytics", "analytics"))
            elif context.context_type == "assessment":
                actions.append(TutorRecommendedAction("Generate assessment drill", context.excerpt, "/review/assessments", "assessment"))
            elif context.context_type in {"asset", "source_segment", "resource"}:
                action_type: ActionType = "confirm_resource" if context.context_type == "resource" else "review"
                actions.append(TutorRecommendedAction("Open cited source", f"Inspect evidence for {context.title}.", route, action_type))
            if len(actions) >= 5:
                break
        actions.append(TutorRecommendedAction("Search related graph", "Trace adjacent nodes and source refs.", "/review/search", "search"))
        if mode == "study_strategy":
            actions.insert(0, TutorRecommendedAction("Open adaptive planner", "Convert the recommendation into a timed block.", "/review/study-planner", "study_plan"))
        return _dedupe_actions(actions)[:5]

    def _context_from_node(self, node: dict[str, Any], *, score: float) -> TutorSourceContext:
        details = self._details_for_node(node)
        source_refs = list(node.get("source_refs") or details.get("source_refs") or [])
        excerpt = self._excerpt_for_node(node, details)
        context_type = _context_type(node.get("node_type"))
        return TutorSourceContext(
            context_id=_stable_id("tutor-context", node.get("node_id"), source_refs[:1], excerpt[:80]),
            node_id=node.get("node_id"),
            source_ref=source_refs[0] if source_refs else None,
            context_type=context_type,
            title=str(node.get("title") or details.get("title") or "Untitled"),
            excerpt=excerpt,
            validation_status=node.get("validation_status") or details.get("validation_status"),
            quality_status=_quality_status(node, details),
            relevance_score=round(score, 4),
            launch_route=node.get("launch_route"),
            source_refs=source_refs,
            details=details,
        )

    def _details_for_node(self, node: dict[str, Any]) -> dict[str, Any]:
        metadata = dict(node.get("metadata") or {})
        node_type = node.get("node_type")
        details: dict[str, Any] = {}
        if node_type in {"asset", "formula"} and metadata.get("asset_id"):
            details = self._load_asset(str(metadata["asset_id"]))
        elif node_type == "lexical_asset" and metadata.get("lexical_id"):
            details = self._load_lexical(str(metadata["lexical_id"]))
        elif node_type in {"study_plan", "study_plan_block"}:
            details = self._load_plan_detail(metadata.get("plan_id"), metadata.get("block_id"))
        elif node_type == "transfer_gap" and metadata.get("gap_id"):
            details = self._load_transfer_gap(str(metadata["gap_id"]))
        elif node_type in {"assessment", "assessment_question"}:
            details = self._load_assessment_detail(metadata.get("assessment_id"), metadata.get("question_id"))
        details.update({key: value for key, value in metadata.items() if key not in details})
        return sanitize_public(details)

    def _excerpt_for_node(self, node: dict[str, Any], details: dict[str, Any]) -> str:
        node_type = node.get("node_type")
        if node_type in {"asset", "formula"}:
            return _trim(
                details.get("correct_rule")
                or details.get("plain_formula")
                or details.get("formula_latex")
                or node.get("title")
            )
        if node_type == "lexical_asset":
            return _trim(
                " / ".join(
                    str(item)
                    for item in [details.get("definition"), details.get("translation"), details.get("example_sentence")]
                    if item
                )
                or node.get("subtitle")
                or node.get("title")
            )
        if node_type == "study_plan_block":
            return _trim(details.get("due_reason") or node.get("subtitle") or node.get("title"))
        if node_type == "transfer_gap":
            severity = details.get("severity") or (node.get("metadata") or {}).get("severity")
            return _trim(f"{details.get('gap_type') or node.get('title')} severity {severity}")
        if node_type == "coverage_record":
            metadata = node.get("metadata") or {}
            return _trim(f"{metadata.get('coverage_status') or node.get('status')} coverage, score {metadata.get('coverage_score')}")
        if node_type == "assessment_question":
            return _trim(details.get("correct_rule") or node.get("title"))
        return _trim(node.get("subtitle") or node.get("title") or json.dumps(details, ensure_ascii=False))

    def _context_score(self, node: dict[str, Any], *, query: str, query_terms: list[str], mode: TutorMode, degree: int) -> float:
        text = _node_text(node)
        exact_query_match = _query_match_score(query, query_terms, text)
        mode_match = 1.0 if node.get("node_type") in MODE_NODE_TYPES.get(mode, set()) else 0.0
        if exact_query_match <= 0 and mode not in {"study_strategy", "assessment_retro"} and not mode_match:
            return 0.0
        if exact_query_match <= 0 and query_terms and mode not in {"study_strategy", "assessment_retro"}:
            return 0.0
        validation_quality = _validation_quality(node)
        source_quality = _source_quality(node)
        evidence_trust = _evidence_trust(node)
        graph_connectivity = min(1.0, degree / 8)
        recent_gap_or_review_relevance = _recent_relevance(node)
        route_actionability = 1.0 if node.get("launch_route") else 0.0
        score = (
            0.28 * exact_query_match
            + 0.19 * validation_quality
            + 0.16 * source_quality
            + 0.12 * evidence_trust
            + 0.12 * graph_connectivity
            + 0.08 * recent_gap_or_review_relevance
            + 0.03 * mode_match
            + 0.02 * route_actionability
        )
        return max(0.0, min(1.0, score))

    @staticmethod
    def _node_allowed(node: dict[str, Any]) -> bool:
        node_type = str(node.get("node_type") or "")
        status = str(node.get("status") or "").lower()
        validation = str(node.get("validation_status") or "").lower()
        if validation in BLOCKED_STATUSES or status in {"rejected", "blocked"}:
            return False
        if node_type in {"asset", "formula", "lexical_asset", "resource", "assessment_question"} and validation and validation not in TRUSTED_STATUSES:
            return False
        return True

    def _fallback_strategy_contexts(self, *, profile_id: str) -> list[TutorSourceContext]:
        try:
            from study_science.mission_control import MissionControlService

            summary = MissionControlService(self.repo_root).summary(profile_id=profile_id)
        except Exception:
            summary = {"recommended_actions": []}
        contexts = []
        for action in (summary.get("recommended_actions") or [])[:5]:
            contexts.append(
                TutorSourceContext(
                    context_id=_stable_id("tutor-context", "mission", action.get("action_id")),
                    node_id=None,
                    source_ref=None,
                    context_type="mission_action",
                    title=action.get("title") or "Recommended action",
                    excerpt=action.get("reason") or "Mission Control action",
                    validation_status="generated",
                    quality_status="mission_control",
                    relevance_score=0.45,
                    launch_route=action.get("href") or "/review/mission-control",
                    source_refs=[],
                    details={"action_id": action.get("action_id"), "priority": action.get("priority")},
                )
            )
        return contexts

    def _load_asset(self, asset_id: str) -> dict[str, Any]:
        return _read_json(self.review_root / "asset-candidates" / f"{asset_id}.json", default={})

    def _load_lexical(self, lexical_id: str) -> dict[str, Any]:
        return _read_json(self.language_root / "lexical-assets" / f"{lexical_id}.json", default={})

    def _load_transfer_gap(self, gap_id: str) -> dict[str, Any]:
        return _read_json(self.review_root / "mock-retro" / "transfer-gaps" / f"{gap_id}.json", default={})

    def _load_plan_detail(self, plan_id: Any, block_id: Any) -> dict[str, Any]:
        if not plan_id:
            return {}
        plan = _read_json(self.planner_root / f"{plan_id}.json", default={})
        if block_id:
            for block in plan.get("blocks", []):
                if block.get("block_id") == block_id:
                    return {**block, "plan_id": plan_id, "available_minutes": plan.get("available_minutes")}
        return plan

    def _load_assessment_detail(self, assessment_id: Any, question_id: Any) -> dict[str, Any]:
        if not assessment_id:
            return {}
        session = _read_json(self.memory_root / "assessments" / "sessions" / f"{assessment_id}.json", default={})
        if question_id:
            for question in session.get("questions", []):
                if question.get("question_id") == question_id:
                    return question
        return session

    def _safety_flags(self, *, missing_evidence: bool) -> list[str]:
        flags = ["deterministic_local_answer", "correct_only_payload", "external_network_disabled", "llm_provider_disabled"]
        if missing_evidence:
            flags.append("missing_evidence")
        return flags

    def _read_conversations(self) -> list[TutorConversation]:
        rows = []
        for path in self.conversation_root.glob("*.json"):
            conversation = self._read_conversation(path.stem)
            if conversation:
                rows.append(conversation)
        return rows

    def _read_conversation(self, conversation_id: str) -> TutorConversation | None:
        path = self.conversation_root / f"{conversation_id}.json"
        if not path.exists():
            return None
        return TutorConversation.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _write_conversation(self, conversation: TutorConversation) -> None:
        self.conversation_root.mkdir(parents=True, exist_ok=True)
        (self.conversation_root / f"{conversation.conversation_id}.json").write_text(
            json.dumps(conversation.as_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def sanitize_public(payload: Any) -> Any:
    sanitized, _ = sanitize_payload(payload)
    return _strip_remaining_sensitive_keys(sanitized)


def _strip_remaining_sensitive_keys(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: _strip_remaining_sensitive_keys(value)
            for key, value in payload.items()
            if not is_forbidden_key(key)
        }
    if isinstance(payload, list):
        return [_strip_remaining_sensitive_keys(item) for item in payload]
    return payload


def _context_type(node_type: str | None) -> ContextType:
    return {
        "formula": "formula",
        "asset": "asset",
        "syllabus_topic": "syllabus_topic",
        "coverage_record": "coverage",
        "transfer_gap": "transfer_gap",
        "resource": "resource",
        "source_segment": "source_segment",
        "source_document": "resource",
        "lexical_asset": "lexical_asset",
        "assessment": "assessment",
        "assessment_question": "assessment",
        "study_plan": "study_plan",
        "study_plan_block": "study_plan",
        "analytics_record": "analytics",
        "mission_action": "mission_action",
    }.get(str(node_type), "asset")


def _quality_status(node: dict[str, Any], details: dict[str, Any]) -> str | None:
    metadata = node.get("metadata") or {}
    for key in ("quality_status", "resource_quality_status", "dictionary_quality_status"):
        if metadata.get(key):
            return str(metadata[key])
        if details.get(key):
            return str(details[key])
    if node.get("quality_score") is not None:
        return "scored"
    return None


def _node_text(node: dict[str, Any]) -> str:
    metadata = node.get("metadata") or {}
    return " ".join(
        [
            str(node.get("title") or ""),
            str(node.get("subtitle") or ""),
            str(node.get("status") or ""),
            str(node.get("validation_status") or ""),
            " ".join(str(ref) for ref in node.get("source_refs") or []),
            json.dumps(metadata, ensure_ascii=False),
        ]
    ).lower()


def _query_match_score(query: str, terms: list[str], text: str) -> float:
    q = query.strip().lower()
    if not q:
        return 0.25
    if q in text:
        return 1.0
    if not terms:
        return 0.0
    hits = sum(1 for term in terms if term in text)
    if hits == 0:
        return 0.0
    return min(1.0, hits / max(1, len(terms)))


def _validation_quality(node: dict[str, Any]) -> float:
    status = str(node.get("validation_status") or node.get("status") or "").lower()
    if status in {"confirmed", "validated"}:
        return 1.0
    if status in {"derived", "generated", "completed", "active", "open", "extracted"}:
        return 0.8
    if not status:
        return 0.55
    return 0.2


def _source_quality(node: dict[str, Any]) -> float:
    has_source = bool(node.get("source_refs"))
    score = node.get("quality_score")
    if score is not None:
        try:
            value = float(score)
            normalized = max(0.0, min(1.0, value if value <= 1 else value / 100))
            return normalized if has_source else min(normalized, 0.45)
        except (TypeError, ValueError):
            pass
    return 0.7 if has_source else 0.2


def _evidence_trust(node: dict[str, Any]) -> float:
    status = str(node.get("validation_status") or node.get("status") or "").lower()
    has_source = bool(node.get("source_refs"))
    if status in {"confirmed", "validated"} and has_source:
        return 1.0
    if status in {"derived", "completed", "active", "open", "extracted"} and has_source:
        return 0.82
    if status == "generated" and has_source:
        return 0.62
    if status == "generated":
        return 0.25
    if has_source:
        return 0.55
    return 0.15


def _recent_relevance(node: dict[str, Any]) -> float:
    node_type = node.get("node_type")
    status = str(node.get("status") or "").lower()
    if node_type in {"transfer_gap", "study_plan_block", "mission_action", "analytics_record"}:
        return 1.0
    if status in {"open", "weak", "missing", "partial", "stale", "pending", "learning"}:
        return 0.85
    return 0.35


def _degree_map(edges: list[dict[str, Any]]) -> dict[str, int]:
    degree: dict[str, int] = {}
    for edge in edges:
        for key in ("from_node_id", "to_node_id"):
            node_id = edge.get(key)
            if node_id:
                degree[str(node_id)] = degree.get(str(node_id), 0) + 1
    return degree


def _terms(query: str) -> list[str]:
    stop = {"the", "and", "with", "for", "what", "should", "only", "have", "explain", "show", "source", "give", "hint"}
    return [term for term in re.findall(r"[a-zA-Z0-9_+-]{2,}", query.lower()) if term not in stop]


def _minutes(query: str) -> int | None:
    match = re.search(r"(\d+)\s*(?:minutes?|mins?)", query.lower())
    return int(match.group(1)) if match else None


def _first_context(contexts: list[TutorSourceContext], types: set[str]) -> TutorSourceContext | None:
    return next((context for context in contexts if context.context_type in types), None)


def _dedupe_actions(actions: list[TutorRecommendedAction]) -> list[TutorRecommendedAction]:
    seen: set[tuple[str, str]] = set()
    ordered: list[TutorRecommendedAction] = []
    for action in actions:
        key = (action.title, action.launch_route)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(action)
    return ordered


def _mode(mode: Any) -> TutorMode:
    allowed = {
        "explain",
        "hint",
        "compare",
        "formula_help",
        "study_strategy",
        "language_help",
        "trace_source",
        "assessment_retro",
        "general",
    }
    text = str(mode or "general")
    return text if text in allowed else "general"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: object) -> str:
    digest = hashlib.sha256("::".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _read_json(path: Path, default: Any) -> Any:
    try:
        return sanitize_public(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return default


def _trim(value: Any, limit: int = 420) -> str:
    text = str(value or "").strip()
    return text if len(text) <= limit else f"{text[: limit - 1]}..."


def _unique(items: list[Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item is None:
            continue
        text = str(item)
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered
