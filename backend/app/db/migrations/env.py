"""Alembic environment — expand-contract discipline (DOC-130 §5).

- URL comes from env (`DATABASE_ADMIN_URL` for schema DDL — RLS-bypass role).
- Every migration is reviewed against the DOC-002 ontology glossary via a CI
  grep (`.github/workflows/ci.yml`).
- `include_schemas=True` because tenant tables span `core`, `licensed`,
  `derived`, `audit`, `events`.
"""

from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path
from typing import Any

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# Import all models so autogenerate sees them.
from app.db.registry import Base  # noqa: E402

config = context.config

url = os.environ.get("DATABASE_ADMIN_URL") or os.environ.get("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_ADMIN_URL / DATABASE_URL required for alembic")
config.set_main_option("sqlalchemy.url", url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _include_object(
    obj: Any, name: str, type_: str, reflected: bool, compare_to: Any
) -> bool:
    return True


def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_object=_include_object,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=_include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
