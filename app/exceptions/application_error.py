"""Базовый класс для всех пользовательских ошибок приложения.

Относится к заданию 10.1: такие исключения централизованно
обрабатываются в app/core/exception_handlers.py.
"""


class ApplicationError(Exception):
    def __init__(self, status_code: int, error: str, message: str) -> None:
        # Сохраняем все части будущего HTTP-ответа прямо внутри исключения.
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(message)
