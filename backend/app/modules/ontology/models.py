"""Ontology models — Property, Owner, Contact, BuyBox, MotivationSignal.

Follows DOC-002 §2 verbatim. Property lives in `licensed` (vendor-sourced);
Owner + Contact live in `core` (owned by us — entity resolution is a
proprietary derivation per ADR-002).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TenantMixin, TimestampMixin


# ---------------------------------------------------------------------------
# Property (licensed layer)
# ---------------------------------------------------------------------------


class Property(IdMixin, TenantMixin, TimestampMixin, Base):
    """A physical parcel or unit (DOC-002 §2)."""

    __tablename__ = "property"
    __table_args__ = (
        Index("ix_property_apn", "county", "apn"),
        {"schema": "licensed"},
    )

    address_line1: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)
    county: Mapped[str | None] = mapped_column(String(120), nullable=True)
    apn: Mapped[str | None] = mapped_column(String(64), nullable=True)

    beds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    baths: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lot_sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)

    assessed_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    tax_delinquent: Mapped[bool] = mapped_column(default=False, nullable=False)
    last_sale_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_sale_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    source: Mapped[str] = mapped_column(String(64), nullable=False, default="stub")
    source_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attributes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


# ---------------------------------------------------------------------------
# Owner (core — proprietary entity resolution)
# ---------------------------------------------------------------------------


class Owner(IdMixin, TenantMixin, TimestampMixin, Base):
    """Entity-resolved owner (DOC-002 §2). Aliases and entity type recorded here."""

    __tablename__ = "owner"
    __table_args__ = (
        CheckConstraint("entity_type IN ('person','entity','trust','unknown')", name="ck_owner_entity_type"),
        {"schema": "core"},
    )

    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
    aliases: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    resolution_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    mailing_address: Mapped[str | None] = mapped_column(String(400), nullable=True)


class OwnershipLink(IdMixin, TenantMixin, TimestampMixin, Base):
    """N:M Owner ↔ Property with recorded interest/percentage.

    The ownership graph is a first-class asset (ADR-002)."""

    __tablename__ = "ownership_link"
    __table_args__ = (
        UniqueConstraint("org_id", "owner_id", "property_id", name="uq_ownership_link"),
        {"schema": "core"},
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.owner.id", ondelete="CASCADE"), nullable=False)
    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    share: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    acquired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------------------------
# Contact + channels + consent
# ---------------------------------------------------------------------------


class Contact(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "contact"
    __table_args__ = {"schema": "core"}

    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="owner_of_record")  # owner_of_record | agent | family | other
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("core.owner.id"), nullable=True)


class ContactChannel(IdMixin, TenantMixin, TimestampMixin, Base):
    """Per-channel address (phone/email/mailing) with confidence + provenance."""

    __tablename__ = "contact_channel"
    __table_args__ = (
        CheckConstraint("channel IN ('sms','voice','email','mail')", name="ck_channel_type"),
        UniqueConstraint("org_id", "contact_id", "channel", "address", name="uq_channel_address"),
        {"schema": "core"},
    )

    contact_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.contact.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    address: Mapped[str] = mapped_column(String(400), nullable=False)  # normalized phone e164 or lowercase email
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    provenance: Mapped[str] = mapped_column(String(64), nullable=False, default="unknown")


class ConsentRecord(IdMixin, TenantMixin, TimestampMixin, Base):
    """Consent state per (contact_channel). Provenance + timestamps.

    States (DOC-002 §7): `consent_unknown | prior_express | ebr | opted_out`.
    Imported contacts default to `consent_unknown` and are unsendable (DD-5).
    """

    __tablename__ = "consent_record"
    __table_args__ = (
        UniqueConstraint("org_id", "channel_id", name="uq_consent_channel"),
        CheckConstraint(
            "state IN ('consent_unknown','prior_express','ebr','opted_out','dnc')",
            name="ck_consent_state",
        ),
        {"schema": "core"},
    )

    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("core.contact_channel.id", ondelete="CASCADE"), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False, default="consent_unknown")
    basis: Mapped[str | None] = mapped_column(String(200), nullable=True)  # e.g., "opt-in form Y, ts Z"
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


# ---------------------------------------------------------------------------
# BuyBox + motivation signals + coverage
# ---------------------------------------------------------------------------


class BuyBox(IdMixin, TenantMixin, TimestampMixin, Base):
    """Machine-readable acquisition criteria (DOC-002 §3)."""

    __tablename__ = "buy_box"
    __table_args__ = {"schema": "core"}

    name: Mapped[str] = mapped_column(String(200), nullable=False, default="Default")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # criteria keys (v1): metros[], property_types[], min_beds, max_price, strategy


class MotivationSignal(IdMixin, TenantMixin, TimestampMixin, Base):
    """A derived indicator (absentee, pre-foreclosure, tax_delinquent, probate,
    inherited, vacant, tired_landlord, code_violation, divorce, high_equity)."""

    __tablename__ = "motivation_signal"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('absentee','pre_foreclosure','tax_delinquent','probate','inherited','vacant','tired_landlord','code_violation','divorce','high_equity')",
            name="ck_signal_kind",
        ),
        Index("ix_motsig_property", "org_id", "property_id"),
        {"schema": "derived"},
    )

    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    kind: Mapped[str] = mapped_column(String(24), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    provenance: Mapped[str] = mapped_column(String(128), nullable=False, default="ingested")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class MetroCoverage(IdMixin, TenantMixin, TimestampMixin, Base):
    """Which metros the org has coverage in (per ADR-005 §c.4). Global rows are
    seeded with `org_id = NIL_UUID` and expanded per-org for overrides."""

    __tablename__ = "metro_coverage"
    __table_args__ = (
        UniqueConstraint("org_id", "metro", name="uq_metro_coverage_org_metro"),
        CheckConstraint("status IN ('live','beta','waitlist','none')", name="ck_metro_status"),
        {"schema": "derived"},
    )

    metro: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="waitlist")
    disclosure_state: Mapped[bool] = mapped_column(default=True, nullable=False)
    freshness_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=48)
