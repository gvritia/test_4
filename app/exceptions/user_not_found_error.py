"""Ошибка отсутствующего пользователя.

Относится к заданиям 10.1, 10.2 и 11.2: используется в get/delete сценариях.
"""

from app.exceptions.application_error import ApplicationError


class UserNotFoundError(ApplicationError):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            status_code=404,
            error="user_not_found",
            message=f"Пользователь с id={user_id} не найден.",
        )
