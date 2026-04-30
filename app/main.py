from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.users import router as users_router
from app.core.exception_handlers import register_exception_handlers

app = FastAPI(
    title="Контрольная работа №4",
    version="1.0.0",
    description=(
        "REST API на FastAPI с валидацией, пользовательскими ошибками, "
        "SQLAlchemy, Alembic и набором синхронных/асинхронных тестов."
    ),
)

register_exception_handlers(app)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)


@app.get(
    "/health",
    tags=["service"],
    summary="Проверка доступности сервиса",
    responses={
        200: {
            "description": "Сервис доступен.",
            "content": {"application/json": {"example": {"status": "ok"}}},
        }
    },
)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
