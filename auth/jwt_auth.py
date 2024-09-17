import jwt
from typing import Annotated, Any
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config.enviroment import env
from models.models import TokenData, UserBase, UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_password_hash(password):
    return pwd_context.hash(password)

#check match of plain pw and hashed pw
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#get the user from DB
async def get_user(db, email: str) -> Any:
    try:
        user = await db.get(email=email)
        return user
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
async def get_user_by_id(db, user_id: int) -> Any:
    try: 
        user = await db.get(id=user_id)
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
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return user

#if the user is valid, creating jwt token for the user
def create_access_token(data: dict) -> str:
    #the reason why copy() is that to prevent accidently modifying the data
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=env.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.secret_key, algorithm=env.algorithm)
    return encoded_jwt

def extract_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        payload = jwt.decode(token, env.secret_key, algorithms=[env.algorithm])
        token_data = TokenData(**payload)
        return token_data
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
