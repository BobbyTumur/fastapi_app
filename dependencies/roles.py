from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.jwt_auth import extract_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
user_roles = ["Tier1", "Tier2"]

async def verify_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = extract_token(token)
    if payload.get("role") not in user_roles:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
async def verify_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = extract_token(token)
    if payload.get("role") != "Tier2":
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )
