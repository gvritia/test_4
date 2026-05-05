from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    field: str
    message: str
    error_type: str

