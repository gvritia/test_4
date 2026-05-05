from itertools import count
from threading import Lock


from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions.invalid_credentials_error import InvalidCredentialsError
from app.exceptions.user_already_exists_error import UserAlreadyExistsError
from app.exceptions.user_not_found_error import UserNotFoundError
from app.models.model_auth_login_request import AuthLoginRequest
from app.models.model_user_create_request import UserCreateRequest


class InMemoryUserStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._users: dict[int, dict] = {}
        self._username_index: dict[str, int] = {}
        self._email_index: dict[str, int] = {}
        self._sessions: dict[str, int] = {}
        self._id_sequence = count(start=1)

    def reset(self) -> None:
        with self._lock:
            self._users.clear()
            self._username_index.clear()
            self._email_index.clear()
            self._sessions.clear()
            self._id_sequence = count(start=1)

    def create_user(self, payload: UserCreateRequest) -> dict:
        username_key = payload.username.lower()
        email_key = payload.email.lower()

        with self._lock:
            if username_key in self._username_index:
                raise UserAlreadyExistsError("Пользователь с таким username уже существует.")

            if email_key in self._email_index:
                raise UserAlreadyExistsError("Пользователь с таким email уже существует.")

            user_id = next(self._id_sequence)
            stored_user = {
                "id": user_id,
                "username": payload.username,
                "age": payload.age,
                "email": payload.email,
                "phone": payload.phone,
                "password_hash": hash_password(payload.password),
            }
            self._users[user_id] = stored_user
            self._username_index[username_key] = user_id
            self._email_index[email_key] = user_id
            return self._to_public_user(stored_user)

    def get_user(self, user_id: int) -> dict:
        with self._lock:
            stored_user = self._users.get(user_id)
            if stored_user is None:
                raise UserNotFoundError(user_id)
            return self._to_public_user(stored_user)

    def delete_user(self, user_id: int) -> None:
        with self._lock:
            stored_user = self._users.pop(user_id, None)
            if stored_user is None:
                raise UserNotFoundError(user_id)

            self._username_index.pop(stored_user["username"].lower(), None)
            self._email_index.pop(stored_user["email"].lower(), None)
            self._sessions = {
                token: session_user_id
                for token, session_user_id in self._sessions.items()
                if session_user_id != user_id
            }

    def authenticate(self, payload: AuthLoginRequest) -> str:
        with self._lock:
            user_id = self._username_index.get(payload.username.lower())
            if user_id is None:
                raise InvalidCredentialsError("Неверный логин или пароль.")

            stored_user = self._users[user_id]
            if not verify_password(payload.password, stored_user["password_hash"]):
                raise InvalidCredentialsError("Неверный логин или пароль.")

            token = create_access_token()
            self._sessions[token] = user_id
            return token

    def get_user_by_token(self, token: str) -> dict:
        with self._lock:
            user_id = self._sessions.get(token)
            if user_id is None:
                raise InvalidCredentialsError("Сессия не найдена или уже завершена.")

            stored_user = self._users.get(user_id)
            if stored_user is None:
                raise InvalidCredentialsError("Пользователь с текущим токеном не найден.")

            return self._to_public_user(stored_user)

    def logout(self, token: str) -> None:
        with self._lock:
            if token not in self._sessions:
                raise InvalidCredentialsError("Сессия не найдена или уже завершена.")
            del self._sessions[token]

    @staticmethod
    def _to_public_user(stored_user: dict) -> dict:
        return {
            "id": stored_user["id"],
            "username": stored_user["username"],
            "age": stored_user["age"],
            "email": stored_user["email"],
            "phone": stored_user["phone"],
        }


user_store = InMemoryUserStore()
