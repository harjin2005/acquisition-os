"""Import job tracking (DOC-121 A3).

Content-hash idempotency (re-import of the same file is a no-op). Quarantine
rows are stored in `derived.import_quarantine` for later review."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class ImportJob(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "import_job"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','running','completed','partial','failed','rolled_back')",
            name="ck_import_status",
        ),
        {"schema": "core"},
    )

    dialect: Mapped[str] = mapped_column(
        String(32), nullable=False, default="generic_csv"
    )
    filename: Mapped[str] = mapped_column(String(400), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    mapping: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    total_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imported_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quarantined_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    consent_attestation: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class ImportQuarantine(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "import_quarantine"
    __table_args__ = {"schema": "derived"}

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    row_num: Mapped[int] = mapped_column(Integer, nullable=False)
    row_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    reasons: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
