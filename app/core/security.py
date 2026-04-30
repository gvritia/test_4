import hashlib
import secrets


def hash_password(password: str) -> str:
    # Для учебного проекта достаточно детерминированного хеша.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token() -> str:
    return secrets.token_urlsafe(32)
