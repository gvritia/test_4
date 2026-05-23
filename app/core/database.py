"""Настройка SQLAlchemy и подключения к базе данных.

Относится к заданиям:
- 9.1: база, модель Product и миграции Alembic используют именно этот модуль;
- 11.1: тесты берут из него SessionLocal и engine.
"""

import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Корень проекта нужен, чтобы по умолчанию хранить SQLite-файл рядом с приложением.
ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_URL = f"sqlite:///{(ROOT_DIR / 'app.db').as_posix()}"


def get_database_url() -> str:
    # Позволяем переопределять адрес БД через переменную окружения DATABASE_URL.
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


class Base(DeclarativeBase):
    # Общий базовый класс для всех SQLAlchemy-моделей проекта.
    pass


DATABASE_URL = get_database_url()

# Для SQLite требуется check_same_thread=False,
# иначе при тестах и нескольких обращениях можно получить ошибку доступа.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# engine управляет физическим подключением к БД.
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal - фабрика ORM-сессий, которую мы используем в эндпоинтах и тестах.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    # Dependency для FastAPI: открываем сессию на время запроса и гарантированно закрываем.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
