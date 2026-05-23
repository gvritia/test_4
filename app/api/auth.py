"""Роуты авторизации.

Относится к заданиям:
- 10.1: демонстрирует пользовательские исключения и коды 401;
- 10.2: входные данные принимаются через JSON-модель с валидацией;
- 11.1: покрывается синхронными тестами.
"""

from fastapi import APIRouter, Depends, Response, status

from app.api.response_docs import AUTH_LOGIN_RESPONSES, AUTH_LOGOUT_RESPONSES, AUTH_ME_RESPONSES
from app.core.dependencies import get_authorization_token, get_current_user
from app.core.user_store import user_store
from app.models.model_auth_login_request import AuthLoginRequest
from app.models.model_auth_token_response import AuthTokenResponse
from app.models.model_user_response import UserResponse

# Все auth-эндпоинты находятся под общим префиксом /auth.
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Выполнить вход",
    description=(
        "Принимает логин и пароль только в JSON-теле запроса, а не в query string.\n\n"
        "**Относится к заданиям:** `10.1`, `10.2`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- валидация модели входа;\n"
        "- пользовательская ошибка `401` при неверных учетных данных;\n"
        "- выдача bearer-токена после успешной аутентификации."
    ),
    responses=AUTH_LOGIN_RESPONSES,
)
def login(payload: AuthLoginRequest) -> AuthTokenResponse:
    # payload уже прошел валидацию Pydantic-моделью.
    # Если логин или пароль неверные, user_store выбросит кастомную 401-ошибку.
    token = user_store.authenticate(payload)
    # В ответе возвращаем токен в отдельной модели, чтобы структура была явной.
    return AuthTokenResponse(
        access_token=token,
        authorization_header=f"Bearer {token}",
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить текущего пользователя",
    description=(
        "Возвращает данные пользователя по Bearer-токену из заголовка `Authorization`.\n\n"
        "**Относится к заданиям:** `10.1`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- зависимость FastAPI для извлечения токена;\n"
        "- пользовательская ошибка `401`, если токен невалиден;\n"
        "- безопасный возврат только публичных полей пользователя."
    ),
    responses=AUTH_ME_RESPONSES,
)
def get_me(current_user: dict = Depends(get_current_user)) -> UserResponse:
    # Depends сначала достает Bearer-токен из заголовка,
    # затем ищет пользователя по активной сессии.
    return UserResponse(**current_user)


@router.delete(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Завершить текущую сессию",
    description=(
        "Инвалидирует текущий Bearer-токен.\n\n"
        "**Относится к заданиям:** `10.1`, `11.1`.\n\n"
        "Здесь демонстрируются:\n"
        "- завершение сессии через `DELETE`;\n"
        "- ответ `204 No Content`;\n"
        "- ошибка `401`, если токен уже недействителен или не передан."
    ),
    responses=AUTH_LOGOUT_RESPONSES,
)
def logout(token: str = Depends(get_authorization_token)) -> Response:
    # В logout нам нужен только токен. Если заголовок неправильный,
    # зависимость get_authorization_token сама выбросит 401.
    user_store.logout(token)
    # 204 No Content означает, что операция выполнена успешно без тела ответа.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
