from pydantic import BaseModel, ConfigDict, constr


class AuthLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8, max_length=16)

