from typing import Literal
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Literal["Tier1", "Tier2"] = "Tier1"
    disabled: bool | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserModelDB(UserBase):
    hashed_password: str