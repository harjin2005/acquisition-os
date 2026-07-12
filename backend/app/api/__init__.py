"""API package — versioned routers live under `v1/`.

Sprint 1 keeps the router wiring in `app.main` (each module exposes its own
router). This file exists so `app.api` is importable as a layer for
import-linter's boundary enforcement.
"""
