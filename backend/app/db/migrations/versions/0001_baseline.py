"""baseline: schemas + organization + member + invite + property + RLS

Revision ID: 0001_baseline
Revises:
Create Date: 2026-01-15 00:00:00

Scope (Sprint 1, DOC-131):
- Ensure logical schemas exist: core, licensed, derived, audit, events.
- Ontology tables: core.organization, core.member, core.invite, licensed.property.
- Row-Level Security policies bound to `app.org_id` GUC (DOC-130 §5).
- Special policy for `core.organization`: the tenant is its own id.

Expand-contract note: this is a greenfield baseline; no contract phase needed.

Rollback: `alembic downgrade -1` drops the tables + policies but leaves the
schemas in place (they may host manual objects; explicit `DROP SCHEMA` requires
an operator step).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


TENANT_TABLES: list[tuple[str, str]] = [
    ("core", "member"),
    ("core", "invite"),
    ("licensed", "property"),
]


def upgrade() -> None:
    # ---- 1. Logical schemas -----------------------------------------------
    for schema in ("core", "licensed", "derived", "audit", "events"):
        op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))

    # ---- 2. Extensions ----------------------------------------------------
    op.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))

    # ---- 3. core.organization --------------------------------------------
    op.create_table(
        "organization",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("workos_org_id", sa.String(128), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        schema="core",
    )

    # ---- 4. core.member --------------------------------------------------
    op.create_table(
        "member",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("org_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column(
            "organization_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("core.organization.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("subject_id", sa.String(128), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("role", sa.String(16), nullable=False, server_default="member"),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "subject_id", name="uq_member_org_id_subject_id"),
        sa.CheckConstraint("role IN ('viewer','member','manager','admin','owner')", name="ck_member_role_enum"),
        sa.CheckConstraint(
            "status IN ('pending','active','suspended','removed')", name="ck_member_status_enum"
        ),
        schema="core",
    )

    # ---- 5. core.invite --------------------------------------------------
    op.create_table(
        "invite",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("org_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("role", sa.String(16), nullable=False, server_default="member"),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("invited_by", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "email", name="uq_invite_org_id_email"),
        sa.CheckConstraint("role IN ('viewer','member','manager','admin')", name="ck_invite_role_enum"),
        sa.CheckConstraint(
            "status IN ('pending','accepted','revoked','expired')", name="ck_invite_status_enum"
        ),
        schema="core",
    )

    # ---- 6. licensed.property (stub) -------------------------------------
    op.create_table(
        "property",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("org_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("address_line1", sa.String(200), nullable=False),
        sa.Column("city", sa.String(120), nullable=False),
        sa.Column("state", sa.String(2), nullable=False),
        sa.Column("postal_code", sa.String(10), nullable=False),
        sa.Column("source", sa.String(64), nullable=False, server_default="stub"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        schema="licensed",
    )

    # ---- 7. RLS ----------------------------------------------------------
    # organization: tenant IS its own id → policy binds `id` to app.org_id.
    op.execute(sa.text('ALTER TABLE core.organization ENABLE ROW LEVEL SECURITY'))
    op.execute(sa.text('ALTER TABLE core.organization FORCE ROW LEVEL SECURITY'))
    op.execute(
        sa.text(
            "CREATE POLICY organization_tenant_iso ON core.organization "
            "USING (id = current_setting('app.org_id', true)::uuid) "
            "WITH CHECK (id = current_setting('app.org_id', true)::uuid)"
        )
    )

    # All other tenant tables bind `org_id`.
    for schema, table in TENANT_TABLES:
        op.execute(sa.text(f'ALTER TABLE {schema}.{table} ENABLE ROW LEVEL SECURITY'))
        op.execute(sa.text(f'ALTER TABLE {schema}.{table} FORCE ROW LEVEL SECURITY'))
        op.execute(
            sa.text(
                f"CREATE POLICY {table}_tenant_iso ON {schema}.{table} "
                "USING (org_id = current_setting('app.org_id', true)::uuid) "
                "WITH CHECK (org_id = current_setting('app.org_id', true)::uuid)"
            )
        )

    # ---- 8. Service role provisioning ------------------------------------
    # The app engine uses the `acquisition_os` login. RLS applies to it because
    # it is not the owner in prod. Locally the same role owns the tables, so we
    # explicitly FORCE RLS (above) to keep the semantics identical to prod.
    # A dedicated `service_role` is added in migration 0002 (Sprint 3, E3).


def downgrade() -> None:
    for schema, table in TENANT_TABLES:
        op.execute(sa.text(f"DROP POLICY IF EXISTS {table}_tenant_iso ON {schema}.{table}"))
    op.execute(sa.text("DROP POLICY IF EXISTS organization_tenant_iso ON core.organization"))
    op.drop_table("property", schema="licensed")
    op.drop_table("invite", schema="core")
    op.drop_table("member", schema="core")
    op.drop_table("organization", schema="core")
