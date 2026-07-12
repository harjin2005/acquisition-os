# CLAUDE.md — AcquisitionOS repo memory (KEEP UNDER ~150 LINES)

**Pruned monthly.** Prose is advisory — hooks and CI are law (DOC-131 §1).

## Stack (five lines)

- Backend: FastAPI + SQLAlchemy 2.0 + Alembic; Postgres 16 (prod) / 15 (dev, ADR-EMERGENT-001); Temporal Cloud (E9+); LiteLLM gateway; WorkOS auth.
- Frontend: Next.js/React + TanStack Query + Tailwind + Radix; generated TS SDK only.
- Data: three logical schemas (`licensed`, `core`, `derived`) + `audit`, `events`; RLS on every tenant table; `SET LOCAL app.org_id` inside every transaction.
- Infra: AWS ECS Fargate, RDS Postgres, ElastiCache Valkey, Meilisearch Cloud, S3, SES + Twilio-class SMS. Terraform. GitHub Actions.
- Ops team: 1–5 engineers + founder. Boring-technology bias throughout.

## Boundary graph (DOC-130 §3, enforced by import-linter)

```
api → modules → {ontology} → db
agents/* → tool registry only
campaigns.send_service is the ONLY messaging-provider egress
campaigns.suppression is the ONLY writer of suppression state
core.tenancy.service_role_session is ONLY importable from ingestion, admin
```

## The five non-negotiables

1. **Ontology naming is law** (DOC-002). Every table/field name must match the glossary; CI greps migrations.
2. **Module import rules** — modules communicate via service interfaces or domain events. Never import another module's models. Import-linter blocks the merge.
3. **Expand → backfill → contract** for every migration on a live table. Rollback note required in the PR.
4. **Tests ship with code.** Modules touched by a PR must have their fast tests pass in the Stop hook.
5. **No new deps without an entry in the OSS table** (DOC-130 §10).

## Where things live (`@`-paths only, don't inline docs)

- Company docs: @docs/product/
- Architecture Decision Records: @docs/adr/
- Per-module README: @docs/modules/<module>.md
- Rules with path scopes: @.claude/rules/
- Skills (repeatable playbooks): @.claude/skills/
- Reviewer + auditor subagents: @.claude/agents/

## Working method (DOC-131 §1.2)

- Plan mode first for any change touching campaigns / underwriting / privacy / >1 file.
- Vertical slices (schema → service → API → UI → tests) over horizontal layers.
- Show evidence: test output, command results. Assertions are not evidence.
- After two failed correction loops: `/clear`, rewrite the prompt.
- One task = one branch = one PR. Human reviews every PR.

## Definition of Done

Acceptance criteria met · tests written and passing · module README updated if interfaces changed · migration follows expand-contract · eval gate green if agent paths touched · no new dep without OSS-table entry · deployed to staging and smoke-checked.

## Never

- Redesign the product, ontology, ADR, or workflows without an ADR PR.
- Insert data manually into prod tables. Use migrations.
- Add a provider SDK outside the LiteLLM gateway (E10 rule).
- Ship an agent path change without the eval gate.
- Loosen an RLS policy to "fix" a test. Open an ADR instead.

## Sprint 1 pointer

Currently building Sprint 1 only. Scope: DOC-131 §2 items 1-6. Do not begin Sprint 2.
