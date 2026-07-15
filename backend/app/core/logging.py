"""Structured logging bootstrap.

DOC-130 §7 mandates structured logs with actor/tenancy provenance. Sprint 1 wires
`structlog` with a JSON renderer and stashes org_id + actor_id from the tenancy
context (see `app.core.tenancy`) into every log line automatically.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from app.core.config import get_settings


def _tenancy_processor(
    _logger: Any, _name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Attach current org_id / actor_id from tenancy context, if any."""
    from app.core.tenancy import current_context  # local import to avoid cycles

    ctx = current_context()
    if ctx is not None:
        event_dict.setdefault("org_id", str(ctx.org_id))
        event_dict.setdefault("actor_id", str(ctx.actor_id) if ctx.actor_id else None)
    return event_dict


def configure_logging() -> None:
    settings = get_settings()

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.app_log_level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            _tenancy_processor,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.app_log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
