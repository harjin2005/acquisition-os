# PROGRESS.md — The one page that shows how much of AcquisitionOS is actually built

**This is for YOU (the founder) to check in on, any time, without re-reading the whole project.**
**Updated whenever a sprint/epic status changes — not every session. See `CURRENT_STATE.md` for
session-by-session detail; this file is the zoomed-out view.**

_Last updated: 2026-07-13_

---

## The one-line answer

**1 of 18 sprints closed. Sprint 2 in progress.** Everything is exactly where the plan
(`docs/product/31-execution-plan-v1.0.md`) says it should be for this stage — no shortcuts taken,
nothing skipped, nothing built out of order.

---

## Epic-by-epic status (13 epics, per DOC-131)

| # | Epic | Sprints | Status | Notes |
|---|---|---|---|---|
| E1 | Foundation | S1–S2 | 🟡 **S1 done, S2 tail open** | Repo, CI, Terraform (unapplied), WorkOS (mock mode), identity module — all verified running locally 2026-07-13. S2 tail = MFA flag + device sessions. |
| E2 | Ontology core | S2–S4 | 🟡 **In progress** | Some models exist (Owner, Contact, Consent, BuyBox) but no migration/service/router yet. Next up: outbox + audit schema. |
| E3 | Ingestion | S3–S6 | ⚪ Not started | **Blocked on vendor term sheet** (external — your task, not engineering's). Adapter framework can be built against fixtures without waiting. |
| E4 | Imports | S4–S5 | ⚪ Not started | |
| E5 | Resolution | S5–S7 | ⚪ Not started | |
| E6 | Underwriting | S6–S10 | ⚪ Not started | Depends on E3 (real data) to mean anything. |
| E7 | Pipeline & workspaces | S5–S9 | ⚪ Not started | Product UI (Today/Pipeline/Inbox) — frontend today is 3 auth-proving screens only. |
| E8 | Conversations | S7–S10 | ⚪ Not started | 10DLC carrier approval has lead time — flag when close. |
| E9 | Campaigns | S9–S12 | ⚪ Not started | Compliance-critical (suppression/consent) — extra review required per CLAUDE.md. |
| E10 | AI Agents | S8–S13 | ⚪ **Not started — 0 lines of code** | `backend/app/agents/*` are empty folders. This is expected at this stage. |
| E11 | Deals & outcomes | S10–S13 | ⚪ Not started | Models exist, nothing wired. |
| E12 | Commercial (billing, admin) | S12–S14 | ⚪ Not started | |
| E13 | Hardening & GA launch | S14–S18 | ⚪ Not started | |

🟢 done · 🟡 in progress · ⚪ not started

---

## What's actually blocking progress (read this before asking "why isn't X built yet")

Per the plan's own critical path:
**vendor data contract → ingestion → underwriting → golden datasets → accuracy gate → GA**

Three things are open and **not code**:
1. **ADR-006** — team size / runway — still undecided. Sprint dating scales off this.
2. **Vendor data contract** — negotiation hasn't started. Blocks E3 onward.
3. **Design partners** — 0 of the ≥5 needed before PRD freeze recruited.

More engineering sessions cannot out-run these three. If progress feels slow past Sprint 2,
check here first — it's very likely waiting on one of these three, not on Claude Code.

---

## Right now

- **Active task:** see `.claude/NEXT_TASK.md` (currently: Backend session fixing the bootstrap
  slug-conflict bug).
- **Session log:** see `.claude/CURRENT_STATE.md` for what each session did, in detail.

## How this file gets kept honest

- Only the **Architect session** updates this file (status changes, not routine work).
- A row moves 🟡→🟢 only when its acceptance criteria (per DOC-131) are actually met and shown
  working — not when someone says "basically done."
