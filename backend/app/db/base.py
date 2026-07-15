"""SQLAlchemy declarative base with cross-schema conventions.

DOC-002 (ontology) naming law:
- table_name is singular_snake_case (property, member, organization).
- id column is `id uuid` and always primary key.
- Tenant-scoped tables include `org_id uuid not null` — enforced by a CI grep
  (see `.github/workflows/ci.yml`) and by the mixin below.
- Timestamps: `created_at`, `updated_at` UTC; `datetime(timezone=True)` only.

Logical schemas per DOC-130 §5 / §2:
- core:    tenant-scoped operational entities (identity, ontology, workspaces)
- licensed: vendor-sourced (Property/Comps stubs) with `expires_at`
- derived:  outputs of AI/ML (empty in Sprint 1)
- audit:    append-only audit + outbox
- events:   domain event log (outbox)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Root declarative base — every schema shares this metadata."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class IdMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=_uuid
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )


class TenantMixin:
    """Every tenant-scoped table inherits this. Combined with RLS policies
    installed in migration `0001`, this is the tenancy contract."""

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )


def as_dict(instance: Any) -> dict[str, Any]:
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
