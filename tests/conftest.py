from pathlib import Path
import sys

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "app.db"
sys.path.insert(0, str(ROOT_DIR))

from app.core.database import SessionLocal, engine
from app.core.user_store import user_store
from app.main import app
from app.models.model_product import Product


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    alembic_config = Config(str(ROOT_DIR / "alembic.ini"))
    command.upgrade(alembic_config, "head")
    yield

    engine.dispose()
    if DB_PATH.exists():
        DB_PATH.unlink()


@pytest.fixture(autouse=True)
def reset_application_state() -> None:
    user_store.reset()

    with SessionLocal() as session:
        session.execute(delete(Product).where(Product.id > 2))
        session.commit()

    yield

    user_store.reset()

    with SessionLocal() as session:
        session.execute(delete(Product).where(Product.id > 2))
        session.commit()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
