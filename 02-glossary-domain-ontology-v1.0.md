# DOC-002 — Glossary & Domain Ontology

**Version:** 1.0 (Proposed for adoption)
**Status:** Review
**Owner:** Technical Writer + Real Estate Consultant
**Applies to:** All documents DOC-1xx through DOC-6xx; database schema naming; API naming; UI copy
**Last updated:** 2026-07-07

---

## 1. Purpose and rules of use

Real estate CRMs routinely conflate "lead," "property," "owner," and "deal," which corrupts data models and makes multi-property owners and repeat sellers impossible to reason about. This document is **normative**: subsequent documents, schema names, API resources, and UI copy use these terms exactly as defined. Proposals to change a definition go through an ADR.

Terms are grouped: platform ontology (§2), lifecycle states (§3), underwriting & finance (§4), transaction & closing (§5), data & lead sources (§6), outreach & compliance (§7), AI & platform (§8).

---

## 2. Core platform ontology

These are the primary entities. The critical discipline: **a Lead is not a Property, an Owner is not a Contact, and a Deal is not a Lead.** Getting these separations right is a competitive advantage in itself — most incumbent tools do not.

**Property** — A physical parcel or unit, identified by address and, where available, APN (Assessor's Parcel Number). Properties exist independently of any marketing activity. One Property can be the subject of many Leads over years. Properties carry physical attributes (beds, baths, sqft, lot, year built), assessed/tax data, transaction history, and lien/distress indicators.

**Owner** — The person or legal entity that holds title to one or more Properties. Owners are **entity-resolved**: "Smith Family Trust," "J. Smith," and "John A Smith" pointing at the same human/trust collapse to one Owner node. An Owner links to many Properties (the ownership graph is a first-class asset per ADR-002).

**Contact** — A reachable human with communication channels (phones, emails, mailing address) and consent state. A Contact may represent an Owner, an agent of an Owner (attorney, heir, property manager), or a third party. Skip tracing produces Contacts *linked to* Owners; it does not modify the Owner record itself.

**Lead** — A dated hypothesis that a specific Property might be acquirable, from a specific source (list pull, driving-for-dollars, inbound call, referral). Leads carry source, status, score, and assignment. Multiple Leads on one Property (e.g., 2024 tax list, 2026 probate list) are distinct records linked to the same Property — recycled interest is signal, not duplication.

**Deal** — Created when pursuit becomes concrete: an Offer is extended or a Contract exists. A Deal carries economics (offer history, contract price, EMD, projected and realized returns), strategy (flip vs hold), and closing state. Deals are the atomic unit of the **outcome dataset** (ADR-002): every Deal's projected-vs-actual economics feed the proprietary layer.

**Offer** — A priced proposal on a Deal, with terms (price, EMD, inspection period, closing timeline, financing/cash) and status (draft, sent, countered, accepted, rejected, expired). Offers are versioned; a negotiation is a chain of Offers.

**Conversation** — The full communication history between the Organization and a Contact, across channels (SMS, email, call logs/recordings, letters), threaded per Contact and visible from the linked Lead/Deal. Conversations are the raw material for motivation signals (§8).

**Campaign** — A human-approved outreach definition per ADR-003: audience specification, channel(s), template family, cadence rules, caps, and approval metadata. The Campaign is the *authorization object*; individual sends execute under it.

**Comp (Comparable)** — A recently sold (or, for rentals, leased) property used as evidence in underwriting, with adjustment records showing how its price was translated to the subject Property. Comps used in an Underwriting Run are frozen with it for auditability.

**Underwriting Run** — A versioned analysis of a Property for a strategy (flip or rental): inputs (comps set, rehab estimate, assumptions), outputs (ARV or rent, MAO or return metrics), model/agent version, and human overrides. Runs are immutable; re-analysis creates a new Run.

**Organization / Workspace** — The tenant. Contains members with roles, and owns all Leads, Deals, Conversations, and derived data. Tenant isolation guarantees are specified in DOC-402/504.

**Portfolio Asset** — A Property the Organization has acquired and holds (buy-and-hold) or is rehabbing (flip in progress), with its own financial tracking distinct from acquisition-stage records.

---

## 3. Acquisition lifecycle states

Canonical pipeline (states, not entities — Leads move through the early states; Deals through the later ones):

`New → Qualifying → Researching → Contact Attempted → In Conversation → Underwriting → Offer Extended → Negotiating → Under Contract → Due Diligence → Clear to Close → Closed → (Disposition | Portfolio)` with terminal branches `Disqualified`, `Dead`, and `Nurture` (long-term follow-up) available from most states.

**Qualification** — Cheap filtering before spending research effort: does the Property fit the buy box, is the Owner plausibly reachable, is there any distress/motivation signal.

**Buy Box** — An Organization's declared acquisition criteria (geographies, property types, price band, condition tolerance, strategy). Machine-readable; Lead Prioritization scores against it.

**Nurture** — Deliberate long-cycle follow-up on Leads not ready to transact. Distinct from Dead; a primary surface for the Follow-up Intelligence agent.

**Disposition** — Exit of a Deal or Asset: assignment, wholetail, retail resale after rehab, or refinance into hold (BRRRR).

---

## 4. Underwriting & finance

**ARV (After Repair Value)** — Projected market value of a Property after planned rehab, evidenced by adjusted Comps. The central number in flip underwriting.

**Rehab Estimate** — Projected renovation cost. V1 supports user-supplied values and range-based estimates (per ADR-004 consequence 4); model-assisted estimation is a staged capability.

**MAO (Maximum Allowable Offer)** — The ceiling price at which a Deal still meets the Organization's required margin. The classic heuristic is the **70% Rule** (MAO ≈ 70% × ARV − rehab), but MAO in this platform is always computed from explicit line items (holding costs, selling costs, financing costs, required profit), with the 70% rule available as a sanity check — never as the hidden formula.

**Holding Costs** — Carrying costs during ownership: financing interest, taxes, insurance, utilities, maintenance, HOA.

**Rental underwriting terms:** **Gross Scheduled Rent**; **NOI** (Net Operating Income = income − operating expenses, excluding debt service); **Cap Rate** (NOI ÷ price); **Cash-on-Cash Return** (annual pre-tax cash flow ÷ cash invested); **DSCR** (NOI ÷ annual debt service — also the qualifying metric for DSCR loans common in this segment); **GRM** (price ÷ gross annual rent); **the 1% Rule** (monthly rent ≥ 1% of price — heuristic only, labeled as such).

**BRRRR** — Buy, Rehab, Rent, Refinance, Repeat: acquiring below market, forcing appreciation via rehab, then refinancing to recover capital. Underwriting a BRRRR requires *both* modes of ADR-004's dual-mode engine plus a refinance assumption (ARV × lender LTV).

**Equity / LTV** — Owner equity = estimated value − open loan balances; LTV = loans ÷ value. High-equity owners are a canonical motivated-seller list dimension.

**Spread** — In assignment/wholetail exits, the difference between contract price and disposition price.

---

## 5. Transaction & closing

**EMD (Earnest Money Deposit)** — Buyer's deposit held in escrow demonstrating good faith; forfeiture terms are contract-defined.

**Assignment** — Selling one's position in a purchase contract to an end buyer for a fee (contract must permit it; state rules per DOC-502).

**Double Close** — Two back-to-back closings (A→B, B→C) used instead of assignment; requires transactional funding or same-day settlement.

**Escrow** — Neutral third party holding funds/documents until contractual conditions are met. In some states this is an attorney (attorney-close states), in others a title/escrow company — a workflow difference DOC-104 must map.

**Title Search / Title Commitment** — Examination of the chain of title producing a commitment to insure, listing requirements and exceptions (liens, easements, judgments) that must be cleared.

**Cloud on Title** — Any unresolved claim or defect (unreleased lien, probate gap, break in chain) blocking insurable transfer.

**Clear to Close** — All lender/title conditions satisfied; closing can be scheduled.

**Inspection Period / Due Diligence Period** — Contractual window during which the buyer may inspect and typically terminate with EMD returned.

**Settlement Statement (HUD-1 / ALTA)** — Itemized closing accounting; source of truth for realized Deal economics feeding the outcome dataset.

---

## 6. Data & lead sources

**APN** — Assessor's Parcel Number; county-level parcel identifier. Not globally unique across counties; the Property entity needs a composite or vendor-neutral key (DOC-402).

**County Records** — Recorder (deeds, mortgages, liens, lis pendens), assessor (valuations, characteristics), and treasurer (tax status) data; the raw material all vendors aggregate.

**Disclosure vs Non-disclosure State** — Whether sale prices are public record. Non-disclosure states (e.g., TX, UT, ID, NM, KS, MO*, MT, ND, WY, LA, MS, AK — *partial/county-dependent; verify in DOC-105) degrade comps built from public data; per ADR-005 launch metros prefer disclosure states.

**MLS / IDX / VOW / RESO** — Multiple Listing Services and their data-access regimes. MLS comp data (including sold prices in non-disclosure states) is licensed to members/participants; access paths for a software platform are a DOC-105 research item, not an assumption.

**Skip Tracing** — Resolving an Owner to reachable Contact channels via data brokers. Output quality varies; provenance and per-channel confidence must be stored (feeds consent handling, §7).

**Motivated-seller list dimensions (canonical):** **Absentee Owner** (tax mailing address ≠ property address); **Pre-foreclosure** (NOD — Notice of Default — or **Lis Pendens** filed); **Tax Delinquent**; **Probate** (deceased owner, estate in administration); **Inherited (non-probate transfer)**; **Vacant** (USPS vacancy flag or utility signals); **Tired Landlord** (long-hold absentee with eviction filings or code violations); **Code Violations**; **Divorce filing**; **High Equity / Free & Clear**.

**Driving for Dollars (D4D)** — Field capture of distressed-looking properties; a Lead source with photo evidence.

**List Stacking** — Counting how many motivated-seller dimensions hit the same Property/Owner; a core prioritization feature and input to the Lead Prioritization agent.

---

## 7. Outreach & compliance

**Consent State** — Per Contact per channel: the recorded basis on which we may contact them (prior express consent, established business relationship, none), with provenance and timestamps. First-class data, per ADR-003.

**TCPA** — Telephone Consumer Protection Act; governs calls/texts, autodialers, artificial/prerecorded voice (which includes AI-generated voice), with statutory damages per violation. The controlling constraint on the outreach module.

**DNC / Internal DNC** — National Do-Not-Call registry and the Organization's own suppression list; both are hard blocks enforced at send time, not list-build time.

**Litigator Scrub** — Screening Contacts against known serial TCPA plaintiffs before outreach.

**10DLC / A2P** — Carrier registration regime for application-to-person SMS over 10-digit long codes; unregistered traffic is filtered. Onboarding requirement for SMS.

**Quiet Hours / Frequency Caps** — Time-of-day and message-count limits enforced platform-wide, configurable stricter per Organization, never looser than law.

**DPPA / GLBA / FCRA** — Federal statutes constraining data-broker sourced personal data. Skip-trace data typically flows under DPPA/GLBA permissible-use regimes; FCRA is implicated only if data is used for credit-like eligibility decisions — which the platform must therefore never do or imply. Counsel review in DOC-501.

**CCPA/CPRA Data Subject Request (DSR)** — Property owners whose data we hold are consumers with rights (access, deletion, opt-out of sale/share). Deletion pipelines across licensed and derived data are a DOC-503 requirement.

---

## 8. AI & platform

**Agent** — A named AI capability with a spec (purpose, tools, memory, decision boundaries, escalation, evals) per DOC-302. V1 agents: Lead Prioritization, Underwriting, Follow-up Intelligence (ADR-004).

**Trust Ladder** — The platform's autonomy model. **Level 1 — Analyst:** recommend + explain only. **Level 2 — Assistant:** act within a human-approved authorization object (e.g., Campaign), fully audited. **Level 3 — Autopilot:** act within standing policy, audited, with defined escalation. Promotion between levels is per-agent, per-Organization, and criteria-gated (DOC-304).

**Authorization Object** — The signed-off artifact that bounds Level-2 action (v1: the Campaign). Records who approved what, when, and the exact bounds of permitted variation.

**Explanation** — The user-facing evidence for any agent output: which comps, which signals, which assumptions, with links to sources. A first-class output requirement, not logging.

**Motivation Signal** — A derived indicator of seller willingness, sourced from list dimensions (§6) and Conversation analysis. Stored in the derived layer with provenance; never presented as fact about a person's intent, always as evidenced inference.

**Licensed Data vs Derived Layer** — Per ADR-002: *licensed data* is vendor-sourced and subject to contract retention/refresh terms; the *derived layer* (entity resolution results, knowledge graph edges, outcome data, motivation signals, embeddings) is proprietary and must survive vendor substitution. The boundary is enforced in schema (DOC-402).

**Golden Dataset** — A held-out, human-verified evaluation set per agent (DOC-303); no agent ships or updates without passing its golden-set gates.

**Knowledge Graph** — The entity-resolved graph of Owners, Entities, Properties, Contacts, Leads, Deals, and their relationships over time; the structural core of the derived layer.

**Underwriting Accuracy** — Per-metro measured error between agent-projected values (ARV, rent) and subsequently observed outcomes; the publishable proof metric per ADR-005.

---

## 9. Naming conventions

Schema, API, and code use the singular entity names above (`property`, `owner`, `contact`, `lead`, `deal`, `offer`, `conversation`, `campaign`, `comp`, `underwriting_run`, `portfolio_asset`, `organization`). UI copy may use friendlier synonyms only where mapped in this document. Terms not defined here may not appear in schema names until added here via ADR or document revision.

---

*Changelog: v1.0 — initial release, aligned to ADR-001..005.*
