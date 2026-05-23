"""Ошибка конфликта при создании пользователя.

Относится к заданиям 10.1 и 10.2: показывает, как предметная ошибка
преобразуется в HTTP 409 Conflict.
"""

from app.exceptions.application_error import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, message: str = "Пользователь уже существует.") -> None:
        super().__init__(status_code=409, error="user_already_exists", message=message)
