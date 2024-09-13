from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.token_models import Token
from auth.jwt_auth import authenticate_user, create_access_token

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise credential_exception
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")