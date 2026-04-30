from typing import Annotated

from fastapi import Depends, Header

from app.core.user_store import user_store
from app.exceptions.invalid_credentials_error import InvalidCredentialsError


def get_authorization_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if authorization is None:
        raise InvalidCredentialsError("Отсутствует заголовок Authorization.")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise InvalidCredentialsError("Ожидается заголовок вида 'Bearer <token>'.")

    return token


def get_current_user(token: str = Depends(get_authorization_token)) -> dict:
    return user_store.get_user_by_token(token)
