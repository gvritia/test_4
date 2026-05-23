"""Небольшие зависимости FastAPI для авторизации.

Относится к заданиям:
- 10.1: помогает централизованно выбрасывать 401-ошибки;
- 10.2: используется в auth-эндпоинтах вместе с проверенными моделями;
- дополнительно: корректно интегрируется со Swagger через HTTP Bearer security scheme.
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.user_store import user_store
from app.exceptions.invalid_credentials_error import InvalidCredentialsError

# Эта схема говорит Swagger/OpenAPI, что защищенные эндпоинты работают
# через Bearer-токен в заголовке Authorization.
bearer_scheme = HTTPBearer(auto_error=False)


def get_authorization_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    # Если заголовок не был отправлен вообще, credentials будет None.
    if credentials is None:
        raise InvalidCredentialsError("Отсутствует заголовок Authorization.")

    # HTTPBearer сам разбирает схему и токен, но дополнительно проверим,
    # что схема действительно Bearer.
    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise InvalidCredentialsError("Ожидается заголовок вида 'Bearer <token>'.")

    return credentials.credentials


def get_current_user(token: str = Depends(get_authorization_token)) -> dict:
    # Сначала получаем токен, затем ищем по нему пользователя.
    return user_store.get_user_by_token(token)
