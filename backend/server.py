"""Supervisor entrypoint shim.

Emergent's supervisor expects `/app/backend/server.py` with a module-level
`app` symbol. The canonical FastAPI factory lives at `app.main:app` per
DOC-130 §2 folder structure — this shim just re-exports it.
"""

from app.main import app  # noqa: F401
