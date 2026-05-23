"""Модель JSON-запроса для создания пользователя.

Относится к заданию 10.2: здесь сосредоточена основная валидация входных данных.
"""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, conint, constr, field_validator


class UserCreateRequest(BaseModel):
    # Запрещаем неожиданные поля и автоматически убираем пробелы по краям строк.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # username - обычная строка с ограничением по длине.
    username: constr(min_length=3, max_length=50)
    # Возраст строго больше 18, как было в условии задания.
    age: conint(gt=18, le=120)
    # EmailStr сам проверяет, что строка похожа на реальный email.
    email: EmailStr
    # Пароль ограничиваем по длине.
    password: constr(min_length=8, max_length=16)
    # Телефон необязательный: если не пришел, подставляется "Unknown".
    phone: str | None = "Unknown"

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str:
        # Если телефон не передан, возвращаем стандартное значение.
        if value is None or value == "":
            return "Unknown"

        # Разрешаем цифры, пробелы, скобки, дефисы и необязательный плюс в начале.
        if not re.fullmatch(r"\+?[0-9()\-\s]{7,20}", value):
            raise ValueError("Телефон должен содержать от 7 до 20 символов и только цифры/скобки/пробелы.")

        return value
