"""Audit log + Outbox — DOC-130 §5.

`audit.log` is append-only. Privileged actions (campaign approve, role
change, member remove, impersonation start/stop, suppression edit) MUST
write a row here. Enforced by service-level convention + a `no_update`
migration policy that revokes UPDATE from the app role.

`events.outbox` is the transactional outbox: services write domain events
inside the same transaction as their state change; a dispatcher process
publishes them to consumers (E9+).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class AuditEntry(IdMixin, TenantMixin, Base):
    """Append-only. `updated_at` intentionally absent — audit records never mutate."""

    __tablename__ = "log"
    __table_args__ = {"schema": "audit"}

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(96), nullable=False)   # e.g., "campaign.approve"
    target_kind: Mapped[str] = mapped_column(String(64), nullable=False)  # e.g., "campaign"
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    dual_witness_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)


class OutboxEvent(IdMixin, TenantMixin, TimestampMixin, Base):
    """Transactional outbox — dispatcher consumes rows FIFO.

    `published_at` NULL means unpublished. `attempts` supports backoff.
    """

    __tablename__ = "outbox"
    __table_args__ = (
        CheckConstraint("status IN ('pending','published','failed','dead')", name="ck_outbox_status"),
        {"schema": "events"},
    )

    kind: Mapped[str] = mapped_column(String(96), nullable=False, index=True)
    aggregate_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ImpersonationSession(IdMixin, TenantMixin, TimestampMixin, Base):
    """Support impersonation with mandatory audit + banner (DOC-121 A15)."""

    __tablename__ = "impersonation"
    __table_args__ = {"schema": "audit"}

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    supporter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    reason: Mapped[str] = mapped_column(String(400), nullable=False)
    consent_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
