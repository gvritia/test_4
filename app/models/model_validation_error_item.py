"""Одна конкретная ошибка валидации поля.

Относится к заданию 10.2.
"""

from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    # field - имя поля, где произошла ошибка.
    field: str
    # message - человекочитаемое пояснение.
    message: str
    # error_type - технический тип ошибки от Pydantic/FastAPI.
    error_type: str
