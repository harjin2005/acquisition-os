# DOC-110 — Phase 1 Venture Due Diligence Report

**Version:** 1.0
**Status:** Delivered to founder
**Prepared by:** Investment committee (adversarial review)
**Research date:** 2026-07-07 — market, pricing, and legal facts verified via live research on this date unless labeled otherwise
**Evidence labels:** VERIFIED (checked against current primary/secondary sources today) · HIGH CONFIDENCE (well-established, low drift risk) · LOW CONFIDENCE (plausible, needs validation) · UNKNOWN (no evidence; do not build on it)

---

## 1. Executive summary and verdict

**Verdict: BUILD WITH CHANGES.** The committee does not recommend abandonment and does not recommend a pivot away from the acquisition-OS thesis. It does require five binding changes (§13) before engineering spend, because the evidence gathered today kills one core assumption of the original vision:

**The "AI workforce" positioning is already commoditized.** Every incumbent has shipped named AI assistants and agents — PropStream ships an "Intelligence Assistant" and AI predictive scores (VERIFIED); BatchLeads ships Reia AI (deal analysis, scripts, offer prices) and BatchRank AI lead scoring (VERIFIED); DealMachine ships Alma, an OpenAI-powered assistant, plus an AI dialer (VERIFIED); REsimpli markets *nine* named AI agents including Speed-to-Lead AI, Call Answer AI, and Lead Score AI at $69–$149/mo entry pricing (VERIFIED); REISift has rebranded to DataSift and sells an "AI Plan" (VERIFIED); and at least one AI-first entrant (Deal Run, $99/mo) is already marketing against incumbents on their own pricing pages (VERIFIED). A startup whose differentiation is "we have AI employees" enters a market where AI employees are a $19/month add-on.

What is *not* commoditized — and where the committee finds a fundable company — is: (a) **measured, publishable underwriting accuracy** at a moment when flip margins are the thinnest since the financial crisis, making a $10–15K valuation error worth roughly a fifth of the median deal's entire gross profit; (b) a **clean domain ontology and outcome dataset** none of the incumbents possess because their data models conflate leads, properties, and owners; and (c) **compliance-grade outreach infrastructure** in a market where TCPA class actions are accelerating and every competitor's customers are exposed. These map directly to ADR-001..005, which the committee largely endorses — with sharpened conditions.

The company should be built as a **decision-quality and system-of-record company that uses AI**, not an AI-theater company. Marketing may say "AI acquisition team"; the product strategy, eval investment, and moat must be accuracy, workflow, and outcome data.

---

## 2. Market research report

### 2.1 Market activity — the wedge customer's world is contracting and margin-compressed (VERIFIED)

- 2025 full year: **297,045 home flips**, the fewest since 2020, down 3.9% from 309,050 in 2024. Flips were 7.4% of all home sales.
- Typical 2025 gross flip profit: **$65,981** (down from ~$77,000 in 2024); gross ROI **25.5% — the lowest since 2008**. Q4 2025 quarterly margin (23.6%) was the lowest since Q3 2007.
- Q4 2025: 68,999 flips executed by **54,992 distinct investors — averaging 1.25 flips per investor per quarter.** The market is radically fragmented; the modal "flipper" is tiny.
- Rehab and transaction expenses typically consume an estimated 20–33% of ARV on top of the purchase spread (ATTOM's stated industry estimate), meaning *net* margins on the median flip are thin to negative for undisciplined operators.
- 37.7% of 2025 flips used financing (rising), and the median flipped property was built in 1978 — the oldest on record — meaning rehab scope and rehab-cost risk are *increasing*.

### 2.2 What this means for the thesis (committee judgment)

1. **Pain is expensive and getting more expensive (HIGH CONFIDENCE).** At a $66K median gross profit with 20–33% of ARV in costs, a 4–5% ARV overestimate on a $320K resale routinely converts a projected profit into a loss. Underwriting precision is now survival, not optimization. This strengthens ADR-004's underwriting-centric agent trio.
2. **The market is cyclical and currently down (VERIFIED), which cuts both ways.** Bear case: customers' budgets shrink; software churn rises; TAM of active flippers is shrinking ~4%/yr. Bull case: margin compression punishes the spreadsheet-and-gut operators first, and disciplined tooling is exactly what survivors buy. The committee weighs this as neutral-to-slightly-favorable for a *quality* tool and unfavorable for a *volume/lead-gen* tool — another reason not to build yet another list-pulling product.
3. **Buy-and-hold demand is the stabilizer (HIGH CONFIDENCE).** Rental acquisition continues through flip downcycles; ADR-001's dual-mode wedge (flip + hold) is a deliberate hedge. Rental-side market sizing was not independently verified today (UNKNOWN — assigned to DOC-101).

### 2.3 TAM/SAM (LOW CONFIDENCE — flagged for DOC-101 with better method)

Order-of-magnitude only: ~55K quarterly-active flippers plus a larger population of active small landlords-who-acquire suggests low hundreds of thousands of active investor-buyers, of which teams matching the ADR-001 wedge (2–10 people, repeat acquirers) plausibly number in the low tens of thousands of organizations. At a $6K–$12K annual contract, the wedge SAM is plausibly **$150M–$400M ARR** — enough for a strong company, **not** enough for a billion-dollar outcome on the wedge alone. The billion-dollar path requires expansion (mid-market teams, disposition/lending adjacencies, data products). The committee flags this explicitly: the wedge is the entry, not the destination, and DOC-106 must show the expansion sequence. Bottom-up validation via design-partner pipeline is mandatory (§13).

---

## 3. Customer research — top 20 unsolved problems, ranked

Ranking synthesized from competitor review patterns observed today, incumbent feature gaps, and domain knowledge. **Ranks 1–8 are the committee's betting order, not validated fact; the 15–20 design-partner interviews (Phase 2 gap #1) must confirm or reorder before the PRD freezes.** Confidence per item noted.

1. **Underwriting error under margin compression** — ARV/rent/rehab misses now destroy entire deal profits (HIGH — market math is verified; salience to buyers needs interviews).
2. **Follow-up discipline / lead leakage** — most contracts come from the 5th+ touch; leads rot in CRMs; incumbents sell cadence tools but nothing that *decides* who/when/why (HIGH).
3. **Rehab cost estimation** — no incumbent solves it; oldest-ever housing stock being flipped raises the stakes (HIGH; solution difficulty also high — see risk register).
4. **Tool fragmentation and double data-entry** — the modal stack is 3–6 tools (data + skip trace + dialer + CRM + mail + spreadsheet); REsimpli's growth is direct evidence consolidation sells (VERIFIED signal).
5. **Skip-trace quality / wrong numbers** — universal complaint across DealMachine, BatchLeads reviews observed today (VERIFIED complaint pattern).
6. **List fatigue** — everyone pulls the same PropStream/BatchLeads lists; response rates decay; differentiated signal (list stacking is table stakes) is the ask (HIGH).
7. **Compliance anxiety** — TCPA filings up sharply (VERIFIED, §9); operators know someone who got sued; no incumbent makes compliance a first-class product surface beyond DNC scrubs (HIGH).
8. **Comps trust in thin-data areas** — non-disclosure states and rural counties (HIGH).
9. **Owner/entity intelligence** — LLC unmasking, multi-property owners, prior conversations forgotten across list re-pulls (HIGH; ties to our ontology advantage).
10. **Projected-vs-actual deal economics** — investors rarely close the loop on their own underwriting error (HIGH; this is also our moat-building behavior).
11. **Speed-to-lead on inbound** (HIGH; REsimpli already sells this — VERIFIED).
12. **Team accountability/KPIs** without spreadsheet gymnastics (MEDIUM-HIGH).
13. **Motivation-signal detection from conversation history** (MEDIUM; differentiating, unproven demand).
14. **Offer consistency across team members** (MEDIUM).
15. **Long-cycle nurture** of not-ready sellers (MEDIUM).
16. **Disposition/buyer matching** (MEDIUM; adjacent product).
17. **Contract-to-close coordination** with title/inspection parties (MEDIUM).
18. **Marketing-spend attribution** to closed deals (MEDIUM).
19. **Market selection/expansion analysis** (LOW-MEDIUM).
20. **Onboarding/training new acquisition hires** (LOW-MEDIUM; the "AI analyst as trainer" angle is interesting but unproven).

**Switching costs (HIGH CONFIDENCE):** primarily (a) data hostage-taking — years of leads/tags live in the incumbent; (b) habit and VA training; (c) annual contracts. A white-glove migration importer from PropStream/BatchLeads/DataSift/Podio exports is therefore a GTM weapon, not a nice-to-have (feeds DOC-605).

**Buying behavior (HIGH CONFIDENCE):** this segment buys through community — masterminds, YouTube educators, Facebook groups, podcasts — and through affiliate recommendation; note that most "review" content found today is affiliate- or competitor-authored, which the committee treated as a bias to correct for, and which also reveals the channel itself.

---

## 4. Competitor reverse engineering

Pricing VERIFIED today unless noted. Complaints are patterns from multiple review sources read today, not isolated anecdotes.

| Competitor | Model & price (monthly unless noted) | AI today | Core strength | Exploitable weakness |
|---|---|---|---|---|
| **PropStream** (owned by Stewart Title; acquired BatchLeads Jul 2025) | Data subscription: $99 / $199 / $699 (annual ≈ $81/$165/$583); per-seat add-ons $30; exports/credits metered | Intelligence Assistant; AI predictive scores | Deepest consumer-priced nationwide data (160M props); brand default | It is a *data terminal*, not a system of work: no real pipeline/deal economics; AI is Q&A, not decisions; owned by a title incumbent → innovates slowly |
| **BatchLeads** (PropStream co.) | $119 / $349 / $749 list + outreach platform; annual ≈ $71/$175; Reia AI in $19 seat fee; DialerAI $89 add-on; SMS via bring-your-own Twilio/10DLC | Reia AI assistant; BatchRank AI scoring; DialerAI live prompts | List building + outreach in one; strong filters | Compliance burden pushed onto customer (BYO SMS/10DLC); AI is generic assistant; review pattern: clunky onboarding, low response-rate complaints |
| **DealMachine** | $99 / $149–179 / $232–299 (+Teams $299+); unlimited skip tracing; mail $0.57–0.72/piece | Alma (OpenAI-powered) analysis/scripts; AI dialer w/ voice cloning, transcription | Best-in-class driving-for-dollars mobile UX; unlimited-contact pricing innovation | D4D niche; doesn't scale to team ops; review pattern: skip-trace accuracy, refund friction; mail costs balloon |
| **REsimpli** | $69 / $149 / higher tiers; all-in-one CRM (dialer minutes, accounting, e-sign included) | **9 named AI agents** (Speed-to-Lead, Call Answer, Lead Score on 150+ points) | The consolidation play; founder-operator credibility; closest to "OS" positioning | Breadth over depth: no evidence its AI is *accurate* (no published metrics anywhere — none of these vendors publish accuracy); underwriting is calculator-grade |
| **DataSift** (ex-REISift) | $149–$1,250; unlimited skip trace $97 add-on; "AI Plan" tier | AI plan w/ auto data enrichment | Best-in-class list hygiene/stacking; loyal power users | Data janitor positioning; no lead-gen data of its own; no underwriting |
| **FreedomSoft / InvestorFuse / Podio stacks** | Legacy all-in-ones and custom CRM builds (pricing not re-verified today — LOW CONFIDENCE) | Minimal | Entrenched in older wholesaling teams | Aging UX; Podio stacks require consultants; churn-vulnerable |
| **Follow Up Boss** (Zillow) | Agent/team CRM, not investor-specific | Yes (agent-oriented) | Follow-up excellence for *agents* | Not investor workflow; included for pattern only |
| **Deal Run** (AI-first entrant) | $99 flat, full-lifecycle claim (VERIFIED existence/price; depth UNKNOWN) | AI-native positioning | Aggressive SEO against incumbents' pricing pages | Unknown data depth; validates category timing and threatens the low end |

**Retention drivers across incumbents (HIGH CONFIDENCE):** data hostage-taking, annual billing, community/education lock-in, and bundled credits. **Why customers leave:** data accuracy disappointment, tool sprawl, price creep from credits/add-ons, and outgrowing the tool's workflow. **The 10x opening:** no competitor (a) publishes accuracy metrics, (b) models deals as economic objects with projected-vs-actual, (c) separates Owner/Property/Lead/Deal properly, or (d) treats compliance as product. Our 10x is *decision quality with receipts*, not more features.

**"What if X builds this?"** — PropStream/Stewart building real decisioning: possible but their incentive is data-terminal upsell and title attach; organizational history says slow (MEDIUM risk). REsimpli adding "underwriting accuracy": the credible fast-follower — our defense is the eval/outcome-data head start and published metrics they can't retrofit without our discipline (see §11). OpenAI/foundation labs: they commoditize the *model* layer, which helps us and hurts anyone whose moat is "we wrapped GPT"; they will not build county-data licensing, consent infrastructure, or REI workflow (HIGH CONFIDENCE). The correct paranoia is REsimpli + PropStream data, not OpenAI.

---

## 5. Opportunity matrix

Scored: customer value × differentiation durability × feasibility (H/M/L), with dependency notes.

| Opportunity | Value | Differentiation | Feasibility | Committee call |
|---|---|---|---|---|
| Dual-mode underwriting with **published per-metro accuracy** | H | H (no one publishes; requires eval discipline + outcome loop) | M (comps solvable; rehab hard) | **Core bet — fund** |
| Follow-up intelligence (who/when/why + approved-campaign execution) | H | M-H (cadence tools exist; *decisioning* + consent-grade audit doesn't) | H | **Core bet — fund** |
| Lead prioritization w/ explanation on entity-resolved graph | H | M (scoring exists — BatchRank, REsimpli LeadScore; graph + explanations are the edge) | H | **Core bet — fund** |
| Outcome dataset / projected-vs-actual deal economics | H (compounds) | H (structural — competitors' schemas can't capture it) | H | **Fund — schema in v1 (ADR-002)** |
| Compliance-as-product (consent provenance, DNC/litigator, audit) | M-H | M-H (incumbents outsource this pain) | H | **Fund — required by ADR-003 anyway** |
| Rehab estimation from photos/permits | H | H | **L** in v1 | Stage: v1 = structured user inputs + ranges (per ADR-004); model-assisted later |
| Migration importer from incumbents | M | L (copyable) but timing asymmetry | H | Fund as GTM tooling |
| AI voice calling | M | L (legally radioactive; §9) | M | **Do not fund** (revisit gate in DOC-304) |
| Disposition/buyer marketplace | M | M | M | Roadmap (DOC-306), not v1 |
| Nationwide data coverage at launch | L (for wedge) | L | L (COGS) | **Rejected — ADR-005 stands** |

---

## 6. Risk register (ranked by expected severity)

| # | Risk | Likelihood | Impact | Mitigation (owner doc) |
|---|---|---|---|---|
| R1 | **Underwriting accuracy insufficient to beat "PropStream + gut"** in launch metros → trust never forms → churn | M | Fatal | Golden datasets + holdout sold-comps per metro *before* GA; go/no-go accuracy gates; disclosure-state metros (DOC-303, ADR-005) |
| R2 | **SMB REI churn** (aspirational investors quit; market cycle down — §2 VERIFIED) | M-H | High | Qualify customers on deal history; team plans (teams churn less than solos); annual w/ migration lock-in; monitor logo vs revenue churn separately (DOC-605) |
| R3 | **TCPA/mini-TCPA exposure** via outreach module (litigation up sharply — §9 VERIFIED) | M | Fatal if unmitigated | ADR-003 architecture; specialist counsel pre-design; litigator scrub; consent provenance; contractual allocation with customers (DOC-501/507) |
| R4 | **Data COGS/contract terms break the margin model** (e.g., ATTOM standard API 24-hour caching limit — VERIFIED — is incompatible with our derived-layer design unless bulk-licensed) | M | High | DOC-105 vendor negotiations for derivative/persistence rights *before* schema freeze; metro-scoped licensing; multi-vendor abstraction (ADR-002) |
| R5 | **Fast-follow by REsimpli / PropStream bundling "good-enough AI" free** | M-H | Medium-High | Compete on measured accuracy + outcome data they can't retrofit; speed on eval infrastructure; avoid feature-checklist warfare (§11) |
| R6 | Rehab estimation disappoints → flip underwriting incomplete | H | Medium | v1 fallback UX is explicit (ADR-004 c.4); set expectations; permit-data enrichment as v1.5 |
| R7 | Wedge SAM too small for venture-scale outcome (§2.3 LOW CONFIDENCE) | M | Medium (strategic) | DOC-106 expansion sequencing; adjacency options (lending/title referral economics — PropStream/Stewart proves data→title attach works) |
| R8 | Skip-trace/consumer-data regulation tightens (state privacy laws proliferating — VERIFIED trend) | M | Medium | DSR deletion pipeline in v1 (DOC-503); provenance per record |
| R9 | AI cost per underwriting run erodes margin at scale | L-M | Medium | Model routing, caching, cost budget per run in DOC-301 |
| R10 | Founder/team lacks proprietary distribution (ADR-007 open) | UNKNOWN | Medium | Answer Q7; if no audience, budget for community GTM is materially higher (DOC-603) |

---

## 7. Business model analysis

**Pricing (proposal to be validated in DOC-602):** Team plans **$299 / $599 / $1,199 per month** (3 / 7 / 15 seats) anchored against the verified incumbent stack cost — a 5-person team running BatchLeads Professional ($349) + dialer ($95–199/agent) + CRM ($149) + skip trace overages plausibly spends $800–$1,500/mo today (VERIFIED component prices; stack-sum LOW CONFIDENCE pending interviews). Include metered usage wallet for skip traces/enrichment (pass-through + margin) so data COGS scales with revenue. Never sell "unlimited" data — DealMachine's unlimited-skip-trace pricing is a margin trap we should not copy without their scale (HIGH CONFIDENCE).

**Gross margin sketch (LOW CONFIDENCE until vendor quotes; framework VERIFIED):** per-record economics observed today — property records ~$0.0066–$0.01 at volume (BatchData tiers), skip traces ~$0.02–$0.15 depending on vendor/volume, ATTOM API calls ~$0.10 list-price with entry access from ~$95–500/mo, MLS/permits/valuation add-ons $400–$1,250/mo each, bulk licensing custom. A metro-scoped deployment with bulk-licensed baseline data plus per-use enrichment supports **75%+ blended gross margin at $299–$599 ACV tiers including AI compute** *if* derivative-rights and caching terms are negotiated (R4). If only 24-hour-cache API terms are available, the model degrades badly — this is the single most important commercial negotiation in the company's first year.

**CAC/LTV assumptions (all LOW CONFIDENCE — design-partner phase must generate real numbers):** community-led + founder sales CAC target <$1,500; at $500 blended MRR and 75% GM, payback <5 months; LTV hinges on churn (R2) — underwrite the plan at 3%/mo logo churn, not the 1.5% we'd like. Expansion revenue: seats, metros, usage, then disposition/lending adjacencies.

**Sales motion:** product-led trial is wrong for this wedge (data COGS per trial + accuracy-trust dynamics); use design-partner → founder-led sales → community/affiliate engine, with published accuracy reports as the demand-gen asset no competitor can copy quickly.

---

## 8. Open source report

Committee guidance, not final selection — DOC-406 performs the scored evaluation with license and maturity re-verified at write time. Labels: HIGH CONFIDENCE on category fit; specific version/maturity claims need re-verification (LOW CONFIDENCE on details).

| Layer | Candidates | Committee lean & rationale |
|---|---|---|
| Agent orchestration | LangGraph; Temporal (durable workflows); CrewAI/AutoGen | **LangGraph for agent graphs + Temporal for long-running business workflows** (follow-up sequences, closings are days-long processes — that's a workflow engine's job, not an LLM loop's). Avoid heavyweight multi-agent frameworks for v1's three agents |
| Memory | Postgres-first; Letta/mem0 patterns | Build tenant memory on our own schema (the knowledge graph IS the memory); adopt libraries only for conversation summarization patterns |
| Knowledge graph | Postgres w/ graph modeling vs Neo4j | **Start Postgres** (edges as tables) — our graph is queried, not traversed at depth; Neo4j only if entity-resolution traversal proves it out. One database until proven otherwise |
| RAG / vectors | pgvector; Qdrant | **pgvector** in v1 (tenant isolation stays in one system); Qdrant if scale demands |
| Search | OpenSearch; Meilisearch/Typesense | Meilisearch/Typesense for in-app property/lead search UX; OpenSearch only when analytics scale requires |
| Entity resolution | Splink (probabilistic linkage); usaddress/libpostal | **Splink + libpostal** — proven record-linkage stack; this is a core-moat component worth deep investment |
| Document processing | Unstructured; Docling; Tesseract/OCR stacks | Docling/Unstructured for contracts/settlement statements ingestion (outcome-data capture) |
| Browser automation | Playwright | For county-site gap-filling where contractually/legally permitted only (see §9 public-records terms) |
| Observability (AI) | Langfuse; OpenTelemetry | **Langfuse** for traces/evals + OTel platform-wide; eval harness is build-worthy IP on top |
| Voice | LiveKit/Pipecat | **Do not build in v1** (ADR-003); track only |
| Workflow/integration | n8n (self-hosted) internal ops; native integrations for product | Product integrations must be native (Twilio-class SMS providers, e-sign, calendars); n8n for internal ops only |
| Auth | Managed (WorkOS/Auth0/Clerk-class) over self-hosted Keycloak | Team-plan SSO needs later; don't run identity infrastructure at seed stage |

Build-vs-buy principle the committee imposes: **build only the moat** (ontology/graph, entity resolution, eval infrastructure, outcome capture, consent provenance); buy/adopt everything else.

---

## 9. Legal report

Ranked by exposure. Items marked VERIFIED reflect today's research.

**L1 — TCPA and state mini-TCPAs (severity: existential for outreach module).** Current state VERIFIED: the FCC's Feb 2024 declaratory ruling that AI-generated voices are "artificial or prerecorded voice" under the TCPA stands — AI voice calls require prior express consent, full stop. The FCC's one-to-one consent rule was vacated by the Eleventh Circuit (Insurance Marketing Coalition v. FCC, Jan 24, 2025) and formally rescinded; consent standards revert to the pre-2023 regime, and a Feb 2026 Fifth Circuit decision (Bradford) has courts independently interpreting consent post-Loper Bright — meaning the rules are in flux circuit-by-circuit. Revocation rules effective April 2025 require honoring opt-outs made by any reasonable means within ~10 business days; the broader "revoke-all" provision is delayed to Jan 31, 2027 but should be built for now. Litigation is accelerating (filings up sharply in 2025; settlements routinely seven figures; statutory $500–$1,500 per call/text, uncapped). State mini-TCPAs (Florida, Oklahoma, Texas SB 140 effective Sep 2025) layer stricter rules. **Committee ruling: ADR-003 is endorsed and hardened — consent provenance, cross-channel opt-out, quiet hours, litigator/DNC scrub, and per-message audit are v1 launch gates, not fast-follows; specialist counsel engagement precedes outreach-module design; AI voice remains out of scope with a formal revisit gate.** Vicarious liability flows up the vendor chain — our terms must allocate responsibility with customers explicitly, and our platform defaults must be the compliant path.

**L2 — Data licensing & derivative rights (severity: moat-defining).** VERIFIED example: ATTOM's standard API carries a 24-hour caching limit, with longer persistence requiring bulk licensing. Our entire ADR-002 derived-layer strategy depends on negotiated persistence/derivative/training rights. No vendor contract is signed without counsel review of these clauses (blocks DOC-105 sign-off).

**L3 — Consumer-data statutes (DPPA/GLBA/FCRA + CCPA/CPRA and state analogs).** Skip-trace data flows under permissible-use regimes; the platform must never use or present data for credit-like eligibility decisions (FCRA trigger). Property owners are consumers with deletion/access rights; DSR pipelines across licensed + derived layers are a v1 requirement (DOC-503). State AI/privacy statutes are proliferating (VERIFIED trend); an annual compliance-refresh cadence is required.

**L4 — Valuation/AVM liability.** Our underwriting outputs must be framed as investment-analysis tools with assumptions exposed, not appraisals; disclaimer architecture + no consumer-lending use cases in ToS (DOC-507). Publishing accuracy metrics (our strategy) also *reduces* misrepresentation risk relative to competitors' unmeasured claims.

**L5 — UPL (contract generation).** Offer documents via attorney-reviewed state templates + customer-supplied contracts only; no bespoke drafting by AI (DOC-302 boundary for the Underwriting/Offer surface).

**L6 — MLS licensing.** Comps depth in non-disclosure states requires MLS access we do not have a confirmed path to (UNKNOWN); ADR-005's disclosure-state metro preference is partly a legal-risk decision. RESO/broker-partnership options assigned to DOC-105.

**L7 — Wholesaling state regimes.** P1 per ADR-001; monitor (several states restrict assignment marketing; list is growing — re-verify at DOC-502 write time).

**L8 — Public-records site terms.** County scraping where vendors have gaps must respect site terms and CFAA-adjacent risk; default to licensed sources (LOW severity if defaults hold).

---

## 10. Data vendor report (preliminary — DOC-105 completes with quotes under NDA)

VERIFIED price signals from today: BatchData property records $0.0066–$0.01/record at tier volumes with plans ~$500–$5,000/mo (20K–750K records), skip tracing $0.02 down to ~$0.0066 at 3M enterprise volume, add-ons MLS $600/mo, valuations $600/mo, permits $1,250/mo, bulk via S3/Snowflake; ATTOM entry API access cited at ~$95–$500/mo with ~$0.10/call list pricing, 30-day trial, bulk/cloud licensing custom, **24-hour API caching limit**, rental AVM covering 72M SFRs, and notably an **MCP server for agentic access** (VERIFIED — directly relevant to our AI architecture and a signal vendors will court AI-native buyers); DataTree ~$0.12/report with title-plant lineage; PropertyRadar ~$0.08/record with West-Coast strength and daily updates.

Committee guidance: (1) **negotiate metro-scoped bulk licenses with explicit derivative/persistence rights** — our ADR-005 metro strategy is leverage, since we're buying 3–5 counties' depth, not nationwide breadth; (2) architect vendor-agnostic ingestion (ADR-002 consequence 2) and dual-source ownership data in launch metros to measure vendor accuracy empirically — accuracy claims found today are all vendor-authored (LOW CONFIDENCE by construction); (3) skip tracing should be multi-vendor waterfall with per-channel confidence and provenance retained (feeds both quality and consent posture); (4) rental comps: ATTOM rental AVM is a candidate baseline; independent verification needed (UNKNOWN accuracy).

---

## 11. Startup kill report (pre-mortem: it is 2029 and we are dead)

**Cause of death 1 — We shipped AI theater.** We demoed 15 agents; customers found the recommendations generic in *their* metro; trust never climbed the ladder; churn at 6%/mo; competitors matched our marketing with $19 add-ons. *Root cause: no accuracy gates, no outcome loop.* → Redesign: accuracy go/no-go gates per metro before GA (R1 mitigation); publish error metrics quarterly; every recommendation carries receipts.

**Cause of death 2 — Data economics ate us.** We promised nationwide, paid API list prices, cached nothing legally, re-fetched everything, and ran 40% gross margins that venture math couldn't survive. *Root cause: signed vendor contracts before understanding derivative rights.* → Redesign: metro-scoped bulk deals with negotiated persistence (R4); usage-metered pricing; COGS dashboard from day one.

**Cause of death 3 — A $12M TCPA class action.** Our follow-up agent texted a re-uploaded list containing revoked opt-outs; plaintiffs' firm found 30,000 violations. *Root cause: consent state lived in the customer's head, not our schema.* → Redesign: consent provenance and platform-enforced suppression that customers *cannot override* (ADR-003 hardened).

**Cause of death 4 — The market cycle + aspirational-customer churn.** We sold to anyone with a credit card; half our logos never closed a deal; the 2027 downturn cut flip activity another 15% and our revenue with it. → Redesign: qualify on deal history; dual-mode wedge (hold-side is countercyclical ballast); expansion revenue not logo-count as the growth engine.

**Cause of death 5 — REsimpli shipped "good enough" and PropStream bundled data cheaper.** We fought a feature-checklist war against an incumbent with structurally lower data costs. *Root cause: we let the battlefield be features instead of measured outcomes.* → Redesign: the moat is the outcome dataset + eval discipline + published accuracy — assets that require years of loop-closing competitors haven't started.

**Cause of death 6 — We built documentation instead of talking to customers.** Beautiful PRDs; zero design partners; first real feedback arrived post-build. → Redesign: §13 gate — no PRD freeze without 15+ interviews and 5+ committed design partners.

---

## 12. Pivot recommendations (evaluated and mostly rejected)

- **Pivot to pure data/AVM vendor:** rejected — capital-intensive, incumbent-owned game (ADR-002 reasoning stands; ATTOM/CoreLogic/First American won it).
- **Pivot to agent-facing (realtor) AI:** rejected — brutally crowded, MLS-gatekept, Zillow-shadowed.
- **Pivot to institutional/SFR-fund tooling:** rejected for now — procurement cycles kill seed-stage cadence; revisit as expansion (DOC-306).
- **Pivot to AI voice/dialer infrastructure:** rejected — legal posture (§9) and infrastructure competition.
- **Narrowing pivot worth holding in reserve (the committee's one genuine alternative):** *underwriting-only* — a measured-accuracy underwriting engine sold as API + app into incumbents' users ("the Bloomberg terminal answer, not the CRM war"). Lower burn, faster proof, weaker lock-in. If design-partner interviews rank follow-up/workflow pain below underwriting pain decisively, shrink v1 to this and add workflow later. Decision point: post-interviews, pre-PRD-freeze.

---

## 13. Final recommendation

**BUILD WITH CHANGES.** The problem is real and worsening (verified margin compression), the pain is expensive (verified deal economics), incumbents are structurally misbuilt to solve it (verified data models and unmeasured AI), the wedge and architecture decisions already taken (ADR-001..005) are directionally correct, and the moat design (outcome data + ontology + measured accuracy + compliance infrastructure) is genuinely hard to fast-follow. The billion-dollar case requires the expansion sequence beyond the wedge and is not yet proven (§2.3) — fundable, with eyes open.

**The five binding changes:**
1. **Reposition:** decision-quality OS that uses AI, with published per-metro accuracy — not "AI workforce." Marketing may personify; strategy may not. (Amends DOC-106 scope.)
2. **Accuracy gates:** underwriting agent does not GA in a metro until it beats defined error thresholds on holdout sold comps; thresholds set in DOC-303 and treated as launch blockers.
3. **Customer-proof gate:** ≥15 wedge-ICP interviews and ≥5 signed design partners (LOI + data-sharing) before DOC-201 freezes; §3 ranking must be re-validated against them.
4. **Data-rights gate:** no schema freeze (DOC-402) until at least one vendor term sheet grants persistence/derivative rights compatible with ADR-002; if unobtainable, escalate to committee — the moat design changes.
5. **Compliance gate:** TCPA-specialist counsel engaged before outreach-module design; consent provenance and platform-enforced suppression are unoverridable v1 requirements.

**Kill criteria (pre-committed, reviewed at month 9):** <5 design partners after 90 days of effort; underwriting error not beating baseline AVM in ≥2 launch metros after two model iterations; blended GM math below 60% under best negotiable data terms; or logo churn >5%/mo persisting two quarters post-GA. Any two of these → reconvene on the §12 narrowing pivot or wind-down.

*Changelog: v1.0 — initial committee report; ADR-001..005 reviewed and endorsed with conditions above.*
