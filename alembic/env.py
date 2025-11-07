import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context


BASE_DIR = Path(__file__).resolve().parent.parent  
PROJECT_ROOT = BASE_DIR.parent  
sys.path.append(str(PROJECT_ROOT))


from src.infrastructure.settings.settings import settings
from src.infrastructure.db.models.base import Base


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


config.set_main_option("sqlalchemy.url", settings.db.DATABASE_URL)


def run_migrations_offline() -> None:
    url = settings.db.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.db.DATABASE_URL_asyncpg

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
