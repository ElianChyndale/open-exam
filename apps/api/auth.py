"""Supabase bearer verification activated only in SaaS mode."""

from __future__ import annotations

import os
import base64
import hashlib
import hmac
import json
import time
from typing import Any


class AuthError(ValueError):
    pass


def verify_supabase_token(token: str) -> dict[str, Any]:
    if token.count(".") != 2:
        raise AuthError("Malformed bearer token")
    secret = os.getenv("SUPABASE_JWT_SECRET", "")
    if secret:
        return _verify_hs256(token, secret)
    try:
        import jwt
    except ImportError as error:
        raise RuntimeError("PyJWT is required to verify Supabase access tokens") from error

    try:
        from jwt import PyJWKClient

        url = os.getenv("SUPABASE_URL", "").rstrip("/")
        signing_key = PyJWKClient(f"{url}/auth/v1/.well-known/jwks.json").get_signing_key_from_jwt(token)
        return jwt.decode(token, signing_key.key, algorithms=["ES256", "RS256"], audience="authenticated")
    except Exception as error:
        raise AuthError("Invalid or expired bearer token") from error


def _verify_hs256(token: str, secret: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        header = json.loads(_decode_segment(encoded_header))
        payload = json.loads(_decode_segment(encoded_payload))
        expected = hmac.new(secret.encode("utf-8"), f"{encoded_header}.{encoded_payload}".encode("ascii"), hashlib.sha256).digest()
        actual = base64.urlsafe_b64decode(encoded_signature + "=" * (-len(encoded_signature) % 4))
        audience = payload.get("aud")
        if header.get("alg") != "HS256" or not hmac.compare_digest(expected, actual):
            raise AuthError("Invalid bearer signature")
        if audience != "authenticated" and "authenticated" not in (audience or []):
            raise AuthError("Invalid bearer audience")
        if not payload.get("sub") or float(payload.get("exp", 0)) <= time.time():
            raise AuthError("Expired bearer token")
        return payload
    except AuthError:
        raise
    except Exception as error:
        raise AuthError("Invalid or expired bearer token") from error


def _decode_segment(value: str) -> str:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode("utf-8")


def bearer_token(authorization: str) -> str:
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise AuthError("Bearer token required")
    token = authorization[len(prefix):].strip()
    if not token:
        raise AuthError("Bearer token required")
    return token
