"""Конфигурация Alembic для миграций.

Относится к заданию 9.1: Alembic должен видеть SQLAlchemy-модели
и применять миграции к той же базе, что и само приложение.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.database import Base, get_database_url

config = context.config

# Подставляем актуальный DATABASE_URL из приложения,
# чтобы FastAPI и Alembic работали с одной и той же БД.
config.set_main_option("sqlalchemy.url", get_database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata нужна Alembic для сравнения ORM-моделей со схемой БД.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Offline-режим генерирует SQL без живого подключения к базе.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Online-режим подключается к БД и применяет миграции напрямую.
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
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
