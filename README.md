# MobyPark 🅿️  
**FastAPI + SQLAlchemy + Alembic + PostgreSQL + Redis (Dockerized)**

A clean, production-ready backend for a parking platform — with authentication, migrations, and Docker-based development.

This guide helps set everything up from a clean environment

---

## 🧭 Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
  - [.env](#env)
  - [`alembic.ini`](#alembicini)
- [First Run (Docker)](#first-run-docker)
- [Migrations (Alembic)](#migrations-alembic)
  - [Create a migration from models](#create-a-migration-from-models)
  - [Apply migrations](#apply-migrations)
  - [Upgrade to head (after model changes)](#upgrade-to-head-after-model-changes)
  - [Inspect the DB](#inspect-the-db)
- [Development Workflow](#development-workflow)
  - [Live reload](#live-reload)
  - [When `requirements.txt` changes](#when-requirementstxt-changes)
  - [Resetting the database](#resetting-the-database)
- [API Quickstart](#api-quickstart)
- [Common Pitfalls](#common-pitfalls)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Optional Enhancements](#optional-enhancements)

---

## 🧩 Prerequisites

- **Docker** and **Docker Compose** installed (Compose v2 → `docker compose`).
- No local Python installation required; everything runs inside Docker.

---

## 🗂 Project Structure

```text
mobypark/
├─ app/
│  ├─ main.py                 # FastAPI entrypoint
│  ├─ routers/
│  │  └─ auth.py              # /auth endpoints (register, login, users)
│  ├─ models/
│  │  ├─ __init__.py          # imports models to populate Base.metadata
│  │  ├─ user.py              # User ORM model
│  │  └─ reservation.py       # Example model
│  ├─ schemas/                # Pydantic v2 schemas (RegisterIn/Out, LoginIn/Out, UserOut)
│  ├─ services/security.py    # Password hashing & JWT helpers
│  ├─ db/
│  │  ├─ base.py              # Declarative Base + imports of all models
│  │  ├─ session.py           # Async session factory / get_session()
│  │  └─ ...
│  └─ core/config.py          # Settings (Pydantic BaseSettings)
├─ migrations/
│  ├─ env.py                  # Alembic env (uses DATABASE_URL)
│  └─ versions/               # Auto-generated migration scripts
├─ alembic.ini                # Alembic config
├─ docker-compose.yml
├─ requirements.txt
└─ .env                       # Local secrets & config (ignored by Git)
```

## ⚙️ Configuration

### `.env`

Create a `.env` file in the project root.

> ⚠️ **Important:** No inline comments (`#`) on the same line as values.

```dotenv
# --- PostgreSQL ---
POSTGRES_USER=app
POSTGRES_PASSWORD=change_me_strong
POSTGRES_DB=parking

# --- App runtime ---
APP_HOST=0.0.0.0
APP_PORT=8000
APP_WORKERS=4

# --- Redis (optional) ---
REDIS_HOST=redis
REDIS_PORT=6379

# --- Security ---
PASSWORD_PEPPER=add_a_long_random_string_here
JWT_SECRET=replace_with_long_random_string
JWT_ALG=HS256
JWT_EXP_MIN=30

# --- Database URLs (psycopg v3 driver) ---
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=${POSTGRES_DB}
DATABASE_USER=${POSTGRES_USER}
DATABASE_PASSWORD=${POSTGRES_PASSWORD}
DATABASE_URL=postgresql+psycopg://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}

