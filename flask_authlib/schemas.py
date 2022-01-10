from typing import Optional

from pydantic import EmailStr
from pydantic import BaseModel


class RegisterData(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password_hash: str
    is_admin: bool
