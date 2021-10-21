from pydantic import EmailStr
from pydantic import BaseModel


class UserRegisterData(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginData(BaseModel):
    username: str
    password: str
