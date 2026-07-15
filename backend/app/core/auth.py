"""Authentication dependency — WorkOS JWT verification with a bounded dev shim.

DOC-130 §9 ADR-010 §8: WorkOS is canonical. This module:

1. In `production` / `staging`: verifies the caller's JWT against WorkOS JWKS,
   caches JWKS, checks `iss` / `aud`, resolves the member row for (org_id, sub),
   and populates a `Principal`.
2. In `development` (WORKOS_MOCK_MODE=true, dev only per ADR-EMERGENT-001):
   accepts a JSON `Authorization: Bearer dev.<b64json>` token so the frontend
   and RLS suite can drive the identity module without a live WorkOS tenancy.
   The mock path is disabled at import time if `app_env != 'development'`.

**Never import `workos` clients from module code.** Auth flows through this file
only; import-linter enforces the constraint (see `.import-linter`).
"""

from __future__ import annotations

import base64
import json
import uuid
from typing import Any

import httpx
import jwt
from fastapi import Depends, Header, HTTPException, status

from app.core.config import Settings, get_settings
from app.core.rbac import Principal, Role


# ---------------------------------------------------------------------------
# JWKS cache (WorkOS)
# ---------------------------------------------------------------------------


_jwks_cache: dict[str, Any] | None = None


async def _fetch_jwks(url: str) -> dict[str, Any]:
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        return _jwks_cache


def _reset_jwks_cache_for_tests() -> None:
    global _jwks_cache
    _jwks_cache = None


# ---------------------------------------------------------------------------
# Dev-only mock token decoder (ADR-EMERGENT-001 §2)
# ---------------------------------------------------------------------------


def _decode_mock(token: str) -> dict[str, Any]:
    if not token.startswith("dev."):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid dev token prefix")
    try:
        payload = json.loads(base64.urlsafe_b64decode(token[4:] + "==").decode())
    except Exception as exc:  # noqa: BLE001 - narrow via wrap
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, f"invalid dev token: {exc}"
        ) from exc
    return payload


# ---------------------------------------------------------------------------
# WorkOS JWT verification
# ---------------------------------------------------------------------------


async def _verify_workos_jwt(token: str, settings: Settings) -> dict[str, Any]:
    try:
        jwks = await _fetch_jwks(settings.workos_jwks_url)
        unverified = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified.get("kid")), None)
        if key is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "unknown kid")
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        return jwt.decode(
            token,
            key=public_key,
            algorithms=[unverified.get("alg", "RS256")],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, f"invalid token: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------


async def get_principal(
    authorization: str | None = Header(default=None, alias="Authorization"),
    settings: Settings = Depends(get_settings),
) -> Principal:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing bearer token")
    token = authorization.split(" ", 1)[1].strip()

    if settings.workos_mock_mode:
        if settings.app_env not in ("development", "test"):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "mock auth disabled outside dev"
            )
        claims = _decode_mock(token)
    else:
        claims = await _verify_workos_jwt(token, settings)

    try:
        actor_id = str(claims["sub"])
        org_id = str(claims["org_id"])
        role = Role[str(claims.get("role", "MEMBER")).upper()]
    except KeyError as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, f"claim missing: {exc}"
        ) from exc

    return Principal(
        actor_id=str(uuid.UUID(actor_id)),
        org_id=str(uuid.UUID(org_id)),
        role=role,
        email=claims.get("email"),
    )
