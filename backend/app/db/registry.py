"""Import surface for Alembic and application startup.

Alembic's `env.py` imports this module so autogenerate sees every model.
Modules that add tables **must** import their model files here.
"""

from app.db.base import Base  # noqa: F401 — re-export for alembic
from app.modules.identity import models as _identity_models  # noqa: F401
from app.modules.ontology import models as _ontology_models  # noqa: F401
from app.modules.leads import models as _lead_models  # noqa: F401
from app.modules.deals import models as _deal_models  # noqa: F401
from app.modules.conversations import models as _conv_models  # noqa: F401
from app.modules.campaigns import models as _camp_models  # noqa: F401
from app.modules.underwriting import models as _uw_models  # noqa: F401
from app.modules.admin import models as _admin_models  # noqa: F401
from app.modules.agents_svc import models as _agent_models  # noqa: F401
from app.modules.imports import models as _import_models  # noqa: F401

__all__ = ["Base"]
