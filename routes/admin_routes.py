from fastapi import APIRouter, Depends

from models.models import UserOut
from models.db_models import UserDatabase
from dependencies.roles import verify_admin
from auth.jwt_auth import get_user_by_id

router = APIRouter(dependencies=[Depends(verify_admin)])

@router.get("/users", response_model=list[UserOut])
async def get_users():
    users = await UserDatabase.all()
    return users

@router.get("/users/total")
async def get_users_total():
    total_users = await UserDatabase.all().count()
    return {"total_users": total_users}

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user = await get_user_by_id(UserDatabase, user_id)
    return user

@router.get("/users/activity")
async def get_user_activity():
    pass

@router.get("/users/active")
async def get_active_user():
    pass
