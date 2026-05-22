"""Supabase JWT verification helpers for Flask routes."""

import os
from functools import lru_cache

from supabase import Client, create_client


@lru_cache(maxsize=1)
def _anon_client() -> Client | None:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not (url and key):
        return None
    return create_client(url, key)


def _extract_token(request) -> str | None:
    header = request.headers.get("Authorization", "")
    if header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    return None


def current_user(request) -> dict | None:
    """Return {'id', 'email'} for the authenticated user, or None."""
    token = _extract_token(request)
    if not token:
        return None
    client = _anon_client()
    if client is None:
        return None
    try:
        resp = client.auth.get_user(token)
        user = getattr(resp, "user", None)
        if user is None:
            return None
        return {"id": user.id, "email": user.email}
    except Exception as e:
        print(f"[Calmora] auth verify failed: {e}")
        return None


def current_user_token(request) -> tuple[dict | None, str | None]:
    """Return (user, access_token) — useful when we want to make per-user DB calls."""
    token = _extract_token(request)
    user = current_user(request)
    return user, token
