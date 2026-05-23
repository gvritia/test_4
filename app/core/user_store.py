"""In-memory хранилище пользователей и сессий.

Относится к заданиям:
- 10.1: выбрасывает кастомные ошибки бизнес-уровня;
- 10.2: работает с валидированными Pydantic-моделями пользователя и логина;
- 11.1, 11.2: служит хранилищем для тестируемых эндпоинтов users и auth.
"""

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
        # Lock нужен, чтобы операции записи были безопаснее при параллельных запросах.
        self._lock = Lock()
        # Основное хранилище: id пользователя -> словарь с данными.
        self._users: dict[int, dict] = {}
        # Вспомогательные индексы ускоряют поиск и проверку уникальности.
        self._username_index: dict[str, int] = {}
        self._email_index: dict[str, int] = {}
        # Активные сессии: token -> user_id.
        self._sessions: dict[str, int] = {}
        # Генератор последовательных идентификаторов пользователей.
        self._id_sequence = count(start=1)

    def reset(self) -> None:
        # Используется в тестах для полного сброса состояния хранилища.
        with self._lock:
            self._users.clear()
            self._username_index.clear()
            self._email_index.clear()
            self._sessions.clear()
            self._id_sequence = count(start=1)

    def create_user(self, payload: UserCreateRequest) -> dict:
        # Приводим ключи к нижнему регистру, чтобы уникальность не зависела от регистра.
        username_key = payload.username.lower()
        email_key = payload.email.lower()

        with self._lock:
            if username_key in self._username_index:
                raise UserAlreadyExistsError("Пользователь с таким username уже существует.")

            if email_key in self._email_index:
                raise UserAlreadyExistsError("Пользователь с таким email уже существует.")

            # Сохраняем только хеш пароля, а не исходный пароль.
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
            # Наружу возвращаем только безопасные публичные поля.
            return self._to_public_user(stored_user)

    def get_user(self, user_id: int) -> dict:
        with self._lock:
            stored_user = self._users.get(user_id)
            if stored_user is None:
                raise UserNotFoundError(user_id)
            return self._to_public_user(stored_user)

    def delete_user(self, user_id: int) -> None:
        with self._lock:
            # pop(..., None) удобно совмещает удаление и проверку существования.
            stored_user = self._users.pop(user_id, None)
            if stored_user is None:
                raise UserNotFoundError(user_id)

            # После удаления пользователя чистим вспомогательные индексы.
            self._username_index.pop(stored_user["username"].lower(), None)
            self._email_index.pop(stored_user["email"].lower(), None)
            # И удаляем все его активные сессии.
            self._sessions = {
                token: session_user_id
                for token, session_user_id in self._sessions.items()
                if session_user_id != user_id
            }

    def authenticate(self, payload: AuthLoginRequest) -> str:
        with self._lock:
            # Сначала ищем пользователя по логину.
            user_id = self._username_index.get(payload.username.lower())
            if user_id is None:
                raise InvalidCredentialsError("Неверный логин или пароль.")

            # Затем сверяем переданный пароль с хранимым хешем.
            stored_user = self._users[user_id]
            if not verify_password(payload.password, stored_user["password_hash"]):
                raise InvalidCredentialsError("Неверный логин или пароль.")

            # При успешной аутентификации создаем новую сессию.
            token = create_access_token()
            self._sessions[token] = user_id
            return token

    def get_user_by_token(self, token: str) -> dict:
        with self._lock:
            # Проверяем наличие активной сессии по токену.
            user_id = self._sessions.get(token)
            if user_id is None:
                raise InvalidCredentialsError("Сессия не найдена или уже завершена.")

            # Дополнительно убеждаемся, что пользователь не был удален.
            stored_user = self._users.get(user_id)
            if stored_user is None:
                raise InvalidCredentialsError("Пользователь с текущим токеном не найден.")

            return self._to_public_user(stored_user)

    def logout(self, token: str) -> None:
        with self._lock:
            # Logout просто инвалидирует токен, удаляя его из таблицы сессий.
            if token not in self._sessions:
                raise InvalidCredentialsError("Сессия не найдена или уже завершена.")
            del self._sessions[token]

    @staticmethod
    def _to_public_user(stored_user: dict) -> dict:
        # Централизованно отсекаем служебные поля вроде password_hash.
        return {
            "id": stored_user["id"],
            "username": stored_user["username"],
            "age": stored_user["age"],
            "email": stored_user["email"],
            "phone": stored_user["phone"],
        }


# Глобальный экземпляр хранилища используется роутами как единая "память" приложения.
user_store = InMemoryUserStore()
