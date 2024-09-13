from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
import jwt

from config.settings import settings
from models.db_models import UserInDB
from models.token_models import Token, TokenData
from models.user_models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#check match of plain pw and hashed pw
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#get the user from DB
async def get_user(username: str) -> UserInDB | None:
    try:
        user = await UserInDB.get(username=username)
        return user
    except DoesNotExist:
        return None

#using 2 func above checking if the user is valid
async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = await get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

#if the user is valid, creating jwt token for the user
def create_access_token(data: dict):
    #the reason why copy() is that to prevent accidently modifying the data
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
