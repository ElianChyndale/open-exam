from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from deps import get_repo

router = APIRouter()


def _repo(repo):
    from app.language_storage import LanguageRepository

    return LanguageRepository(repo)


def _raise(exc: Exception) -> None:
    if isinstance(exc, KeyError):
        raise HTTPException(status_code=404, detail=f"LanguageOS resource not found: {exc.args[0]}") from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    raise exc


@router.get("/profiles")
async def profiles(repo=Depends(get_repo)):
    from app.language_workflows import list_profiles

    language_repo = _repo(repo)
    return {"active_profile_id": language_repo.replay()["active_profile_id"], "profiles": list_profiles(language_repo)}


@router.get("/settings")
async def settings(repo=Depends(get_repo)):
    from app.feature_flags import FeatureFlags

    flags = FeatureFlags.load(repo.root)
    return {key: value for key, value in flags.values.items() if key.startswith("language_") or key in {"gsap_motion_enabled", "reduced_motion_safe"}}


@router.post("/profiles/select")
async def profile_select(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import select_profile

    try:
        return select_profile(_repo(repo), str(payload.get("profile_id", "")))
    except Exception as exc:
        _raise(exc)


@router.get("/sources")
async def sources(repo=Depends(get_repo)):
    return {"sources": list(_repo(repo).replay()["sources"].values())}


@router.get("/sources/{source_id}")
async def source(source_id: str, repo=Depends(get_repo)):
    try:
        return _repo(repo).replay()["sources"][source_id]
    except Exception as exc:
        _raise(exc)


@router.post("/sources", status_code=status.HTTP_201_CREATED)
@router.post("/imports", status_code=status.HTTP_201_CREATED)
async def source_import(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import import_source

    try:
        return import_source(_repo(repo), **payload)
    except Exception as exc:
        _raise(exc)


@router.get("/segments")
async def segments(source_id: str = Query(default=""), repo=Depends(get_repo)):
    rows = list(_repo(repo).replay()["segments"].values())
    return {"segments": [segment for segment in rows if not source_id or segment["source_id"] == source_id]}


@router.post("/segments", status_code=status.HTTP_201_CREATED)
async def segment_create(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import create_segment

    try:
        return create_segment(_repo(repo), **payload)
    except Exception as exc:
        _raise(exc)


@router.get("/items")
async def items(repo=Depends(get_repo)):
    return {"items": list(_repo(repo).replay()["items"].values())}


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def item_create(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import collect_item

    try:
        return collect_item(_repo(repo), **payload)
    except Exception as exc:
        _raise(exc)


@router.post("/items/{item_id}/merge")
async def item_merge(item_id: str, payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import collect_item

    state = _repo(repo).replay()
    try:
        item = state["items"][item_id]
        return collect_item(
            _repo(repo),
            item_type=item["item_type"],
            canonical_form=item["canonical_form"],
            language=item["language"],
            segment_id=str(payload["segment_id"]),
            surface_form=str(payload.get("surface_form") or item["surface_form"]),
        )
    except Exception as exc:
        _raise(exc)


@router.get("/cards/due")
async def cards_due(repo=Depends(get_repo)):
    from app.language_workflows import due_cards

    cards = due_cards(_repo(repo))
    return {"count": len(cards), "cards": cards}


@router.post("/cards/generate", status_code=status.HTTP_201_CREATED)
async def cards_generate(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import generate_cards

    try:
        return {"cards": generate_cards(_repo(repo), str(payload.get("item_id", "")), card_types=payload.get("card_types"))}
    except Exception as exc:
        _raise(exc)


@router.post("/cards/{card_id}/review")
async def card_review(card_id: str, payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import review_card

    try:
        return review_card(_repo(repo), card_id, str(payload.get("rating", "")))
    except Exception as exc:
        _raise(exc)


@router.post("/grammar/analyze")
async def grammar_analyze(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import analyze_grammar

    try:
        return analyze_grammar(_repo(repo), str(payload.get("segment_id", "")))
    except Exception as exc:
        _raise(exc)


@router.get("/grammar/{segment_id}")
async def grammar_read(segment_id: str, repo=Depends(get_repo)):
    try:
        return _repo(repo).replay()["grammar_analyses"][segment_id]
    except Exception as exc:
        _raise(exc)


@router.patch("/grammar/{segment_id}")
async def grammar_edit(segment_id: str, payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import edit_grammar

    try:
        return edit_grammar(_repo(repo), segment_id, payload)
    except Exception as exc:
        _raise(exc)


@router.get("/intuition/graph")
async def intuition_graph(repo=Depends(get_repo)):
    return {"edges": _repo(repo).replay()["intuition_edges"]}


@router.get("/intuition/search")
async def intuition_search(q: str = Query(..., min_length=1), repo=Depends(get_repo)):
    from app.language_workflows import search_intuition

    return {"items": search_intuition(_repo(repo), q)}


@router.post("/intuition/rebuild")
async def intuition_rebuild(repo=Depends(get_repo)):
    from app.language_workflows import rebuild_intuition_graph

    edges = rebuild_intuition_graph(_repo(repo))
    return {"count": len(edges), "edges": edges}


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def session_create(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import record_session

    try:
        return record_session(_repo(repo), **payload)
    except Exception as exc:
        _raise(exc)


@router.post("/bridges", status_code=status.HTTP_201_CREATED)
async def bridge_create(payload: dict, repo=Depends(get_repo)):
    from app.language_workflows import record_exam_language_bridge

    try:
        return record_exam_language_bridge(_repo(repo), **payload)
    except Exception as exc:
        _raise(exc)


@router.get("/stats")
async def stats(repo=Depends(get_repo)):
    from app.language_workflows import language_stats

    return language_stats(_repo(repo))


@router.post("/transcriptions", status_code=status.HTTP_202_ACCEPTED)
async def transcription(payload: dict, repo=Depends(get_repo)):
    from app.feature_flags import FeatureFlags
    from app.language_workflows import request_transcription

    try:
        return request_transcription(
            _repo(repo),
            str(payload.get("source_id", "")),
            provider=str(payload.get("provider") or "deepseek"),
            feature_enabled=FeatureFlags.load(repo.root).enabled("language_cloud_transcription"),
        )
    except Exception as exc:
        _raise(exc)


@router.get("/exports/{format_}")
async def export(format_: str, repo=Depends(get_repo)):
    from app.language_workflows import export_language

    try:
        return export_language(_repo(repo), format_)
    except Exception as exc:
        _raise(exc)
