from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.models import Token
from models.db_models import UserDatabase
from auth.jwt_auth import authenticate_user, create_access_token

router = APIRouter()

@router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(UserDatabase, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")