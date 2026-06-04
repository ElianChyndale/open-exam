"""Lexical graph — word-sense relationships for semantic navigation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class LexicalEdge:
    """A relationship between two lexical entries or senses."""

    edge_id: str
    source_id: str
    target_id: str
    relation: Literal[
        "synonym",
        "antonym",
        "hypernym",
        "hyponym",
        "meronym",
        "holonym",
        "collocation",
        "translation",
        "derivation",
        "false_friend",
    ]
    weight: float = 1.0
    bidirectional: bool = False
    evidence: list[str] = field(default_factory=list)


class LexicalGraph:
    """In-memory lexical graph with adjacency-list storage."""

    def __init__(self) -> None:
        self._nodes: set[str] = set()
        self._outgoing: dict[str, list[LexicalEdge]] = {}
        self._incoming: dict[str, list[LexicalEdge]] = {}

    def add_node(self, node_id: str) -> None:
        self._nodes.add(node_id)
        if node_id not in self._outgoing:
            self._outgoing[node_id] = []
        if node_id not in self._incoming:
            self._incoming[node_id] = []

    def add_edge(self, edge: LexicalEdge) -> None:
        self.add_node(edge.source_id)
        self.add_node(edge.target_id)
        self._outgoing[edge.source_id].append(edge)
        self._incoming[edge.target_id].append(edge)
        if edge.bidirectional:
            reverse = LexicalEdge(
                edge_id=f"{edge.edge_id}-rev",
                source_id=edge.target_id,
                target_id=edge.source_id,
                relation=edge.relation,
                weight=edge.weight,
                bidirectional=True,
                evidence=edge.evidence,
            )
            self._outgoing[edge.target_id].append(reverse)
            self._incoming[edge.source_id].append(reverse)

    def neighbors(
        self,
        node_id: str,
        relation: str = "",
        min_weight: float = 0.0,
    ) -> list[LexicalEdge]:
        edges = self._outgoing.get(node_id, [])
        return [
            e for e in edges
            if (not relation or e.relation == relation)
            and e.weight >= min_weight
        ]

    def related_nodes(self, node_id: str, max_depth: int = 2) -> dict[str, float]:
        """BFS to find related nodes up to a depth, returning cumulative weights."""
        from collections import deque

        visited: dict[str, float] = {node_id: 1.0}
        queue: deque[tuple[str, int, float]] = deque([(node_id, 0, 1.0)])

        while queue:
            current, depth, weight = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self._outgoing.get(current, []):
                new_weight = weight * edge.weight
                if edge.target_id not in visited or visited[edge.target_id] < new_weight:
                    visited[edge.target_id] = new_weight
                    queue.append((edge.target_id, depth + 1, new_weight))

        del visited[node_id]
        return visited

    def build_from_entries(self, entries: list) -> int:
        """Build graph edges from a list of LexicalEntry objects."""
        edge_count = 0
        for entry in entries:
            node_id = entry.entry_id
            self.add_node(node_id)
            for sense in entry.senses:
                sense_node = sense.sense_id
                self.add_node(sense_node)
                self.add_edge(LexicalEdge(
                    edge_id=f"{node_id}-has-sense",
                    source_id=node_id,
                    target_id=sense_node,
                    relation="derivation",
                    weight=1.0,
                ))
                for syn in sense.synonyms:
                    syn_id = f"syn:{syn}"
                    self.add_node(syn_id)
                    self.add_edge(LexicalEdge(
                        edge_id=f"{sense_node}-syn-{syn}",
                        source_id=sense_node,
                        target_id=syn_id,
                        relation="synonym",
                        weight=0.9,
                        bidirectional=True,
                    ))
                    edge_count += 1
                for ant in sense.antonyms:
                    ant_id = f"ant:{ant}"
                    self.add_node(ant_id)
                    self.add_edge(LexicalEdge(
                        edge_id=f"{sense_node}-ant-{ant}",
                        source_id=sense_node,
                        target_id=ant_id,
                        relation="antonym",
                        weight=0.8,
                        bidirectional=True,
                    ))
                    edge_count += 1
                for trans in sense.translations:
                    trans_id = f"trans:{trans.target_lemma}"
                    self.add_node(trans_id)
                    self.add_edge(LexicalEdge(
                        edge_id=f"{sense_node}-trans-{trans.target_lemma}",
                        source_id=sense_node,
                        target_id=trans_id,
                        relation="translation",
                        weight=0.85,
                    ))
                    edge_count += 1
        return edge_count

    def to_dict(self) -> dict[str, list[dict]]:
        return {
            node: [{
                "target": e.target_id,
                "relation": e.relation,
                "weight": e.weight,
            } for e in edges]
            for node, edges in self._outgoing.items()
        }
