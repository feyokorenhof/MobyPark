from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Register models so they attach to Base.metadata ---
# Import Base and ALL model modules here
from app.db.base import Base  # noqa: E402
from app.models import user  # noqa: F401
from app.models import reservation  # noqa: F401
# add any other model modules here, e.g. from app.models import spot

# Override the sqlalchemy.url from env when present
url = os.getenv("SYNC_DATABASE_URL", config.get_main_option("sqlalchemy.url"))
if url:
    config.set_main_option("sqlalchemy.url", url)

# This is what Alembic needs for --autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()