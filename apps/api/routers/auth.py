"""Local authentication and session endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_current_user, get_repo

router = APIRouter()


@router.post("/bootstrap-admin")
async def bootstrap_admin(payload: dict, repo=Depends(get_repo)):
    from app.local_auth import bootstrap_admin as create_admin

    try:
        user = create_admin(repo, str(payload.get("username", "")), str(payload.get("password", "")))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"user": user}


@router.post("/login")
async def login(payload: dict, repo=Depends(get_repo)):
    from app.local_auth import login as create_session

    try:
        result = create_session(repo, str(payload.get("username", "")), str(payload.get("password", "")))
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return result


@router.post("/logout")
async def logout(current_user=Depends(get_current_user), repo=Depends(get_repo)):
    from app.local_auth import logout as revoke_session

    revoke_session(repo, str(current_user.get("session_token", "")))
    return {"ok": True}


@router.get("/session")
async def session(current_user=Depends(get_current_user)):
    return {
        "authenticated": True,
        "user": {
            "user_id": current_user["user_id"],
            "username": current_user["username"],
            "role": current_user["role"],
        },
    }
