# Jarvis — Executive Summary

**Version 1.0 · 2026-07-07 · Owner: Founder · Status: Design complete, V1 buildable**

Jarvis is the Founder Operating System: the reusable substrate of memory, capabilities, decisions, and Claude Code workflows that builds and operates AcquisitionOS (Startup #1) and every startup after it. It is a **platform, not a product** — and, critically, in V1 it is *not software the company must build*. It is a structured repository (`founder-os`), a company-memory ingestion pipeline, a capability framework with a maturity ladder, and a Claude Code environment engineered so that any AI session starts with full company context.

**The three design commitments:**
1. **Memory is the platform.** Every capability is thin logic over one Company Memory (documents, decisions, meetings, metrics, code, research — ingested, linked, versioned, searchable). Capabilities are replaceable; memory is permanent.
2. **Capabilities, not personalities.** Thirteen capabilities (Executive → Security) share one spec template and one maturity ladder — L0 Library → L1 Assisted → L2 Supervised → L3 Autonomous — deliberately mirroring AcquisitionOS's customer-facing trust ladder. Nothing gets an "agent" until an L1 human-in-loop version has proven measurable value (operating principle: no agent without a measurable outcome).
3. **Domain independence by extraction, not speculation.** Jarvis reuses what AcquisitionOS *proves* (eval harness, model gateway, Terraform modules, CI patterns, document governance) rather than pre-building abstractions. Startup #2 = Jarvis clone + domain adapter (see StartupFactory.md).

**The honest risk, stated up front:** Jarvis is the founder's most seductive procrastination project. The roadmap therefore hard-caps Jarvis investment (V1 ≤ 1 week of setup; ≤10% of founder time until AcquisitionOS milestone M3) and defines Jarvis success by *AcquisitionOS's* velocity, not Jarvis's feature count.

**Read next:** Architecture.md (how it fits together) → MASTER_CONTEXT.md (the live state file) → Capabilities.md (the framework) → ImplementationRoadmap.md (what gets built when).
