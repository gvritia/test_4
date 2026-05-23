"""Модель входного JSON для /auth/login.

Относится к заданию 10.2: валидация данных запроса.
"""

from pydantic import BaseModel, ConfigDict, constr


class AuthLoginRequest(BaseModel):
    # extra="forbid" запрещает лишние поля,
    # str_strip_whitespace=True обрезает пробелы по краям строк.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # Логин должен быть строкой разумной длины.
    username: constr(min_length=3, max_length=50)
    # Пароль тоже валидируется на длину еще до входа в бизнес-логику.
    password: constr(min_length=8, max_length=16)
