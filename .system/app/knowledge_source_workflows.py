from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.storage import Repository
from knowledge_ingestion.models import AtomType, KnowledgeAtom, KnowledgeSource, QuarantineItem
from knowledge_ingestion.pdf_loader import PDFLoader
from knowledge_ingestion.layout_parser import LayoutParser
from knowledge_ingestion.atom_extractor import AtomExtractor
from knowledge_ingestion.atom_classifier import AtomClassifier


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _knowledge_storage(root: Path) -> Path:
    path = root / ".system" / "private" / "knowledge-sources"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _events_path(repo: Repository) -> Path:
    path = repo.events_root / "knowledge"
    path.mkdir(parents=True, exist_ok=True)
    return path / "knowledge-events.jsonl"


def _append_knowledge_event(repo: Repository, event_type: str, payload: dict[str, Any]) -> None:
    """Append a knowledge event to the JSONL stream."""
    import json
    from learning_records.envelope import EventEnvelopeV2

    event = EventEnvelopeV2.create(
        event_type=event_type,
        source_layer="knowledge",
        payload=payload,
        idempotency_key=stable_id("knowledge", event_type, payload.get("source_id", "")),
    )
    event_path = _events_path(repo)
    with event_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.as_dict(), ensure_ascii=False) + "\n")


def ingest_pdf(
    repo: Repository,
    file_path: Path,
    *,
    filename: str,
    title: str = "",
    subject: str = "",
    module_id: str = "",
    module_title: str = "",
) -> dict[str, Any]:
    """Ingest a PDF: store, hash, parse, extract atoms, classify, quarantine check."""
    file_hash = sha256(file_path.read_bytes()).hexdigest()
    source_id = stable_id("ksource", file_hash, filename)

    # Idempotency check
    event_path = _events_path(repo)
    if event_path.exists():
        existing = _find_source_by_hash(repo, file_hash)
        if existing:
            return {"duplicate": True, "source": existing}

    # Store PDF
    storage = _knowledge_storage(repo.root)
    loader = PDFLoader(storage)
    content_ref = str(loader.store_pdf(file_path, source_id))
    page_count = loader.get_page_count(file_path)

    source = KnowledgeSource(
        source_id=source_id,
        filename=filename,
        file_hash=file_hash,
        title=title or filename,
        subject=subject,
        module_id=module_id,
        module_title=module_title,
        page_count=page_count,
        upload_at=_now(),
        status="uploaded",
        content_ref=content_ref,
    )

    _append_knowledge_event(repo, "knowledge.source.uploaded", {"source": source.as_dict()})

    # Parse pipeline
    try:
        raw_pages = loader.load_pages(file_path)
        source = _update_source_status(source, "parsing")

        parser = LayoutParser()
        parsed_pages = parser.parse_pages(raw_pages)
        source = _update_source_status(source, "extracting")

        extractor = AtomExtractor()
        atoms = extractor.extract_atoms(parsed_pages, source_id, subject, module_id)

        classifier = AtomClassifier()
        atoms = classifier.classify_all(atoms)

        # Quarantine gate
        quarantine_items: list[QuarantineItem] = []
        confirmed_atoms: list[KnowledgeAtom] = []
        seen_hashes: set[str] = set()

        for atom in atoms:
            # Duplicate detection
            if atom.content_hash in seen_hashes:
                quarantine_items.append(_create_quarantine_item(atom, "duplicate_content"))
                continue
            seen_hashes.add(atom.content_hash)

            # Confidence gate
            if atom.extraction_confidence < 0.6:
                quarantine_items.append(_create_quarantine_item(atom, "low_classification_confidence"))
                continue

            # Formula extraction failure
            if atom.atom_type == AtomType.FORMULA and not atom.formula_latex:
                quarantine_items.append(_create_quarantine_item(atom, "formula_extraction_failed"))
                continue

            # Length anomaly
            if len(atom.content) > 5000 or len(atom.content) < 10:
                quarantine_items.append(_create_quarantine_item(atom, "length_anomaly"))
                continue

            confirmed_atoms.append(atom)

        # Emit events
        for atom in confirmed_atoms:
            _append_knowledge_event(repo, "knowledge.atom.extracted", {"atom": atom.as_dict()})

        for item in quarantine_items:
            _append_knowledge_event(repo, "knowledge.quarantine.queued", {"item": item.as_dict()})

        if quarantine_items:
            source = _update_source_status(source, "quarantined")
        else:
            source = _update_source_status(source, "promoted")

        _append_knowledge_event(repo, "knowledge.source.status_changed", {
            "source_id": source_id,
            "status": source.status,
            "atoms_extracted": len(confirmed_atoms),
            "quarantined": len(quarantine_items),
        })

        return {
            "source": source.as_dict(),
            "atoms": [a.as_dict() for a in confirmed_atoms],
            "quarantine": [q.as_dict() for q in quarantine_items],
        }

    except Exception as exc:
        source = _update_source_status(source, "failed")
        _append_knowledge_event(repo, "knowledge.source.failed", {
            "source_id": source_id,
            "error": str(exc),
        })
        return {
            "source": source.as_dict(),
            "error": str(exc),
        }


def resolve_quarantine(
    repo: Repository,
    quarantine_id: str,
    action: str,
    reviewer_notes: str = "",
    edited_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve a quarantine item: approve, reject, or edit."""
    # Find in events
    event_path = _events_path(repo)
    item = _find_quarantine_item(repo, quarantine_id)
    if not item:
        raise KeyError(f"Quarantine item not found: {quarantine_id}")

    resolved_at = _now()

    if action == "approve":
        atom_data = item.atom_payload
        atom_data["verified"] = True
        _append_knowledge_event(repo, "knowledge.atom.promoted", {"atom": atom_data})
        _append_knowledge_event(repo, "knowledge.quarantine.resolved", {
            "quarantine_id": quarantine_id,
            "action": "approved",
            "reviewer_notes": reviewer_notes,
            "resolved_at": resolved_at,
        })
        return {"status": "approved", "atom": atom_data}

    elif action == "reject":
        _append_knowledge_event(repo, "knowledge.quarantine.resolved", {
            "quarantine_id": quarantine_id,
            "action": "rejected",
            "reviewer_notes": reviewer_notes,
            "resolved_at": resolved_at,
        })
        return {"status": "rejected"}

    elif action == "edit":
        if edited_payload:
            atom_data = edited_payload
            atom_data["verified"] = True
            _append_knowledge_event(repo, "knowledge.atom.promoted", {"atom": atom_data})
        _append_knowledge_event(repo, "knowledge.quarantine.resolved", {
            "quarantine_id": quarantine_id,
            "action": "edited",
            "reviewer_notes": reviewer_notes,
            "resolved_at": resolved_at,
        })
        return {"status": "edited", "atom": edited_payload}

    else:
        raise ValueError(f"Invalid action: {action}")


def list_sources(repo: Repository) -> list[dict[str, Any]]:
    """List all knowledge sources from events."""
    sources: dict[str, dict[str, Any]] = {}
    event_path = _events_path(repo)
    if not event_path.exists():
        return []

    import json
    with event_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("event_type") == "knowledge.source.uploaded":
                src = event["payload"]["source"]
                sources[src["source_id"]] = src
            elif event.get("event_type") == "knowledge.source.status_changed":
                sid = event["payload"]["source_id"]
                if sid in sources:
                    sources[sid]["status"] = event["payload"]["status"]

    return sorted(sources.values(), key=lambda s: s["upload_at"], reverse=True)


def list_quarantine(repo: Repository) -> list[dict[str, Any]]:
    """List pending quarantine items."""
    items: dict[str, dict[str, Any]] = {}
    event_path = _events_path(repo)
    if not event_path.exists():
        return []

    import json
    with event_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("event_type") == "knowledge.quarantine.queued":
                item = event["payload"]["item"]
                items[item["quarantine_id"]] = item
            elif event.get("event_type") == "knowledge.quarantine.resolved":
                qid = event["payload"]["quarantine_id"]
                if qid in items:
                    items[qid]["status"] = event["payload"]["action"]
                    items[qid]["resolved_at"] = event["payload"].get("resolved_at", "")

    return [
        item for item in items.values()
        if item.get("status", "pending") == "pending"
    ]


def _find_source_by_hash(repo: Repository, file_hash: str) -> dict[str, Any] | None:
    for source in list_sources(repo):
        if source.get("file_hash") == file_hash:
            return source
    return None


def _find_quarantine_item(repo: Repository, quarantine_id: str) -> QuarantineItem | None:
    import json
    event_path = _events_path(repo)
    if not event_path.exists():
        return None
    with event_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("event_type") == "knowledge.quarantine.queued":
                item = event["payload"]["item"]
                if item["quarantine_id"] == quarantine_id:
                    return QuarantineItem(**item)
    return None


def _update_source_status(source: KnowledgeSource, status: str) -> KnowledgeSource:
    data = source.as_dict()
    data["status"] = status
    return KnowledgeSource(**data)


def _create_quarantine_item(atom: KnowledgeAtom, reason: str) -> QuarantineItem:
    return QuarantineItem(
        quarantine_id=stable_id("kq", atom.atom_id, reason),
        atom_id=atom.atom_id,
        source_id=atom.source_id,
        reason=reason,
        atom_payload=atom.as_dict(),
        suggested_action="approve" if reason == "length_anomaly" else "edit",
    )
