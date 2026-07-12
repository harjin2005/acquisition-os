# FounderOS — The Executive Capability & Operating Cadence

**Purpose:** the founder's scarcest resources are attention and decision quality. This capability turns company state into decisions made on time, with memory.

**Responsibilities:** maintain MASTER_CONTEXT.md (the live state file); run the operating cadence; track OKRs and decisions; assemble board/investor reports; keep the risk register current.

**Operating cadence (the actual OS):**
- **Daily (10 min):** auto-generated brief — yesterday's material events (PRs merged, metrics deltas, inbound of note, research alerts), today's top-3 vs current sprint, approval queue items, decision-aging alarms.
- **Weekly (60 min):** metrics review vs DOC-120 §12 targets · risk register deltas · decision log review (anything open >7 days gets a forcing question) · next week's top-3 · MASTER_CONTEXT auto-refresh diff approved.
- **Monthly:** finance close pack (Finance.md) · capability KPI review (promote/demote per ladder) · debt/risk register grooming.
- **Quarterly:** OKR set/score (template in SOPs.md) · board/investor pack assembled from memory (metrics, milestones, risks, asks) · Jarvis itself reviewed against its success metrics.

**Inputs:** all of Company Memory. **Outputs:** briefs, OKR docs, board packs, updated MASTER_CONTEXT, decision records. **Knowledge sources:** decision log, metrics store, meeting memory, risk registers. **Memory writes:** every brief, every decision, every OKR score — permanently.

**Approval rules:** Jarvis drafts everything here; the founder signs everything here. L1 permanently for external communications (board packs never auto-send).
**Decision boundaries:** never communicates externally; never reprioritizes the sprint (proposes only); never edits ADR statuses.
**Failure modes:** brief noise → ruthless top-3 format, item budget; stale MASTER_CONTEXT → refresh is hook-enforced weekly with diff review; decision theater (logging without deciding) → aging alarms escalate to the weekly review's first agenda item.
**Observability:** briefs and packs are files in git — the audit trail is the medium.
**KPIs:** decision latency (open→decided) · % weekly reviews held · founder hours/week on assembly (target: →0) · board pack prep time (target: <1 hr from memory).
**Continuous improvement:** every month, the founder marks brief items useful/noise; the brief prompt evolves against that labeled set (a tiny eval, same discipline as the product).
