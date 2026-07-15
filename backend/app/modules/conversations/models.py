"""Conversation + Message models — DOC-121 A7.

`conversation` is the per-Contact thread across all channels. `message` is the
atomic communication unit; `direction` is `in|out`; inbound STOP-family opt-out
messages trip cross-channel suppression on write (compliance-critical §7).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class Conversation(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "conversation"
    __table_args__ = {"schema": "core"}

    contact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    subject: Mapped[str | None] = mapped_column(String(200), nullable=True)
    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    assignee_member_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    urgency: Mapped[str] = mapped_column(
        String(16), nullable=False, default="normal"
    )  # low|normal|urgent
    summary_pinned: Mapped[str | None] = mapped_column(Text, nullable=True)


class Message(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "message"
    __table_args__ = (
        CheckConstraint("direction IN ('in','out')", name="ck_message_direction"),
        CheckConstraint(
            "channel IN ('sms','email','voice','mail','note')",
            name="ck_message_channel",
        ),
        CheckConstraint(
            "status IN ('queued','sent','delivered','failed','received','opened','clicked','bounced','suppressed')",
            name="ck_message_status",
        ),
        {"schema": "core"},
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("core.conversation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    direction: Mapped[str] = mapped_column(String(4), nullable=False)
    from_address: Mapped[str | None] = mapped_column(String(400), nullable=True)
    to_address: Mapped[str | None] = mapped_column(String(400), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    provider_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    campaign_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    template_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    consent_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    suppression_reason: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
