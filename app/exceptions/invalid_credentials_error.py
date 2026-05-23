"""Ошибка авторизации.

Относится к заданиям 10.1 и 10.2: используется в auth-логике и зависимостях.
"""

from app.exceptions.application_error import ApplicationError


class InvalidCredentialsError(ApplicationError):
    def __init__(self, message: str = "Не удалось выполнить аутентификацию.") -> None:
        # 401 Unauthorized подходит для неверного токена, логина или пароля.
        super().__init__(status_code=401, error="unauthorized", message=message)
