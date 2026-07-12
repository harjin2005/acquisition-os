#!/usr/bin/env bash
# scripts/dev-up.sh — Sprint 1 AC #1: fresh clone → this script → API health + frontend render.
#
# Steps:
#   1. Ensure Postgres is running with the expected roles/schemas.
#   2. Install backend + frontend dependencies (idempotent).
#   3. Run alembic migrations.
#   4. Start (or restart) supervisor-managed services and wait for /api/health.
#
# Emergent adaptation: this script targets the local preview container. In
# staging/prod the equivalent is `.github/workflows/deploy.yml`.

set -euo pipefail

APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_ROOT"

echo "==> [1/5] Postgres — ensuring cluster + roles + schemas"
if ! pg_isready -h localhost -p 5432 -U postgres >/dev/null 2>&1; then
  # Start via supervisor (see /etc/supervisor/conf.d/postgresql.conf).
  sudo supervisorctl start postgresql || true
  sleep 3
fi
su - postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='acquisition_os'\" | grep -q 1 || psql -c \"CREATE USER acquisition_os WITH PASSWORD 'acquisition_os_dev';\"" >/dev/null
su - postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname='acquisition_os'\" | grep -q 1 || psql -c \"CREATE DATABASE acquisition_os OWNER acquisition_os;\"" >/dev/null
su - postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='acquisition_os_svc'\" | grep -q 1 || psql -c \"CREATE USER acquisition_os_svc WITH PASSWORD 'acquisition_os_svc_dev' BYPASSRLS;\"" >/dev/null
su - postgres -c "psql -d acquisition_os -c 'CREATE SCHEMA IF NOT EXISTS licensed; CREATE SCHEMA IF NOT EXISTS core; CREATE SCHEMA IF NOT EXISTS derived; CREATE SCHEMA IF NOT EXISTS audit; CREATE SCHEMA IF NOT EXISTS events;' >/dev/null"
su - postgres -c "psql -d acquisition_os -c 'GRANT USAGE ON SCHEMA core, licensed, derived, audit, events TO acquisition_os_svc; GRANT ALL ON ALL TABLES IN SCHEMA core, licensed, derived, audit, events TO acquisition_os_svc; ALTER DEFAULT PRIVILEGES FOR ROLE acquisition_os IN SCHEMA core, licensed, derived, audit, events GRANT ALL ON TABLES TO acquisition_os_svc;' >/dev/null"

echo "==> [2/5] Backend deps"
pip install -q -r backend/requirements.txt

echo "==> [3/5] Alembic migrations"
(cd backend && alembic upgrade head)

echo "==> [4/5] Frontend deps"
if [ -f frontend/yarn.lock ]; then
  (cd frontend && yarn install --frozen-lockfile --silent)
else
  (cd frontend && yarn install --silent)
fi

echo "==> [5/5] Supervisor restart"
sudo supervisorctl restart backend frontend
for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS http://localhost:8001/api/health >/dev/null 2>&1; then
    echo "OK — API healthy: $(curl -sS http://localhost:8001/api/health)"
    exit 0
  fi
  sleep 2
done

echo "!! API failed to become healthy in 20s. Check /var/log/supervisor/backend.err.log" >&2
exit 1
