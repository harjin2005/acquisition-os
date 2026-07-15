"""Adversarial cross-tenant isolation tests — MERGE-BLOCKING (DOC-130 §5, ER2).

If any assertion here regresses, cross-tenant data leak is possible. Do not
"fix" a failure by loosening the check. If the RLS policy needs to change,
open an ADR and update the pooler-change checklist (D10).
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text

from app.core.tenancy import (
    TenancyMissingError,
    app_session,
    service_role_session,
    tenancy,
)
from app.modules.identity.models import Member, Organization
from app.modules.ontology.models import Property


def test_missing_tenancy_context_denies_query(clean_db):
    with pytest.raises(TenancyMissingError):
        with app_session() as db:  # no tenancy() wrapping
            db.execute(text("SELECT 1"))


def test_org_a_cannot_read_org_b_property(two_orgs):
    org_a, org_b = two_orgs
    with tenancy(org_a):
        with app_session() as db:
            rows = db.execute(select(Property)).scalars().all()
            assert len(rows) == 1
            assert rows[0].org_id == org_a


def test_org_a_cannot_read_org_b_member(two_orgs):
    org_a, org_b = two_orgs
    with tenancy(org_a):
        with app_session() as db:
            members = db.execute(select(Member)).scalars().all()
            assert {m.org_id for m in members} == {org_a}


def test_org_a_cannot_read_org_b_organization(two_orgs):
    org_a, org_b = two_orgs
    with tenancy(org_a):
        with app_session() as db:
            orgs = db.execute(select(Organization)).scalars().all()
            assert len(orgs) == 1
            assert orgs[0].id == org_a


def test_org_a_cannot_write_row_for_org_b(two_orgs):
    """Cross-tenant WRITE must fail because policy has WITH CHECK."""
    org_a, org_b = two_orgs
    with tenancy(org_a):
        with pytest.raises(Exception):  # noqa: BLE001 - psycopg raises via sqlalchemy
            with app_session() as db:
                db.add(
                    Property(
                        id=uuid.uuid4(),
                        org_id=org_b,  # <-- adversarial: writing for another tenant
                        address_line1="pwn",
                        city="pwn",
                        state="TX",
                        postal_code="75000",
                    )
                )
                db.flush()


def test_org_a_cannot_update_org_b_row_via_raw_sql(two_orgs):
    org_a, org_b = two_orgs
    with tenancy(org_a):
        with app_session() as db:
            # UPDATE affects zero rows because RLS filters out org_b's row.
            result = db.execute(
                text(
                    "UPDATE licensed.property SET city='hacked' WHERE org_id = :other"
                ),
                {"other": org_b},
            )
            assert result.rowcount == 0


def test_forgetting_org_id_write_is_blocked(two_orgs):
    """A model instance created without org_id under RLS must be rejected."""
    org_a, _ = two_orgs
    with tenancy(org_a):
        with pytest.raises(Exception):
            with app_session() as db:
                db.add(
                    Property(
                        id=uuid.uuid4(),
                        org_id=None,  # type: ignore[arg-type]
                        address_line1="oops",
                        city="oops",
                        state="TX",
                        postal_code="75000",
                    )
                )
                db.flush()


def test_service_role_bypass_still_works_for_ingestion(two_orgs):
    """Sanity: the ingestion escape hatch must still see all rows.
    Import-linter enforces which modules can import it (see .importlinter)."""
    org_a, org_b = two_orgs
    with service_role_session() as db:
        rows = db.execute(select(Property)).scalars().all()
        assert {r.org_id for r in rows} == {org_a, org_b}


def test_guc_is_local_not_session(two_orgs):
    """Regression for D10: verify SET LOCAL semantics — outside the txn the
    GUC is not visible. This is what makes pooler-mode safe."""
    org_a, _ = two_orgs
    with tenancy(org_a):
        with app_session() as db:
            val = db.execute(
                text("SELECT current_setting('app.org_id', true)")
            ).scalar()
            assert val == str(org_a)
    # After the with-block closes, a new session outside tenancy must not see it.
    with pytest.raises(TenancyMissingError):
        with app_session() as db:
            db.execute(text("SELECT 1"))
