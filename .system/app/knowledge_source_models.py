from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


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


class KnowledgeSourceModel(BaseModel):
    source_id: str
    filename: str
    file_hash: str
    title: str = ""
    subject: str = ""
    module_id: str = ""
    module_title: str = ""
    page_count: int = 0
    upload_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    status: str = "uploaded"  # uploaded | parsing | extracting | quarantined | promoted | failed
    content_ref: str = ""
    error_log: list[str] = Field(default_factory=list)


class KnowledgeAtomModel(BaseModel):
    atom_id: str
    source_id: str
    atom_type: AtomType = AtomType.DEFINITION
    subject: str = ""
    module_id: str = ""
    los_codes: list[str] = Field(default_factory=list)
    title: str = ""
    content: str = ""
    summary: str = ""
    formula_latex: str = ""
    table_markdown: str = ""
    conditions: list[str] = Field(default_factory=list)
    related_atom_ids: list[str] = Field(default_factory=list)
    page_number: int = 0
    block_refs: list[str] = Field(default_factory=list)
    extraction_confidence: float = 1.0
    verified: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def source_span_ids(self) -> list[str]:
        return [
            f"{self.source_id}:p{self.page_number}:{ref}"
            for ref in self.block_refs
        ]


class QuarantineItemModel(BaseModel):
    quarantine_id: str
    atom_id: str
    source_id: str
    reason: str
    atom_payload: dict[str, Any] = Field(default_factory=dict)
    suggested_action: str = "approve"  # approve | edit | reject | split
    reviewer_notes: str = ""
    status: str = "pending"  # pending | approved | rejected | edited
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    resolved_at: str = ""


class PDFUploadRequest(BaseModel):
    filename: str
    title: str = ""
    subject: str = ""
    module_id: str = ""
    module_title: str = ""


class QuarantineActionRequest(BaseModel):
    action: str  # approve | reject | edit
    reviewer_notes: str = ""
    edited_payload: dict[str, Any] | None = None
