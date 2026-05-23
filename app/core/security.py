"""Простейшие утилиты безопасности для учебного проекта.

Относится к заданиям:
- 10.1: участвует в логике логина и логаута;
- 10.2: помогает не хранить пароль в открытом виде;
- 11.1: поведение косвенно проверяется тестами авторизации.
"""

import hashlib
import secrets


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    # Повторно хешируем входной пароль и сравниваем с сохраненным хешем.
    return hash_password(password) == password_hash


def create_access_token() -> str:
    # Генерируем случайную строку, которая будет идентификатором пользовательской сессии.
    return secrets.token_urlsafe(32)
