"""Central error taxonomy.

Follows DOC-130 §5 posture: illegal transitions and permission denials return
machine-readable JSON, not bare strings. Errors are surfaced via a single
FastAPI exception handler so routers stay thin.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


class DomainError(Exception):
    """Business-rule violation (state machine, invariant)."""

    status_code = 409
    code = "domain_error"

    def __init__(self, message: str, code: str | None = None, **extra: object) -> None:
        super().__init__(message)
        if code:
            self.code = code
        self.extra = extra


class NotFoundError(DomainError):
    status_code = 404
    code = "not_found"


class InsufficientEvidence(DomainError):
    """Underwriting: <3 comps etc. Never a numeric value — always this error."""

    status_code = 422
    code = "insufficient_evidence"


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain_handler(_request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.code, "message": str(exc), **exc.extra},
        )

    @app.exception_handler(IntegrityError)
    async def _integrity_handler(_request: Request, exc: IntegrityError) -> JSONResponse:
        """Defense-in-depth: any DB-level uniqueness or check violation becomes
        a machine-readable 409 rather than a bare 500. Business logic should
        catch these in `service.py` first — this is the safety net."""
        detail = str(exc.orig) if exc.orig else str(exc)
        code = "integrity_error"
        if "slug" in detail.lower():
            code = "slug_conflict"
        elif "uq_" in detail.lower() or "unique" in detail.lower():
            code = "unique_conflict"
        return JSONResponse(
            status_code=409,
            content={"error": code, "message": "database integrity constraint violated"},
        )
