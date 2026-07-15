"""RBAC — Role-based access control matrix as data.

DOC-130 §9 mandates:
- The permission matrix is data, not code sprinkled in routers.
- `require_permission` is a FastAPI dependency; tests are generated from the matrix.
- Privileged actions (campaign approval, trust promotion, merge) additionally
  require role >= Manager and dual-log.

Sprint 1 seeds the identity/ontology row-set. Later modules extend `PERMISSIONS`
via `register_permission()` inside their module init.

Roles are ordered (lowest → highest):
    viewer < member < manager < admin < owner

If two roles are supplied to `require_permission`, the caller must hold *at
least* the higher one — role monotonicity is enforced in tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Callable


class Role(IntEnum):
    VIEWER = 10
    MEMBER = 20
    MANAGER = 30
    ADMIN = 40
    OWNER = 50


@dataclass(frozen=True)
class Permission:
    """A single named capability that a role must meet or exceed."""

    name: str
    min_role: Role
    description: str
    dual_log: bool = False  # requires audit log with a second actor witness
    surface: str = "api"  # api|admin|internal


PERMISSIONS: dict[str, Permission] = {}


def register_permission(perm: Permission) -> Permission:
    if perm.name in PERMISSIONS:
        raise ValueError(f"Permission {perm.name!r} already registered")
    PERMISSIONS[perm.name] = perm
    return perm


# ---------------------------------------------------------------------------
# Sprint 1 permission seed set (identity + ontology stubs only).
# ---------------------------------------------------------------------------

register_permission(Permission("org.read", Role.VIEWER, "Read own organization"))
register_permission(Permission("org.invite", Role.MANAGER, "Invite members"))
register_permission(
    Permission("org.member.role", Role.ADMIN, "Change member roles", dual_log=True)
)
register_permission(
    Permission("org.member.remove", Role.ADMIN, "Remove members", dual_log=True)
)
register_permission(Permission("property.read", Role.VIEWER, "Read properties (stub)"))
register_permission(
    Permission("property.write", Role.MEMBER, "Create/update properties (stub)")
)
register_permission(
    Permission(
        "admin.impersonate",
        Role.OWNER,
        "Impersonate a tenant",
        dual_log=True,
        surface="admin",
    )
)


# ---------------------------------------------------------------------------
# Enforcement
# ---------------------------------------------------------------------------


@dataclass
class Principal:
    """The authenticated caller as extracted by the auth dependency."""

    actor_id: str
    org_id: str
    role: Role
    email: str | None = None


class PermissionDenied(PermissionError):
    def __init__(self, perm: str, principal: Principal) -> None:
        super().__init__(f"{principal.actor_id} lacks {perm}")
        self.perm = perm


def require_permission(name: str) -> Callable[[Principal], Principal]:
    """FastAPI dependency factory. Usage::

    @router.post("/invites", dependencies=[Depends(require_permission("org.invite"))])
    """
    perm = PERMISSIONS.get(name)
    if perm is None:
        raise ValueError(f"Unknown permission {name!r} — register it in app.core.rbac.")

    from fastapi import Depends, HTTPException, status

    from app.core.auth import get_principal

    def dep(principal: Principal = Depends(get_principal)) -> Principal:
        if principal.role.value < perm.min_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "permission_denied", "permission": name},
            )
        return principal

    dep.__name__ = f"require_{name.replace('.', '_')}"
    return dep
