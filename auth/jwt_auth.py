from typing import Any
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status

from config.enviroment import env


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#check match of plain pw and hashed pw
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#get the user from DB
async def get_user(db, username: str) -> Any:
    try:
        user = await db.get(username=username)
        return user
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

#using 2 func above checking if the user is valid
async def authenticate_user(db, username: str, password: str) -> Any:
    user = await get_user(db, username)
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user.role)
    return user

#if the user is valid, creating jwt token for the user
def create_access_token(data: dict) -> str:
    #the reason why copy() is that to prevent accidently modifying the data
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=env.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.secret_key, algorithm=env.algorithm)
    return encoded_jwt

def extract_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, env.secret_key, algorithms=[env.algorithm])
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
