from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class AtomType(str, Enum):
    DEFINITION = "definition"
    FORMULA = "formula"
    FORMULA_VARIANT = "formula_variant"
    PROCEDURE = "procedure"
    EXAMPLE = "example"
    EXAM_TRAP = "exam_trap"
    COMPARISON = "comparison"
    CONDITION = "condition"
    EXCEPTION = "exception"
    MNEMONIC = "mnemonic"


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    source_id: str
    filename: str
    file_hash: str
    title: str
    subject: str
    module_id: str
    module_title: str
    page_count: int
    upload_at: str
    status: str
    content_ref: str
    error_log: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ParsedBlock:
    block_id: str
    block_type: str
    bbox: tuple[float, float, float, float]
    text: str
    markdown: str
    font_size: float
    is_bold: bool
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ParsedPage:
    page_number: int
    blocks: list[ParsedBlock]

    def as_dict(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "blocks": [b.as_dict() for b in self.blocks],
        }


@dataclass(frozen=True, slots=True)
class KnowledgeAtom:
    atom_id: str
    source_id: str
    atom_type: AtomType
    subject: str
    module_id: str
    los_codes: list[str] = field(default_factory=list)
    title: str = ""
    content: str = ""
    summary: str = ""
    formula_latex: str = ""
    table_markdown: str = ""
    conditions: list[str] = field(default_factory=list)
    related_atom_ids: list[str] = field(default_factory=list)
    page_number: int = 0
    block_refs: list[str] = field(default_factory=list)
    extraction_confidence: float = 1.0
    verified: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def as_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["atom_type"] = self.atom_type.value
        return d

    @property
    def source_span_ids(self) -> list[str]:
        """Return source span references for this atom."""
        spans = []
        for block_ref in self.block_refs:
            spans.append(f"{self.source_id}:p{self.page_number}:{block_ref}")
        return spans

    @property
    def content_hash(self) -> str:
        """Hash of content for duplicate detection."""
        from hashlib import sha256

        return sha256(self.content.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True, slots=True)
class QuarantineItem:
    quarantine_id: str
    atom_id: str
    source_id: str
    reason: str
    atom_payload: dict[str, Any] = field(default_factory=dict)
    suggested_action: str = "approve"
    reviewer_notes: str = ""
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    resolved_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
