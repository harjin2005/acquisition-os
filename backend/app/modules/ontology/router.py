"""Ontology router — thin. Business logic for Owner is in `service.py`;
Property stays inline as the original Sprint-1 RLS-proving stub.

Full ontology surface (leads, deals, offers) lands incrementally in E2.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.rbac import Principal, require_permission
from app.core.tenancy import app_session, tenancy
from app.modules.ontology.models import Property
from app.modules.ontology.service import OwnerService, to_owner_dict


router = APIRouter(prefix="/ontology", tags=["ontology"])


class PropertyIn(BaseModel):
    address_line1: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=2, max_length=2)
    postal_code: str = Field(min_length=3, max_length=10)


class PropertyOut(BaseModel):
    id: str
    org_id: str
    address_line1: str
    city: str
    state: str
    postal_code: str


@router.post("/properties", status_code=201)
def create_property(
    body: PropertyIn = Body(...),
    principal: Principal = Depends(require_permission("property.write")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            prop = Property(
                org_id=uuid.UUID(principal.org_id),
                address_line1=body.address_line1,
                city=body.city,
                state=body.state.upper(),
                postal_code=body.postal_code,
            )
            db.add(prop)
            db.flush()
            return {
                "id": str(prop.id),
                "org_id": str(prop.org_id),
                "address_line1": prop.address_line1,
                "city": prop.city,
                "state": prop.state,
                "postal_code": prop.postal_code,
            }


@router.get("/properties")
def list_properties(
    principal: Principal = Depends(require_permission("property.read")),
) -> list[dict]:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            rows = (
                db.execute(select(Property).order_by(Property.created_at))
                .scalars()
                .all()
            )
            return [
                {
                    "id": str(p.id),
                    "org_id": str(p.org_id),
                    "address_line1": p.address_line1,
                    "city": p.city,
                    "state": p.state,
                    "postal_code": p.postal_code,
                }
                for p in rows
            ]


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------


class OwnerIn(BaseModel):
    display_name: str = Field(min_length=1, max_length=200)
    entity_type: str = Field(
        default="unknown", pattern="^(person|entity|trust|unknown)$"
    )
    mailing_address: str | None = Field(default=None, max_length=400)


@router.post("/owners", status_code=201)
def create_owner(
    body: OwnerIn = Body(...),
    principal: Principal = Depends(require_permission("owner.write")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            owner = OwnerService(db).create_owner(
                org_id=uuid.UUID(principal.org_id),
                display_name=body.display_name,
                entity_type=body.entity_type,
                mailing_address=body.mailing_address,
            )
            return to_owner_dict(owner)


@router.get("/owners")
def list_owners(
    principal: Principal = Depends(require_permission("owner.read")),
) -> list[dict]:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            owners = OwnerService(db).list_owners(uuid.UUID(principal.org_id))
            return [to_owner_dict(o) for o in owners]


@router.get("/owners/{owner_id}")
def get_owner(
    owner_id: uuid.UUID,
    principal: Principal = Depends(require_permission("owner.read")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            owner = OwnerService(db).get_owner(uuid.UUID(principal.org_id), owner_id)
            return to_owner_dict(owner)
