"""Application settings — single source of runtime configuration.

DOC-130 §5 / §7 compliance:
- Postgres is the canonical database. Connection URLs come from env; no defaults so
  missing config fails fast (per Emergent environment rule).
- WorkOS is the canonical auth provider (ADR-010). Mock mode is a dev-only adapter
  documented in ADR-EMERGENT-001; it never runs in staging or prod.
- MongoDB is present only to keep the Emergent runtime healthy while the Postgres
  substrate boots; it is never used for tenant data (ADR-EMERGENT-001 §3).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings loaded once at process start."""

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=False
    )

    app_env: Literal["development", "staging", "production", "test"] = Field(
        default="development"
    )
    app_log_level: str = Field(default="INFO")

    # --- Postgres (canonical, DOC-130 §5) -----------------------------------
    database_url: str
    database_url_async: str
    database_admin_url: str

    # --- MongoDB (Emergent runtime coexistence only, ADR-EMERGENT-001) -----
    mongo_url: str
    db_name: str

    # --- WorkOS (canonical AuthN, ADR-010 §8) ------------------------------
    workos_api_key: str
    workos_client_id: str
    workos_jwks_url: str
    workos_mock_mode: bool = True

    # --- JWT verification --------------------------------------------------
    jwt_issuer: str
    jwt_audience: str

    # --- HTTP / CORS -------------------------------------------------------
    cors_origins: str = "*"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings; call at request time, never at import time."""
    return Settings()  # type: ignore[call-arg]
