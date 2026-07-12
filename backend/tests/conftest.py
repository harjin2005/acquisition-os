"""Shared pytest fixtures — DB, tenancy, seeded data.

The RLS suite (tests/rls) is the merge-blocking cross-tenant isolation
certification. Fixtures here must never bypass RLS unless the fixture itself
is testing the service-role escape hatch.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Iterator

import pytest
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
os.environ.setdefault("APP_ENV", "test")

from sqlalchemy import text  # noqa: E402

from app.core.tenancy import (  # noqa: E402
    get_service_engine,
    service_role_session,
)
from app.modules.identity.models import Member, Organization  # noqa: E402
from app.modules.ontology.models import Property  # noqa: E402


@pytest.fixture(scope="session")
def _pg_ready() -> None:
    engine = get_service_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


@pytest.fixture()
def clean_db(_pg_ready) -> Iterator[None]:
    """Truncate all tenant tables between tests — order matters for FKs."""
    engine = get_service_engine()
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE licensed.property, core.invite, core.member, core.organization CASCADE"))
    yield


@pytest.fixture()
def two_orgs(clean_db) -> tuple[uuid.UUID, uuid.UUID]:
    """Seed two organizations directly via the service-role engine (RLS-bypass).

    Returns (org_a_id, org_b_id). Used by the adversarial cross-tenant tests.
    """
    org_a = uuid.uuid4()
    org_b = uuid.uuid4()
    with service_role_session() as db:
        db.add_all(
            [
                Organization(id=org_a, name="Alpha", slug="alpha"),
                Organization(id=org_b, name="Bravo", slug="bravo"),
                Member(
                    id=uuid.uuid4(),
                    org_id=org_a,
                    organization_id=org_a,
                    subject_id="sub-a",
                    email="a@alpha.local",
                    role="owner",
                    status="active",
                ),
                Member(
                    id=uuid.uuid4(),
                    org_id=org_b,
                    organization_id=org_b,
                    subject_id="sub-b",
                    email="b@bravo.local",
                    role="owner",
                    status="active",
                ),
                Property(
                    id=uuid.uuid4(),
                    org_id=org_a,
                    address_line1="123 Alpha St",
                    city="Alpha City",
                    state="TX",
                    postal_code="75001",
                ),
                Property(
                    id=uuid.uuid4(),
                    org_id=org_b,
                    address_line1="456 Bravo Ave",
                    city="Bravo City",
                    state="TX",
                    postal_code="75002",
                ),
            ]
        )
    return org_a, org_b
