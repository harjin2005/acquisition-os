"""Deal + Offer models (DOC-002 §2/§5, DOC-121 A8).

Offer chain: version increments monotonically per deal; the entire chain is
immutable once sent. Editing a sent offer voids it and starts a new version.
Deal state machine: `pursued → offer_sent → negotiating → under_contract →
due_diligence → clear_to_close → closed | dead`.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


DEAL_STATES = ("pursued", "offer_sent", "negotiating", "under_contract",
               "due_diligence", "clear_to_close", "closed", "dead")


class Deal(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "deal"
    __table_args__ = (
        CheckConstraint(f"status IN ({','.join(repr(s) for s in DEAL_STATES)})", name="ck_deal_status"),
        CheckConstraint("strategy IN ('flip','rental','brrrr')", name="ck_deal_strategy"),
        {"schema": "core"},
    )

    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    strategy: Mapped[str] = mapped_column(String(16), nullable=False, default="flip")
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="pursued")

    projected_arv: Mapped[float | None] = mapped_column(Float, nullable=True)
    projected_rehab: Mapped[float | None] = mapped_column(Float, nullable=True)
    projected_mao: Mapped[float | None] = mapped_column(Float, nullable=True)

    contract_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    contract_signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    emd_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    close_target_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Realized (populated on Closed via outcome capture)
    actual_close_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_arv: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_rehab: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_profit: Mapped[float | None] = mapped_column(Float, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    disposition: Mapped[str | None] = mapped_column(String(32), nullable=True)  # assignment | wholetail | retail | brrrr

    dead_reason: Mapped[str | None] = mapped_column(String(200), nullable=True)


class Offer(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "offer"
    __table_args__ = (
        UniqueConstraint("org_id", "deal_id", "version", name="uq_offer_version"),
        CheckConstraint(
            "status IN ('draft','sent','countered','accepted','rejected','expired','void')",
            name="ck_offer_status",
        ),
        {"schema": "core"},
    )

    deal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.deal.id", ondelete="CASCADE"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    emd: Mapped[float | None] = mapped_column(Float, nullable=True)
    inspection_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    close_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    financing: Mapped[str] = mapped_column(String(16), nullable=False, default="cash")  # cash | conventional | dscr | hard_money
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    terms: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class DealChecklistItem(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "deal_checklist"
    __table_args__ = (
        CheckConstraint("status IN ('todo','in_progress','done','waived')", name="ck_checklist_status"),
        {"schema": "core"},
    )

    deal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.deal.id", ondelete="CASCADE"), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False, default="task")  # title | inspection | emd | task
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="todo")
