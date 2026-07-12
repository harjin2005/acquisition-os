"""Import surface for Alembic and application startup.

Alembic's `env.py` imports this module so autogenerate sees every model.
Modules that add tables **must** import their model files here.
"""

from app.db.base import Base  # noqa: F401 — re-export for alembic
from app.modules.identity import models as _identity_models  # noqa: F401
from app.modules.ontology import models as _ontology_models  # noqa: F401

__all__ = ["Base"]
