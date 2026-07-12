"""Central error taxonomy.

Follows DOC-130 §5 posture: illegal transitions and permission denials return
machine-readable JSON, not bare strings. Errors are surfaced via a single
FastAPI exception handler so routers stay thin.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


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
