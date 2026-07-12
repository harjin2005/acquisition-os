# Architecture Decision Records

Every architectural decision at AcquisitionOS is captured here as an ADR. New ADRs use `_template.md`. Superseded ADRs stay in place — history is a feature.

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| ADR-001 | ICP wedge | Accepted | (DOC-001 v0.4) |
| ADR-002 | Hybrid data (licensed + derived moat) | Accepted | (DOC-001 v0.4) |
| ADR-003 | Outreach = human-approved campaigns, no AI voice | Accepted | (DOC-001 v0.4) |
| ADR-004 | Three agents (Prioritization, Underwriting, Follow-up) | Accepted | (DOC-001 v0.4) |
| ADR-005 | 3–5 disclosure-state metros | Accepted | (DOC-001 v0.4) |
| ADR-006 | Runway / team | Open | — |
| ADR-007 | Founder assets | Open | — |
| ADR-008 | Metro selection | Open | — |
| ADR-009 | Positioning | Proposed | (DOC-001 v0.4) |
| ADR-010 | Architecture (modular monolith, FastAPI, Postgres, RLS, Temporal, AWS) | Proposed | (DOC-001 v0.4) |
| ADR-011 | Pricing ($299 / $599 / $1,199 + usage wallet) | Proposed | (DOC-001 v0.4) |
| **ADR-EMERGENT-001** | **Runtime adaptation for Emergent preview** | **Accepted (dev-only)** | **2026-01-15** |

## Rules

- No architectural change ships without an ADR PR.
- Superseding an ADR is a new ADR, not an edit.
- Open ADRs (ADR-006 etc.) are blockers — call them out in your PR if you touch adjacent code.

The formal ADR files for ADR-001..011 live at the top of the repo (`01-decision-log-v0.4.md`) and are mirrored into `docs/product/`. This directory hosts **codebase-scoped** ADRs going forward.
