#!/usr/bin/env bash
set -euo pipefail

# This database is initialized by the backend (SQLAlchemy creates tables at startup).
# Ensure Postgres is running and listening on port 5001 before starting the backend.
echo "PostgreSQL should be available on port 5001. Backend will auto-create schema."
