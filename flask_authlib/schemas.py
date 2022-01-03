from pydantic import EmailStr
from pydantic import BaseModel


class RegisterData(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str
