"""Главный модуль FastAPI-приложения.

Относится к заданиям:
- 10.1: подключает пользовательскую обработку ошибок;
- 10.2: собирает API с валидацией входных данных;
- 11.1, 11.2: используется как целевое приложение для тестов.
"""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.users import router as users_router
from app.core.exception_handlers import register_exception_handlers

# Метаданные тегов отображаются прямо в Swagger UI
# и помогают быстро понять, к каким заданиям относится группа эндпоинтов.
openapi_tags = [
    {
        "name": "users",
        "description": (
            "Операции над пользователями.\n\n"
            "**Относятся к заданиям:** `10.2`, `11.1`, `11.2`.\n\n"
            "Здесь показаны прием JSON, валидация входных данных, "
            "REST-операции и их тестирование."
        ),
    },
    {
        "name": "auth",
        "description": (
            "Операции авторизации и работы с текущей сессией.\n\n"
            "**Относятся к заданиям:** `10.1`, `10.2`, `11.1`.\n\n"
            "Здесь показаны пользовательские ошибки `401`, "
            "валидация JSON и проверка токена."
        ),
    },
    {
        "name": "products",
        "description": (
            "Операции над товарами из базы данных.\n\n"
            "**Относятся к заданиям:** `9.1`, `10.1`, `11.1`.\n\n"
            "Эта группа связана с SQLAlchemy, Alembic-миграциями, "
            "REST-обработкой ресурса Product и ошибкой `404`."
        ),
    },
    {
        "name": "service",
        "description": (
            "Технические сервисные эндпоинты.\n\n"
            "Используются для проверки доступности API и не относятся "
            "к отдельному заданию контрольной."
        ),
    },
]

# Создаем основной объект FastAPI, который объединяет все части приложения.
app = FastAPI(
    title="Контрольная работа №4",
    version="1.0.0",
    description=(
        "REST API на FastAPI с валидацией, пользовательскими ошибками, "
        "SQLAlchemy, Alembic и набором синхронных/асинхронных тестов.\n\n"
        "В Swagger UI у каждой группы и каждого маршрута указано, "
        "к какому заданию контрольной он относится."
    ),
    openapi_tags=openapi_tags,
)

# Подключаем глобальные обработчики ошибок до регистрации роутеров,
# чтобы единый формат ответов работал по всему приложению.
register_exception_handlers(app)

# Каждый ресурс вынесен в отдельный файл с роутами, как требовалось в задании.
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)


@app.get(
    "/health",
    tags=["service"],
    summary="Проверка доступности сервиса",
    description=(
        "Техническая проверка, что приложение запущено и отвечает.\n\n"
        "**Относится:** к инфраструктурной части проекта, а не к отдельному заданию."
    ),
    responses={
        200: {
            "description": "Сервис доступен.",
            "content": {"application/json": {"example": {"status": "ok"}}},
        }
    },
)
def healthcheck() -> dict[str, str]:
    # Технический эндпоинт для быстрой проверки, что сервер поднялся.
    return {"status": "ok"}
