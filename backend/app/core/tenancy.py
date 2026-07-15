"""Tenancy context + Postgres session wrapper.

**This is the load-bearing security surface of the platform.**

Non-negotiables enforced here (DOC-130 §5, ER2 mitigation):

1. Every application session **must** run inside a `TenancyContext` before it
   touches a tenant-scoped table. Sessions opened outside the wrapper refuse
   queries by raising `TenancyMissingError`.
2. The wrapper uses `SET LOCAL app.org_id = <uuid>` inside each transaction.
   `SET LOCAL` is mandatory because production runs behind RDS Proxy in
   transaction-pooling mode where session-level GUCs leak between borrowers
   (D10 in DOC-131 §3).
3. The service role (`ingestion` / `admin`) is a **separate SQLAlchemy engine**
   with `BYPASSRLS`. Import-linter forbids modules outside `ingestion` and
   `admin` from importing `service_role_session`.
4. `current_context()` is a `contextvars.ContextVar` so it works under FastAPI's
   async dispatch without leaking across requests.

If you change this file, re-run `pytest backend/tests/rls -q` — it is the
merge-blocking suite that certifies cross-tenant isolation.
"""

from __future__ import annotations

import contextvars
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TenancyContext:
    """The tenancy envelope every request/session runs inside."""

    org_id: uuid.UUID
    actor_id: uuid.UUID | None = None
    """Actor is the authenticated member; None for system jobs (impersonation
    banners still fire — see admin module)."""


_CTX: contextvars.ContextVar[TenancyContext | None] = contextvars.ContextVar(
    "tenancy_context", default=None
)


def current_context() -> TenancyContext | None:
    return _CTX.get()


@contextmanager
def tenancy(
    org_id: uuid.UUID | str, actor_id: uuid.UUID | str | None = None
) -> Iterator[TenancyContext]:
    """Push a tenancy context for the duration of the `with` block."""
    ctx = TenancyContext(
        org_id=uuid.UUID(str(org_id)),
        actor_id=uuid.UUID(str(actor_id)) if actor_id else None,
    )
    token = _CTX.set(ctx)
    try:
        yield ctx
    finally:
        _CTX.reset(token)


class TenancyMissingError(RuntimeError):
    """Raised when a tenant-scoped query is attempted without a TenancyContext."""


# ---------------------------------------------------------------------------
# Engines / Sessions
# ---------------------------------------------------------------------------


def _build_engine(url: str, *, service_role: bool) -> Engine:
    engine = create_engine(
        url,
        pool_pre_ping=True,
        future=True,
        connect_args={
            "application_name": "acquisition-os-svc"
            if service_role
            else "acquisition-os-app"
        },
    )
    return engine


_app_engine: Engine | None = None
_service_engine: Engine | None = None


def get_app_engine() -> Engine:
    global _app_engine
    if _app_engine is None:
        _app_engine = _build_engine(get_settings().database_url, service_role=False)
        _install_tenancy_guardrail(_app_engine)
    return _app_engine


def get_service_engine() -> Engine:
    """RLS-bypass engine — only importable inside `ingestion` and `admin` modules
    (import-linter enforced). Never expose to routers."""
    global _service_engine
    if _service_engine is None:
        _service_engine = _build_engine(
            get_settings().database_admin_url, service_role=True
        )
    return _service_engine


AppSession = sessionmaker(bind=None, expire_on_commit=False, future=True)
ServiceSession = sessionmaker(bind=None, expire_on_commit=False, future=True)


def _install_tenancy_guardrail(engine: Engine) -> None:
    """Deny any query on the app engine when no TenancyContext is set."""

    @event.listens_for(engine, "begin")
    def _begin(conn) -> None:  # noqa: ANN001 - SQLAlchemy signature
        ctx = _CTX.get()
        if ctx is None:
            raise TenancyMissingError(
                "Attempted to open a transaction on the app engine without a TenancyContext. "
                "Wrap the call site in `with tenancy(org_id): ...`."
            )
        # SET LOCAL is mandatory in transaction-pooled deployments (DOC-131 D10).
        conn.execute(
            text("SET LOCAL app.org_id = :org_id"), {"org_id": str(ctx.org_id)}
        )
        if ctx.actor_id is not None:
            conn.execute(
                text("SET LOCAL app.actor_id = :actor_id"),
                {"actor_id": str(ctx.actor_id)},
            )


@contextmanager
def app_session() -> Iterator[Session]:
    """Yield a Session bound to the app (RLS-enforced) engine."""
    engine = get_app_engine()
    session = AppSession(bind=engine)
    try:
        with session.begin():
            yield session
    finally:
        session.close()


@contextmanager
def service_role_session() -> Iterator[Session]:
    """Yield a Session bound to the RLS-bypass engine.

    **Import-linter forbids importing this outside `app.modules.ingestion` and
    `app.modules.admin`.** Do not add a new caller without a documented ADR.
    """
    engine = get_service_engine()
    session = ServiceSession(bind=engine)
    try:
        with session.begin():
            yield session
    finally:
        session.close()
