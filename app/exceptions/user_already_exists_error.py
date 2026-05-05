from app.exceptions.application_error import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, message: str = "Пользователь уже существует.") -> None:
        super().__init__(status_code=409, error="user_already_exists", message=message)

