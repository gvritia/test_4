from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    email: str
    phone: str
