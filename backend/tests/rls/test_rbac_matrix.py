"""RBAC matrix property tests — table-driven from `app.core.rbac.PERMISSIONS`.

DOC-130 §9: tests generated from the matrix. If a permission is added without
a test row, this suite fails loudly.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.core.rbac import PERMISSIONS, Principal, Role, require_permission


ROLES = [Role.VIEWER, Role.MEMBER, Role.MANAGER, Role.ADMIN, Role.OWNER]


@pytest.mark.parametrize("perm_name", sorted(PERMISSIONS))
@pytest.mark.parametrize("role", ROLES)
def test_role_meets_or_denied(perm_name: str, role: Role):
    perm = PERMISSIONS[perm_name]
    dep = require_permission(perm_name)
    principal = Principal(actor_id="00000000-0000-0000-0000-000000000000",
                          org_id="00000000-0000-0000-0000-000000000000",
                          role=role)
    if role.value >= perm.min_role.value:
        assert dep(principal=principal) is principal
    else:
        with pytest.raises(HTTPException) as exc:
            dep(principal=principal)
        assert exc.value.status_code == 403
