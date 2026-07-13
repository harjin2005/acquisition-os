# CLAUDE.md — AcquisitionOS (read me first, every session)

You are helping build **AcquisitionOS**: a decision-quality software platform for small
US real-estate investment teams. The full plans already exist in `/docs`. Your job is to
BUILD from those plans — not to redesign them.

## THE 5 RULES YOU NEVER BREAK
1. **Small steps.** Do one task at a time. Never rewrite files you weren't asked to touch.
2. **When unsure, STOP and ask.** Guessing wastes tokens and breaks things. See `.claude/STOP_RULES.md`.
3. **Don't re-read everything.** The docs are large. Read only the specific doc section a task
   needs (paths below). Re-reading the whole project every task wastes tokens — don't.
4. **Prove it works.** Show test output or a run result. Never say "done" without evidence.
5. **Stay in your lane.** Each session has ONE role and ONE folder area (see `.claude/sessions/`).
   Do not edit outside your assigned area.

## HOW WE WORK (the loop)
- Before starting: read `.claude/CURRENT_STATE.md` (what's done) and `.claude/NEXT_TASK.md` (your job).
- Plan first for anything bigger than one file. Show the plan. Wait for "go".
- After finishing: update `.claude/CURRENT_STATE.md`, and run the `end-of-session` skill so
  nothing is forgotten between sessions.
- Every change goes through a Pull Request. A human (the founder) approves every merge.

## THE NON-NEGOTIABLES (from our design docs — do not violate)
- **Naming:** use the exact entity names from `docs/product/02-glossary.md` (Property, Owner,
  Contact, Lead, Deal — these are five SEPARATE things, never merged).
- **Data safety:** every database table has an `org_id` and row-level security. Never write code
  that could let one customer see another's data.
- **Compliance is sacred:** anything touching outreach (SMS/email), consent, or suppression is
  high-risk. STOP and get founder review. Never auto-send messages.
- **Money & data costs:** we pay per record for property data and per AI call. Don't write loops
  that fetch or call in bulk without asking.

## WHERE THINGS ARE (read only what your task needs)
- Vision & scope: `docs/product/20-company-blueprint.md`
- What to build (features): `docs/product/21-prd-ux-blueprint.md`
- How to build it (tech): `docs/product/30-engineering-handbook.md`
- Step-by-step plan: `docs/product/31-execution-plan.md`  ← Sprint 1 is here
- Decisions already made: `docs/product/01-decision-log.md`
- Word meanings: `docs/product/02-glossary.md`
- Live status snapshot: `docs/product/MASTER_CONTEXT.md`

## IF YOU ARE ABOUT TO...
- ...start coding a feature → check it's in Sprint 1 (`31-execution-plan.md`). If not, STOP.
- ...create a database change → use the `.claude/skills/new-migration` checklist. Don't freehand it.
- ...add a new tool/library/plugin → STOP. See `.claude/TOOLS.md` for what's approved and ask first.
- ...touch outreach/consent/suppression code → STOP. Founder must review.
- ...feel unsure what the task means → STOP and ask ONE clear question.
