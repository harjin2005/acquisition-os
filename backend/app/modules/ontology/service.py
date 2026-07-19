"""Ontology module — business logic. Router calls this; no logic in the router.

Sprint 2 scope: Owner CRUD (create/list/get). Full ontology surface (Contact,
Lead, Deal, BuyBox...) lands incrementally — see .claude/PROGRESS.md.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.modules.ontology.models import Owner


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
