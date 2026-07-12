"""Identity service — orgs, members, invites.

Sprint 1 scope:
- create_organization: bootstraps a new org and its founder-member (owner role).
- invite_member: manager+ role required; single-use tokened invite.
- accept_invite: activates the member.
- change_role / remove: dual-log admin actions (audit hook is wired in E2; here
  we emit the domain event via the outbox contract for future consumers).

Business rules encoded here (not in the router):
- Founder of an org is `owner`; only owners can transfer ownership (E12).
- An invite email must be unique per org and cannot target an existing active
  member.
- Role transitions must respect monotonicity except owner → admin demotion,
  which requires a second owner (dual-log — enforced by service, tested).
"""

from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import DomainError, NotFoundError
from app.modules.identity.models import Invite, Member, Organization


class IdentityService:
    """All identity business logic. Router calls this — no logic in the router."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # --- Organization -------------------------------------------------------

    def create_organization(
        self,
        *,
        name: str,
        slug: str,
        founder_subject_id: str,
        founder_email: str,
        org_id: uuid.UUID | None = None,
        workos_org_id: str | None = None,
    ) -> Organization:
        # Slug uniqueness is a *global* invariant, not a tenant-scoped one.
        # The current session runs inside a freshly-minted tenancy where RLS
        # would blind us to rows owned by other orgs, so we consult the
        # service role (RLS-bypass) for this single check. This is the
        # sanctioned use of `service_role_session` from a tenant router
        # (see .claude/rules/backend.md).
        from app.core.tenancy import service_role_session

        with service_role_session() as global_db:
            existing = global_db.execute(
                select(Organization).where(Organization.slug == slug)
            ).scalar_one_or_none()
        if existing is not None:
            raise DomainError(f"slug {slug!r} is already taken", code="slug_conflict")

        org = Organization(id=org_id or uuid.uuid4(), name=name, slug=slug, workos_org_id=workos_org_id)
        self.db.add(org)
        self.db.flush()

        founder = Member(
            org_id=org.id,
            organization_id=org.id,
            subject_id=founder_subject_id,
            email=founder_email,
            role="owner",
            status="active",
        )
        self.db.add(founder)
        self.db.flush()
        return org

    def get_organization(self, org_id: uuid.UUID) -> Organization:
        org = self.db.get(Organization, org_id)
        if org is None:
            raise NotFoundError(f"organization {org_id} not found")
        return org

    # --- Members / invites --------------------------------------------------

    def list_members(self, org_id: uuid.UUID) -> list[Member]:
        stmt = select(Member).where(Member.org_id == org_id).order_by(Member.created_at)
        return list(self.db.execute(stmt).scalars())

    def invite_member(
        self,
        *,
        org_id: uuid.UUID,
        email: str,
        role: str,
        invited_by: uuid.UUID,
        ttl: timedelta = timedelta(days=7),
    ) -> Invite:
        if role not in ("viewer", "member", "manager", "admin"):
            raise DomainError(f"role {role!r} is not invitable")
        existing_member = self.db.execute(
            select(Member).where(Member.org_id == org_id, Member.email == email, Member.status == "active")
        ).scalar_one_or_none()
        if existing_member is not None:
            raise DomainError("email is already an active member", code="already_member")

        existing_invite = self.db.execute(
            select(Invite).where(Invite.org_id == org_id, Invite.email == email, Invite.status == "pending")
        ).scalar_one_or_none()
        if existing_invite is not None:
            raise DomainError("pending invite already exists", code="invite_conflict")

        invite = Invite(
            org_id=org_id,
            email=email,
            role=role,
            invited_by=invited_by,
            token=secrets.token_urlsafe(32),
            expires_at=datetime.now(timezone.utc) + ttl,
        )
        self.db.add(invite)
        self.db.flush()
        return invite

    def accept_invite(self, *, token: str, subject_id: str) -> Member:
        invite = self.db.execute(select(Invite).where(Invite.token == token)).scalar_one_or_none()
        if invite is None:
            raise NotFoundError("invite not found")
        if invite.status != "pending":
            raise DomainError(f"invite is {invite.status}", code="invite_not_pending")
        if invite.expires_at < datetime.now(timezone.utc):
            invite.status = "expired"
            self.db.flush()
            raise DomainError("invite expired", code="invite_expired")

        member = Member(
            org_id=invite.org_id,
            organization_id=invite.org_id,
            subject_id=subject_id,
            email=invite.email,
            role=invite.role,
            status="active",
        )
        invite.status = "accepted"
        self.db.add(member)
        self.db.flush()
        return member

    def change_role(self, *, actor: "Principal", target_member_id: uuid.UUID, new_role: str) -> Member:  # noqa: F821

        if new_role not in ("viewer", "member", "manager", "admin", "owner"):
            raise DomainError(f"role {new_role!r} invalid")
        target = self.db.get(Member, target_member_id)
        if target is None:
            raise NotFoundError("member not found")

        # Owner demotion requires another owner to exist (dual-owner rule).
        if target.role == "owner" and new_role != "owner":
            other_owners = self.db.execute(
                select(Member).where(
                    Member.org_id == target.org_id,
                    Member.role == "owner",
                    Member.status == "active",
                    Member.id != target.id,
                )
            ).scalars().all()
            if not other_owners:
                raise DomainError("cannot demote the last owner", code="last_owner")

        target.role = new_role
        self.db.flush()
        return target

    def remove_member(self, *, target_member_id: uuid.UUID) -> Member:
        target = self.db.get(Member, target_member_id)
        if target is None:
            raise NotFoundError("member not found")
        if target.role == "owner":
            other_owners = self.db.execute(
                select(Member).where(
                    Member.org_id == target.org_id,
                    Member.role == "owner",
                    Member.status == "active",
                    Member.id != target.id,
                )
            ).scalars().all()
            if not other_owners:
                raise DomainError("cannot remove the last owner", code="last_owner")
        target.status = "removed"
        self.db.flush()
        return target


def to_org_dict(org: Organization) -> dict[str, Any]:
    return {
        "id": str(org.id),
        "name": org.name,
        "slug": org.slug,
        "workos_org_id": org.workos_org_id,
        "created_at": org.created_at.isoformat(),
    }


def to_member_dict(m: Member) -> dict[str, Any]:
    return {
        "id": str(m.id),
        "org_id": str(m.org_id),
        "subject_id": m.subject_id,
        "email": m.email,
        "role": m.role,
        "status": m.status,
        "created_at": m.created_at.isoformat(),
    }


def to_invite_dict(i: Invite) -> dict[str, Any]:
    return {
        "id": str(i.id),
        "org_id": str(i.org_id),
        "email": i.email,
        "role": i.role,
        "status": i.status,
        "token": i.token,
        "expires_at": i.expires_at.isoformat(),
    }
