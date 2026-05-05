from app.models.model_error_response import ErrorResponse
from app.models.model_validation_error_response import ValidationErrorResponse


AUTH_LOGIN_RESPONSES = {
    200: {"description": "Аутентификация выполнена успешно."},
    401: {"model": ErrorResponse, "description": "Неверный логин или пароль."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

AUTH_ME_RESPONSES = {
    200: {"description": "Данные текущего пользователя успешно получены."},
    401: {"model": ErrorResponse, "description": "Отсутствует или некорректен Bearer-токен."},
}

AUTH_LOGOUT_RESPONSES = {
    204: {"description": "Текущая сессия успешно завершена."},
    401: {"model": ErrorResponse, "description": "Отсутствует или некорректен Bearer-токен."},
}

PRODUCT_LIST_RESPONSES = {
    200: {"description": "Список товаров успешно получен."},
}

PRODUCT_CREATE_RESPONSES = {
    201: {"description": "Товар успешно создан."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

PRODUCT_GET_RESPONSES = {
    200: {"description": "Товар успешно найден."},
    404: {"model": ErrorResponse, "description": "Товар с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор товара."},
}

USER_CREATE_RESPONSES = {
    201: {"description": "Пользователь успешно создан."},
    409: {"model": ErrorResponse, "description": "Пользователь с таким username или email уже существует."},
    422: {"model": ValidationErrorResponse, "description": "Некорректное JSON-тело запроса."},
}

USER_GET_RESPONSES = {
    200: {"description": "Пользователь успешно найден."},
    404: {"model": ErrorResponse, "description": "Пользователь с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор пользователя."},
}

USER_DELETE_RESPONSES = {
    204: {"description": "Пользователь успешно удален."},
    404: {"model": ErrorResponse, "description": "Пользователь с указанным идентификатором не найден."},
    422: {"model": ValidationErrorResponse, "description": "Некорректный идентификатор пользователя."},
}
