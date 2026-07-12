"""Ontology stub models (Sprint 1 scope only).

DOC-131 Sprint 1 AC #5: baseline Alembic migration must include organization,
member (identity, above), and *property stub* with RLS.

Property here is the licensed-layer property record (DOC-002 §4). The full
comps/derivation model lands in E2 / E3; Sprint 1 keeps only the minimal shape
required to validate RLS end-to-end.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class Property(IdMixin, TenantMixin, TimestampMixin, Base):
    """Stub property record — Sprint 1 shape only.

    Lives in `licensed` schema because the canonical property snapshot is
    vendor-sourced (DOC-002). `expires_at` supports the licensed-layer expiry
    sweep that Sprint 3 (E3) will drive; Sprint 1 populates it manually via
    tests so the RLS suite can exercise a tenant-scoped licensed table.
    """

    __tablename__ = "property"
    __table_args__ = {"schema": "licensed"}

    address_line1: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="stub")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
