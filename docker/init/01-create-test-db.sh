#!/usr/bin/env bash
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<SQL
SELECT format('CREATE DATABASE %I', '$POSTGRES_TEST_DB')
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_TEST_DB')
\gexec
SQL
