"""Local knowledge graph, search, and traceability projection.

The projector is deliberately read-only against existing subsystem stores. It
builds a cached graph projection under `.system/memory/knowledge-graph` and
sanitizes public payloads so wrong-answer phrases never become learning
content.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha1
import json
import re
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, sanitize_payload


NodeType = Literal[
    "source_file",
    "source_document",
    "source_segment",
    "resource",
    "asset",
    "formula",
    "syllabus_topic",
    "coverage_record",
    "transfer_gap",
    "assessment",
    "assessment_question",
    "lexical_asset",
    "study_plan",
    "study_plan_block",
    "analytics_record",
    "mission_action",
]

EdgeType = Literal[
    "derived_from",
    "supported_by",
    "covers",
    "requires",
    "tests",
    "revealed_gap",
    "addresses_gap",
    "promoted_to",
    "reviewed_in",
    "planned_by",
    "measured_by",
    "same_formula_family",
    "same_syllabus_topic",
    "same_source_ref",
    "lexical_relation",
    "recommended_next",
]

WRONG_KEYS = FORBIDDEN_SAFE_PAYLOAD_KEYS
UPSTREAM_EDGE_TYPES = {"derived_from", "supported_by", "requires", "planned_by", "measured_by"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(text.encode('utf-8')).hexdigest()[:16]}"


def _node_id(node_type: str, raw_id: Any) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(raw_id or "unknown")).strip("-")
    return f"{node_type}:{safe or _stable_id('node', node_type, raw_id)}"


@dataclass(slots=True)
class KnowledgeGraphNode:
    node_id: str
    profile_id: str
    node_type: NodeType
    title: str
    subtitle: str | None = None
    status: str | None = None
    quality_score: float | None = None
    validation_status: str | None = None
    source_refs: list[str] = field(default_factory=list)
    launch_route: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return strip_graph_payload(
            {
                "node_id": self.node_id,
                "profile_id": self.profile_id,
                "node_type": self.node_type,
                "title": self.title,
                "subtitle": self.subtitle,
                "status": self.status,
                "quality_score": self.quality_score,
                "validation_status": self.validation_status,
                "source_refs": self.source_refs,
                "launch_route": self.launch_route,
                "metadata": self.metadata,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> KnowledgeGraphNode:
        return cls(
            node_id=str(payload.get("node_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            node_type=payload.get("node_type", "asset"),
            title=str(payload.get("title") or "Untitled"),
            subtitle=payload.get("subtitle"),
            status=payload.get("status"),
            quality_score=_float_or_none(payload.get("quality_score")),
            validation_status=payload.get("validation_status"),
            source_refs=list(payload.get("source_refs") or []),
            launch_route=payload.get("launch_route"),
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True)
class KnowledgeGraphEdge:
    edge_id: str
    profile_id: str
    from_node_id: str
    to_node_id: str
    edge_type: EdgeType
    confidence: float
    reason: str
    source_refs: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now)

    def as_dict(self) -> dict[str, Any]:
        return strip_graph_payload(
            {
                "edge_id": self.edge_id,
                "profile_id": self.profile_id,
                "from_node_id": self.from_node_id,
                "to_node_id": self.to_node_id,
                "edge_type": self.edge_type,
                "confidence": self.confidence,
                "reason": self.reason,
                "source_refs": self.source_refs,
                "created_at": self.created_at,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> KnowledgeGraphEdge:
        return cls(
            edge_id=str(payload.get("edge_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            from_node_id=str(payload.get("from_node_id", "")),
            to_node_id=str(payload.get("to_node_id", "")),
            edge_type=payload.get("edge_type", "derived_from"),
            confidence=float(payload.get("confidence", 0.0) or 0.0),
            reason=str(payload.get("reason") or ""),
            source_refs=list(payload.get("source_refs") or []),
            created_at=str(payload.get("created_at") or _now()),
        )


class KnowledgeGraphService:
    """Builds a deterministic local projection across learning subsystems."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.review_root = self.repo_root / ".system" / "memory" / "review"
        self.language_root = self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel"
        self.assessment_root = self.repo_root / ".system" / "memory" / "assessments" / "sessions"
        self.planner_root = self.repo_root / ".system" / "memory" / "study-planner" / "plans"
        self.graph_root = self.repo_root / ".system" / "memory" / "knowledge-graph"
        self.graph_root.mkdir(parents=True, exist_ok=True)
        self.nodes: dict[str, KnowledgeGraphNode] = {}
        self.edges: dict[str, KnowledgeGraphEdge] = {}
        self.source_ref_index: dict[str, set[str]] = {}
        self.asset_index: dict[str, str] = {}
        self.formula_by_asset: dict[str, str] = {}
        self.topic_index: dict[str, str] = {}
        self.lexical_index: dict[str, str] = {}
        self.gap_index: dict[str, str] = {}
        self.assessment_index: dict[str, str] = {}

    def recompute(self, *, profile_id: str = "default") -> dict[str, Any]:
        graph = self.project(profile_id=profile_id or "default")
        self._graph_path(profile_id).write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
        return graph

    def summary(self, *, profile_id: str = "default") -> dict[str, Any]:
        return self._ensure_graph(profile_id)["summary"]

    def nodes_query(
        self,
        *,
        profile_id: str = "default",
        node_type: str | None = None,
        validation_status: str | None = None,
        quality_status: str | None = None,
        source_ref: str | None = None,
        limit: int = 200,
    ) -> dict[str, Any]:
        graph = self._ensure_graph(profile_id)
        nodes = [KnowledgeGraphNode.from_dict(item) for item in graph["nodes"]]
        filtered = self._filter_nodes(nodes, node_type=node_type, validation_status=validation_status, quality_status=quality_status, source_ref=source_ref)
        return {"profile_id": profile_id, "count": len(filtered), "nodes": [node.as_dict() for node in filtered[:limit]]}

    def get_node(self, node_id: str, *, profile_id: str = "default") -> dict[str, Any] | None:
        graph = self._ensure_graph(profile_id)
        for node in graph["nodes"]:
            if node.get("node_id") == node_id:
                return strip_graph_payload(node)
        return None

    def edges_query(
        self,
        *,
        profile_id: str = "default",
        edge_type: str | None = None,
        from_node_id: str | None = None,
        to_node_id: str | None = None,
        limit: int = 500,
    ) -> dict[str, Any]:
        graph = self._ensure_graph(profile_id)
        edges = [KnowledgeGraphEdge.from_dict(item) for item in graph["edges"]]
        if edge_type:
            edges = [edge for edge in edges if edge.edge_type == edge_type]
        if from_node_id:
            edges = [edge for edge in edges if edge.from_node_id == from_node_id]
        if to_node_id:
            edges = [edge for edge in edges if edge.to_node_id == to_node_id]
        return {"profile_id": profile_id, "count": len(edges), "edges": [edge.as_dict() for edge in edges[:limit]]}

    def search(
        self,
        *,
        profile_id: str = "default",
        query: str = "",
        node_type: str | None = None,
        validation_status: str | None = None,
        quality_status: str | None = None,
        module: str | None = None,
        topic: str | None = None,
        source_ref: str | None = None,
        limit: int = 25,
    ) -> dict[str, Any]:
        graph = self._ensure_graph(profile_id)
        nodes = [KnowledgeGraphNode.from_dict(item) for item in graph["nodes"]]
        edges = [KnowledgeGraphEdge.from_dict(item) for item in graph["edges"]]
        filtered = self._filter_nodes(nodes, node_type=node_type, validation_status=validation_status, quality_status=quality_status, source_ref=source_ref)
        if module:
            filtered = [node for node in filtered if module.lower() in str(node.metadata.get("module", "")).lower()]
        if topic:
            filtered = [node for node in filtered if topic.lower() in f"{node.metadata.get('topic_id', '')} {node.title} {node.subtitle or ''}".lower()]

        results = []
        for node in filtered:
            score = self._rank(node, query=query, source_ref=source_ref)
            if query and score <= 0:
                continue
            connected = self._connected_nodes(node.node_id, nodes=nodes, edges=edges, limit=4)
            results.append({"node": node.as_dict(), "score": round(score, 4), "connected_nodes": connected})
        results.sort(key=lambda item: item["score"], reverse=True)
        return {"profile_id": profile_id, "query": query, "count": len(results), "results": results[:limit]}

    def trace(self, node_id: str, *, profile_id: str = "default") -> dict[str, Any]:
        graph = self._ensure_graph(profile_id)
        nodes = {item["node_id"]: KnowledgeGraphNode.from_dict(item) for item in graph["nodes"]}
        edges = [KnowledgeGraphEdge.from_dict(item) for item in graph["edges"]]
        node = nodes.get(node_id)
        if node is None:
            raise KeyError(node_id)

        outgoing = [edge for edge in edges if edge.from_node_id == node_id]
        incoming = [edge for edge in edges if edge.to_node_id == node_id]
        upstream_ids = [edge.to_node_id for edge in outgoing if edge.edge_type in UPSTREAM_EDGE_TYPES or edge.edge_type in {"same_source_ref"}]
        downstream_ids = [edge.from_node_id for edge in incoming]
        downstream_ids.extend(edge.to_node_id for edge in outgoing if edge.edge_type in {"tests", "revealed_gap", "recommended_next", "covers"})
        related_ids = [
            edge.to_node_id if edge.from_node_id == node_id else edge.from_node_id
            for edge in edges
            if node_id in {edge.from_node_id, edge.to_node_id}
            and edge.edge_type in {"same_formula_family", "same_syllabus_topic", "same_source_ref", "lexical_relation"}
        ]
        related_ids.extend(self._same_source_ref_neighbors(node, nodes.values()))
        related_ids = [item for item in _unique(related_ids) if item != node_id and item not in set(upstream_ids) and item not in set(downstream_ids)]

        return strip_graph_payload(
            {
                "profile_id": profile_id,
                "node": node.as_dict(),
                "source_refs": node.source_refs,
                "upstream_lineage": [nodes[item].as_dict() for item in _unique(upstream_ids) if item in nodes],
                "downstream_usage": [nodes[item].as_dict() for item in _unique(downstream_ids) if item in nodes],
                "related_nodes": [nodes[item].as_dict() for item in related_ids[:25] if item in nodes],
                "quality_gates": {
                    "status": node.status,
                    "validation_status": node.validation_status,
                    "quality_score": node.quality_score,
                    "quality_status": node.metadata.get("quality_status") or node.metadata.get("resource_quality_status") or node.metadata.get("dictionary_quality_status"),
                    "blocked_reason": node.metadata.get("blocked_reason"),
                },
                "edges": [edge.as_dict() for edge in outgoing + incoming],
            }
        )

    def related(self, node_id: str, *, profile_id: str = "default", limit: int = 50) -> dict[str, Any]:
        trace = self.trace(node_id, profile_id=profile_id)
        nodes = trace["related_nodes"] + trace["upstream_lineage"] + trace["downstream_usage"]
        seen = set()
        ordered = []
        for node in nodes:
            if node["node_id"] in seen:
                continue
            seen.add(node["node_id"])
            ordered.append(node)
        return {"profile_id": profile_id, "node_id": node_id, "count": len(ordered), "nodes": ordered[:limit]}

    def impact(self, node_id: str, *, profile_id: str = "default", limit: int = 100) -> dict[str, Any]:
        graph = self._ensure_graph(profile_id)
        nodes = {item["node_id"]: KnowledgeGraphNode.from_dict(item) for item in graph["nodes"]}
        edges = [KnowledgeGraphEdge.from_dict(item) for item in graph["edges"]]
        if node_id not in nodes:
            raise KeyError(node_id)
        reverse: dict[str, list[KnowledgeGraphEdge]] = {}
        for edge in edges:
            reverse.setdefault(edge.to_node_id, []).append(edge)
        affected: list[str] = []
        queue: deque[str] = deque([node_id])
        seen = {node_id}
        while queue and len(affected) < limit:
            current = queue.popleft()
            for edge in reverse.get(current, []):
                candidate = edge.from_node_id
                if candidate in seen:
                    continue
                seen.add(candidate)
                affected.append(candidate)
                queue.append(candidate)
        affected_nodes = [nodes[item].as_dict() for item in affected if item in nodes]
        return strip_graph_payload(
            {
                "profile_id": profile_id,
                "node": nodes[node_id].as_dict(),
                "affected_count": len(affected_nodes),
                "affected_nodes": affected_nodes,
                "impact_notes": self._impact_notes(nodes[node_id], affected_nodes),
            }
        )

    def project(self, *, profile_id: str = "default") -> dict[str, Any]:
        self.nodes = {}
        self.edges = {}
        self.source_ref_index = {}
        self.asset_index = {}
        self.formula_by_asset = {}
        self.topic_index = {}
        self.lexical_index = {}
        self.gap_index = {}
        self.assessment_index = {}

        self._project_sources(profile_id)
        self._project_resources(profile_id)
        self._project_assets(profile_id)
        self._project_syllabus(profile_id)
        self._project_transfer_gaps(profile_id)
        self._project_lexical_assets(profile_id)
        self._project_assessments(profile_id)
        self._project_study_plans(profile_id)
        self._project_analytics(profile_id)
        self._project_mission_actions(profile_id)
        self._add_source_ref_edges(profile_id)
        self._add_formula_family_edges(profile_id)

        nodes = [node.as_dict() for node in sorted(self.nodes.values(), key=lambda item: (item.node_type, item.title, item.node_id))]
        edges = [edge.as_dict() for edge in sorted(self.edges.values(), key=lambda item: (item.edge_type, item.from_node_id, item.to_node_id))]
        summary = self._summary(nodes, edges, profile_id=profile_id)
        return strip_graph_payload({"profile_id": profile_id, "generated_at": _now(), "summary": summary, "nodes": nodes, "edges": edges})

    def _project_sources(self, profile_id: str) -> None:
        for path in (self.review_root / "asset-sources").glob("*.json"):
            source = self._read_json(path)
            if not self._profile_matches(source, profile_id):
                continue
            source_id = source.get("source_id") or path.stem
            node = self._add_node(
                node_type="source_document",
                raw_id=source_id,
                profile_id=source.get("profile_id") or profile_id,
                title=source.get("title") or source_id,
                subtitle=source.get("source_type"),
                status=source.get("extraction_status"),
                source_refs=list(source.get("source_refs") or []),
                launch_route="/review/assets",
                metadata={
                    "source_id": source_id,
                    "source_type": source.get("source_type"),
                    "file_path": source.get("file_path"),
                    "imported_at": source.get("imported_at"),
                    "content_hash": source.get("content_hash"),
                },
            )
            for ref in node.source_refs:
                self._index_source_ref(ref, node.node_id)

        for path in (self.review_root / "asset-segments").glob("*.json"):
            segments = self._read_json(path, default=[])
            for segment in segments if isinstance(segments, list) else []:
                source_id = segment.get("source_id") or path.stem
                segment_id = segment.get("segment_id") or _stable_id("segment", source_id, segment.get("source_ref"))
                node = self._add_node(
                    node_type="source_segment",
                    raw_id=segment_id,
                    profile_id=profile_id,
                    title=self._trim(segment.get("text") or segment.get("heading") or segment_id, 96),
                    subtitle=segment.get("evidence_type"),
                    status="extracted",
                    quality_score=_float_or_none(segment.get("confidence")),
                    source_refs=[segment.get("source_ref")] if segment.get("source_ref") else [],
                    launch_route="/review/assets",
                    metadata={
                        "segment_id": segment_id,
                        "source_id": source_id,
                        "page": segment.get("page"),
                        "heading": segment.get("heading"),
                        "evidence_type": segment.get("evidence_type"),
                    },
                )
                for ref in node.source_refs:
                    self._index_source_ref(ref, node.node_id)
                source_node_id = _node_id("source_document", source_id)
                if source_node_id in self.nodes:
                    self._add_edge(node.node_id, source_node_id, "derived_from", 0.99, "segment extracted from source document", node.source_refs, profile_id)

    def _project_resources(self, profile_id: str) -> None:
        for path in (self.review_root / "resources").glob("*.json"):
            resource = self._read_json(path)
            if not self._profile_matches(resource, profile_id):
                continue
            resource_id = resource.get("resource_id") or path.stem
            quality = resource.get("quality_gate") or resource.get("quality") or {}
            quality_status = resource.get("quality_status") or quality.get("recommendation") or quality.get("status")
            node = self._add_node(
                node_type="resource",
                raw_id=resource_id,
                profile_id=resource.get("profile_id") or profile_id,
                title=resource.get("title") or resource_id,
                subtitle=resource.get("resource_type"),
                status=resource.get("validation_status") or resource.get("status"),
                quality_score=_float_or_none(quality.get("normalized_score") or quality.get("overall_score") or resource.get("quality_score")),
                validation_status=resource.get("validation_status"),
                source_refs=list(resource.get("source_refs") or []),
                launch_route="/review/resources",
                metadata={
                    "resource_id": resource_id,
                    "resource_type": resource.get("resource_type"),
                    "quality_status": quality_status,
                    "origin": resource.get("origin"),
                    "url": resource.get("url"),
                },
            )
            for ref in node.source_refs:
                self._index_source_ref(ref, node.node_id)

    def _project_assets(self, profile_id: str) -> None:
        for path in (self.review_root / "asset-candidates").glob("*.json"):
            asset = self._read_json(path)
            if not self._profile_matches(asset, profile_id):
                continue
            asset_id = asset.get("asset_id") or path.stem
            asset_type = asset.get("asset_type") or "asset"
            source_refs = list(asset.get("source_refs") or [])
            asset_node = self._add_node(
                node_type="asset",
                raw_id=asset_id,
                profile_id=asset.get("profile_id") or profile_id,
                title=asset.get("title") or asset.get("trigger") or asset_id,
                subtitle=asset_type,
                status=asset.get("mastery_state") or asset.get("status"),
                quality_score=_float_or_none(asset.get("source_quality")),
                validation_status=asset.get("validation_status"),
                source_refs=source_refs,
                launch_route="/review/assets",
                metadata={
                    "asset_id": asset_id,
                    "asset_type": asset_type,
                    "module": asset.get("module"),
                    "subject": asset.get("subject"),
                    "los": asset.get("los"),
                    "formula_family": asset.get("formula_family"),
                    "syllabus_topic_id": asset.get("syllabus_topic_id"),
                    "resource_id": asset.get("resource_id"),
                    "resource_quality_status": asset.get("resource_quality_status"),
                    "created_from": asset.get("created_from"),
                },
            )
            self.asset_index[asset_id] = asset_node.node_id
            for ref in source_refs:
                self._index_source_ref(ref, asset_node.node_id)
                for segment_id in self.source_ref_index.get(ref, set()):
                    if segment_id != asset_node.node_id and self.nodes.get(segment_id, None) and self.nodes[segment_id].node_type == "source_segment":
                        self._add_edge(asset_node.node_id, segment_id, "supported_by", 0.92, "asset cites source segment", [ref], profile_id)
            if asset.get("resource_id") and _node_id("resource", asset.get("resource_id")) in self.nodes:
                self._add_edge(asset_node.node_id, _node_id("resource", asset.get("resource_id")), "promoted_to", 0.8, "asset promoted from resource evidence", source_refs, profile_id)
            if asset.get("syllabus_topic_id"):
                topic_id = asset.get("syllabus_topic_id")
                self._add_edge(asset_node.node_id, _node_id("syllabus_topic", topic_id), "covers", 0.8, "asset declares syllabus topic", source_refs, profile_id)
            if asset_type == "formula" or asset.get("formula_latex") or asset.get("plain_formula"):
                formula_node = self._add_node(
                    node_type="formula",
                    raw_id=asset_id,
                    profile_id=asset.get("profile_id") or profile_id,
                    title=asset.get("plain_formula") or asset.get("formula_latex") or asset.get("title") or asset_id,
                    subtitle=asset.get("formula_family") or asset.get("title"),
                    status=asset.get("mastery_state"),
                    quality_score=_float_or_none(asset.get("source_quality")),
                    validation_status=asset.get("validation_status"),
                    source_refs=source_refs,
                    launch_route="/review/formulas",
                    metadata={
                        "asset_id": asset_id,
                        "formula_family": asset.get("formula_family"),
                        "module": asset.get("module"),
                        "ba_ii_plus_steps_count": len(asset.get("ba_ii_plus_steps") or []),
                        "plain_formula": asset.get("plain_formula"),
                    },
                )
                self.formula_by_asset[asset_id] = formula_node.node_id
                self._add_edge(formula_node.node_id, asset_node.node_id, "derived_from", 0.99, "formula metadata projected from asset", source_refs, profile_id)

    def _project_syllabus(self, profile_id: str) -> None:
        topics_payload = self._read_json(self.review_root / "syllabus" / "topics.json", default=[])
        for topic in topics_payload if isinstance(topics_payload, list) else []:
            if not self._profile_matches(topic, profile_id):
                continue
            self._add_topic_node(topic, profile_id)

        for path in (self.review_root / "syllabus").glob("coverage-*.json"):
            coverage = self._read_json(path)
            if coverage.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            for record in coverage.get("records", []):
                topic = record.get("topic") or {}
                if topic:
                    self._add_topic_node(topic, profile_id)
                record_id = record.get("record_id") or _stable_id("coverage", record.get("topic_id"))
                node = self._add_node(
                    node_type="coverage_record",
                    raw_id=record_id,
                    profile_id=record.get("profile_id") or profile_id,
                    title=f"Coverage: {topic.get('title') or record.get('topic_id') or record_id}",
                    subtitle=record.get("coverage_status"),
                    status=record.get("coverage_status"),
                    quality_score=_float_or_none(record.get("coverage_score")),
                    source_refs=list(topic.get("source_refs") or []),
                    launch_route="/review/coverage",
                    metadata={
                        "record_id": record_id,
                        "topic_id": record.get("topic_id"),
                        "coverage_status": record.get("coverage_status"),
                        "coverage_score": record.get("coverage_score"),
                        "confirmed_asset_count": record.get("confirmed_asset_count"),
                        "missing_asset_types": list(record.get("missing_asset_types") or []),
                        "exam_weight": topic.get("exam_weight"),
                    },
                )
                topic_node_id = _node_id("syllabus_topic", record.get("topic_id"))
                if topic_node_id in self.nodes:
                    self._add_edge(node.node_id, topic_node_id, "measured_by", 0.98, "coverage record measures syllabus topic", node.source_refs, profile_id)
                for link in record.get("links", []):
                    asset_node_id = self.asset_index.get(link.get("asset_id")) or _node_id("asset", link.get("asset_id"))
                    if asset_node_id in self.nodes and topic_node_id in self.nodes:
                        self._add_edge(asset_node_id, topic_node_id, "covers", _float_or_none(link.get("confidence")) or 0.7, link.get("match_reason") or "coverage link", [], profile_id)
                        self._add_edge(node.node_id, asset_node_id, "measured_by", 0.7, "coverage includes asset", [], profile_id)

    def _project_transfer_gaps(self, profile_id: str) -> None:
        for path in (self.review_root / "mock-retro" / "transfer-gaps").glob("transfer-gap-*.json"):
            gap = self._read_json(path)
            if not self._profile_matches(gap, profile_id):
                continue
            gap_id = gap.get("gap_id") or path.stem
            node = self._add_node(
                node_type="transfer_gap",
                raw_id=gap_id,
                profile_id=gap.get("profile_id") or profile_id,
                title=gap.get("gap_type") or gap_id,
                subtitle=gap.get("formula_family") or gap.get("topic_id"),
                status=gap.get("status"),
                quality_score=_float_or_none(gap.get("severity")),
                source_refs=list(gap.get("source_refs") or []),
                launch_route="/review/mock-retro",
                metadata={
                    "gap_id": gap_id,
                    "gap_type": gap.get("gap_type"),
                    "topic_id": gap.get("topic_id"),
                    "asset_id": gap.get("asset_id"),
                    "formula_family": gap.get("formula_family"),
                    "severity": gap.get("severity"),
                    "evidence_count": gap.get("evidence_count"),
                },
            )
            self.gap_index[gap_id] = node.node_id
            asset_node_id = self.asset_index.get(gap.get("asset_id"))
            if asset_node_id:
                self._add_edge(node.node_id, asset_node_id, "revealed_gap", 0.9, "gap is linked to asset", node.source_refs, profile_id)
            formula_node_id = self.formula_by_asset.get(gap.get("asset_id"))
            if formula_node_id:
                self._add_edge(node.node_id, formula_node_id, "revealed_gap", 0.9, "gap is linked to formula asset", node.source_refs, profile_id)
            topic_node_id = self.topic_index.get(gap.get("topic_id"))
            if topic_node_id:
                self._add_edge(node.node_id, topic_node_id, "same_syllabus_topic", 0.72, "gap shares syllabus topic", node.source_refs, profile_id)

    def _project_lexical_assets(self, profile_id: str) -> None:
        for path in (self.language_root / "dictionaries").glob("*.json"):
            dictionary = self._read_json(path)
            if not self._profile_matches(dictionary, profile_id):
                continue
            dictionary_id = dictionary.get("dictionary_id") or path.stem
            self._add_node(
                node_type="source_document",
                raw_id=dictionary_id,
                profile_id=dictionary.get("profile_id") or profile_id,
                title=dictionary.get("title") or dictionary_id,
                subtitle=dictionary.get("dictionary_type") or "dictionary",
                status=dictionary.get("validation_status"),
                quality_score=_float_or_none(dictionary.get("quality_score")),
                validation_status=dictionary.get("validation_status"),
                source_refs=list(dictionary.get("source_refs") or []),
                launch_route="/language/dictionaries",
                metadata={"dictionary_id": dictionary_id, "dictionary_type": dictionary.get("dictionary_type")},
            )
        for path in (self.language_root / "lexical-assets").glob("*.json"):
            lexical = self._read_json(path)
            if not self._profile_matches(lexical, profile_id):
                continue
            lexical_id = lexical.get("lexical_id") or path.stem
            node = self._add_node(
                node_type="lexical_asset",
                raw_id=lexical_id,
                profile_id=lexical.get("profile_id") or profile_id,
                title=lexical.get("headword") or lexical_id,
                subtitle=lexical.get("translation") or lexical.get("definition"),
                status=lexical.get("mastery_state"),
                quality_score=_float_or_none(lexical.get("quality_score")),
                validation_status=lexical.get("validation_status"),
                source_refs=list(lexical.get("source_refs") or []),
                launch_route="/language/review",
                metadata={
                    "lexical_id": lexical_id,
                    "dictionary_id": lexical.get("dictionary_id"),
                    "language": lexical.get("language"),
                    "target_language": lexical.get("target_language"),
                    "part_of_speech": lexical.get("part_of_speech"),
                    "dictionary_quality_status": lexical.get("dictionary_quality_status"),
                },
            )
            self.lexical_index[lexical_id] = node.node_id
            dictionary_node_id = _node_id("source_document", lexical.get("dictionary_id"))
            if dictionary_node_id in self.nodes:
                self._add_edge(node.node_id, dictionary_node_id, "derived_from", 0.95, "lexical asset derived from dictionary", node.source_refs, profile_id)

    def _project_assessments(self, profile_id: str) -> None:
        for path in self.assessment_root.glob("assessment-*.json"):
            session = self._read_json(path)
            if not self._profile_matches(session, profile_id):
                continue
            assessment_id = session.get("assessment_id") or path.stem
            assessment_node = self._add_node(
                node_type="assessment",
                raw_id=assessment_id,
                profile_id=session.get("profile_id") or profile_id,
                title=session.get("title") or assessment_id,
                subtitle=session.get("mode"),
                status=session.get("status"),
                quality_score=_float_or_none((session.get("summary") or {}).get("score")),
                source_refs=[],
                launch_route="/review/assessments",
                metadata={
                    "assessment_id": assessment_id,
                    "mode": session.get("mode"),
                    "question_count": len(session.get("questions") or []),
                    "transfer_gaps_created": (session.get("summary") or {}).get("transfer_gaps_created"),
                },
            )
            self.assessment_index[assessment_id] = assessment_node.node_id
            for question in session.get("questions", []):
                question_id = question.get("question_id")
                if not question_id:
                    continue
                q_node = self._add_node(
                    node_type="assessment_question",
                    raw_id=question_id,
                    profile_id=question.get("profile_id") or session.get("profile_id") or profile_id,
                    title=question.get("prompt") or question_id,
                    subtitle=question.get("question_type"),
                    status=question.get("validation_status"),
                    validation_status=question.get("validation_status"),
                    source_refs=list(question.get("source_refs") or []),
                    launch_route="/review/assessments",
                    metadata={
                        "question_id": question_id,
                        "assessment_id": assessment_id,
                        "question_type": question.get("question_type"),
                        "category": question.get("category"),
                        "correct_rule": question.get("correct_rule"),
                    },
                )
                self._add_edge(q_node.node_id, assessment_node.node_id, "reviewed_in", 0.99, "question belongs to assessment", q_node.source_refs, profile_id)
                for asset_id in question.get("linked_asset_ids") or []:
                    if asset_id in self.asset_index:
                        self._add_edge(q_node.node_id, self.asset_index[asset_id], "tests", 0.9, "question tests linked asset", q_node.source_refs, profile_id)
                    if asset_id in self.formula_by_asset:
                        self._add_edge(q_node.node_id, self.formula_by_asset[asset_id], "tests", 0.92, "question tests formula", q_node.source_refs, profile_id)
                for topic_id in question.get("linked_topic_ids") or []:
                    if topic_id in self.topic_index:
                        self._add_edge(q_node.node_id, self.topic_index[topic_id], "tests", 0.8, "question tests syllabus topic", q_node.source_refs, profile_id)
                for gap_id in question.get("linked_gap_ids") or []:
                    if gap_id in self.gap_index:
                        self._add_edge(q_node.node_id, self.gap_index[gap_id], "addresses_gap", 0.82, "question addresses transfer gap", q_node.source_refs, profile_id)
                for lexical_id in question.get("linked_lexical_ids") or []:
                    if lexical_id in self.lexical_index:
                        self._add_edge(q_node.node_id, self.lexical_index[lexical_id], "tests", 0.88, "question tests lexical asset", q_node.source_refs, profile_id)

    def _project_study_plans(self, profile_id: str) -> None:
        for path in self.planner_root.glob("study-plan-*.json"):
            plan = self._read_json(path)
            if not self._profile_matches(plan, profile_id):
                continue
            plan_id = plan.get("plan_id") or path.stem
            plan_node = self._add_node(
                node_type="study_plan",
                raw_id=plan_id,
                profile_id=plan.get("profile_id") or profile_id,
                title=f"Study plan {plan.get('plan_date') or plan_id}",
                subtitle=plan.get("energy_mode"),
                status=plan.get("status"),
                source_refs=[],
                launch_route="/review/study-planner",
                metadata={"plan_id": plan_id, "plan_date": plan.get("plan_date"), "available_minutes": plan.get("available_minutes")},
            )
            for block in plan.get("blocks", []):
                block_id = block.get("block_id")
                if not block_id:
                    continue
                block_node = self._add_node(
                    node_type="study_plan_block",
                    raw_id=block_id,
                    profile_id=plan.get("profile_id") or profile_id,
                    title=block.get("title") or block_id,
                    subtitle=block.get("block_type"),
                    status=block.get("status"),
                    quality_score=_float_or_none(block.get("priority")),
                    launch_route=block.get("launch_route") or "/review/study-planner",
                    metadata={
                        "block_id": block_id,
                        "plan_id": plan_id,
                        "block_type": block.get("block_type"),
                        "due_reason": block.get("due_reason"),
                        "target_minutes": block.get("target_minutes"),
                    },
                )
                self._add_edge(block_node.node_id, plan_node.node_id, "planned_by", 0.99, "block belongs to study plan", [], profile_id)
                for asset_id in block.get("linked_asset_ids") or []:
                    if asset_id in self.asset_index:
                        self._add_edge(block_node.node_id, self.asset_index[asset_id], "requires", 0.75, "planner block references asset", [], profile_id)
                for topic_id in block.get("linked_topic_ids") or []:
                    if topic_id in self.topic_index:
                        self._add_edge(block_node.node_id, self.topic_index[topic_id], "requires", 0.75, "planner block references topic", [], profile_id)
                for gap_id in block.get("linked_gap_ids") or []:
                    if gap_id in self.gap_index:
                        self._add_edge(block_node.node_id, self.gap_index[gap_id], "requires", 0.75, "planner block references transfer gap", [], profile_id)
                for lexical_id in block.get("linked_lexical_ids") or []:
                    if lexical_id in self.lexical_index:
                        self._add_edge(block_node.node_id, self.lexical_index[lexical_id], "requires", 0.75, "planner block references lexical asset", [], profile_id)

    def _project_analytics(self, profile_id: str) -> None:
        try:
            from study_science.learning_analytics import LearningAnalyticsService
        except ImportError:
            return
        service = LearningAnalyticsService(self.repo_root)
        for event in service.events(profile_id=profile_id, range_key="30d"):
            event_id = _event_get(event, "event_id")
            metadata = _event_get(event, "metadata", {}) or {}
            node = self._add_node(
                node_type="analytics_record",
                raw_id=event_id,
                profile_id=_event_get(event, "profile_id", profile_id),
                title=_event_get(event, "event_type"),
                subtitle=_event_get(event, "subsystem"),
                status=_event_get(event, "outcome"),
                quality_score=_float_or_none(metadata.get("score")),
                source_refs=list(_event_get(event, "source_refs", []) or []),
                launch_route="/review/analytics",
                metadata={
                    "event_id": event_id,
                    "subsystem": _event_get(event, "subsystem"),
                    "outcome": _event_get(event, "outcome"),
                    "occurred_at": _event_get(event, "occurred_at"),
                    "asset_id": _event_get(event, "asset_id"),
                    "topic_id": _event_get(event, "topic_id"),
                    "lexical_id": _event_get(event, "lexical_id"),
                    "formula_family": _event_get(event, "formula_family"),
                    "assessment_id": metadata.get("assessment_id"),
                },
            )
            asset_id = _event_get(event, "asset_id")
            topic_id = _event_get(event, "topic_id")
            lexical_id = _event_get(event, "lexical_id")
            if asset_id and asset_id in self.asset_index:
                self._add_edge(node.node_id, self.asset_index[asset_id], "measured_by", 0.7, "analytics event measures asset", node.source_refs, profile_id)
            if asset_id and asset_id in self.formula_by_asset:
                self._add_edge(node.node_id, self.formula_by_asset[asset_id], "measured_by", 0.72, "analytics event measures formula", node.source_refs, profile_id)
            if topic_id and topic_id in self.topic_index:
                self._add_edge(node.node_id, self.topic_index[topic_id], "measured_by", 0.7, "analytics event measures topic", node.source_refs, profile_id)
            if lexical_id and lexical_id in self.lexical_index:
                self._add_edge(node.node_id, self.lexical_index[lexical_id], "measured_by", 0.7, "analytics event measures lexical asset", node.source_refs, profile_id)
            assessment_id = metadata.get("assessment_id")
            if assessment_id and assessment_id in self.assessment_index:
                self._add_edge(node.node_id, self.assessment_index[assessment_id], "measured_by", 0.7, "analytics event measures assessment", node.source_refs, profile_id)

    def _project_mission_actions(self, profile_id: str) -> None:
        try:
            from study_science.mission_control import MissionControlService
        except ImportError:
            return
        summary = MissionControlService(self.repo_root).summary(profile_id=profile_id)
        for action in summary.get("recommended_actions", []):
            action_id = action.get("action_id") or _stable_id("mission", action.get("title"), action.get("href"))
            self._add_node(
                node_type="mission_action",
                raw_id=action_id,
                profile_id=profile_id,
                title=action.get("title") or action_id,
                subtitle=action.get("href"),
                status="recommended",
                quality_score=_float_or_none(action.get("priority")),
                launch_route=action.get("href"),
                metadata={"action_id": action_id, "priority": action.get("priority"), "reason": action.get("reason")},
            )

    def _add_topic_node(self, topic: dict[str, Any], profile_id: str) -> KnowledgeGraphNode:
        topic_id = topic.get("topic_id") or _stable_id("topic", topic.get("title"))
        node = self._add_node(
            node_type="syllabus_topic",
            raw_id=topic_id,
            profile_id=topic.get("profile_id") or profile_id,
            title=topic.get("title") or topic_id,
            subtitle=topic.get("module") or topic.get("subject"),
            status="active" if topic.get("active", True) else "inactive",
            quality_score=_float_or_none(topic.get("importance") or topic.get("exam_weight")),
            source_refs=list(topic.get("source_refs") or []),
            launch_route="/review/coverage",
            metadata={
                "topic_id": topic_id,
                "exam": topic.get("exam"),
                "subject": topic.get("subject"),
                "module": topic.get("module"),
                "los": topic.get("los"),
                "exam_weight": topic.get("exam_weight"),
                "importance": topic.get("importance"),
            },
        )
        self.topic_index[topic_id] = node.node_id
        return node

    def _add_source_ref_edges(self, profile_id: str) -> None:
        for ref, node_ids in self.source_ref_index.items():
            ordered = sorted(node_ids)
            for left_index, left in enumerate(ordered):
                for right in ordered[left_index + 1:]:
                    if self.nodes[left].node_type == "source_segment" or self.nodes[right].node_type == "source_segment":
                        continue
                    self._add_edge(left, right, "same_source_ref", 0.55, f"shared source ref {ref}", [ref], profile_id)

    def _add_formula_family_edges(self, profile_id: str) -> None:
        groups: dict[str, list[str]] = {}
        for node in self.nodes.values():
            family = node.metadata.get("formula_family")
            if family and node.node_type in {"asset", "formula", "transfer_gap"}:
                groups.setdefault(str(family), []).append(node.node_id)
        for family, node_ids in groups.items():
            ordered = sorted(set(node_ids))
            for left_index, left in enumerate(ordered):
                for right in ordered[left_index + 1:]:
                    self._add_edge(left, right, "same_formula_family", 0.6, f"same formula family: {family}", [], profile_id)

    def _add_node(
        self,
        *,
        node_type: NodeType,
        raw_id: Any,
        profile_id: str,
        title: Any,
        subtitle: Any = None,
        status: Any = None,
        quality_score: float | None = None,
        validation_status: Any = None,
        source_refs: list[str] | None = None,
        launch_route: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> KnowledgeGraphNode:
        node_id = _node_id(node_type, raw_id)
        node = KnowledgeGraphNode(
            node_id=node_id,
            profile_id=profile_id or "default",
            node_type=node_type,
            title=self._trim(title or str(raw_id), 180),
            subtitle=self._trim(subtitle, 180) if subtitle is not None else None,
            status=str(status) if status is not None and status != "" else None,
            quality_score=quality_score,
            validation_status=str(validation_status) if validation_status is not None and validation_status != "" else None,
            source_refs=[str(ref) for ref in source_refs or [] if ref],
            launch_route=launch_route,
            metadata=dict(metadata or {}),
        )
        self.nodes[node_id] = node
        for ref in node.source_refs:
            self._index_source_ref(ref, node_id)
        return node

    def _add_edge(
        self,
        from_node_id: str,
        to_node_id: str,
        edge_type: EdgeType,
        confidence: float,
        reason: str,
        source_refs: list[str],
        profile_id: str,
    ) -> None:
        if not from_node_id or not to_node_id or from_node_id == to_node_id:
            return
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return
        edge_id = _stable_id("edge", from_node_id, to_node_id, edge_type, reason)
        self.edges[edge_id] = KnowledgeGraphEdge(
            edge_id=edge_id,
            profile_id=profile_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            edge_type=edge_type,
            confidence=round(float(confidence or 0.0), 4),
            reason=reason,
            source_refs=[str(ref) for ref in source_refs or [] if ref],
        )

    def _index_source_ref(self, ref: str, node_id: str) -> None:
        if not ref:
            return
        self.source_ref_index.setdefault(str(ref), set()).add(node_id)

    def _ensure_graph(self, profile_id: str) -> dict[str, Any]:
        path = self._graph_path(profile_id)
        if path.exists():
            return strip_graph_payload(json.loads(path.read_text(encoding="utf-8")))
        return self.recompute(profile_id=profile_id)

    def _graph_path(self, profile_id: str) -> Path:
        return self.graph_root / f"graph-{profile_id or 'default'}.json"

    @staticmethod
    def _filter_nodes(
        nodes: list[KnowledgeGraphNode],
        *,
        node_type: str | None,
        validation_status: str | None,
        quality_status: str | None,
        source_ref: str | None,
    ) -> list[KnowledgeGraphNode]:
        filtered = nodes
        if node_type:
            filtered = [node for node in filtered if node.node_type == node_type]
        if validation_status:
            filtered = [node for node in filtered if node.validation_status == validation_status]
        if quality_status:
            filtered = [
                node for node in filtered
                if quality_status in {
                    str(node.metadata.get("quality_status") or ""),
                    str(node.metadata.get("resource_quality_status") or ""),
                    str(node.metadata.get("dictionary_quality_status") or ""),
                    str(node.status or ""),
                }
            ]
        if source_ref:
            filtered = [node for node in filtered if source_ref in node.source_refs or source_ref in json.dumps(node.metadata, ensure_ascii=False)]
        return filtered

    @staticmethod
    def _rank(node: KnowledgeGraphNode, *, query: str, source_ref: str | None) -> float:
        if not query and not source_ref:
            return 1.0
        q = (query or "").lower().strip()
        title = node.title.lower()
        subtitle = (node.subtitle or "").lower()
        refs = " ".join(node.source_refs).lower()
        metadata = json.dumps(node.metadata, ensure_ascii=False).lower()
        haystack = f"{title} {subtitle} {refs} {metadata}"
        score = 0.0
        if q:
            matched = False
            structured_match = _structured_field_match_score(node, q)
            if q == title:
                score += 120
                matched = True
            elif title.startswith(q):
                score += 90
                matched = True
            elif q in title:
                score += 70
                matched = True
            elif structured_match:
                score += structured_match
                matched = True
            elif q in subtitle:
                score += 45
                matched = True
            elif q in refs:
                score += 55
                matched = True
            elif q in metadata:
                score += 25
                matched = True
            else:
                terms = [term for term in re.findall(r"[a-zA-Z0-9_+-]{2,}", q) if len(term) > 1]
                term_hits = sum(1 for term in terms if term in haystack)
                score += 8 * term_hits
                matched = term_hits > 0
            if not matched:
                return 0.0
        if source_ref and source_ref in refs:
            score += 60
        if node.validation_status in {"confirmed", "validated", "derived"}:
            score += 12
        if node.status in {"open", "weak", "missing", "partial", "stale"}:
            score += 8
        if node.quality_score is not None:
            score += min(10, max(0, node.quality_score * 10 if node.quality_score <= 1 else node.quality_score / 10))
        if node.metadata.get("exam_weight"):
            score += min(8, float(node.metadata.get("exam_weight") or 0) * 8)
        return score * _node_type_rank_weight(node)

    @staticmethod
    def _connected_nodes(node_id: str, *, nodes: list[KnowledgeGraphNode], edges: list[KnowledgeGraphEdge], limit: int) -> list[dict[str, Any]]:
        node_map = {node.node_id: node for node in nodes}
        connected_ids = []
        for edge in edges:
            if edge.from_node_id == node_id:
                connected_ids.append(edge.to_node_id)
            elif edge.to_node_id == node_id:
                connected_ids.append(edge.from_node_id)
        return [node_map[item].as_dict() for item in _unique(connected_ids)[:limit] if item in node_map]

    @staticmethod
    def _same_source_ref_neighbors(node: KnowledgeGraphNode, nodes: Any) -> list[str]:
        refs = set(node.source_refs)
        if not refs:
            return []
        return [candidate.node_id for candidate in nodes if candidate.node_id != node.node_id and refs.intersection(candidate.source_refs)]

    @staticmethod
    def _impact_notes(node: KnowledgeGraphNode, affected_nodes: list[dict[str, Any]]) -> list[str]:
        counts = Counter(item["node_type"] for item in affected_nodes)
        notes = []
        if node.node_type in {"source_document", "source_file", "resource"}:
            notes.append(f"Rejecting this {node.node_type} can affect {counts.get('asset', 0)} assets and {counts.get('formula', 0)} formulas.")
        if node.node_type in {"asset", "formula"}:
            notes.append(f"Changing this item can stale {counts.get('assessment_question', 0)} assessment questions and {counts.get('analytics_record', 0)} analytics records.")
        if node.node_type == "transfer_gap":
            notes.append(f"Resolving this gap can affect {counts.get('study_plan_block', 0)} planner blocks and {counts.get('analytics_record', 0)} analytics records.")
        if not notes:
            notes.append("No destructive action is performed; this is a read-only impact projection.")
        return notes

    @staticmethod
    def _summary(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], *, profile_id: str) -> dict[str, Any]:
        nodes_by_type = Counter(node["node_type"] for node in nodes)
        edges_by_type = Counter(edge["edge_type"] for edge in edges)
        unconfirmed = [
            node for node in nodes
            if node.get("validation_status") in {"draft", "needs_review"} or node.get("status") in {"draft", "needs_review"}
        ]
        missing_source = [
            node for node in nodes
            if node.get("node_type") in {"asset", "formula", "lexical_asset"} and not node.get("source_refs")
        ]
        topic_scores = [
            node for node in nodes
            if node.get("node_type") == "syllabus_topic" and float(node.get("quality_score") or 0) >= 0.75
        ]
        return {
            "profile_id": profile_id,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes_by_type": dict(nodes_by_type),
            "edges_by_type": dict(edges_by_type),
            "unconfirmed_islands": len(unconfirmed),
            "missing_source_assets": len(missing_source),
            "high_value_connected_topics": len(topic_scores),
        }

    @staticmethod
    def _profile_matches(payload: dict[str, Any], profile_id: str) -> bool:
        return bool(payload) and payload.get("profile_id", profile_id) in {profile_id, "default"}

    @staticmethod
    def _read_json(path: Path, default: Any | None = None) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {} if default is None else default

    @staticmethod
    def _trim(value: Any, limit: int = 160) -> str:
        text = str(value or "").strip()
        return text if len(text) <= limit else f"{text[: limit - 1]}..."


def strip_graph_payload(payload: Any) -> Any:
    sanitized, _ = sanitize_payload(payload)
    return sanitized


def _structured_field_match_score(node: KnowledgeGraphNode, query: str) -> float:
    fields = _structured_rank_fields(node)
    if not fields:
        return 0.0
    query_key = _rank_key(query)
    if not query_key:
        return 0.0
    best = 0.0
    for value in fields:
        value_text = str(value or "").strip().lower()
        if not value_text:
            continue
        value_key = _rank_key(value_text)
        if query == value_text or query_key == value_key:
            best = max(best, 105.0)
        elif value_text.startswith(query) or value_key.startswith(query_key):
            best = max(best, 82.0)
        elif query in value_text or query_key in value_key:
            best = max(best, 62.0)
    return best


def _structured_rank_fields(node: KnowledgeGraphNode) -> list[Any]:
    metadata = node.metadata or {}
    if node.node_type == "formula":
        return [
            metadata.get("plain_formula"),
            metadata.get("formula_latex"),
            metadata.get("formula_family"),
            metadata.get("correct_rule"),
        ]
    if node.node_type == "lexical_asset":
        return [
            metadata.get("headword"),
            metadata.get("lemma"),
            metadata.get("translation"),
            metadata.get("definition"),
        ]
    if node.node_type == "asset":
        return [
            metadata.get("asset_id"),
            metadata.get("trigger"),
            metadata.get("correct_rule"),
            metadata.get("los"),
        ]
    if node.node_type == "assessment_question":
        return [metadata.get("correct_rule"), metadata.get("question_id")]
    return []


def _rank_key(value: str) -> str:
    return " ".join(re.sub(r"[\W_]+", " ", value.lower(), flags=re.UNICODE).split())


def _node_type_rank_weight(node: KnowledgeGraphNode) -> float:
    if node.node_type in {"mission_action", "analytics_record", "study_plan", "study_plan_block"}:
        return 0.72
    if node.node_type in {"source_file"}:
        return 0.85
    return 1.0


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _event_get(event: Any, key: str, default: Any = None) -> Any:
    if isinstance(event, dict):
        return event.get(key, default)
    return getattr(event, key, default)


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered
