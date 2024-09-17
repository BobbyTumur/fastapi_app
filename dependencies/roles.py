from typing import Annotated
from fastapi import Depends, HTTPException, status

from models.models import TokenData
from auth.jwt_auth import extract_token



USER_ROLES = ["Tier1", "Tier2"]


async def verify_user(token_data: Annotated[TokenData, Depends(extract_token)]):
    if token_data.role.value not in USER_ROLES:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
async def verify_admin(token_data: Annotated[TokenData, Depends(extract_token)]):
    if token_data.role.value != USER_ROLES[1]:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )
