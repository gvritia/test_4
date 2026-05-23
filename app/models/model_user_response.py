"""Публичная модель пользователя для ответа клиенту.

Относится к заданиям 10.2, 11.1 и 11.2.
"""

from pydantic import BaseModel


class UserResponse(BaseModel):
    # Здесь нет password и password_hash: наружу такие поля никогда не отдаем.
    id: int
    username: str
    age: int
    email: str
    phone: str
