"""Agent run tracking + eval + LLM gateway spans (DOC-130 §9).

Every model call logs one row here for observability (Langfuse trace + OTel
span are parallel; this DB row is the *durable* record for cost + adoption
metrics). Sprint 10 wires the eval framework against this table."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class AgentRun(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "agent_run"
    __table_args__ = (
        CheckConstraint(
            "agent_name IN ('prioritization','underwriting','followup')",
            name="ck_agent_name",
        ),
        CheckConstraint(
            "status IN ('running','ok','failed','refused','human_review')",
            name="ck_agent_status",
        ),
        {"schema": "derived"},
    )

    agent_name: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    agent_version: Mapped[str] = mapped_column(String(32), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(32), nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    inputs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    output: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    tool_trace: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="running")
    refuse_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    subject_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
