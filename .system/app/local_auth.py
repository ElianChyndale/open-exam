from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.storage import Repository


def _users_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "security" / "users.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _sessions_path(repo: Repository) -> Path:
    path = repo.system_root / "private" / "security" / "sessions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_users(repo: Repository) -> list[dict[str, Any]]:
    return list(_load_json(_users_path(repo), []))


def _save_users(repo: Repository, users: list[dict[str, Any]]) -> None:
    _save_json(_users_path(repo), users)


def _load_sessions(repo: Repository) -> list[dict[str, Any]]:
    return list(_load_json(_sessions_path(repo), []))


def _save_sessions(repo: Repository, sessions: list[dict[str, Any]]) -> None:
    _save_json(_sessions_path(repo), sessions)


def _hash_password(password: str, *, salt_hex: str | None = None) -> tuple[str, str]:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex(), digest.hex()


def _verify_password(password: str, *, salt_hex: str, digest_hex: str) -> bool:
    _, computed = _hash_password(password, salt_hex=salt_hex)
    return hmac.compare_digest(computed, digest_hex)


def _append_security_event(repo: Repository, event_type: str, payload: dict[str, Any]) -> None:
    repo.append_jsonl_event(
        "security",
        {
            "event_type": event_type,
            "created_at": _now_iso(),
            "event_id": stable_id("security-event", event_type, json.dumps(payload, ensure_ascii=False, sort_keys=True)),
            **payload,
        },
    )


def bootstrap_admin(repo: Repository, username: str, password: str) -> dict[str, Any]:
    username = username.strip()
    if not username:
        raise ValueError("username is required")
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")
    users = _load_users(repo)
    if users:
        raise PermissionError("admin bootstrap already completed")
    salt_hex, digest_hex = _hash_password(password)
    user = {
        "user_id": stable_id("user", username.lower()),
        "username": username,
        "role": "admin",
        "password_salt": salt_hex,
        "password_hash": digest_hex,
        "created_at": _now_iso(),
        "status": "active",
    }
    users.append(user)
    _save_users(repo, users)
    _append_security_event(repo, "auth.bootstrap_admin", {"user_id": user["user_id"], "username": username})
    return {"user_id": user["user_id"], "username": username, "role": "admin"}


def login(repo: Repository, username: str, password: str) -> dict[str, Any]:
    users = _load_users(repo)
    user = next((item for item in users if item.get("username") == username and item.get("status") == "active"), None)
    if not user or not _verify_password(password, salt_hex=str(user["password_salt"]), digest_hex=str(user["password_hash"])):
        _append_security_event(repo, "auth.login_failed", {"username": username})
        raise PermissionError("invalid credentials")
    token = secrets.token_urlsafe(32)
    session = {
        "session_id": stable_id("session", user["user_id"], token),
        "session_token": token,
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "created_at": _now_iso(),
        "status": "active",
    }
    sessions = [item for item in _load_sessions(repo) if item.get("status") == "active" and item.get("user_id") != user["user_id"]]
    sessions.append(session)
    _save_sessions(repo, sessions)
    _append_security_event(repo, "auth.login_succeeded", {"user_id": user["user_id"], "username": username})
    return {
        "session_token": token,
        "user": {"user_id": user["user_id"], "username": user["username"], "role": user["role"]},
    }


def load_session(repo: Repository, session_token: str) -> dict[str, Any] | None:
    if not session_token:
        return None
    sessions = _load_sessions(repo)
    return next((item for item in sessions if item.get("session_token") == session_token and item.get("status") == "active"), None)


def load_user(repo: Repository, user_id: str) -> dict[str, Any] | None:
    return next((item for item in _load_users(repo) if item.get("user_id") == user_id), None)


def get_authenticated_user(repo: Repository, session_token: str) -> dict[str, Any] | None:
    session = load_session(repo, session_token)
    if not session:
        return None
    user = load_user(repo, str(session.get("user_id", "")))
    if not user or user.get("status") != "active":
        return None
    return {"user_id": user["user_id"], "username": user["username"], "role": user["role"], "session_id": session["session_id"]}


def logout(repo: Repository, session_token: str) -> None:
    sessions = _load_sessions(repo)
    changed = False
    for session in sessions:
        if session.get("session_token") == session_token and session.get("status") == "active":
            session["status"] = "revoked"
            session["revoked_at"] = _now_iso()
            changed = True
            _append_security_event(repo, "auth.logout", {"user_id": session.get("user_id", ""), "session_id": session.get("session_id", "")})
            break
    if changed:
        _save_sessions(repo, sessions)
