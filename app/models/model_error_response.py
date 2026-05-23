"""Единая модель обычной бизнес-ошибки.

Относится к заданию 10.1: все кастомные ошибки приводятся к этому формату.
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    # HTTP-статус дублируем в теле, чтобы клиенту было удобнее разбирать ответ.
    status_code: int
    error: str
    message: str
