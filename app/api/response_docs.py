"""Словари с описанием возможных HTTP-ответов для OpenAPI.

Относится к заданиям:
- 10.1, 10.2: помогает явно показать все важные статус-коды и модели ошибок;
- 11.1, 11.2: тесты проверяют именно те статусы, которые здесь документируются.
"""

from app.models.model_error_response import ErrorResponse
from app.models.model_validation_error_response import ValidationErrorResponse

# Для /auth/login показываем успешный вход, ошибку авторизации и ошибку валидации JSON.
AUTH_LOGIN_RESPONSES = {
    200: {"description": "Аутентификация выполнена успешно."},
    401: {"model": ErrorResponse, "description": "Неверный логин или пароль."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

# /auth/me либо возвращает текущего пользователя, либо сообщает о проблеме с токеном.
AUTH_ME_RESPONSES = {
    200: {"description": "Данные текущего пользователя успешно получены."},
    401: {"model": ErrorResponse, "description": "Отсутствует или некорректен Bearer-токен."},
}

# Для logout тело ответа не требуется, поэтому основной статус здесь 204.
AUTH_LOGOUT_RESPONSES = {
    204: {"description": "Текущая сессия успешно завершена."},
    401: {"model": ErrorResponse, "description": "Отсутствует или некорректен Bearer-токен."},
}

# Получение списка товаров не имеет специальных ошибок предметной области.
PRODUCT_LIST_RESPONSES = {
    200: {"description": "Список товаров успешно получен."},
}

# Создание товара может завершиться успехом или ошибкой валидации тела запроса.
PRODUCT_CREATE_RESPONSES = {
    201: {"description": "Товар успешно создан."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

# Получение товара по id дополнительно документирует случай 404.
PRODUCT_GET_RESPONSES = {
    200: {"description": "Товар успешно найден."},
    404: {"model": ErrorResponse, "description": "Товар с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор товара."},
}

# При создании пользователя отдельно описываем 409 Conflict для дублей.
USER_CREATE_RESPONSES = {
    201: {"description": "Пользователь успешно создан."},
    409: {"model": ErrorResponse, "description": "Пользователь с таким username или email уже существует."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

# Получение пользователя по id возвращает либо 200, либо 404/422.
USER_GET_RESPONSES = {
    200: {"description": "Пользователь успешно найден."},
    404: {"model": ErrorResponse, "description": "Пользователь с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор пользователя."},
}

# Для DELETE по REST тоже явно документируем все основные статусы.
USER_DELETE_RESPONSES = {
    204: {"description": "Пользователь успешно удален."},
    404: {"model": ErrorResponse, "description": "Пользователь с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор пользователя."},
}
