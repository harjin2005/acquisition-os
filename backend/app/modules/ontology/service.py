"""Ontology module — business logic. Router calls this; no logic in the router.

Sprint 2 scope: Owner, Contact + ContactChannel + ConsentRecord CRUD. Full
ontology surface (Lead, Deal, BuyBox...) lands incrementally — see
.claude/PROGRESS.md.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import DomainError, NotFoundError
from app.modules.ontology.models import Contact, ContactChannel, ConsentRecord, Owner


class OwnerService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_owner(
        self,
        *,
        org_id: uuid.UUID,
        display_name: str,
        entity_type: str = "unknown",
        mailing_address: str | None = None,
    ) -> Owner:
        owner = Owner(
            org_id=org_id,
            display_name=display_name,
            entity_type=entity_type,
            mailing_address=mailing_address,
        )
        self.db.add(owner)
        self.db.flush()
        return owner

    def list_owners(self, org_id: uuid.UUID) -> list[Owner]:
        stmt = select(Owner).where(Owner.org_id == org_id).order_by(Owner.created_at)
        return list(self.db.execute(stmt).scalars())

    def get_owner(self, org_id: uuid.UUID, owner_id: uuid.UUID) -> Owner:
        owner = self.db.get(Owner, owner_id)
        if owner is None or owner.org_id != org_id:
            raise NotFoundError(f"owner {owner_id} not found")
        return owner


def to_owner_dict(o: Owner) -> dict[str, Any]:
    return {
        "id": str(o.id),
        "org_id": str(o.org_id),
        "display_name": o.display_name,
        "entity_type": o.entity_type,
        "aliases": o.aliases,
        "resolution_confidence": o.resolution_confidence,
        "mailing_address": o.mailing_address,
        "created_at": o.created_at.isoformat(),
    }


class ContactService:
    """Contact + ContactChannel + ConsentRecord.

    Compliance-critical (DD change 5, DOC-002 §7): a channel is *never*
    created without a consent record, and that record always starts at
    `consent_unknown` — never a default that could make it sendable.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_contact(
        self,
        *,
        org_id: uuid.UUID,
        display_name: str,
        role: str = "owner_of_record",
        owner_id: uuid.UUID | None = None,
    ) -> Contact:
        contact = Contact(
            org_id=org_id,
            display_name=display_name,
            role=role,
            owner_id=owner_id,
        )
        self.db.add(contact)
        self.db.flush()
        return contact

    def list_contacts(self, org_id: uuid.UUID) -> list[Contact]:
        stmt = (
            select(Contact).where(Contact.org_id == org_id).order_by(Contact.created_at)
        )
        return list(self.db.execute(stmt).scalars())

    def get_contact(self, org_id: uuid.UUID, contact_id: uuid.UUID) -> Contact:
        contact = self.db.get(Contact, contact_id)
        if contact is None or contact.org_id != org_id:
            raise NotFoundError(f"contact {contact_id} not found")
        return contact

    def add_channel(
        self,
        *,
        org_id: uuid.UUID,
        contact_id: uuid.UUID,
        channel: str,
        address: str,
        provenance: str = "unknown",
    ) -> ContactChannel:
        # Confirms the contact is actually in this org before attaching a
        # channel to it — RLS would also catch a cross-org id, but failing
        # with a clear 404 here is better than a confusing constraint error.
        self.get_contact(org_id, contact_id)

        existing = self.db.execute(
            select(ContactChannel).where(
                ContactChannel.org_id == org_id,
                ContactChannel.contact_id == contact_id,
                ContactChannel.channel == channel,
                ContactChannel.address == address,
            )
        ).scalar_one_or_none()
        if existing is not None:
            raise DomainError(
                "channel already exists for this contact", code="channel_conflict"
            )

        ch = ContactChannel(
            org_id=org_id,
            contact_id=contact_id,
            channel=channel,
            address=address,
            provenance=provenance,
        )
        self.db.add(ch)
        self.db.flush()

        # Every channel gets a consent record at creation — always
        # `consent_unknown`. This is not a default to rely on; it is
        # asserted explicitly here so it can never silently drift.
        consent = ConsentRecord(
            org_id=org_id,
            channel_id=ch.id,
            state="consent_unknown",
            recorded_at=datetime.now(timezone.utc),
        )
        self.db.add(consent)
        self.db.flush()
        return ch

    def list_channels(
        self, org_id: uuid.UUID, contact_id: uuid.UUID
    ) -> list[tuple[ContactChannel, ConsentRecord | None]]:
        self.get_contact(org_id, contact_id)
        channels = list(
            self.db.execute(
                select(ContactChannel)
                .where(
                    ContactChannel.org_id == org_id,
                    ContactChannel.contact_id == contact_id,
                )
                .order_by(ContactChannel.created_at)
            ).scalars()
        )
        result: list[tuple[ContactChannel, ConsentRecord | None]] = []
        for ch in channels:
            consent = self.db.execute(
                select(ConsentRecord).where(
                    ConsentRecord.org_id == org_id, ConsentRecord.channel_id == ch.id
                )
            ).scalar_one_or_none()
            result.append((ch, consent))
        return result


def to_contact_dict(c: Contact) -> dict[str, Any]:
    return {
        "id": str(c.id),
        "org_id": str(c.org_id),
        "display_name": c.display_name,
        "role": c.role,
        "owner_id": str(c.owner_id) if c.owner_id else None,
        "created_at": c.created_at.isoformat(),
    }


def to_channel_dict(
    ch: ContactChannel, consent: ConsentRecord | None
) -> dict[str, Any]:
    return {
        "id": str(ch.id),
        "org_id": str(ch.org_id),
        "contact_id": str(ch.contact_id),
        "channel": ch.channel,
        "address": ch.address,
        "confidence": ch.confidence,
        "provenance": ch.provenance,
        "consent_state": consent.state if consent else "consent_unknown",
    }
