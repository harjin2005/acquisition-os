"""ontology expansion + all core modules (M1)

Revision ID: 0002_ontology_expansion
Revises: 0001_baseline
Create Date: 2026-01-20

Adds every entity table for the V1 modular monolith:
- licensed.property: extended with the full DOC-002 §2 attribute set.
- core: owner, ownership_link, contact, contact_channel, consent_record,
  buy_box, lead, lead_event, deal, offer, deal_checklist, conversation,
  message, template, campaign, suppression, import_job.
- derived: motivation_signal, metro_coverage, underwriting_run, comp,
  agent_run, import_quarantine.
- audit: log, impersonation.
- events: outbox.

RLS enabled on every tenant table using the same policy shape as 0001.

Expand-only per DOC-130 §5. No contract phase needed (greenfield).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID


revision = "0002_ontology_expansion"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None


# Tables to add RLS policies to (schema, table).
TENANT_TABLES = [
    ("core", "owner"),
    ("core", "ownership_link"),
    ("core", "contact"),
    ("core", "contact_channel"),
    ("core", "consent_record"),
    ("core", "buy_box"),
    ("core", "lead"),
    ("core", "lead_event"),
    ("core", "deal"),
    ("core", "offer"),
    ("core", "deal_checklist"),
    ("core", "conversation"),
    ("core", "message"),
    ("core", "template"),
    ("core", "campaign"),
    ("core", "suppression"),
    ("core", "import_job"),
    ("derived", "motivation_signal"),
    ("derived", "metro_coverage"),
    ("derived", "underwriting_run"),
    ("derived", "comp"),
    ("derived", "agent_run"),
    ("derived", "import_quarantine"),
    ("audit", "log"),
    ("audit", "impersonation"),
    ("events", "outbox"),
]


def _uuid_pk():
    return sa.Column("id", UUID(as_uuid=True), primary_key=True)


def _tenant_cols():
    return [
        sa.Column("org_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    # ---- Extend licensed.property (expand-only additive columns) ---------
    with op.batch_alter_table("property", schema="licensed") as b:
        b.add_column(sa.Column("county", sa.String(120), nullable=True))
        b.add_column(sa.Column("apn", sa.String(64), nullable=True))
        b.add_column(sa.Column("beds", sa.Integer(), nullable=True))
        b.add_column(sa.Column("baths", sa.Float(), nullable=True))
        b.add_column(sa.Column("sqft", sa.Integer(), nullable=True))
        b.add_column(sa.Column("lot_sqft", sa.Integer(), nullable=True))
        b.add_column(sa.Column("year_built", sa.Integer(), nullable=True))
        b.add_column(sa.Column("assessed_value", sa.Float(), nullable=True))
        b.add_column(
            sa.Column(
                "tax_delinquent",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        b.add_column(sa.Column("last_sale_price", sa.Float(), nullable=True))
        b.add_column(
            sa.Column("last_sale_date", sa.DateTime(timezone=True), nullable=True)
        )
        b.add_column(sa.Column("source_ref", sa.String(128), nullable=True))
        b.add_column(
            sa.Column(
                "attributes",
                JSONB(),
                nullable=False,
                server_default=sa.text("'{}'::jsonb"),
            )
        )
    op.create_index("ix_property_apn", "property", ["county", "apn"], schema="licensed")

    # ---- core.owner ------------------------------------------------------
    op.create_table(
        "owner",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column(
            "entity_type", sa.String(16), nullable=False, server_default="unknown"
        ),
        sa.Column(
            "aliases", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")
        ),
        sa.Column(
            "resolution_confidence", sa.Float(), nullable=False, server_default="1.0"
        ),
        sa.Column("mailing_address", sa.String(400), nullable=True),
        sa.CheckConstraint(
            "entity_type IN ('person','entity','trust','unknown')",
            name="ck_owner_entity_type",
        ),
        schema="core",
    )

    op.create_table(
        "ownership_link",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "owner_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.owner.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("share", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("acquired_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "org_id", "owner_id", "property_id", name="uq_ownership_link"
        ),
        schema="core",
    )

    # ---- core.contact + channel + consent --------------------------------
    op.create_table(
        "contact",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column(
            "role", sa.String(32), nullable=False, server_default="owner_of_record"
        ),
        sa.Column(
            "owner_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.owner.id"),
            nullable=True,
        ),
        schema="core",
    )
    op.create_table(
        "contact_channel",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "contact_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.contact.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("address", sa.String(400), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column(
            "provenance", sa.String(64), nullable=False, server_default="unknown"
        ),
        sa.CheckConstraint(
            "channel IN ('sms','voice','email','mail')", name="ck_channel_type"
        ),
        sa.UniqueConstraint(
            "org_id", "contact_id", "channel", "address", name="uq_channel_address"
        ),
        schema="core",
    )
    op.create_table(
        "consent_record",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "channel_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.contact_channel.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "state", sa.String(20), nullable=False, server_default="consent_unknown"
        ),
        sa.Column("basis", sa.String(200), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "channel_id", name="uq_consent_channel"),
        sa.CheckConstraint(
            "state IN ('consent_unknown','prior_express','ebr','opted_out','dnc')",
            name="ck_consent_state",
        ),
        schema="core",
    )

    # ---- core.buy_box ----------------------------------------------------
    op.create_table(
        "buy_box",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("name", sa.String(200), nullable=False, server_default="Default"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "criteria", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        schema="core",
    )

    # ---- derived.motivation_signal + metro_coverage ---------------------
    op.create_table(
        "motivation_signal",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(24), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column(
            "provenance", sa.String(128), nullable=False, server_default="ingested"
        ),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "details", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.CheckConstraint(
            "kind IN ('absentee','pre_foreclosure','tax_delinquent','probate','inherited','vacant','tired_landlord','code_violation','divorce','high_equity')",
            name="ck_signal_kind",
        ),
        schema="derived",
    )
    op.create_index(
        "ix_motsig_property",
        "motivation_signal",
        ["org_id", "property_id"],
        schema="derived",
    )

    op.create_table(
        "metro_coverage",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("metro", sa.String(64), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="waitlist"),
        sa.Column(
            "disclosure_state", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column("freshness_hours", sa.Integer(), nullable=False, server_default="48"),
        sa.UniqueConstraint("org_id", "metro", name="uq_metro_coverage_org_metro"),
        sa.CheckConstraint(
            "status IN ('live','beta','waitlist','none')", name="ck_metro_status"
        ),
        schema="derived",
    )

    # ---- core.lead + lead_event -----------------------------------------
    lead_states = "'new','qualifying','researching','contact_attempted','in_conversation','underwriting','offer_extended','negotiating','under_contract','due_diligence','clear_to_close','closed','disqualified','dead','nurture'"
    op.create_table(
        "lead",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", UUID(as_uuid=True), nullable=True),
        sa.Column("source", sa.String(64), nullable=False, server_default="manual"),
        sa.Column("list_tag", sa.String(128), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="new"),
        sa.Column("assignee_member_id", UUID(as_uuid=True), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("score_version", sa.String(32), nullable=True),
        sa.Column(
            "reason_chips",
            JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("disqualified_reason", sa.String(200), nullable=True),
        sa.Column("last_state_change_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(f"status IN ({lead_states})", name="ck_lead_status"),
        schema="core",
    )
    op.create_index(
        "ix_lead_property_id", "lead", ["org_id", "property_id"], schema="core"
    )

    op.create_table(
        "lead_event",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "lead_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.lead.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("from_state", sa.String(32), nullable=True),
        sa.Column("to_state", sa.String(32), nullable=False),
        sa.Column("actor_id", UUID(as_uuid=True), nullable=True),
        sa.Column("reason", sa.String(200), nullable=True),
        sa.Column(
            "details", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        schema="core",
    )
    op.create_index(
        "ix_lead_event_lead", "lead_event", ["org_id", "lead_id"], schema="core"
    )

    # ---- core.deal + offer + checklist ----------------------------------
    deal_states = "'pursued','offer_sent','negotiating','under_contract','due_diligence','clear_to_close','closed','dead'"
    op.create_table(
        "deal",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("lead_id", UUID(as_uuid=True), nullable=False),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("strategy", sa.String(16), nullable=False, server_default="flip"),
        sa.Column("status", sa.String(24), nullable=False, server_default="pursued"),
        sa.Column("projected_arv", sa.Float(), nullable=True),
        sa.Column("projected_rehab", sa.Float(), nullable=True),
        sa.Column("projected_mao", sa.Float(), nullable=True),
        sa.Column("contract_price", sa.Float(), nullable=True),
        sa.Column("contract_signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("emd_amount", sa.Float(), nullable=True),
        sa.Column("close_target_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_close_price", sa.Float(), nullable=True),
        sa.Column("actual_arv", sa.Float(), nullable=True),
        sa.Column("actual_rehab", sa.Float(), nullable=True),
        sa.Column("actual_profit", sa.Float(), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("disposition", sa.String(32), nullable=True),
        sa.Column("dead_reason", sa.String(200), nullable=True),
        sa.CheckConstraint(f"status IN ({deal_states})", name="ck_deal_status"),
        sa.CheckConstraint(
            "strategy IN ('flip','rental','brrrr')", name="ck_deal_strategy"
        ),
        schema="core",
    )
    op.create_index("ix_deal_lead", "deal", ["org_id", "lead_id"], schema="core")

    op.create_table(
        "offer",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "deal_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.deal.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("emd", sa.Float(), nullable=True),
        sa.Column("inspection_days", sa.Integer(), nullable=True),
        sa.Column("close_days", sa.Integer(), nullable=True),
        sa.Column("financing", sa.String(16), nullable=False, server_default="cash"),
        sa.Column("status", sa.String(16), nullable=False, server_default="draft"),
        sa.Column(
            "terms", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.UniqueConstraint("org_id", "deal_id", "version", name="uq_offer_version"),
        sa.CheckConstraint(
            "status IN ('draft','sent','countered','accepted','rejected','expired','void')",
            name="ck_offer_status",
        ),
        schema="core",
    )
    op.create_index("ix_offer_deal", "offer", ["org_id", "deal_id"], schema="core")

    op.create_table(
        "deal_checklist",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "deal_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.deal.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False, server_default="task"),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="todo"),
        sa.CheckConstraint(
            "status IN ('todo','in_progress','done','waived')",
            name="ck_checklist_status",
        ),
        schema="core",
    )
    op.create_index(
        "ix_checklist_deal", "deal_checklist", ["org_id", "deal_id"], schema="core"
    )

    # ---- core.conversation + message ------------------------------------
    op.create_table(
        "conversation",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("contact_id", UUID(as_uuid=True), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), nullable=True),
        sa.Column("subject", sa.String(200), nullable=True),
        sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assignee_member_id", UUID(as_uuid=True), nullable=True),
        sa.Column("urgency", sa.String(16), nullable=False, server_default="normal"),
        sa.Column("summary_pinned", sa.Text(), nullable=True),
        schema="core",
    )
    op.create_index(
        "ix_conv_contact", "conversation", ["org_id", "contact_id"], schema="core"
    )
    op.create_index(
        "ix_conv_lead", "conversation", ["org_id", "lead_id"], schema="core"
    )

    op.create_table(
        "message",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "conversation_id",
            UUID(as_uuid=True),
            sa.ForeignKey("core.conversation.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("direction", sa.String(4), nullable=False),
        sa.Column("from_address", sa.String(400), nullable=True),
        sa.Column("to_address", sa.String(400), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="queued"),
        sa.Column("provider_ref", sa.String(128), nullable=True),
        sa.Column("campaign_id", UUID(as_uuid=True), nullable=True),
        sa.Column("template_version", sa.String(64), nullable=True),
        sa.Column(
            "consent_snapshot",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("suppression_reason", sa.String(64), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("direction IN ('in','out')", name="ck_message_direction"),
        sa.CheckConstraint(
            "channel IN ('sms','email','voice','mail','note')",
            name="ck_message_channel",
        ),
        sa.CheckConstraint(
            "status IN ('queued','sent','delivered','failed','received','opened','clicked','bounced','suppressed')",
            name="ck_message_status",
        ),
        schema="core",
    )
    op.create_index(
        "ix_msg_conv", "message", ["org_id", "conversation_id"], schema="core"
    )
    op.create_index(
        "ix_msg_campaign", "message", ["org_id", "campaign_id"], schema="core"
    )

    # ---- core.template + campaign + suppression --------------------------
    op.create_table(
        "template",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("version", sa.String(32), nullable=False, server_default="1.0.0"),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "variables", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")
        ),
        sa.CheckConstraint(
            "channel IN ('sms','email','mail')", name="ck_template_channel"
        ),
        schema="core",
    )
    op.create_table(
        "campaign",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column(
            "audience_query",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("audience_snapshot_hash", sa.String(64), nullable=True),
        sa.Column("audience_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "channels", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")
        ),
        sa.Column(
            "template_ids",
            JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "cadence", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column("status", sa.String(24), nullable=False, server_default="draft"),
        sa.Column("approved_by", UUID(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("signed_hash", sa.String(64), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('draft','pending_approval','approved','running','paused','void','completed')",
            name="ck_campaign_status",
        ),
        schema="core",
    )
    op.create_table(
        "suppression",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("channel", sa.String(8), nullable=False),
        sa.Column("address", sa.String(400), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("origin", sa.String(32), nullable=False, server_default="org"),
        sa.Column("added_by", UUID(as_uuid=True), nullable=True),
        sa.UniqueConstraint("org_id", "channel", "address", name="uq_suppression"),
        sa.CheckConstraint(
            "channel IN ('sms','voice','email','mail','all')",
            name="ck_suppression_channel",
        ),
        schema="core",
    )
    op.create_index(
        "ix_suppression_addr", "suppression", ["org_id", "address"], schema="core"
    )

    # ---- derived.underwriting_run + comp --------------------------------
    op.create_table(
        "underwriting_run",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), nullable=True),
        sa.Column("strategy", sa.String(16), nullable=False, server_default="flip"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "inputs", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "outputs", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "assumptions",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "overrides", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column("status", sa.String(24), nullable=False, server_default="draft"),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column(
            "model_version", sa.String(32), nullable=False, server_default="rulebase-v1"
        ),
        sa.Column("agent_run_id", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint(
            "strategy IN ('flip','rental','brrrr')", name="ck_uw_strategy"
        ),
        sa.CheckConstraint(
            "status IN ('draft','ready','insufficient_evidence','failed')",
            name="ck_uw_status",
        ),
        schema="derived",
    )
    op.create_index(
        "ix_uw_property",
        "underwriting_run",
        ["org_id", "property_id"],
        schema="derived",
    )

    op.create_table(
        "comp",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "run_id",
            UUID(as_uuid=True),
            sa.ForeignKey("derived.underwriting_run.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("property_id", UUID(as_uuid=True), nullable=False),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("sale_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sqft", sa.Integer(), nullable=True),
        sa.Column("beds", sa.Integer(), nullable=True),
        sa.Column("baths", sa.Float(), nullable=True),
        sa.Column("distance_miles", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("similarity", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column(
            "adjustment_details",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("excluded", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("exclusion_reason", sa.String(200), nullable=True),
        schema="derived",
    )
    op.create_index("ix_comp_run", "comp", ["org_id", "run_id"], schema="derived")

    # ---- derived.agent_run ----------------------------------------------
    op.create_table(
        "agent_run",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("agent_name", sa.String(32), nullable=False),
        sa.Column("agent_version", sa.String(32), nullable=False),
        sa.Column("prompt_version", sa.String(32), nullable=False),
        sa.Column("model", sa.String(64), nullable=False),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column(
            "inputs", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "output", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "tool_trace", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")
        ),
        sa.Column("tokens_in", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tokens_out", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cost_usd", sa.Float(), nullable=False, server_default="0"),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="running"),
        sa.Column("refuse_reason", sa.Text(), nullable=True),
        sa.Column("subject_id", UUID(as_uuid=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "agent_name IN ('prioritization','underwriting','followup')",
            name="ck_agent_name",
        ),
        sa.CheckConstraint(
            "status IN ('running','ok','failed','refused','human_review')",
            name="ck_agent_status",
        ),
        schema="derived",
    )
    op.create_index(
        "ix_agent_run_name",
        "agent_run",
        ["org_id", "agent_name", "started_at"],
        schema="derived",
    )

    # ---- core.import_job + derived.import_quarantine --------------------
    op.create_table(
        "import_job",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column(
            "dialect", sa.String(32), nullable=False, server_default="generic_csv"
        ),
        sa.Column("filename", sa.String(400), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column(
            "mapping", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("imported_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("quarantined_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column(
            "consent_attestation",
            JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending','running','completed','partial','failed','rolled_back')",
            name="ck_import_status",
        ),
        schema="core",
    )
    op.create_index(
        "ix_import_content_hash",
        "import_job",
        ["org_id", "content_hash"],
        schema="core",
    )

    op.create_table(
        "import_quarantine",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("job_id", UUID(as_uuid=True), nullable=False),
        sa.Column("row_num", sa.Integer(), nullable=False),
        sa.Column(
            "row_data", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "reasons", JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")
        ),
        schema="derived",
    )
    op.create_index(
        "ix_quarantine_job", "import_quarantine", ["org_id", "job_id"], schema="derived"
    )

    # ---- audit.log + audit.impersonation --------------------------------
    op.create_table(
        "log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(96), nullable=False),
        sa.Column("target_kind", sa.String(64), nullable=False),
        sa.Column("target_id", UUID(as_uuid=True), nullable=True),
        sa.Column(
            "metadata", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column("dual_witness_id", UUID(as_uuid=True), nullable=True),
        schema="audit",
    )
    op.create_index(
        "ix_audit_action", "log", ["org_id", "action", "created_at"], schema="audit"
    )

    op.create_table(
        "impersonation",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("supporter_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.String(400), nullable=False),
        sa.Column("consent_ref", sa.String(200), nullable=True),
        schema="audit",
    )

    # ---- events.outbox --------------------------------------------------
    op.create_table(
        "outbox",
        _uuid_pk(),
        *_tenant_cols(),
        sa.Column("kind", sa.String(96), nullable=False),
        sa.Column("aggregate_kind", sa.String(64), nullable=False),
        sa.Column("aggregate_id", UUID(as_uuid=True), nullable=False),
        sa.Column(
            "payload", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending','published','failed','dead')", name="ck_outbox_status"
        ),
        schema="events",
    )
    op.create_index("ix_outbox_kind", "outbox", ["kind", "status"], schema="events")

    # ---- RLS enable + policies ------------------------------------------
    for schema, table in TENANT_TABLES:
        op.execute(sa.text(f"ALTER TABLE {schema}.{table} ENABLE ROW LEVEL SECURITY"))
        op.execute(sa.text(f"ALTER TABLE {schema}.{table} FORCE ROW LEVEL SECURITY"))
        op.execute(
            sa.text(
                f"CREATE POLICY {table}_tenant_iso ON {schema}.{table} "
                "USING (org_id = current_setting('app.org_id', true)::uuid) "
                "WITH CHECK (org_id = current_setting('app.org_id', true)::uuid)"
            )
        )

    # audit.log: revoke UPDATE / DELETE from app role to enforce append-only
    op.execute(sa.text("REVOKE UPDATE, DELETE ON audit.log FROM acquisition_os"))


def downgrade() -> None:
    for schema, table in TENANT_TABLES:
        op.execute(
            sa.text(f"DROP POLICY IF EXISTS {table}_tenant_iso ON {schema}.{table}")
        )

    op.drop_table("outbox", schema="events")
    op.drop_table("impersonation", schema="audit")
    op.drop_table("log", schema="audit")
    op.drop_table("import_quarantine", schema="derived")
    op.drop_table("import_job", schema="core")
    op.drop_table("agent_run", schema="derived")
    op.drop_table("comp", schema="derived")
    op.drop_table("underwriting_run", schema="derived")
    op.drop_table("suppression", schema="core")
    op.drop_table("campaign", schema="core")
    op.drop_table("template", schema="core")
    op.drop_table("message", schema="core")
    op.drop_table("conversation", schema="core")
    op.drop_table("deal_checklist", schema="core")
    op.drop_table("offer", schema="core")
    op.drop_table("deal", schema="core")
    op.drop_table("lead_event", schema="core")
    op.drop_table("lead", schema="core")
    op.drop_table("metro_coverage", schema="derived")
    op.drop_table("motivation_signal", schema="derived")
    op.drop_table("buy_box", schema="core")
    op.drop_table("consent_record", schema="core")
    op.drop_table("contact_channel", schema="core")
    op.drop_table("contact", schema="core")
    op.drop_table("ownership_link", schema="core")
    op.drop_table("owner", schema="core")

    with op.batch_alter_table("property", schema="licensed") as b:
        for col in (
            "attributes",
            "source_ref",
            "last_sale_date",
            "last_sale_price",
            "tax_delinquent",
            "assessed_value",
            "year_built",
            "lot_sqft",
            "sqft",
            "baths",
            "beds",
            "apn",
            "county",
        ):
            b.drop_column(col)
