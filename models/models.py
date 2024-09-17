from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, Enum):
    TIER1 = "Tier1"
    TIER2 = "Tier2"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: int
    role: UserRole

class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    disabled: bool


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserInDB(UserBase):
    id: int
    hashed_password: str