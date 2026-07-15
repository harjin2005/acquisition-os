"""Underwriting: Comp + UnderwritingRun. Runs are immutable — re-analysis
creates a new Run (DOC-002 §2).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class UnderwritingRun(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "underwriting_run"
    __table_args__ = (
        CheckConstraint("strategy IN ('flip','rental','brrrr')", name="ck_uw_strategy"),
        CheckConstraint(
            "status IN ('draft','ready','insufficient_evidence','failed')",
            name="ck_uw_status",
        ),
        {"schema": "derived"},
    )

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    strategy: Mapped[str] = mapped_column(String(16), nullable=False, default="flip")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    inputs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    outputs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    assumptions: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    overrides: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    status: Mapped[str] = mapped_column(String(24), nullable=False, default="draft")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0..1
    model_version: Mapped[str] = mapped_column(
        String(32), nullable=False, default="rulebase-v1"
    )
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )


class Comp(IdMixin, TenantMixin, TimestampMixin, Base):
    """A Comp used *in a run*. Comps are frozen with the run for auditability."""

    __tablename__ = "comp"
    __table_args__ = {"schema": "derived"}

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("derived.underwriting_run.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False)
    sale_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    beds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    baths: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_miles: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    similarity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    adjustment_details: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    excluded: Mapped[bool] = mapped_column(default=False, nullable=False)
    exclusion_reason: Mapped[str | None] = mapped_column(String(200), nullable=True)
