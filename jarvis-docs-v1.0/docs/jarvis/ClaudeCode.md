# Claude Code Integration (Jarvis-wide, domain-independent)

**Purpose:** every Claude Code/Cowork session — engineering or not — starts with full context, works inside rails, and leaves knowledge behind. Extends DOC-131 §1 from "how we build the product" to "how the company works."

## Onboarding a session (any repo, any startup)
1. T0 loads: MASTER_CONTEXT.md (auto via CLAUDE.md @-reference) + repo CLAUDE.md.
2. Task declared → matching capability skill loads just-in-time (`.claude/skills/<capability>-*`).
3. Retrieval tools (Company Memory MCP server) available in every session; bulk-pasting documents is a rule violation — query and cite.

## Repository memory layout (the reusable scaffold — identical across startups)
`CLAUDE.md` (<150 lines: stack, boundaries, non-negotiables, @-pointers) · `.claude/rules/*.md` path-scoped · `.claude/skills/` (engineering set per DOC-131 + jarvis set: `end-of-session`, `new-decision-record`, `research-brief`, `weekly-review`, `board-pack`, `new-capability`) · `.claude/agents/` (code-reviewer, schema-auditor, spec-checker + `brief-editor`, `claim-verifier` for research/growth content) · `.claude/settings.json` (permissions allowlist; deny prod paths and external-send tools by default).

## Hooks (deterministic law, natural language is advisory)
- PreToolUse: block edits to `/docs/decisions/*` statuses; block anything matching secret patterns; block sends/publishes (no such tool mounts outside an approval object anyway — defense in depth).
- PostToolUse: format/lint; memory-sensitivity tagging on new docs.
- Stop: affected tests must pass (product repo); **end-of-session write-back check** (founder-os repo) — material sessions must produce a summary/decision/artifact commit or explicitly declare "exploratory, no write-back."

## Task execution & review workflow
Plan mode for multi-file or governed-path work → human plan approval → vertical-slice execution → evidence shown (tests/output) → reviewer subagent (gaps vs acceptance criteria only) → human PR review → merge. Non-engineering work mirrors it: draft → claim-verifier subagent (facts, labels, as-of dates) → human review → publish/send by human.

## Definition of Done (universal)
Acceptance criteria met · evidence attached · write-backs committed (memory updated, decision records filed, docs touched if interfaces/meaning changed) · no unregistered automation introduced · CHANGELOG/brief entry where material.

## Knowledge & memory updates
Docs change via PRs like code; MASTER_CONTEXT refreshes weekly by skill with human-approved diff; decisions only via `new-decision-record`; session summaries auto-ingest. The repo *is* the wiki; git *is* version history.
