"""Роуты для ресурса users.

Относится к заданиям:
- 10.2: принимает JSON и валидирует пользовательские данные;
- 10.1: использует кастомные ошибки 404 и 409;
- 11.1, 11.2: покрывается синхронными и асинхронными тестами.
"""

from fastapi import APIRouter, Path, Response, status

from app.api.response_docs import USER_CREATE_RESPONSES, USER_DELETE_RESPONSES, USER_GET_RESPONSES
from app.core.user_store import user_store
from app.models.model_user_create_request import UserCreateRequest
from app.models.model_user_response import UserResponse

# Все операции над пользователями объединены в отдельный роутер.
router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    description=(
        "Создает пользователя из JSON payload.\n\n"
        "**Относится к заданиям:** `10.2`, `11.1`, `11.2`.\n\n"
        "Здесь демонстрируются:\n"
        "- валидация входных пользовательских данных;\n"
        "- REST-создание ресурса через `POST`;\n"
        "- запрет передачи логина/пароля через query string."
    ),
    responses=USER_CREATE_RESPONSES,
)
def create_user(payload: UserCreateRequest) -> UserResponse:
    # Пользователь создается только из JSON-тела запроса,
    # что соответствует REST-подходу
    return UserResponse(**user_store.create_user(payload))


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по идентификатору",
    description=(
        "Возвращает пользователя по его идентификатору.\n\n"
        "**Относится к заданиям:** `10.1`, `11.1`, `11.2`.\n\n"
        "Здесь демонстрируются:\n"
        "- REST-чтение ресурса через `GET`;\n"
        "- пользовательская ошибка `404`, если запись не найдена;\n"
        "- валидация path-параметра `user_id`."
    ),
    responses=USER_GET_RESPONSES,
)
def get_user(user_id: int = Path(gt=0, description="Положительный идентификатор пользователя.")) -> UserResponse:
    # Ограничение gt=0 на Path позволяет отловить некорректный id
    # еще до выполнения основной бизнес-логики.
    return UserResponse(**user_store.get_user(user_id))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя по идентификатору",
    description=(
        "Удаляет пользователя по идентификатору.\n\n"
        "**Относится к заданиям:** `10.1`, `11.1`, `11.2`.\n\n"
        "Здесь демонстрируются:\n"
        "- REST-удаление ресурса через `DELETE`;\n"
        "- ответ `204 No Content` при успешном удалении;\n"
        "- пользовательская ошибка `404`, если удалять нечего."
    ),
    responses=USER_DELETE_RESPONSES,
)
def delete_user(user_id: int = Path(gt=0, description="Положительный идентификатор пользователя.")) -> Response:
    # Если пользователя нет, user_store сам выбросит кастомную 404-ошибку.
    user_store.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
