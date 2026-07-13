---
name: new-migration
description: The safe checklist for any database structure change. Database changes are risky; never freehand them.
---

# Database change checklist (do every step)

Database changes can break everything or expose customer data. Go slow.

1. STOP and confirm with the founder that this change is needed and in scope.
2. Follow the "expand then contract" rule: add new things first, move data, remove old things
   LAST in a separate step — never rename/delete in one shot on a live table.
3. Every new table MUST have `org_id` and row-level security. No exceptions.
4. Use only the entity names from `docs/product/02-glossary.md`.
5. Write a rollback note: how to undo this if it goes wrong.
6. Run the migration on a test copy first. Show it works.
7. Run the data-safety tests (the ones that try to read across customers). They must pass.

If any step is unclear, STOP. A broken migration is one of the most expensive mistakes possible.
