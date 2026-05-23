"""Модель ответа после успешного логина.

Относится к заданиям 10.1 и 10.2.
"""

from typing import Literal

from pydantic import BaseModel


class AuthTokenResponse(BaseModel):
    # Сам токен клиент позже отправляет в заголовке Authorization.
    access_token: str
    # Literal помогает явно зафиксировать тип токена как bearer.
    token_type: Literal["bearer"] = "bearer"
    # Готовое значение для заголовка Authorization, удобное для ручного тестирования.
    authorization_header: str
