"""Единый формат ответа для ошибок валидации.

Относится к заданию 10.2: используется обработчиком RequestValidationError.
"""

from pydantic import BaseModel, Field

from app.models.model_validation_error_item import ValidationErrorItem


class ValidationErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    # details содержит список конкретных ошибок по полям запроса.
    details: list[ValidationErrorItem] = Field(default_factory=list)
