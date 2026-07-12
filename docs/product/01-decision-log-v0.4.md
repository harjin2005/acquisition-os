# DOC-001 — Decision Log / ADR Register

**Version:** 0.4
**Status:** Active
**Owner:** CEO / CTO
**Last updated:** 2026-07-07

Convention: decisions are numbered ADR-NNN, immutable once **Accepted**. Reversals get a new ADR that supersedes the old one. Every ADR records context, decision, rationale, and consequences — consequences are the part engineering reads.

---

## ADR-001 — Wedge ICP: SMB flippers & buy-and-hold teams (2–10 people)

**Status:** Accepted (Founder, 2026-07-07)
**Context:** Four candidate segments spanned \$100/mo self-serve to six-figure enterprise deals. A single wedge was required before the PRD could be written.
**Decision:** V1 is built for small investment teams (2–10 people) running fix-and-flip and/or buy-and-hold strategies. Other segments are explicitly out of scope for v1 (they remain in the long-term roadmap, DOC-306/106).

**Consequences:**
1. **Underwriting is the heart of the product** and must support two models from day one: flip underwriting (ARV via comps, rehab cost estimate, MAO formula, holding/selling costs) and rental underwriting (rent comps, cash flow, expense ratios, financing assumptions). This is more underwriting depth than a wholesaler wedge would need — and it raises two new data requirements: **rental comp data** and **rehab cost estimation**, both added to Phase 2 knowledge gaps.
2. Team-level features (pipeline stages, deal assignment, shared owner/conversation history, lightweight roles) are v1 requirements; enterprise RBAC/SSO is not.
3. Pricing hypothesis shifts to team plans (working range to validate in DOC-602: roughly \$300–\$1,500/mo per team, anchored against the combined cost of the 3–4 point tools these teams currently stack).
4. DOC-502 (state wholesaling matrix) drops from conditional-P0 to **P1** — assignment-based wholesaling is not the wedge workflow. Buyers still occasionally assign, so it is not dropped.
5. GTM channel focus (DOC-603): flipper/landlord communities, local REIAs, lending and title partners — not wholesaling masterminds.

---

## ADR-002 — Data posture: license baseline, build proprietary outcome & graph layer

**Status:** Accepted (Founder, 2026-07-07)
**Context:** Options were (a) license everything, (b) hybrid, (c) build a proprietary county-record pipeline. Incumbents already won the raw-data aggregation game.
**Decision:** License property records, ownership, valuation inputs, and skip tracing from established vendors. Build the moat as a proprietary layer on top: entity-resolved knowledge graph (owner ↔ entity ↔ property ↔ conversation over time), deal outcome data (what was offered, what closed, at what spread), and motivation signals derived from customer interactions.

**Consequences:**
1. **Vendor contracts become a product constraint.** Rights to cache, persist, derive, and train on licensed data must be negotiated explicitly. This is now a named requirement in DOC-105 and a counsel task in DOC-501. No vendor is selected without a derivatives-rights review.
2. **Data architecture (DOC-402) must enforce a hard boundary** between licensed raw data (subject to per-vendor retention/expiry/refresh terms) and the proprietary derived layer (ours, portable across vendor switches). Vendor swap-ability is an explicit design goal.
3. Outcome data is only a moat if captured cleanly: deal economics (offer → contract → close → resale/refi) must be first-class schema in v1, not a later add-on. Affects DOC-201 and DOC-402.
4. Customer data contributes to cross-tenant intelligence only under explicit, documented consent terms — flagged for DOC-503 and DOC-507.

---

## ADR-003 — Outreach autonomy: AI sends text/email within human-approved campaigns

**Status:** Accepted (Founder, 2026-07-07)
**Context:** Options ranged from AI-drafts-only to fully autonomous including AI voice. TCPA statutory damages (\$500–\$1,500 per violation) make outreach the highest-severity legal surface in the product.
**Decision:** V1 ships level (b) of the trust ladder for outreach: humans define and approve campaigns, audiences, and templates; the AI composes and sends individual text/email messages and handles reply triage within those bounds. Autonomous AI voice calling is **out of scope** until legal posture and consent infrastructure mature (revisit gate defined in DOC-304).

**Consequences:**
1. The following become **v1 requirements**, not P2 hardening: consent capture and provenance per contact, opt-out/DNC handling across channels, quiet-hours and frequency caps, litigator/DNC scrub integration, A2P 10DLC registration support, and a per-message audit log recording what the AI sent, to whom, under which approved campaign.
2. **Engaging TCPA-specialist counsel is now a P0 task** (DOC-501) and gates the outreach module's PRD — not its launch, its *design*.
3. DOC-304 (Autonomy Policy) must define the approval object precisely: what a "human-approved campaign" contains, what the AI may vary (wording, timing within caps), and what it may never do (new audiences, new claims, price commitments).
4. Deliverability infrastructure (domain warm-up, number pools, carrier compliance) enters DOC-403 integrations scope.

---

## ADR-004 — V1 agents: Lead Prioritization, Dual-mode Underwriting, Follow-up Intelligence

**Status:** Accepted (Founder, 2026-07-07)
**Context:** The long-term vision names ~15 AI roles; shipping all of them in v1 multiplies eval cost, latency, and trust-building burden (see DOC-000 §1.2).
**Decision:** V1 ships exactly three agents. (1) **Lead Prioritization** — scores and ranks pipeline with explainable reasons. (2) **Underwriting** — dual-mode per ADR-001: flip (comps → ARV → rehab estimate → MAO) and rental (rent comps → cash flow → return metrics), always with visible assumptions. (3) **Follow-up Intelligence** — recommends who to contact, when, and why; executes only through the human-approved campaign mechanism defined in ADR-003.

**Consequences:**
1. DOC-302 contains exactly three agent specs plus the shared platform spec; every other named role moves to DOC-306 (staged roadmap) with graduation criteria.
2. Each agent requires a golden eval dataset before launch (DOC-303): historical deals with known outcomes for prioritization; sold-comp holdout sets per launch metro for underwriting; response/conversion data for follow-up timing.
3. All three launch at trust-ladder level 1 (recommend + explain); Follow-up Intelligence connects to level-2 execution only via ADR-003's approved-campaign object.
4. Rehab estimation accuracy is the weakest link in the trio (see knowledge gap #11); the flip-underwriting spec must define a fallback UX (user-supplied or range-based rehab numbers) so the agent is useful before estimation is proven.

---

## ADR-005 — Geographic scope: 3–5 launch metros

**Status:** Accepted (Founder, 2026-07-07)
**Context:** Nationwide day-one coverage maximizes addressable market but multiplies data COGS and dilutes comps quality; per-metro accuracy is measurable and marketable.
**Decision:** V1 launches in 3–5 metros. Specific metro selection is deferred to **ADR-008** (open), informed by DOC-105 economics and early customer pipeline.

**Consequences:**
1. DOC-105 models data licensing costs per metro, enabling honest gross-margin math in DOC-602 before any nationwide commitment.
2. **Metro selection criteria** (to be scored in DOC-105): investor/flip transaction density; data quality and refresh cadence; **disclosure state preferred** — non-disclosure states (e.g., Texas) withhold sale prices from public records, materially degrading comps accuracy and raising MLS-dependence; proximity to design-partner customers.
3. DOC-303 sets underwriting accuracy targets *per metro* (e.g., median ARV error vs subsequent sale), which becomes a publishable proof point.
4. Product must handle out-of-coverage gracefully: clear boundaries in UX, waitlist capture for expansion metros (feeds DOC-605 expansion strategy).

---

## Open decisions (blocking noted documents)

| # | Decision | Blocks | Status |
|---|----------|--------|--------|
| ADR-006 | Runway, launch target, engineering headcount | P0/P1 cut lines across all workstreams | **Open — Q5** |
| ADR-007 | Founding-team proprietary assets (outcome data, audience, operator experience) | DOC-106 moat framing, DOC-603 | **Open — Q7** |
| ADR-008 | Launch metro selection | DOC-105 final cost model, DOC-303 eval datasets | **Open — needs DOC-105** |
| ADR-009 | Positioning: "decision-quality Acquisition OS" + five-line product philosophy as binding law (DOC-120 §13) | DOC-106, all marketing | **Proposed — awaiting founder acceptance** |
| ADR-010 | V1 architecture: modular monolith, Python/FastAPI + React/TS, single Postgres (pgvector, RLS), Temporal, AWS/ECS (DOC-120 §6–9) | DOC-401/402/405 | **Proposed — awaiting founder acceptance** |
| ADR-011 | Pricing: $299/$599/$1,199 tiers + usage wallet, no unlimited data, design-partner terms (DOC-120 §10) | DOC-602 | **Proposed — awaiting founder acceptance** |
