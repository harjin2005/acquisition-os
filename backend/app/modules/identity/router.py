"""Identity router — thin. Business logic is in `service.py`.

Endpoints:
- POST   /api/v1/identity/orgs                    (bootstrap; no tenancy — takes org from body)
- GET    /api/v1/identity/orgs/me                 (current org)
- GET    /api/v1/identity/orgs/me/members         (list)
- POST   /api/v1/identity/orgs/me/invites         (manager+)
- POST   /api/v1/identity/invites/accept          (public, tokened)
- PATCH  /api/v1/identity/orgs/me/members/{id}    (admin+, dual-log)
- DELETE /api/v1/identity/orgs/me/members/{id}    (admin+, dual-log)
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.core.rbac import Principal, require_permission
from app.core.tenancy import app_session, tenancy
from app.modules.identity import schemas
from app.modules.identity.service import (
    IdentityService,
    to_invite_dict,
    to_member_dict,
    to_org_dict,
)


router = APIRouter(prefix="/identity", tags=["identity"])


# ---------------------------------------------------------------------------
# Bootstrap — the ONE endpoint outside the tenancy envelope, guarded by
# `X-Bootstrap-Token` (Sprint 1: dev only; production goes via WorkOS admin API).
# ---------------------------------------------------------------------------


@router.post("/orgs", status_code=201)
def bootstrap_org(payload: schemas.OrganizationCreate = Body(...)) -> dict:
    """Create an org and its founder-owner.

    Sprint 1 dev mode: the founder's subject_id is minted synthetically here as
    a stand-in for the WorkOS provisioning callback. Production replaces this
    with a WorkOS webhook (§E12).
    """
    subject_id = str(uuid.uuid4())
    email = f"founder+{payload.slug}@dev.local"
    new_org_id = uuid.uuid4()
    with tenancy(new_org_id):
        with app_session() as db:
            org = IdentityService(db).create_organization(
                org_id=new_org_id,
                name=payload.name,
                slug=payload.slug,
                founder_subject_id=subject_id,
                founder_email=email,
            )
            return {
                "org": to_org_dict(org),
                "founder": {"subject_id": subject_id, "email": email, "role": "owner"},
            }


# ---------------------------------------------------------------------------
# Tenant-scoped endpoints
# ---------------------------------------------------------------------------


def _tenanted_session(principal: Principal):
    """Context helper: open a DB session under the principal's tenancy."""
    return (principal, tenancy(principal.org_id, principal.actor_id))


@router.get("/orgs/me")
def get_my_org(principal: Principal = Depends(require_permission("org.read"))) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            org = IdentityService(db).get_organization(uuid.UUID(principal.org_id))
            return to_org_dict(org)


@router.get("/orgs/me/members")
def list_members(
    principal: Principal = Depends(require_permission("org.read")),
) -> list[dict]:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            members = IdentityService(db).list_members(uuid.UUID(principal.org_id))
            return [to_member_dict(m) for m in members]


@router.post("/orgs/me/invites", status_code=201)
def create_invite(
    body: schemas.InviteCreate = Body(...),
    principal: Principal = Depends(require_permission("org.invite")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            invite = IdentityService(db).invite_member(
                org_id=uuid.UUID(principal.org_id),
                email=body.email,
                role=body.role,
                invited_by=uuid.UUID(principal.actor_id),
            )
            return to_invite_dict(invite)


@router.post("/invites/accept")
def accept_invite(body: schemas.InviteAccept = Body(...)) -> dict:
    """Public endpoint — no tenancy from caller; the invite token *is* the
    tenancy. We look up the invite via the service role, then bind."""
    from app.core.tenancy import service_role_session
    from app.modules.identity.models import Invite

    with service_role_session() as svc_db:
        invite = svc_db.query(Invite).filter(Invite.token == body.token).one_or_none()
        if invite is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "invite not found")
        org_id = invite.org_id

    with tenancy(org_id):
        with app_session() as db:
            member = IdentityService(db).accept_invite(
                token=body.token, subject_id=body.subject_id
            )
            return to_member_dict(member)


@router.patch("/orgs/me/members/{member_id}")
def change_member_role(
    member_id: uuid.UUID,
    body: schemas.RoleChange = Body(...),
    principal: Principal = Depends(require_permission("org.member.role")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            m = IdentityService(db).change_role(
                actor=principal, target_member_id=member_id, new_role=body.role
            )
            return to_member_dict(m)


@router.delete("/orgs/me/members/{member_id}")
def remove_member(
    member_id: uuid.UUID,
    principal: Principal = Depends(require_permission("org.member.remove")),
) -> dict:
    with tenancy(principal.org_id, principal.actor_id):
        with app_session() as db:
            m = IdentityService(db).remove_member(target_member_id=member_id)
            return to_member_dict(m)
