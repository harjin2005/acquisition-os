#!/usr/bin/env bash
# Stop hook — run the affected module's fast tests before Claude declares done.
# Deterministic guarantee that CLAUDE.md's "tests ship with code" rule is met.
set -euo pipefail

cd "$(dirname "$0")/../.." >/dev/null

# Detect changed modules via git and run only their pytest markers.
changed=$(git diff --name-only HEAD 2>/dev/null | grep -E '^backend/app/modules/[^/]+/' | cut -d/ -f4 | sort -u || true)

if [[ -z "$changed" ]]; then
  # No module-scoped changes; run the fast smoke suite.
  cd backend && python -m pytest tests/rls -q --no-header --disable-warnings 2>&1 | tail -20
  exit 0
fi

cd backend
for mod in $changed; do
  echo "=== fast tests: $mod ==="
  python -m pytest "app/modules/$mod/tests" "tests/rls" -q --no-header --disable-warnings 2>&1 | tail -20
done
