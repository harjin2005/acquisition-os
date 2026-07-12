# DOC-120 — Company Blueprint

**Version:** 1.0
**Status:** Delivered for founder review; sections marked "gated" freeze only after DD gates 3–4 clear
**Prepared by:** Founding executive team
**Governed by:** ADR-001..005 (accepted), DD binding changes 1–5 (DOC-110 §13), Domain Ontology (DOC-002, normative)
**Companion:** DOC-121 (Complete PRD + UX Blueprint, v0.9 gated)
**Evidence labels:** VERIFIED / HIGH CONFIDENCE / LOW CONFIDENCE / UNKNOWN, per DOC-110 conventions. Market and competitor facts labeled VERIFIED were verified 2026-07-07 in DOC-110.

---

## 14 → 1. Executive summary (deliverable 14, placed first)

We are building the **Acquisition Operating System** for small real-estate investment teams: the system of record and system of decision for finding, underwriting, pursuing, and closing property acquisitions. The company's product philosophy, imposed by evidence rather than preference: **accuracy is the product, workflow is the retention, outcome data is the moat, the knowledge graph is the intelligence layer, and AI is an implementation detail** (this philosophy is proposed for formal adoption as ADR-009, §13).

V1 serves 2–10 person flip and buy-and-hold teams (ADR-001) in 3–5 disclosure-state metros (ADR-005) with three AI capabilities (ADR-004) operating on a licensed-plus-derived data architecture (ADR-002) and a compliance-grade outreach layer (ADR-003). The smallest valuable version — defined precisely in §11 — is *not* a thin MVP: it is the full decision loop (ingest → prioritize → underwrite → pursue → close → capture outcome) at reduced breadth, because the moat (the outcome loop) only exists if the loop is closed from day one.

The complete vision (§1) is a platform where every acquisition decision an investment company makes is measurably better than the industry baseline, expanding from the wedge into mid-market teams, adjacent transaction economics (disposition, lending, title referral), and eventually the industry's reference dataset for private-market acquisition outcomes. The blueprint below is buildable by a competent team with minimal ambiguity; the fourteen deliverables map to sections as numbered.

---

## 1. Company Blueprint (Vision)

**Mission.** Make every acquisition decision an investment team takes as good as the best investor's best day — measurably.

**Vision (10-year).** The default operating system for private real-estate acquisition in the United States: when a property changes hands off-market, the buyer ran it through us; the industry's benchmark for underwriting accuracy and acquisition outcomes is our published data.

**Category definition.** *Acquisition Operating System (Acquisition OS).* Not a CRM (CRMs record activity; we drive decisions), not a data platform (data platforms sell records; we sell being right), not an "AI workforce" (VERIFIED commoditized — DOC-110 §1). The category claim we can own, because no competitor publishes accuracy and none can retrofit an outcome loop onto a schema that conflates leads, properties, and owners (VERIFIED structural gap — DOC-110 §4).

**Core principles (normative for all product decisions):**
1. **Receipts, always.** No recommendation without evidence the user can inspect: which comps, which signals, which assumptions. An unexplained output is a bug.
2. **Measured, then trusted.** Every AI capability launches at Trust Ladder Level 1 (DOC-002 §8) and earns promotion per-org with published criteria. We never ship autonomy ahead of accuracy.
3. **Close the loop.** Every projection meets its actual. Deal economics capture is a first-class workflow, not an admin chore, because it is simultaneously the customer's ROI proof and our moat.
4. **The compliant path is the default path.** Consent, suppression, quiet hours, and audit are platform-enforced and cannot be overridden by customers (DD binding change 5).
5. **One ontology.** Property ≠ Owner ≠ Contact ≠ Lead ≠ Deal (DOC-002). Every feature, table, and API respects it.
6. **Ruthless scope.** A feature exists only if it improves a measurable decision or is legally required. Feature-checklist warfare against incumbents is a named cause of death (DOC-110 §11.5) and is banned.

**Long-term strategy (three horizons).**
- **H1 (0–18 mo): Win the wedge on accuracy.** 3–5 metros, published error metrics, design-partner-led. Success = the wedge's operators say "their numbers are right" unprompted in communities.
- **H2 (18–36 mo): Own the record.** Metro expansion on a repeatable playbook; mid-market team tier; the outcome dataset reaches statistical usefulness (thousands of closed loops); begin monetizing decision infrastructure adjacencies (disposition matching, lender/title referral economics — the PropStream/Stewart structure proves data→title attach works, VERIFIED).
- **H3 (36+ mo): Become the reference.** Benchmark reports, capital-markets-grade data products, API platform. This is the billion-dollar case flagged as unproven in DOC-110 §2.3 (LOW CONFIDENCE — honest posture: H1/H2 are evidence-based; H3 is thesis).

**Competitive positioning.** Against PropStream/BatchLeads: "They sell you the same lists they sell everyone. We tell you which of them to act on, what to pay, and we show our error rate." Against REsimpli: "Nine AI agents, zero published accuracy. We publish ours per metro, every quarter." Against spreadsheets: "Your spreadsheet doesn't remember that you talked to this owner's LLC two years ago. We do."

**North Star Metric (NSM):** **Underwritten Deals Closed per active organization per month (UDC)** — a deal counts when it was underwritten on-platform before contract and its closing is recorded. Chosen because it is the customer's outcome, requires the whole loop to function, and directly grows the moat. **Guardrail metrics:** median absolute ARV error per metro (accuracy must not degrade as UDC grows) and weekly recommendation-acted-upon rate (trust proxy). Anti-gaming note: UDC cannot be inflated by usage theater; it requires closings.

**Company narrative (the story every hire and customer hears).** Margins in this industry are the thinnest since the financial crisis (VERIFIED: 25.5% gross ROI in 2025, lowest since 2008). The median flip's entire profit is one bad ARV away from zero. The incumbents responded by selling more leads and bolting chatbots onto list databases. We built the opposite: a system that makes fewer, better decisions — and proves it with published numbers. Investors don't need more software. They need to be right more often.

---

## 2. Product Strategy

**Jobs-to-be-done (ranked per DOC-110 §3; re-validation against design-partner interviews is DD gate 3):**
- JTBD-1: "When I'm about to commit capital, tell me the most I can pay and be right." (Underwriting; pain rank #1, HIGH)
- JTBD-2: "Never let a workable lead die of neglect — tell me who to contact today and why." (Follow-up; rank #2, HIGH)
- JTBD-3: "When 500 leads arrive, tell me which 20 deserve a human." (Prioritization; ranks #6/#9, HIGH)
- JTBD-4: "Run my acquisition business in one place with numbers I trust." (System of record; rank #4 consolidation, VERIFIED demand signal)
- JTBD-5: "Keep me out of a lawsuit while my team does outreach." (Compliance; rank #7, HIGH)

**Ideal Customer Profile (v1, sharpened from ADR-001):** US investment team, 2–10 people, ≥4 closed acquisitions in trailing 12 months (qualification gate per DOC-110 R2), strategy flip and/or hold, operating in a launch metro, currently paying ≥$400/mo across 2+ tools, with a designated acquisitions lead. **Anti-ICP (do not sell):** aspirational investors with zero closings; pure wholesalers running 50K-text blast operations (compliance and churn profile mismatch); institutions (procurement mismatch).

**Customer journey / decision journey.** Discover (community, accuracy reports, migration content) → Evaluate (accuracy demo on *their* metro + their last 3 closed deals re-underwritten — "backtest onboarding," our signature sales motion: we underwrite deals they already closed and show our error against their reality) → Commit (design-partner or annual plan; white-glove migration from PropStream/BatchLeads/DataSift/Podio exports) → Adopt (weeks 1–4 scripted: pipeline live, buy box configured, first campaign approved) → Trust (Level-1 recommendations reviewed daily; promotion offers appear when per-org accuracy thresholds met) → Expand (seats, metros, usage) → Advocate (their closed-loop stats become referenceable proof).

**Why customers switch (evidence-ranked):** backtest demo makes accuracy tangible pre-purchase; consolidation savings (verified incumbent stack costs, DOC-110 §7); migration importer kills the data-hostage lock (VERIFIED switching cost #1); compliance anxiety relief. **Why customers stay:** their outcome history and knowledge graph live here and compound (structural); the follow-up engine's value grows with tenure (data network effect within the org); published accuracy in their metro keeps improving with their own closed loops; annual plans + team habit.

**Differentiation durability test (per design principles):** accuracy discipline — copyable in theory, but requires eval infrastructure, holdout data, and a willingness to publish errors that incumbents' marketing departments will resist (HIGH); outcome dataset — not copyable without years of loop-closing and a schema rebuild (HIGH); ontology/graph — copyable by a new entrant, not by incumbents without breaking their installed base (HIGH); compliance infrastructure — copyable with effort (MEDIUM); everything else — assume copyable within 12 months and plan accordingly.

**Expansion strategy:** land (3-seat plan, one metro) → expand seats → expand metros → expand usage (enrichment wallet) → upgrade tier (mid-market features H2) → adjacencies (disposition, referral economics H2/H3). Net revenue retention target ≥110% by month 24 (LOW CONFIDENCE target, industry-plausible for team SaaS).

---

## 5. AI Blueprint

### 5.0 Platform (shared by all agents)

- **Model layer:** provider-agnostic gateway; routing policy per task class (cheap/fast models for extraction and drafts, frontier models for underwriting synthesis and negotiation-context reasoning); per-org and per-run **cost budgets** enforced at the gateway (DOC-110 R9). Prompt + model versions pinned per agent release; every output stamped with (agent_version, model, prompt_version) for auditability.
- **Tool layer:** agents act only through typed, permissioned tools (query_graph, get_comps, get_property, log_recommendation, draft_message, schedule_task…). No agent holds raw DB or network access. Tools enforce tenant isolation and trust-level checks server-side — an agent at Level 1 physically lacks send-capable tools (prompt-injection blast radius control; see §8 threat model).
- **Memory:** three scopes. *Org memory* — buy box, strategy, historical override patterns, tone preferences (structured, not free-text). *Entity memory* — the knowledge graph itself is the long-term memory (DOC-002 §8); conversation summaries attach to Contacts/Deals. *Run memory* — ephemeral per task. No cross-tenant memory, ever; cross-tenant learning happens only via aggregate model improvement under consent terms (ADR-002 c.4).
- **Evaluation harness (build-worthy IP):** golden datasets per agent per metro; offline eval gates in CI (no agent version deploys on regression); online metrics (acted-upon rate, override rate, downstream outcome deltas); quarterly published accuracy report generated from this harness. HITL review queues for low-confidence outputs.
- **Non-agent AI services:** entity resolution (Splink-based probabilistic linkage — deliberately *not* an LLM; determinism and auditability required, HIGH CONFIDENCE correct choice), conversation summarization, document extraction (settlement statements, contracts) feeding outcome capture.

### 5.1 Agent: Lead Prioritization ("which 20 deserve a human")

- **Purpose:** rank the org's active leads daily against the buy box and motivation evidence; explain every rank.
- **Inputs:** Leads + linked Property/Owner/Contact graph, list-stack dimensions (DOC-002 §6), conversation-derived motivation signals, buy box, historical org conversion patterns.
- **Outputs:** ranked queue with score components and receipts; disqualification suggestions (never auto-disqualify — decision boundary).
- **Tools:** query_graph, get_property, get_owner_portfolio, log_recommendation.
- **Memory:** org buy box + override history (an org repeatedly overriding a signal down-weights it *for that org*, surfaced transparently).
- **Decision boundaries:** recommends only; cannot change lead status; cannot contact anyone.
- **Escalation:** conflicting entity-resolution states, out-of-coverage properties, and buy-box-ambiguous leads route to a human review queue with the ambiguity named.
- **Evaluation:** precision@k against subsequent human qualification and contract outcomes; golden set = historical leads with known dispositions; online acted-upon rate. Failure modes: stale-data ranking (mitigation: data-freshness stamp on every receipt), popularity bias toward over-marketed list types (mitigation: response-decay features).
- **Trust level:** launches L1; L2 form = auto-assigning leads to team members under approved routing rules (post-GA, per-org promotion).

### 5.2 Agent: Underwriting ("the most I can pay, and be right")

- **Purpose:** dual-mode analysis per ADR-001/004 — flip (comps → adjusted ARV → rehab inputs → line-item MAO) and rental (rent comps → NOI → cash flow, DSCR, CoC, cap rate; BRRRR = both plus refi assumption).
- **Inputs:** subject Property, candidate comps (licensed data), org cost assumptions, user-supplied or range-based rehab estimate (ADR-004 c.4 fallback is the v1 default; model-assisted rehab is roadmap V2).
- **Outputs:** an immutable **Underwriting Run** (DOC-002): value conclusion with confidence band, comp set with per-comp adjustment table, full assumption sheet, MAO or return metrics, sensitivity view (what moves the answer). Every number traceable.
- **Tools:** get_comps, get_property, compute_adjustments, get_market_stats, create_underwriting_run.
- **Memory:** org assumption defaults; per-metro model calibration (from closed-loop actuals).
- **Decision boundaries:** never presents a value without ≥3 usable comps — below that it returns "insufficient evidence" with what's missing (explicit anti-hallucination stance; an authoritative-sounding wrong number is our worst failure mode); never auto-generates offers or contracts (L5 UPL boundary, DOC-110 §9); flags non-disclosure-data limitations explicitly.
- **Escalation:** confidence below threshold, comp-set disagreement above threshold, or user-override >X% from model value → flags for second-human review under org policy.
- **Evaluation (launch-gating per DD change 2):** median/percentile absolute error vs holdout sold comps per metro; post-hoc error vs actual resale/appraisal/refi values from the outcome loop; calibration of confidence bands. Go/no-go thresholds set in DOC-303; a metro doesn't GA until beaten.
- **Trust level:** L1 permanently in spirit — underwriting is advice by nature; "promotion" here means widening claims (tighter bands) as calibration proves out, never auto-acting.

### 5.3 Agent: Follow-up Intelligence ("never let a lead die of neglect")

- **Purpose:** daily who/when/why contact recommendations across active pipeline and nurture; drafts channel-appropriate messages; executes sends *only* within an approved Campaign (ADR-003 authorization object).
- **Inputs:** conversation history + summaries, lead/deal states and staleness, prior response patterns, campaign definitions, consent states.
- **Outputs:** L1 — recommendation cards (contact X today because Y, suggested message draft); L2 — sends executed under campaign bounds with full per-message audit.
- **Tools:** L1: query_graph, get_conversation, draft_message, log_recommendation. L2 adds send_message — a tool that is only mounted for orgs at L2 and that *itself* enforces consent, DNC/litigator suppression, quiet hours, and caps server-side (the agent cannot bypass what the tool refuses).
- **Memory:** per-contact cadence history; org tone profile; response-timing patterns.
- **Decision boundaries:** may vary wording and send-timing within caps; may never expand audience, invent claims, state prices or terms not in the approved template variables, or contact any consent-unknown/opted-out Contact (hard tool-level block).
- **Escalation:** any inbound reply expressing distress, legal threat, or opt-out ambiguity → human immediately + suppression pending review; sentiment-negative threads exit automation.
- **Evaluation:** response rate and progression rate vs org baseline and holdout cadences; complaint/opt-out rate (guardrail — rising opt-outs throttle the agent automatically); zero tolerance suppression-violation metric (must be 0.00%, monitored, alarmed).
- **Trust level:** L1 at onboarding; L2 per-org after (a) org completes compliance onboarding (10DLC, consent import attestation) and (b) 30 days of L1 with acted-upon rate above threshold. L3 not offered in v1 (ADR-003).

**Agents deliberately not built (simplification rule applied):** Market Research, Comparable Sales, Seller Motivation, Offer Generation, Negotiation, CRM Intelligence, Portfolio, Title Prep, Risk, Executive Dashboard "agents" from the original vision are views, reports, or sub-functions of the three above; each gets a one-line disposition in DOC-306 with graduation criteria if ever promoted to agenthood.

---

## 6. Database Blueprint

**System of record: PostgreSQL, single cluster, multi-tenant** (proposed ADR-010, §13). One database until proven otherwise (DOC-110 §8): graph-as-tables, pgvector for embeddings, logical schemas for licensed/derived separation. Redis for cache/queues where Temporal doesn't apply; Meilisearch for user-facing search (synced via outbox); S3 for documents.

**Schema organization (three logical layers, enforcing ADR-002):**
- `licensed.*` — vendor-sourced raw data. Every row: vendor_id, license_ref, fetched_at, expires_at, refresh_policy. Retention jobs enforce contract terms mechanically; nothing outside this schema may copy licensed raw fields, only reference them. Vendor swap = new adapter + backfill, derived layer untouched.
- `core.*` — the ontology entities (tenant data): organization, member, role_binding, property, owner, owner_alias, contact, contact_channel (with **consent_state, consent_provenance, suppression flags** as first-class columns), lead, deal, offer, conversation, message, campaign (with approval metadata: approved_by, approved_at, bounds jsonb), comp, underwriting_run (immutable; new analysis = new row), portfolio_asset, task, note, document.
- `derived.*` — the moat: graph_edge (typed: OWNS, CONTROLS_ENTITY, REACHABLE_AT, RELATED_TO…; columns: src, dst, type, confidence, provenance, valid_from, valid_to — **temporal edges**, because ownership changes), entity_resolution_cluster, motivation_signal (typed, evidenced, timestamped), outcome_record (deal economics: projected vs actual line items, realized spread, error attribution), embedding (pgvector), org_calibration.

**Event model:** append-only `events.domain_event` via transactional outbox (aggregate_type, aggregate_id, event_type, payload, org_id, actor, occurred_at). Consumers: search indexer, notification service, analytics, webhooks. This is also the substrate for audit and for replaying outcome-loop computations.

**Audit & versioning:** `audit.log` immutable (append-only, no UPDATE/DELETE grants): actor (human or agent+version), action, entity ref, before/after digest, tool call ref for agent actions. Mutable business entities use updated_at + event history rather than full temporal tables in v1 (pragmatic; underwriting_runs and campaigns are immutable where it legally matters).

**Tenant isolation:** org_id NOT NULL on every tenant table + Postgres **row-level security** as defense-in-depth beneath application scoping; RLS enforced in CI by tests that attempt cross-tenant reads. Per-org encryption keys deferred to enterprise tier (P3).

**Indexing (representative, exhaustive list in DOC-402):** (org_id, status, score desc) on lead for queue queries; GIST on property location; (org_id, contact_id, occurred_at) on message; unique partial on contact_channel(value) per org with suppression lookups covered; trigram on owner_alias.name for resolution candidates; ivfflat/HNSW on embeddings; (org_id, valid_to null) on graph_edge for current-state traversal.

**Caching:** Redis for hot property lookups and comp-set candidates with TTL ≤ licensed expires_at (cache may never outlive license terms — mechanical R4 compliance); computed org dashboards cached with event-driven invalidation.

**Outcome dataset (the moat, restated as schema):** outcome_record joins underwriting_run projections to settlement-statement actuals; every closed deal yields error attribution (value error, rehab error, timeline error, cost error). Cross-org aggregates computed only under consent flags (ADR-002 c.4) into anonymized `research.*` marts.

---

## 7. API Blueprint

- **Style:** REST, `/v1`, resources = ontology entities (singular names per DOC-002 §9). JSON; cursor pagination; RFC-7807 errors; idempotency keys on all POSTs that create or send; consistent `include=` expansion for graph context.
- **AuthN:** browser sessions (managed auth provider) + org-scoped API keys (hashed, prefixed, rotatable) for integration use; OAuth2 client-credentials deferred to public-platform phase (P2).
- **AuthZ:** role bindings evaluated per-resource; API keys carry scoped permissions (read:leads, write:deals…); trust-level checks on agent-invoked endpoints; all enforcement server-side, mirrored in RLS.
- **Rate limits:** per-key token bucket (default 10 rps, 100k/day), per-org send-rate limits on messaging endpoints aligned to compliance caps; 429 + Retry-After.
- **Async architecture:** Temporal for long-running business workflows (campaign execution, follow-up sequences, closing checklists, data ingestion pipelines — days-long, retryable, auditable); lightweight queue workers (Redis-backed) for fan-out jobs (enrichment, indexing, webhook delivery with signed payloads + retries/backoff + dead-letter).
- **Webhooks (v1 outbound set):** lead.created, lead.status_changed, deal.stage_changed, underwriting.completed, message.sent, message.received, consent.revoked, campaign.completed. HMAC-signed, versioned payloads, replay endpoint.
- **Internal events:** the §6 outbox is the single source; webhooks are a filtered projection of it.
- **SDK strategy:** OpenAPI spec is the contract; generated TypeScript SDK first (matches customer integrators and our own frontend), Python second. No hand-written SDKs.
- **Integration strategy (v1 = native, few, deep):** SMS/voice provider (Twilio-class) with 10DLC onboarding flows; email (transactional + sending domains with warm-up); e-sign (P1); calendar (P1); accounting export (P2); Zapier connector (P1 — the wedge lives in Zapier). Import pipeline: PropStream/BatchLeads/DataSift/Podio CSV dialects as first-class parsers (GTM weapon, DOC-110 §3).

---

## 8. Security Blueprint

- **Authentication:** managed provider (WorkOS/Auth0-class per DOC-110 §8); MFA available v1, enforceable per org; SSO/SAML deferred to mid-market tier (P2). Session hardening: short-lived tokens, refresh rotation, device listing.
- **RBAC (v1 roles, permissions matrix in DOC-504):** Org Owner (billing + all), Admin (config, members, campaign approval), Acquisition Manager (approve campaigns, promote trust levels within org policy, full pipeline), Member (work assigned leads/deals, draft campaigns), Read-only (reporting). Campaign approval and trust-level changes are privileged actions requiring Manager+ and are dual-logged.
- **Encryption:** TLS 1.2+ everywhere; AES-256 at rest (RDS/S3 with KMS, key rotation); secrets in AWS Secrets Manager, never in env-committed files; PII columns (contact channels) additionally application-encrypted where feasible without killing suppression lookups (design detail in DOC-504).
- **Audit:** §6 immutable log; admin console viewer with export; agent actions carry tool-call provenance; retention ≥ 7 years for consent/message audit (litigation posture, L1).
- **Threat model highlights (full STRIDE pass in DOC-504):** (a) **Prompt injection via untrusted content** — inbound SMS/email and scraped/ingested text are hostile inputs; agents reading them run with read-only tools; send-capable tools validate against approved-campaign bounds server-side; injected "instructions" cannot mint permissions. (b) **Cross-tenant leakage** — RLS + CI adversarial tests + no cross-tenant memory. (c) **Consent bypass** — suppression enforced in the send tool/service, not in agent logic; customers cannot override (DD change 5). (d) **Data exfiltration via export** — export permissioning + volume anomaly alerts (licensed-data contract obligation as much as security). (e) **Vendor key compromise** — scoped keys, egress allow-lists.
- **SOC 2:** controls designed-in from month 0 (access reviews, change management via PR-only deploys, vendor register); Type I target month 12, Type II month 20 (DOC-505). GDPR posture: US-market product, but privacy program (DOC-503) implements DSR pipelines that satisfy CCPA/CPRA and generalize.
- **Backups/DR:** RDS PITR + daily snapshots, cross-region copy; S3 versioning + replication; RPO ≤ 1h (PITR), RTO ≤ 8h v1 with quarterly restore drills; runbooks in DOC-506.

---

## 9. Engineering Blueprint

- **Architecture: modular monolith + workers** (proposed ADR-010). One deployable API/app with enforced module boundaries (ontology modules, underwriting, campaigns, ingestion), plus Temporal workers and queue workers. Justification: 3–6 engineers, one database, transactional integrity across ontology entities, and every named cause of death in DOC-110 §11 is a product/data failure, not a scaling failure. Microservices are rejected for v1 with a documented extraction path (ingestion and the send-service are the first candidates if ever needed).
- **Language/stack:** **Python (FastAPI) backend** — chosen over TS-backend because the moat components (Splink entity resolution, comps/calibration modeling, eval harness) are Python-native and a single backend language keeps a seed-stage team fungible (tradeoff acknowledged: TS full-stack sharing types is attractive; OpenAPI-generated types recover 80% of that). **React + TypeScript (Next.js) frontend.** Temporal (Python SDK). Postgres 16 + pgvector, Redis, Meilisearch, S3.
- **Infrastructure:** AWS, ECS Fargate (not Kubernetes at this size — ops burden), Terraform IaC, single production region + DR copies; staging + preview environments.
- **CI/CD:** GitHub Actions; trunk-based, PR-only, required checks: unit/integration tests, RLS adversarial tests, migration safety check, **AI eval regression gates** (agent versions ship like code — a failing golden-set eval blocks merge), OpenAPI drift check. Deploys: blue/green on ECS; feature flags for trust-level and metro rollouts.
- **Testing strategy:** pyramid (unit > integration > few E2E) plus the eval harness as a first-class test tier; synthetic tenant fixtures; load tests on queue/send paths before GA.
- **Observability:** OpenTelemetry traces end-to-end including tool calls; Langfuse for agent traces/evals; metrics + alerting (Grafana-stack or Datadog — cost decision in DOC-405); per-org COGS dashboard from day one (data + AI spend per org — DOC-110 §11.2 redesign requirement).
- **Cost optimization:** model routing + response caching keyed on (inputs, model_version); licensed-data cache-to-contract-limit; metro-scoped ingestion; Fargate right-sizing; the COGS dashboard makes unit economics a weekly engineering metric, not a quarterly surprise.

---

## 10. Business Model

- **Packaging (proposed ADR-011):** **Team $299/mo** (3 seats, 1 metro, L1 agents, 1k enrichment credits), **Growth $599/mo** (7 seats, 2 metros, L2 eligibility, 3k credits, API read, Zapier), **Scale $1,199/mo** (15 seats, 4 metros, priority support, API write, advanced reporting). Annual = 2 months free. **Usage wallet** for skip-trace/enrichment beyond credits at pass-through + ~40% margin. **Never unlimited data** (DOC-110 §7, HIGH CONFIDENCE). Design-partner cohort: Growth features at $299 + data-sharing agreement.
- **Data economics / margins:** metro-scoped bulk licensing + metered enrichment targets ≥75% blended GM (LOW CONFIDENCE until vendor term sheets — DD gate 4); the send/telephony layer is pass-through-plus; AI compute budgeted per run with gateway enforcement. Margin floor 60% is a kill-criterion input (DOC-110 §13).
- **Sales motion:** design partners → founder-led sales with the **backtest demo** as the conversion weapon → community/affiliate channel (VERIFIED as the segment's buying channel) with a clean-hands affiliate policy (no fake-review content — we compete with published accuracy, and our affiliate content must survive scrutiny).
- **Growth loops:** (1) quarterly published accuracy report → community distribution → demo requests; (2) closed-loop customer stats → referenceable proof → referrals (incentivized); (3) migration importer → switch content ("leave PropStream in an afternoon") → SEO; (4) outcome benchmarks ("teams like yours convert X% from probate lists in metro Y") → expansion and stickiness.
- **Customer success:** onboarding is scripted weeks 1–4 (above); health score = weekly active decision-makers + recommendation-acted-upon rate + loop-closure rate; churn saves focus on orgs whose *deal flow* dropped (market-cycle churn, R2) with plan-pause option rather than logo loss.

---

## 11. Product Roadmap

**V1 — "The Loop," months 0–9 (the smallest valuable version).** Scope: everything in DOC-121 marked P0. 3 launch metros (ADR-008 selects). Definition of done: a design-partner org runs its entire acquisition operation on-platform; ≥1 metro passes accuracy gates; ≥25 closed deals captured in the outcome dataset; zero suppression violations. **Explicitly excluded from V1:** AI voice (ADR-003), model-based rehab estimation, driving-for-dollars mobile capture, disposition marketplace, public write API, SSO, nationwide coverage, direct mail (partner referral only).

**V2 — "Proof at Width," months 9–18.** Metros 4–8 via repeatable data-onboarding playbook; permit-data rehab enrichment + structured rehab estimator v1; L2 trust promotion GA'd broadly; e-sign + calendar + Zapier live; reporting suite; first published accuracy report; disposition buyer-list module (P1 from matrix); pricing tier enforcement matured.

**V3 — "The Record," months 18–36.** Mid-market tier (15–50 seats, SSO, advanced RBAC, audit exports); outcome-benchmark products; lender/title referral economics pilots; L3 autonomy pilots for Follow-up under strict gates; evaluate MLS partnership paths for non-disclosure expansion (L6); ADR-012 decision on nationwide.

**What we will not build (standing list, changeable only by ADR):** AI voice calling (until DOC-304 gate), consumer-facing anything, agent/realtor tooling, a general-purpose CRM, unlimited-data pricing, lead marketplaces/selling customer leads (trust-fatal), and any feature whose only justification is competitor parity.

---

## 12. Success Metrics

| Category | Metric | V1 target (LOW CONFIDENCE until baselined) |
|---|---|---|
| North Star | UDC/org/month | ≥1.0 by month 9 across design partners |
| AI — accuracy | Median abs ARV error per metro (holdout) | Beats baseline AVM by ≥15% relative; gates GA |
| AI — calibration | Actuals within stated confidence band | ≥80% |
| AI — trust | Recommendation acted-upon rate (7-day) | ≥40% |
| AI — safety | Suppression violations | 0 (alarmed) |
| Product | Weekly active decision-makers per org | ≥60% of seats |
| Product | Loop closure (closed deals with captured economics) | ≥80% |
| Business | Logo churn / NRR | ≤3%/mo underwriting assumption; NRR ≥110% by mo 24 |
| Business | Blended gross margin | ≥75% (floor 60% = kill input) |
| Business | CAC payback | <6 months founder-led |
| Engineering | Deploy frequency / change-fail rate | ≥daily / <10% |
| Engineering | p95 underwriting run latency | <60s full run |
| Financial | Per-org COGS visibility | 100% orgs on dashboard, weekly review |

---

## 13. Recommended ADR changes (proposed, not silently applied)

- **ADR-009 (new): Positioning & product philosophy.** Adopt "decision-quality Acquisition OS" positioning and the five-line philosophy (accuracy/workflow/outcome data/graph/AI-as-detail) as binding product law, implementing DD binding change 1. Supersedes the "AI workforce" framing of the original vision *as strategy* while permitting personified marketing. No prior ADR contradicted.
- **ADR-010 (new): v1 technical architecture.** Modular monolith on Python/FastAPI + React/TS, single Postgres (pgvector, RLS), Temporal, Redis, Meilisearch, AWS/ECS, per §6–9. Includes the rejected-alternatives record (microservices, Neo4j-first, TS-backend, Kubernetes) and extraction paths.
- **ADR-011 (new): Pricing architecture.** Tiered team plans + usage wallet, no unlimited data, design-partner terms, per §10.
- **No changes proposed to ADR-001–005.** ADR-006/007 remain open (runway/team, founder assets) and now materially block final roadmap dating and GTM budget in this blueprint — flagged again.

## 12b. Outstanding unknowns (deliverable 12 of the brief's final list)

Carried and new: (U1) interview-validated pain ranking — DD gate 3, blocks PRD freeze; (U2) vendor derivative/persistence terms + real COGS — DD gate 4, blocks schema freeze and ADR-011 margins; (U3) rehab estimation feasibility/accuracy path (R6); (U4) rental comp source accuracy (UNKNOWN per DOC-110 §10); (U5) MLS access path for non-disclosure expansion (L6); (U6) ADR-006/007 answers; (U7) launch-metro selection (ADR-008, needs U2); (U8) real churn behavior of qualified wedge (R2 — only design partners answer this); (U9) whether backtest-onboarding converts as modeled (test in first 10 sales conversations); (U10) open-source selections' current maturity (re-verify at DOC-406 write time).

*Changelog: v1.0 — initial blueprint; proposes ADR-009..011; companion PRD/UX at DOC-121 v0.9 (gated).*
