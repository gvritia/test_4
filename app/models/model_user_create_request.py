import re

from pydantic import BaseModel, ConfigDict, EmailStr, conint, constr, field_validator


class UserCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    username: constr(min_length=3, max_length=50)
    age: conint(gt=18, le=120)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: str | None = "Unknown"

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str:
        if value is None or value == "":
            return "Unknown"

        if not re.fullmatch(r"\+?[0-9()\-\s]{7,20}", value):
            raise ValueError("Телефон должен содержать от 7 до 20 символов и только цифры/скобки/пробелы.")

        return value
