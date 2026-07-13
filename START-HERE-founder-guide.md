# START HERE — Your plain-language guide

Hi. This folder is your "Claude operating setup." It makes Claude Code work like a small,
careful team instead of one robot that wanders off. Read this once. It's short.

## What you got (in normal words)

1. **`CLAUDE.md`** — the "welcome note." Every time you open Claude Code, it reads this first and
   instantly knows your project, your rules, and where your docs are. You never re-explain again.

2. **`.claude/STOP_RULES.md`** — your nervousness, turned into law. It tells Claude: when unsure,
   STOP and ask. Don't guess. Don't burn tokens wandering. This is your anti-chaos rule.

3. **`.claude/CURRENT_STATE.md` and `NEXT_TASK.md`** — the shared notebook. Every session writes
   down what it did and what's next. This is how sessions "remember" across days without you.

4. **`.claude/sessions/` (the cards)** — ready-made instruction cards, one per role. You COPY a
   card, PASTE it, done. **You never write a prompt from scratch again.** This kills your biggest
   pain.

5. **`.claude/settings.json` (the tripwires)** — automatic safety nets. They format code, run
   tests, and block risky actions BY THEMSELVES. You don't watch. They just work.

6. **`.claude/skills/` and `.claude/agents/`** — a memory-saver skill and a "Reviewer" robot that
   checks work before you do — so you review less.

## What to actually DO (your simple routine)

**One-time setup:**
1. Put this whole folder at the root of your code project.
2. Put your design docs in a `docs/product/` folder (the CLAUDE.md points there). If your files
   have different names, just tell Claude "my docs are named X" once and it'll adjust.
3. Install Claude Code (I can walk you through this — just ask).

**Every work session (this is the whole loop):**
1. Open Claude Code.
2. Open `.claude/sessions/` and pick the role you need. **Start with card 1 (Architect).**
3. Copy the card's "PROMPT TO PASTE" block. Paste it. Enter.
4. Claude shows you a PLAN. You read it (30 seconds). Say "go" or "no, do X instead."
5. Claude works. When it says "done," it shows you proof (test results).
6. Run card 8 (Reviewer) to double-check. It gives a verdict: safe, or needs fixes.
7. You say "merge it" or "fix these." Done for that task.

That's it. Your job is: **pick a card, glance at a plan, glance at a verdict, say yes/no.**
A few minutes per task. Not hours.

## The three things that protect you

- **You review LESS, not zero.** The Reviewer robot checks first. You wrote in your own product
  that AI must earn trust before acting alone — same rule applies to building. Start by checking
  most things; check less as it proves reliable.
- **Tokens stay low** because CLAUDE.md says "don't re-read everything" and STOP_RULES says "ask,
  don't wander."
- **It can't go rogue** because the tripwires physically block dangerous actions and the cards
  keep each session in one lane.

## The honest reminder

There is no "walk away for a week and come back to a finished app" button. Anyone selling you
that is selling you the Emergent story again. What you have here is the real thing: a setup where
Claude does 90% of the *typing and building*, and you do 10% of *deciding and approving* — the
10% that is exactly what keeps the project from turning into the 5% mess you got before.

Start with the Architect card. When you're ready, ask me and I'll walk you through installing
Claude Code and running that first card, step by step.
