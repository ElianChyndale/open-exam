from __future__ import annotations

from typing import Any

from knowledge_ingestion.models import AtomType, KnowledgeAtom, ParsedBlock, ParsedPage
from knowledge_ingestion.formula_extractor import FormulaExtractor
from knowledge_ingestion.table_extractor import TableExtractor
from knowledge_ingestion.note_segmenter import NoteSegmenter


class AtomExtractor:
    """Group parsed blocks into candidate KnowledgeAtoms."""

    def __init__(self) -> None:
        self.formula_extractor = FormulaExtractor()
        self.table_extractor = TableExtractor()
        self.note_segmenter = NoteSegmenter()

    def extract_atoms(
        self,
        pages: list[ParsedPage],
        source_id: str,
        subject: str,
        module_id: str,
    ) -> list[KnowledgeAtom]:
        """Extract candidate atoms from all parsed pages."""
        atoms: list[KnowledgeAtom] = []
        for page in pages:
            page_atoms = self._extract_from_page(page, source_id, subject, module_id)
            atoms.extend(page_atoms)
        return atoms

    def _extract_from_page(
        self,
        page: ParsedPage,
        source_id: str,
        subject: str,
        module_id: str,
    ) -> list[KnowledgeAtom]:
        """Extract atoms from a single page."""
        atoms: list[KnowledgeAtom] = []
        blocks = page.blocks
        i = 0
        while i < len(blocks):
            block = blocks[i]

            # Heading starts a new atom group
            if block.block_type == "heading":
                group, consumed = self._collect_atom_group(blocks, i, source_id, subject, module_id, page.page_number)
                if group:
                    atoms.append(group)
                i += consumed
                continue

            # Standalone formula
            formula_result = self.formula_extractor.extract_from_block(block)
            if formula_result:
                atom = KnowledgeAtom(
                    atom_id=f"atom-{source_id}-p{page.page_number}-{block.block_id}",
                    source_id=source_id,
                    atom_type=AtomType.FORMULA,
                    subject=subject,
                    module_id=module_id,
                    title="Formula",
                    content=block.text,
                    formula_latex=formula_result.get("latex", ""),
                    page_number=page.page_number,
                    block_refs=[block.block_id],
                    extraction_confidence=formula_result.get("confidence", 0.7),
                )
                atoms.append(atom)
                i += 1
                continue

            # Standalone table
            table_result = self.table_extractor.extract_from_block(block)
            if table_result:
                atom = KnowledgeAtom(
                    atom_id=f"atom-{source_id}-p{page.page_number}-{block.block_id}",
                    source_id=source_id,
                    atom_type=AtomType.COMPARISON,
                    subject=subject,
                    module_id=module_id,
                    title="Table",
                    content=block.text,
                    table_markdown=table_result.get("markdown", ""),
                    page_number=page.page_number,
                    block_refs=[block.block_id],
                    extraction_confidence=table_result.get("confidence", 0.85),
                )
                atoms.append(atom)
                i += 1
                continue

            # Note/callout
            note_type = self.note_segmenter._detect_note_type(block)
            if note_type:
                atom_type = AtomType.EXAM_TRAP if "warning" in block.text.lower() or "caution" in block.text.lower() else AtomType.NOTE
                atom = KnowledgeAtom(
                    atom_id=f"atom-{source_id}-p{page.page_number}-{block.block_id}",
                    source_id=source_id,
                    atom_type=atom_type,
                    subject=subject,
                    module_id=module_id,
                    title=note_type.capitalize(),
                    content=block.text,
                    page_number=page.page_number,
                    block_refs=[block.block_id],
                    extraction_confidence=0.75,
                )
                atoms.append(atom)
                i += 1
                continue

            i += 1

        return atoms

    def _collect_atom_group(
        self,
        blocks: list[ParsedBlock],
        start_idx: int,
        source_id: str,
        subject: str,
        module_id: str,
        page_number: int,
    ) -> tuple[KnowledgeAtom | None, int]:
        """Collect a heading and its following content blocks into an atom."""
        if start_idx >= len(blocks):
            return None, 1

        heading = blocks[start_idx]
        title = heading.text.strip("#* ").strip()
        content_lines: list[str] = []
        block_refs = [heading.block_id]
        consumed = 1

        for j in range(start_idx + 1, len(blocks)):
            block = blocks[j]
            if block.block_type == "heading":
                break
            content_lines.append(block.text)
            block_refs.append(block.block_id)
            consumed += 1

        content = "\n\n".join(content_lines)
        if not content.strip():
            content = title

        atom = KnowledgeAtom(
            atom_id=f"atom-{source_id}-p{page_number}-{heading.block_id}",
            source_id=source_id,
            atom_type=AtomType.DEFINITION,  # Will be refined by classifier
            subject=subject,
            module_id=module_id,
            title=title,
            content=content,
            page_number=page_number,
            block_refs=block_refs,
            extraction_confidence=0.7,
        )
        return atom, consumed
