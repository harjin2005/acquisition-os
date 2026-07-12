"""Identity module SQLAlchemy models (schema: core).

Ontology (DOC-002 §3 identity):
- organization: the tenant.
- member: (organization, subject_id) — WorkOS-authoritative subject bound to a
  role. `subject_id` is the WorkOS user id (or the mock's) — never PII.
- invite: pending membership; single-use; role captured at create time.

State: `member.status` is a state machine {pending, active, suspended, removed}
enforced in `app.modules.identity.service`.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class Organization(IdMixin, TimestampMixin, Base):
    __tablename__ = "organization"
    __table_args__ = {"schema": "core"}

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    workos_org_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)

    members: Mapped[list["Member"]] = relationship(back_populates="organization", cascade="all, delete-orphan")


class Member(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "member"
    __table_args__ = (
        UniqueConstraint("org_id", "subject_id", name="uq_member_org_id_subject_id"),
        CheckConstraint("role IN ('viewer','member','manager','admin','owner')", name="role_enum"),
        CheckConstraint(
            "status IN ('pending','active','suspended','removed')",
            name="status_enum",
        ),
        {"schema": "core"},
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("core.organization.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="member")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")

    organization: Mapped[Organization] = relationship(back_populates="members")


class Invite(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "invite"
    __table_args__ = (
        UniqueConstraint("org_id", "email", name="uq_invite_org_id_email"),
        CheckConstraint("role IN ('viewer','member','manager','admin')", name="invite_role_enum"),
        CheckConstraint(
            "status IN ('pending','accepted','revoked','expired')", name="invite_status_enum"
        ),
        {"schema": "core"},
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="member")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    invited_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
