from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status

from models.models import TokenData, UserOut, UserPasswordUpdate, UserInDB
from models.db_models import UserDatabase
from auth.jwt_auth import extract_token, get_user_by_id, verify_password, get_password_hash
from dependencies.roles import verify_user

router = APIRouter(dependencies=[Depends(verify_user)])


async def get_current_user(token_data: Annotated[TokenData, Depends(extract_token)]) -> Any:
    user = await get_user_by_id(UserDatabase, token_data.sub)
    return user

@router.get("/users/me", response_model=UserOut)
async def get_profile(user: Annotated[UserDatabase, Depends(get_current_user)]) -> Any:
    return user

@router.put("/users/me")
async def update_password(form: UserPasswordUpdate, user: Annotated[UserDatabase, Depends(get_current_user)]):
    if not verify_password(form.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    user.hashed_password = get_password_hash(form.new_password)
    await user.save()
    return {"status": "Password updated"}