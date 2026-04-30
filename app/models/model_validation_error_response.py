from pydantic import BaseModel, Field

from app.models.model_validation_error_item import ValidationErrorItem


class ValidationErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    details: list[ValidationErrorItem] = Field(default_factory=list)
