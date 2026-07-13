# TOOLS.md — Helpful add-ons, and WHEN to use them

Plain rule: **add ONE tool at a time. Only add the next one after the current one feels easy.**
Piling on tools = wasted tokens + chaos. This is the same "earn trust one step at a time"
rule from our product design.

Do not load this file every session. Only open it when deciding whether to add a tool.

---

## USE NOW (the only one you need to start)

### Superpowers  ✅ recommended
- **What it does:** teaches Claude good building habits — plan before coding, test properly,
  debug systematically, and auto-review work before you see it.
- **Why it fits you:** it's the professional version of your `.claude/` setup. It fights exactly
  your two fears: wandering off, and re-doing broken work forever.
- **Install:** `/plugin marketplace add obra/superpowers-marketplace` then
  `/plugin install superpowers@superpowers-marketplace`
- **When to add:** after you've run 3-4 tasks with the basic setup and feel the rhythm.
- **Cost warning:** it adds some tokens per session. Worth it. But do NOT install the giant
  "1000+ skills" bundles — those drain your budget for no real gain.
- **Important:** Superpowers does NOT know YOUR project rules. Keep your `CLAUDE.md` and
  `STOP_RULES.md` on top of it. They stack together.

---

## MAYBE LATER (only if you feel a real gap — most people don't need these early)

### A memory tool (e.g. semantic search over past sessions)
- **What it does:** lets Claude search everything it discussed before.
- **Do you need it?** Not yet. Your `CURRENT_STATE.md` + `end-of-session` skill already do the
  simple version. Add a memory tool ONLY if you feel the notebook failing.

### Context7 (live docs lookup)
- **What it does:** pulls up-to-date documentation for libraries so Claude uses correct, current
  code instead of guessing from memory.
- **When useful:** later, when engineers are building lots of features against many libraries.
- **When to add:** if you hit bugs caused by Claude using outdated code patterns.

### A browser tool (for the AI agents to read web pages)
- **What it does:** lets Claude open and read websites.
- **When useful:** ONLY when you build the parts that fetch data from the web. Not in early sprints.
- **Caution:** anything reading the open web is a security-sensitive area. Founder review required.

---

## DO NOT USE (for now — these are traps for a nervous solo founder)

### Hermes / "Claude commands other Claude sessions" auto-swarms
- **Why skip:** young, breaks often, and burns tokens fast when it goes wrong (robots spawning
  robots). Highest-risk thing you could add. Revisit only when you have engineers and a bigger
  budget.

### Giant "mega skill-pack" bundles (hundreds/thousands of skills)
- **Why skip:** they load huge amounts of stuff every session = token drain. You need a handful
  of good skills, not thousands.

### Any brand-new tool with few users / no track record
- **Why skip:** you just got burned by an overpromise. Only add tools that are proven and popular.

---

## THE RULE, one line
Master the basic setup → add Superpowers → then STOP and build for a while. Add nothing else
until a real problem tells you exactly what you're missing.
