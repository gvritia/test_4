"""Общие фикстуры для тестов.

Относится к заданиям:
- 11.1: синхронные тесты через TestClient;
- 11.2: асинхронные тесты через httpx.AsyncClient и ASGITransport;
- 9.1: перед тестами поднимаются миграции Alembic.
"""

import os
from pathlib import Path
import sys

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

# Добавляем корень проекта в sys.path, чтобы pytest корректно импортировал пакет app.
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "test_app.db"
TEST_DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
sys.path.insert(0, str(ROOT_DIR))

# До импорта модулей приложения переключаем тесты на отдельную БД,
# чтобы не зависеть от основной app.db и не конфликтовать с внешними процессами.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.core.database import SessionLocal, engine
from app.core.user_store import user_store
from app.main import app
from app.models.model_product import Product


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> None:
    # Перед всей тестовой сессией создаем отдельную тестовую БД и применяем миграции.
    engine.dispose()
    if DB_PATH.exists():
        DB_PATH.unlink()

    alembic_config = Config(str(ROOT_DIR / "alembic.ini"))
    command.upgrade(alembic_config, "head")
    yield

    # После тестов освобождаем соединение с SQLite и удаляем временную БД.
    engine.dispose()
    if DB_PATH.exists():
        DB_PATH.unlink()


@pytest.fixture(autouse=True)
def reset_application_state() -> None:
    # Каждый тест должен быть изолирован:
    # 1) очищаем in-memory пользователей и сессии,
    # 2) удаляем из products только записи, созданные самими тестами.
    user_store.reset()

    with SessionLocal() as session:
        session.execute(delete(Product).where(Product.id > 2))
        session.commit()

    yield

    # Повторяем очистку после теста, чтобы состояние не "утекало" дальше.
    user_store.reset()

    with SessionLocal() as session:
        session.execute(delete(Product).where(Product.id > 2))
        session.commit()


@pytest.fixture
def client() -> TestClient:
    # Синхронный клиент нужен для тестов из задания 11.1.
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # ASGITransport позволяет тестировать приложение напрямую, без запуска Uvicorn.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
