"""Campaign + Suppression + Template models.

The Campaign is the *authorization object* (ADR-003). Once approved, edits
void it. `template_family_hash` locks the claim/price variables in place; the
send-time compliance-verifier rehydrates the audience under the same hash.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class Template(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "template"
    __table_args__ = (
        CheckConstraint("channel IN ('sms','email','mail')", name="ck_template_channel"),
        {"schema": "core"},
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False, default="1.0.0")
    body: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)


class Campaign(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "campaign"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft','pending_approval','approved','running','paused','void','completed')",
            name="ck_campaign_status",
        ),
        {"schema": "core"},
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    audience_query: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    audience_snapshot_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    audience_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    channels: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)  # ["sms","email"]
    template_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    cadence: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)  # {daily_cap, quiet_hours, frequency_cap_days}
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="draft")
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    signed_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SuppressionEntry(IdMixin, TenantMixin, TimestampMixin, Base):
    """Per-org internal DNC + platform-wide DNC (org_id = NIL, unwriteable to
    orgs). Once suppressed, unsuppression is a manager-audited action."""

    __tablename__ = "suppression"
    __table_args__ = (
        UniqueConstraint("org_id", "channel", "address", name="uq_suppression"),
        CheckConstraint("channel IN ('sms','voice','email','mail','all')", name="ck_suppression_channel"),
        {"schema": "core"},
    )

    channel: Mapped[str] = mapped_column(String(8), nullable=False)
    address: Mapped[str] = mapped_column(String(400), nullable=False)
    reason: Mapped[str] = mapped_column(String(64), nullable=False)  # STOP | manual | dnc_national | litigator | complaint
    origin: Mapped[str] = mapped_column(String(32), nullable=False, default="org")  # org | platform
    added_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
