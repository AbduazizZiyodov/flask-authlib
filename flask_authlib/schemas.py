import typing as t
from pydantic import EmailStr, BaseModel

class RegisterData(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: t.Optional[int]
    username: str
    email: EmailStr
    password: str
    is_admin: bool