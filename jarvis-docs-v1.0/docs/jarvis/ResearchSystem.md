# Research System

**Purpose:** the company's radar — competitors, legal changes, security advisories, models/tools, funding/hiring markets — delivered as labeled, dated briefs into memory instead of anxiety-driven founder browsing.

**Responsibilities & cadence (V1 watchlists live in the domain adapter):**
- Competitors (adapter list, e.g. PropStream/BatchLeads/REsimpli/Deal Run): pricing/feature/positioning deltas — biweekly.
- Legal/regulatory (adapter list: TCPA + FCC dockets, state mini-TCPAs, privacy statutes, wholesaling rules): change alerts — weekly. High-severity items page the founder via brief top-slot.
- Security advisories: dependency CVEs (from Security.md tooling) + vendor incidents — weekly digest, criticals immediate.
- AI models/tools: relevant releases scored against our gateway routing — monthly.
- Funding/hiring market: quarterly, pre-fundraise cadence on demand.

**Method (quality bar):** every claim carries VERIFIED/HIGH/LOW/UNKNOWN + source + verified-as-of date (the DOC-110 discipline, systematized); briefs diff against the previous brief (what *changed* is the product); primary sources preferred; affiliate/competitor-authored content flagged as such.
**Outputs → memory:** brief documents, watchlist deltas, decision-relevant alerts linked to affected ADRs/risks (graph edges).
**Approval rules:** L1 — research never triggers action by itself; it feeds the Decision Engine.
**KPIs:** founder surprises that memory already knew about (target 0) · alert precision (founder marks noise) · time from external change → brief (<1 week routine, <24h critical).
**Failure modes:** confident staleness → mandatory as-of dates + freshness in retrieval; volume creep → per-brief item budget; SEO-slop sources → source quality list maintained in adapter.
