"""Minimal in-process rate limiter — Sprint 1 stopgap.

Fixed-window, in-memory, keyed by caller (typically IP). Deliberately
dependency-free: this exists to stop trivial spam on the one unauthenticated
endpoint in Sprint 1 (`POST /api/v1/identity/orgs`), which is itself a
dev-only path replaced by a real WorkOS provisioning webhook in Sprint 2
(ADR-EMERGENT-001) — not worth a Redis-backed library for something that
short-lived.

Known limitation: state is per-process, not shared across instances. Do not
reuse this for a longer-lived public endpoint without first revisiting —
once ECS actually runs more than one task, this stops being effective and a
Redis-backed limiter (e.g. fastapi-limiter, once Valkey is wired up) is
the correct replacement.
"""

from __future__ import annotations

import threading
import time

from fastapi import HTTPException, status


class RateLimiter:
    """Fixed-window limiter: at most `max_requests` per `window_seconds` per key."""

    def __init__(self, *, max_requests: int, window_seconds: float) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._lock = threading.Lock()
        self._buckets: dict[str, tuple[float, int]] = {}

    def check(self, key: str) -> None:
        """Raise 429 if `key` has exceeded the limit; otherwise record the hit."""
        now = time.monotonic()
        with self._lock:
            window_start, count = self._buckets.get(key, (now, 0))
            if now - window_start > self._window_seconds:
                window_start, count = now, 0
            count += 1
            self._buckets[key] = (window_start, count)
            if count > self._max_requests:
                raise HTTPException(
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    "rate limit exceeded — try again later",
                )

    def reset(self) -> None:
        """Test-only hook — clear all buckets between tests."""
        with self._lock:
            self._buckets.clear()
