from app.exceptions.application_error import ApplicationError


class InvalidCredentialsError(ApplicationError):
    def __init__(self, message: str = "Не удалось выполнить аутентификацию.") -> None:
        super().__init__(status_code=401, error="unauthorized", message=message)
