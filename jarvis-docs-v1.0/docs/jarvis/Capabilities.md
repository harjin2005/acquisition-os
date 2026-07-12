# Jarvis Capabilities Framework

**Owner: Founder · The registry + the template every capability file instantiates.**

## 1. The Capability Spec Template (normative)

Every capability document defines: **Purpose** (the expensive problem) · **Responsibilities** · **Inputs** · **Outputs** · **Knowledge sources** (memory queries it depends on) · **Memory writes** (what it must record back) · **Tools** · **Approval rules** (what needs the founder, per DecisionEngine.md) · **Decision boundaries** (what it may never do) · **Failure modes** · **Observability** (where its activity is visible) · **KPIs** · **Maturity level + promotion criteria** · **Automation opportunities** (ranked) · **Continuous improvement** (the feedback loop that makes it better).

## 2. The Maturity Ladder (mirrors the product trust ladder — one mental model company-wide)

- **L0 Library** — templates, SOPs, checklists. No AI required. Value: consistency.
- **L1 Assisted** — AI drafts/researches/synthesizes; human reviews and executes. Value: speed.
- **L2 Supervised** — AI executes within an approval object (scope, budget, duration signed by founder); full audit. Value: leverage.
- **L3 Autonomous** — standing policy, exception-based review. Reserved; nothing launches here.

**Promotion rule:** a capability climbs one level only with (a) a measured KPI improvement at the current level and (b) a written approval-rules amendment. Demotion is one command (kill switch per capability).

## 3. Registry (V1 states — honest, not aspirational)

| Capability | V1 level | First measurable outcome | File |
|---|---|---|---|
| Executive | L1 | Weekly brief + decision latency < 7 days on tracked decisions | FounderOS.md |
| Product | L1 | Interview→insight pipeline; PRD drafts in house style | (in Operations.md §Product) |
| Engineering | L2 (already) | DOC-131 playbook is this capability, live | Engineering.md |
| AI Platform | L2 (shared infra) | Gateway/evals extracted & reused | AIPlatform.md |
| Knowledge | L1 | 100% of listed sources ingested; retrieval used daily | CompanyMemory.md |
| Research | L1 | Scheduled briefs (competitors/legal/security) with confidence labels | ResearchSystem.md |
| Growth | L0→L1 | Content calendar + drafts; publish stays human | Growth.md |
| Sales | L0→L1 | Design-partner pipeline tracked; outreach drafts | (Growth.md §Sales) |
| Customer Success | L0 | Onboarding SOP + health-score definition ready for first customers | (Operations.md §CS) |
| Finance | L0→L1 | Monthly close pack + burn/runway auto-assembled for review | Finance.md |
| Legal | L0→L1 | Obligation register + renewal alerts; counsel remains counsel | Legal.md |
| Operations | L1 | SOP system live; task hygiene automated | Operations.md |
| Security | L1→L2 | Advisory triage + dependency audit digest; incident SOP | Security.md |

**Anti-principle enforced:** Sales, CS, Finance, Legal are *deliberately* L0/L1 — the measurable-outcome bar isn't met for automation yet, and a founder with zero customers automating customer success is theater. The registry exists precisely to make that discipline visible.

## 4. Domain independence

Capabilities reference domains only through **adapter files** (`/adapters/<startup>/`): ICP definitions, competitor lists, legal watchlists, metric definitions, tone guides. A capability that hard-codes PropTech knowledge outside an adapter fails review (rule in .claude/rules/jarvis.md).
