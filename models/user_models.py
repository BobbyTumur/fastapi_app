from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    disabled: bool | None = None
