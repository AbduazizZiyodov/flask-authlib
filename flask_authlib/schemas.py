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
    id: int
    username: str
    email: EmailStr
    password_hash: str
