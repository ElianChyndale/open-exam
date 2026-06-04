from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from deps import get_repo

router = APIRouter()


def _repo(repo):
    from app.language_storage import LanguageRepository

    return LanguageRepository(repo)


def _raise(exc: Exception) -> None:
    if isinstance(exc, KeyError):
        raise HTTPException(status_code=404, detail=f"Dictionary resource not found: {exc.args[0]}") from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    raise exc


def _check_flag(repo) -> None:
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("dictionary_os"):
        raise HTTPException(status_code=403, detail="dictionary_os feature flag is disabled")


@router.post("/import", status_code=status.HTTP_201_CREATED)
async def dictionary_import(payload: dict, repo=Depends(get_repo)):
    _check_flag(repo)
    from app.language_storage import LanguageRepository
    from language_science.dictionary_importers import import_dictionary
    from language_science.dictionary_index import DictionaryIndex

    language_repo = LanguageRepository(repo)
    content_bytes = payload.get("content", "").encode("utf-8")
    if not content_bytes:
        raise HTTPException(status_code=422, detail="content is required")

    try:
        result = import_dictionary(
            repo.root,
            title=str(payload.get("title", "")),
            language_pair=str(payload.get("language_pair", "")),
            content=content_bytes,
            filename=str(payload.get("filename", "")),
            license_mode=str(payload.get("license_mode", "unknown")),
            priority=int(payload.get("priority", 0)),
        )
    except Exception as exc:
        _raise(exc)

    source = result["source"]
    entries = result["entries"]

    # Deduplicate by file_hash via event replay
    state = language_repo.replay()
    existing = next(
        (d for d in state.get("dictionaries", {}).values() if d.get("file_hash") == source.file_hash),
        None,
    )
    if existing:
        return {"duplicate": True, "source": existing, "count": 0}

    # Persist source metadata and entries as events
    index_db = repo.root / ".system" / "private" / "language-dictionaries" / "index.db"
    index = DictionaryIndex(index_db)
    index.bulk_insert(entries)

    language_repo.append(
        "language.dictionary.imported",
        {"source": source.as_dict(), "entry_count": len(entries)},
        evidence_refs=[source.file_hash],
    )
    for entry in entries:
        language_repo.append(
            "language.dictionary.entry.indexed",
            {"entry": entry.as_dict(), "source_id": source.dictionary_id},
            evidence_refs=[source.dictionary_id],
        )

    return {"duplicate": False, "source": source.as_dict(), "count": len(entries)}


@router.get("/search")
async def dictionary_search(
    q: str = Query(..., min_length=1),
    language: str = Query(default=""),
    pos: str = Query(default=""),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    repo=Depends(get_repo),
):
    _check_flag(repo)
    from language_science.dictionary_index import DictionaryIndex

    index_db = repo.root / ".system" / "private" / "language-dictionaries" / "index.db"
    index = DictionaryIndex(index_db)
    try:
        results = index.search(q, language=language, pos=pos, limit=limit, offset=offset)
    except Exception as exc:
        _raise(exc)
    return {"query": q, "count": len(results), "results": results}


@router.get("/lookup/{lemma}")
async def dictionary_lookup(
    lemma: str,
    language: str = Query(default=""),
    repo=Depends(get_repo),
):
    _check_flag(repo)
    from language_science.dictionary_index import DictionaryIndex

    index_db = repo.root / ".system" / "private" / "language-dictionaries" / "index.db"
    index = DictionaryIndex(index_db)
    try:
        results = index.lookup_lemma(lemma, language=language)
    except Exception as exc:
        _raise(exc)
    return {"lemma": lemma, "count": len(results), "results": results}
