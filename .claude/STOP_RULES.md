# STOP_RULES.md — When you MUST stop and ask the founder

The founder is nervous about two things: **wasted tokens** and **going in random directions.**
These rules exist to prevent both. Stopping to ask is ALWAYS cheaper than guessing wrong.

## STOP immediately and ask a single clear question if:
1. The task in `.claude/NEXT_TASK.md` is unclear, or could mean two different things.
2. The task seems to require touching files OUTSIDE your assigned folder area.
3. You would need to add a new library, tool, or dependency.
4. You are about to change the database schema (structure of tables).
5. The work touches: outreach, messaging, consent, suppression, or customer personal data.
6. You are about to delete or heavily rewrite existing working code.
7. You've tried the same fix twice and it still fails. (Do NOT try a third time — stop, explain.)
8. A task looks like it will take more than ~10 steps. Break it up and confirm the plan first.
9. Anything about spending: bulk data fetches, many AI calls, anything that costs money at scale.

## HOW to stop (do this, don't just keep going):
- Say clearly: "STOPPING — here's why, and here's my one question."
- Ask ONE specific question, not five vague ones.
- Suggest what you THINK the answer is, so the founder can just say "yes" quickly.
- Wait. Do not proceed on assumption.

## Token-saving rules (the founder is watching the budget):
- Do NOT re-read the whole `/docs` folder. Read only the one section your task names.
- Do NOT re-summarize the whole project back to the founder. They wrote it; they know it.
- If context is getting long and messy, say so and suggest starting a fresh session with a
  clean handoff note — this is CHEAPER than pushing on in a bloated session.
- Prefer small, verifiable steps over big sweeping changes that are hard to check.

## The golden rule:
**A stop-and-ask costs a few tokens. A wrong guess costs hours of cleanup and thousands of
tokens. When in doubt, stop.**
