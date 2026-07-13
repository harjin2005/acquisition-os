---
name: end-of-session
description: Run this at the end of every work session so nothing is forgotten between sessions. Updates the shared memory files.
---

# End of session — save the memory

When the founder says "wrap up" or the task is finished, do this so the NEXT session starts smart:

1. Write a 3-5 line summary of what you did into `.claude/CURRENT_STATE.md` (newest at top, in the Log).
2. Update the "What's built" and "What's in progress" sections if they changed.
3. If you hit any problem or made any decision, add it to "Known problems / things to watch".
4. Set `.claude/NEXT_TASK.md` to the next single task (or write "AWAITING FOUNDER" if unsure).
5. List anything the founder must decide before work continues.

Keep it SHORT and plain. This file is read at the start of every session — bloat here costs tokens
in every future session. One tight paragraph beats a page.
