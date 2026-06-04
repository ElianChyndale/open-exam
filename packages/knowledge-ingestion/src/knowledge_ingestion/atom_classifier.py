from __future__ import annotations

import re
from typing import Any

from knowledge_ingestion.models import AtomType, KnowledgeAtom


class AtomClassifier:
    """Classify extracted atoms into the 10-type taxonomy."""

    DEFINITION_INDICATORS = [
        r"\b(is defined as|is called|refers to|means|denotes|signifies)\b",
        r"\b(definition|define|concept|term)\b",
    ]
    FORMULA_INDICATORS = [
        r"\b(formula|equation|calculation|compute|solve for)\b",
        r"[=$\[\]\\]",
    ]
    PROCEDURE_INDICATORS = [
        r"\b(step|procedure|process|method|approach|how to|follow these)\b",
        r"\b(first|second|third|then|next|finally)\b",
    ]
    EXAMPLE_INDICATORS = [
        r"\b(example|e\.g\.|for instance|illustrate|suppose)\b",
        r"\b(if a|if the|assume|given)\b",
    ]
    EXAM_TRAP_INDICATORS = [
        r"\b(trap|common mistake|watch out|beware|caution|warning|often confused)\b",
        r"\b(do not|never|avoid|incorrect|wrong)\b",
    ]
    COMPARISON_INDICATORS = [
        r"\b(versus|vs\.|compare|contrast|difference|similarity|unlike|whereas)\b",
    ]
    CONDITION_INDICATORS = [
        r"\b(if|when|provided that|assuming|given that|only if)\b",
        r"\b(condition|requirement|prerequisite)\b",
    ]
    EXCEPTION_INDICATORS = [
        r"\b(exception|unless|except|however|but note|important exception)\b",
    ]
    MNEMONIC_INDICATORS = [
        r"\b(mnemonic|remember|memory aid|acronym|acrostic)\b",
        r"\b(remember the|think of|use the)\b",
    ]

    def classify(self, atom: KnowledgeAtom) -> tuple[AtomType, float]:
        """Classify an atom and return (atom_type, confidence)."""
        text = f"{atom.title} {atom.content}".lower()

        # Prioritize explicit signals
        if atom.formula_latex:
            return AtomType.FORMULA, 0.95

        if atom.table_markdown:
            if self._matches_any(text, self.COMPARISON_INDICATORS):
                return AtomType.COMPARISON, 0.85
            return AtomType.COMPARISON, 0.7

        # Score each type
        scores: list[tuple[AtomType, float]] = []

        if self._matches_any(text, self.DEFINITION_INDICATORS):
            scores.append((AtomType.DEFINITION, 0.8))

        if self._matches_any(text, self.FORMULA_INDICATORS):
            scores.append((AtomType.FORMULA, 0.75))

        if self._matches_any(text, self.PROCEDURE_INDICATORS):
            scores.append((AtomType.PROCEDURE, 0.75))

        if self._matches_any(text, self.EXAMPLE_INDICATORS):
            scores.append((AtomType.EXAMPLE, 0.8))

        if self._matches_any(text, self.EXAM_TRAP_INDICATORS):
            scores.append((AtomType.EXAM_TRAP, 0.85))

        if self._matches_any(text, self.COMPARISON_INDICATORS):
            scores.append((AtomType.COMPARISON, 0.75))

        if self._matches_any(text, self.CONDITION_INDICATORS):
            scores.append((AtomType.CONDITION, 0.7))

        if self._matches_any(text, self.EXCEPTION_INDICATORS):
            scores.append((AtomType.EXCEPTION, 0.75))

        if self._matches_any(text, self.MNEMONIC_INDICATORS):
            scores.append((AtomType.MNEMONIC, 0.85))

        if scores:
            best = max(scores, key=lambda x: x[1])
            return best

        # Default fallback
        return AtomType.DEFINITION, 0.5

    def classify_all(self, atoms: list[KnowledgeAtom]) -> list[KnowledgeAtom]:
        """Reclassify all atoms with confidence scores."""
        result: list[KnowledgeAtom] = []
        for atom in atoms:
            atom_type, confidence = self.classify(atom)
            # Rebuild atom with new type and confidence
            data = atom.as_dict()
            data["atom_type"] = atom_type
            data["extraction_confidence"] = min(confidence, atom.extraction_confidence)
            result.append(KnowledgeAtom(**data))
        return result

    def _matches_any(self, text: str, patterns: list[str]) -> bool:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
