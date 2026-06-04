from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any


class PDFLoader:
    """Load and hash PDF files using PyMuPDF4LLM for layout-aware extraction."""

    def __init__(self, storage_root: Path) -> None:
        self.storage_root = storage_root
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def compute_hash(self, file_path: Path) -> str:
        return sha256(file_path.read_bytes()).hexdigest()

    def store_pdf(self, file_path: Path, source_id: str) -> Path:
        """Copy PDF to private storage and return content_ref path."""
        dest = self.storage_root / f"{source_id}.pdf"
        dest.write_bytes(file_path.read_bytes())
        return dest

    def load_pages(self, file_path: Path) -> list[dict[str, Any]]:
        """Extract pages with layout awareness using PyMuPDF4LLM.

        Falls back to plain PyMuPDF if pymupdf4llm is not available.
        """
        try:
            return self._load_with_pymupdf4llm(file_path)
        except Exception:
            return self._load_with_pymupdf(file_path)

    def _load_with_pymupdf4llm(self, file_path: Path) -> list[dict[str, Any]]:
        import pymupdf4llm

        md_text = pymupdf4llm.to_markdown(str(file_path), page_chunks=True)
        pages: list[dict[str, Any]] = []
        for chunk in md_text:
            pages.append(
                {
                    "page_number": chunk.get("metadata", {}).get("page", 0) + 1,
                    "text": chunk.get("text", ""),
                    "images": chunk.get("images", []),
                }
            )
        return pages

    def _load_with_pymupdf(self, file_path: Path) -> list[dict[str, Any]]:
        import fitz  # PyMuPDF

        doc = fitz.open(str(file_path))
        pages: list[dict[str, Any]] = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pages.append(
                {
                    "page_number": page_num + 1,
                    "text": page.get_text(),
                    "images": [],
                }
            )
        doc.close()
        return pages

    def get_page_count(self, file_path: Path) -> int:
        import fitz

        doc = fitz.open(str(file_path))
        count = len(doc)
        doc.close()
        return count
