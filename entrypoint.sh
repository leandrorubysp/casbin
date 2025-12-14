#!/usr/bin/env sh
set -e

echo "Waiting for DB before seeding..."
# A simple wait loop; or you can rely on depends_on:service_healthy only.
# Here we just sleep a bit to be safe.
sleep 3

echo "Running Casbin seeds..."
python -m app.scripts.seed_casbin || echo "Casbin seed failed (maybe already seeded?)"

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload