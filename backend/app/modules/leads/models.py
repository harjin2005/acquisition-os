"""Lead models + state machine.

State machine (DOC-002 §3), enforced in service:
  new → qualifying → researching → contact_attempted → in_conversation
      → underwriting → offer_extended → negotiating → under_contract
      → due_diligence → clear_to_close → closed
  Terminal branches: disqualified, dead, nurture (available from most states).

`transition_lead()` is the ONLY function permitted to mutate `lead.status`.
Direct writes are refused by an event listener installed in service.py.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


LEAD_STATES = (
    "new", "qualifying", "researching", "contact_attempted", "in_conversation",
    "underwriting", "offer_extended", "negotiating", "under_contract",
    "due_diligence", "clear_to_close", "closed",
    "disqualified", "dead", "nurture",
)


class Lead(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "lead"
    __table_args__ = (
        CheckConstraint(f"status IN ({','.join(repr(s) for s in LEAD_STATES)})", name="ck_lead_status"),
        {"schema": "core"},
    )

    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="manual")
    list_tag: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="new")
    assignee_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reason_chips: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    disqualified_reason: Mapped[str | None] = mapped_column(String(200), nullable=True)
    last_state_change_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LeadEvent(IdMixin, TenantMixin, TimestampMixin, Base):
    """Immutable transition log — every state change appends here."""

    __tablename__ = "lead_event"
    __table_args__ = {"schema": "core"}

    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.lead.id", ondelete="CASCADE"), nullable=False, index=True)
    from_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    to_state: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    reason: Mapped[str | None] = mapped_column(String(200), nullable=True)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
