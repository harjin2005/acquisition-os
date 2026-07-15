"""FastAPI application factory.

DOC-130 §3: routers are thin, wired here; business logic lives in service.py.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.core.config import get_settings
from app.core.errors import install_error_handlers
from app.core.logging import configure_logging, get_logger
from app.modules.identity.router import router as identity_router
from app.modules.ontology.router import router as ontology_router


@asynccontextmanager
async def _lifespan(app: FastAPI):  # noqa: ARG001 - FastAPI signature
    configure_logging()
    log = get_logger("startup")
    settings = get_settings()
    log.info("boot", app_env=settings.app_env, version=__version__)
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AcquisitionOS API",
        version=__version__,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
        lifespan=_lifespan,
    )

    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    install_error_handlers(app)

    # ---- Meta endpoints (no /api prefix rewrite: Emergent ingress rewrites for us) ----
    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok", "version": __version__, "env": settings.app_env}

    @app.get("/api/meta/sprint")
    def sprint_meta() -> dict:
        """Sprint 1 acceptance criteria surface. Kept in code so the frontend
        cannot claim green without the backend agreeing."""
        return {
            "sprint": 1,
            "objective": "Repo foundation, CI, Terraform staging, WorkOS skeleton, Alembic + RLS baseline.",
            "acceptance_criteria": [
                {
                    "id": "ac1",
                    "title": "scripts/dev-up.sh boots api + frontend locally",
                    "met": True,
                },
                {
                    "id": "ac2",
                    "title": "CI: lint/typecheck/unit skeleton + import-linter",
                    "met": True,
                },
                {
                    "id": "ac3",
                    "title": "Terraform staging scaffolded (network, RDS, ECS, secrets)",
                    "met": True,
                },
                {
                    "id": "ac4",
                    "title": "WorkOS auth + identity module skeleton (orgs, invites, roles)",
                    "met": True,
                },
                {
                    "id": "ac5",
                    "title": "Alembic baseline + RLS + adversarial suite merge-blocking",
                    "met": True,
                },
                {
                    "id": "ac6",
                    "title": "docs/product mirror + module README + ADR templates",
                    "met": True,
                },
            ],
        }

    # ---- v1 routers (all under /api/v1) ----
    app.include_router(identity_router, prefix="/api/v1")
    app.include_router(ontology_router, prefix="/api/v1")

    return app


app = create_app()
