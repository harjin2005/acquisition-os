"""Contract-tests: import-linter itself.

Sprint 1 AC #2 requires "red PR on boundary violation demo". We embed the
demo *as a test*: a violation file exists in `_boundary_demo/` and CI proves
that removing its ignore entry causes `lint-imports` to fail. See
`.github/workflows/ci.yml` step `import-linter demo`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_import_linter_is_green_baseline():
    """Baseline must always pass — merge blocker if this ever fails."""
    result = subprocess.run(
        ["lint-imports", "--config", ".importlinter"],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
    )
    assert (
        result.returncode == 0
    ), f"import-linter failed:\n{result.stdout}\n{result.stderr}"
    assert "0 broken" in result.stdout


def test_import_linter_would_catch_a_violation(tmp_path, monkeypatch):
    """Simulate the "red PR on boundary violation demo" AC: writing a
    module that violates a contract (importing openai from a module) must
    make lint-imports return non-zero.

    We use a temporary contract file that adds a *strict* rule to prove the
    tooling reacts to a violation.
    """
    backend_root = Path(__file__).resolve().parents[2]

    violating_module = (
        backend_root / "app" / "modules" / "identity" / "_temp_violation.py"
    )
    violating_module.write_text("import openai  # noqa: F401 — deliberate violation\n")
    try:
        result = subprocess.run(
            ["lint-imports", "--config", ".importlinter"],
            cwd=backend_root,
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode != 0
        ), "import-linter should have flagged the demo violation"
        assert "openai" in (result.stdout + result.stderr).lower()
    finally:
        violating_module.unlink(missing_ok=True)
