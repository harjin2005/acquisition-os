# DOC-121 — Complete PRD & UX Blueprint

**Version:** 0.9 — **GATED.** Content-complete; freezes to v1.0 only after DD gate 3 (≥15 interviews, ≥5 design partners re-validate priorities) and gate 4 (data-rights term sheet). Changes after freeze require PM sign-off + ADR where architectural.
**Governed by:** DOC-002 (ontology, normative), ADR-001..005, DOC-120 (blueprint), proposed ADR-009..011.
**Priorities:** P0 = V1 launch-blocking · P1 = V1.x/V2 · P2 = V2/V3 · P3 = explicitly deferred/roadmap-only.
**Convention:** every module states purpose (the expensive problem), requirements, permissions, notifications, error/edge states, and out-of-scope. Representative edge cases are enumerated here; module PRDs (DOC-202 series) exhaustively enumerate per module before that module's build sprint — this master PRD is the contract, module PRDs are the appendices.

---

# PART A — PRODUCT REQUIREMENTS

## A1. Identity, Organizations & RBAC — P0

**Problem:** teams need shared, permissioned truth; privileged actions (campaign approval, trust promotion) need accountability.
**Requirements:** managed-auth signup/login, MFA optional (org-enforceable); org creation with single-org membership per user in v1 (multi-org P2); invitations with role assignment; five roles per DOC-120 §8 with a permissions matrix maintained in DOC-504; seat enforcement per plan; profile & notification preferences.
**Permissions:** role changes = Admin+; Owner transfer requires email confirmation; privileged actions dual-logged to audit.
**Notifications:** invite, role-change, new-device login.
**Edge/error states:** invite to existing-org email → clear conflict message; last-Owner demotion blocked; seat limit reached → upgrade prompt, never silent failure; SSO requested → roadmap message (P2).
**Out of scope v1:** SSO/SAML, SCIM, multi-org, per-org encryption keys.

## A2. Data Ingestion & Coverage (licensed layer) — P0

**Problem:** everything downstream depends on current, provenance-tracked property/owner data in launch metros (ADR-005), under contract terms (ADR-002/R4).
**Requirements:** vendor adapter framework (≥1 bulk property/ownership source + ≥1 skip-trace waterfall provider at launch; dual-source ownership in ≥1 metro for empirical vendor QA per DOC-110 §10); scheduled refresh per contract; freshness metadata surfaced on every record ("data as of"); coverage registry (which metros/counties live); mechanical retention/expiry enforcement; ingestion observability (row counts, anomaly alerts).
**Edge cases:** property outside coverage → explicit "out of coverage" state, waitlist capture (ADR-005 c.4), all agents decline gracefully with reason; vendor feed gap/late → staleness banner + agent receipts show data age; conflicting vendor values → precedence rules + conflict flag on record; county remap/APN changes → ATTOM-ID-style persistent key strategy (DOC-402).
**Out of scope v1:** nationwide, self-serve county scraping, direct MLS feeds.

## A3. Import & Migration — P0

**Problem:** switching cost #1 is data hostage-taking (VERIFIED); migration is the GTM weapon.
**Requirements:** CSV import with mapping UI; first-class dialect parsers for PropStream, BatchLeads, DataSift, DealMachine, Podio exports; on import: USPS normalization, dedupe, entity resolution against licensed layer, list-source tagging preserved (recycled-interest signal per DOC-002), **consent-state initialization** — imported contacts default to consent_unknown and are unsendable until the org attests consent provenance per list (compliance-critical, DD change 5); import preview + rollback within 24h.
**Edge cases:** duplicate leads on same property → linked as distinct Leads per ontology, not merged silently; malformed rows → quarantine file with per-row reasons, partial import allowed; 500k-row file → async with progress + email on completion; re-import of same file → idempotent by content hash.

## A4. Properties, Owners, Contacts (workspaces & graph) — P0

**Problem:** incumbents conflate these; entity-resolved owner intelligence is pain #9 and moat substrate.
**Requirements:** Property page (facts, transaction/lien history, linked Leads across time, linked Deals, freshness); Owner page (resolved identity, aliases, **portfolio view of all linked properties**, controlling-entity links, all Contacts, full conversation history across every lead ever); Contact page (channels with per-channel consent state + provenance + confidence, suppression status, conversation thread); manual merge/split of resolution clusters with Manager permission + full audit (resolution is probabilistic; humans arbitrate).
**Edge cases:** resolution confidence below threshold → "possible same owner" suggestion card, never auto-merge; owner deceased/probate signal → surfaced as motivation signal with sensitivity guidance in UI copy; contact channel shared across owners (family line) → flagged ambiguous; DSR deletion request → A13 pipeline.

## A5. Leads & Pipeline — P0

**Problem:** JTBD-3; leads must carry source, score, assignment, and never rot silently.
**Requirements:** lifecycle states exactly per DOC-002 §3 (customizable labels, fixed semantics — analytics depend on stable state machine); kanban + table views; assignment (manual v1; agent-suggested routing = L2 roadmap); buy box configuration per org (machine-readable, versioned); Lead Prioritization agent queue ("Today's 20") with receipts; staleness SLAs per state with escalation notifications; disqualify/nurture flows requiring reason codes (feeds learning + analytics).
**Permissions:** members see assigned + unassigned pools per org policy; Managers see all.
**Notifications:** assignment, SLA breach, agent daily queue ready, inbound reply on owned lead.
**Edge cases:** state skip attempts (New → Under Contract) allowed with confirmation + event log (reality is messy; analytics tag anomalies); bulk state changes require Manager; lead on out-of-coverage property → allowed but agents annotate limited data.

## A6. Underwriting Workspace — P0

**Problem:** JTBD-1, pain #1; the accuracy product.
**Requirements:** dual-mode runs per DOC-120 §5.2: subject panel; comps map+grid with per-comp adjustment table (editable — **user adjustments create a new run version**, immutability per ontology); assumption sheet (org defaults, per-run overrides); flip outputs (ARV + band, line-item MAO — the 70% rule shown only as sanity check per DOC-002 §4); rental outputs (rent + band, NOI, CoC, DSCR, cap rate); BRRRR combo view with refi assumption; sensitivity strip (which inputs move the answer most); confidence banding with plain-language meaning; run history & diff view; export to PDF (share with lenders/partners); "insufficient evidence" state design (below 3 comps: shows what's missing and nearest-miss comps rather than a number — anti-hallucination requirement, launch-blocking).
**Permissions:** anyone runs; org policy may require Manager review when user override deviates >X% from model (configurable; default 10%).
**Edge cases:** non-disclosure-style data thinness inside disclosure metros (rural pockets) → banded output + explicit limitation receipt; subject is multi-parcel → v1 supports 1–4 unit residential only, others rejected with reason (scope guard); comps straddle a school/flood boundary → boundary flags on comp cards; stale comp (>12mo) auto-excluded with visible toggle.
**Out of scope v1:** model-based rehab estimation (structured inputs + ranges only, ADR-004 c.4), commercial/multifamily 5+, offer-document generation (A8 handles offers as *data*; documents are templates).

## A7. Conversations & Communication Inbox — P0

**Problem:** conversation history is motivation-signal raw material and the memory incumbents lose across list re-pulls.
**Requirements:** unified per-Contact thread across SMS + email + manual call logs (v1 channels; native dialer P1 decision post-partner feedback); org inbox with assignment; templates with variable slots; conversation summaries (AI service) pinned to Lead/Deal; sentiment/urgency flags routing per DOC-120 §5.3 escalation; click-to-text/email from any workspace; opt-out keywords processed platform-wide instantly (STOP et al. + free-form per revocation rules — VERIFIED legal state) with cross-channel suppression write.
**Edge cases:** inbound from unknown number → creates unmatched conversation, resolution suggestions offered; reply after opt-out (re-consent) → guided re-consent capture flow, no shortcut; carrier filtering/delivery failure → per-message status + campaign health alert; two members reply simultaneously → soft-lock indicator.

## A8. Deals, Offers & Outcome Capture — P0

**Problem:** JTBD-4 economics + the moat loop (DOC-120 principle 3).
**Requirements:** Deal created from Lead at offer/contract per ontology; offer chains (versioned terms, status); deal economics tab: projected (auto-imported from the linked underwriting run) vs committed (contract) vs actual; closing checklist (title, inspection, EMD dates) with task generation; **outcome capture flow**: on Closed, guided actuals entry + settlement-statement upload with AI extraction (extraction P0, works-without-AI fallback manual entry); disposition recording (assignment/wholetail/retail/refi-hold → Portfolio Asset creation); error attribution view per deal ("your ARV was +4.1%, rehab −12%").
**Notifications:** stage changes, checklist due dates, outcome-capture nag until closed loop (gentle, persistent — loop closure is a top-3 product metric).
**Edge cases:** deal falls through → terminal state + reason code + EMD outcome; partial actuals → loop marked incomplete, excluded from calibration; multi-exit (partial assignment) → v1 single-exit model, note field (documented limitation).

## A9. Campaigns & Outreach (the ADR-003 module) — P0

**Problem:** JTBD-2 execution + JTBD-5; legally the most dangerous surface; compliance is product.
**Requirements:** campaign builder producing the **authorization object** (audience snapshot query + freeze, channels, template family with locked claim/price variables, cadence & caps, quiet-hours profile ≥ legal, start/end, approval signature: who/when); pre-flight compliance report (consent coverage of audience, DNC/litigator scrub results, 10DLC status) — **unsendable until green**; L1 mode: agent drafts daily send list for human send; L2 mode (per-org promotion, DOC-120 §5.3): agent executes within bounds; per-message audit (template version, variables, consent basis snapshot at send time); org + platform suppression lists, platform list non-overridable; A2P 10DLC onboarding wizard; sending-domain warm-up for email; campaign analytics (delivery, response, opt-out rate with auto-throttle).
**Permissions:** draft = Member+; approve = Manager+; edit-after-approval = void + re-approval (immutable authorization).
**Edge cases:** audience member's consent revoked mid-campaign → next-send skip, visible in log; template variable missing for a contact → skip + reason, never send malformed; carrier campaign rejection (10DLC) → guided remediation; org tries CSV-blast without consent attestation → hard block with education screen (this loses us bad-fit deals on purpose — Anti-ICP by design).
**Out of scope v1:** AI voice (ADR-003), ringless voicemail (legal review first), direct mail (partner referral link only, P1 native).

## A10. Search — P0

Global cmd-K: entities by name/address/phone/email (suppression-aware display), saved filters as smart lists (list-stacking UX per DOC-002 §6 — stack count as a first-class filter). Edge: search by opted-out phone → returns contact with suppression banner (findable for compliance, unusable for outreach).

## A11. Notifications — P0

Channels: in-app, email digest, mobile push P1. Per-user preference matrix by event class; org-level mandatory classes (compliance alerts non-optional). Anti-noise principle: agent outputs batch into the daily queue, not per-item pings. Edge: notification storm compression ("14 leads breached SLA" not 14 pings).

## A12. Reporting & Analytics — P0-lite, P1-full

V1 (P0): pipeline funnel by source/state, campaign performance, outcome dashboard (projected-vs-actual, realized spread, error trend), agent adoption metrics for the org. P1: KPI suite (per-member activity, marketing ROI by channel/list — pain #18), scheduled exports. Edge: small-n orgs → confidence-aware displays, no fake precision.

## A13. Privacy & Compliance Ops — P0

DSR intake (owner/contact requests access/deletion): identity verification flow, deletion pipeline across licensed cache + core + derived (embeddings + graph edges included), legal-hold override, SLA tracking (DOC-503). FCRA guardrail: no credit/eligibility framing anywhere in product copy — checked in design review. Retention: consent/message audit ≥7yr; licensed data per contract.

## A14. Billing & Plans — P0

Stripe: tiers per ADR-011, seat enforcement, usage wallet (credits, auto-top-up opt-in, hard-stop option), invoices, dunning, plan-pause (churn-save per DOC-120 §10). Edge: wallet empty mid-campaign → pause sends + notify, never silent partial send; downgrade below seat count → guided seat removal.

## A15. Admin Console (internal) — P0-lite

Tenant lookup, coverage registry management, vendor feed health, eval dashboard link, suppression-list management, impersonation with consent + audit banner. P1: billing ops, feature-flag UI.

## A16. Public API & Webhooks — P1 (read), P2 (write)

Per DOC-120 §7. V1 ships internal-only API discipline (OpenAPI from day one) so P1 is exposure, not construction.

## A17–A20. Deferred modules — P2/P3

Disposition/buyer lists (P2, V2), mobile field capture (P2 — DealMachine owns D4D; we integrate/import rather than fight, VERIFIED their strength), accounting export (P2), SSO/enterprise RBAC/audit export (P2, mid-market tier), lender/title referral surfaces (P3, H2/H3), MLS-dependent features (P3, gated on L6/U5).

---

# PART B — UX BLUEPRINT

**Design language:** calm, dense, numbers-forward ("Bloomberg for house buyers," not consumer-app whitespace); every AI output rendered with the **Receipts pattern** — a consistent right-side drawer showing evidence, data freshness, and confidence, identical across all three agents (one mental model to learn). Explanation UI is a P0 design system component, not per-feature improvisation.

**Navigation (left rail):** Today · Pipeline · Inbox · Properties · Owners · Underwriting · Campaigns · Deals · Reports · Settings. Global: cmd-K search, notification tray, org switcher (hidden until multi-org exists), help.

**B1. Today (home).** The daily operating screen: (1) "Your 20" — prioritization queue as cards: address, stack badges, score with top-3 reason chips, one-click actions (call/text within consent, open lead, snooze w/ reason); (2) Follow-up recommendations rail (contact X, draft ready, why-now chip); (3) SLA/escalation strip; (4) org pulse (deals moving, replies waiting). Empty state (new org): guided setup checklist (buy box → import → first underwrite → first campaign) with progress. Design intent: a Manager runs the morning standup from this screen.

**B2. Pipeline.** Kanban per lifecycle states with WIP staleness heat; table view with saved smart-list tabs; bulk actions gated by role; per-card: address, owner name (resolved), stack count, score, days-in-state, assignee. Drag between states = state machine transitions with side-effect prompts (e.g., → Offer Extended asks to link/create offer).

**B3. Lead workspace (three-pane).** Left: context stack — property summary card (photo, facts, freshness stamp), owner card (portfolio count chip → Owner page), signals list with provenance. Center: timeline — every conversation, note, task, state change, agent recommendation, interleaved chronologically. Right: action rail — next-best-action from agents (with receipts drawer), quick underwrite button (spawns A6 run pre-filled), task/note composer. This screen is where users live; every element deep-links to its workspace.

**B4. Property workspace.** Header: address, coverage/freshness badges. Tabs: Facts & History (transactions, liens, permits-P2), Leads (every historical lead on this property — recycled-interest timeline), Underwriting (run history with value trend), Deals. Map context panel.

**B5. Owner workspace.** Identity header with resolution confidence + alias list ("also appears as…"); Portfolio grid (all linked properties with equity/status chips) — the "wow" screen competitors can't render; Entities panel (LLC/trust links); Contacts with per-channel consent chips (green/gray/red = consented/unknown/suppressed); unified conversation history across all leads ever. Merge/split flows behind Manager permission with side-by-side evidence diff.

**B6. Underwriting workspace.** Split view: left = comps map (subject pin, comp pins colored by similarity, boundary overlays) + comp grid with adjustment cells; right = conclusion panel (value + band rendered as a range bar, not false-precision point), assumption sheet accordion, MAO/returns block, sensitivity strip (tornado mini-chart), mode toggle (Flip/Rental/BRRRR). Top bar: run version history with diff. "Insufficient evidence" renders as a designed state: what's missing, nearest-miss comps grayed with exclusion reasons, actions (widen radius with tradeoff note, request review). Export = clean PDF (lender-shareable).

**B7. Campaign workspace.** Builder as a 5-step wizard (Audience → Channels & Templates → Cadence & Caps → Compliance Pre-flight → Approval). Pre-flight screen is deliberately unglamorous and mandatory: consent coverage donut, scrub results table, 10DLC status, quiet-hours confirmation; red = cannot proceed (with fix-paths). Approval screen renders the authorization object in human language + signature click. Running view: sends timeline, response/opt-out gauges with auto-throttle indicator, per-message audit table (filter: contact, status, consent basis). L1 mode adds a daily "review & send" checklist UI.

**B8. Deal workspace.** Header: address, stage, days-to-close countdown. Tabs: Economics (three-column projected/committed/actual with variance chips; error attribution after close), Offers (chain visualization), Checklist (title/inspection/EMD tasks with dates), Documents (uploads + extraction status), Timeline. Close flow: guided actuals entry with settlement-statement upload → extraction review diff → confirm → loop-closed celebration state (small, earned — this is the moat moment).

**B9. Inbox.** Unified threads with assignment chips, consent banner on every thread, template inserter, summary pin, escalation flags surfaced top. Opt-out events render as system messages in-thread.

**B10. Reports.** V1: four fixed dashboards (Funnel, Campaigns, Outcomes, Adoption) with date/metro/member filters and export. Confidence-aware rendering for small n.

**B11. Settings/Admin.** Org profile, members & roles (matrix view), buy box editor (structured criteria builder with plain-language preview), assumptions defaults, compliance center (10DLC status, suppression list viewer, consent attestations log, quiet-hours profile), integrations, billing & wallet, audit log viewer (filterable, export), notification preferences.

**Cross-cutting states:** every list has designed empty/loading/error states; every AI surface has "insufficient evidence" and "data stale" variants; every destructive action confirms with consequence text; every compliance block explains *why* and the path to green. Accessibility: WCAG 2.1 AA target; keyboard-first for power users (the VA workforce reality).

*Changelog: v0.9 — content-complete, gated on DD gates 3–4.*
