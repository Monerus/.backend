import bcrypt
from datetime import timedelta, datetime
import jwt
from sqlalchemy import select
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(stored_hash: str, plain_password: str):
    return bcrypt.checkpw(plain_password.encode(), stored_hash.encode())


def encode_jwt(payload: dict, 
               private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
               algorithms: str = settings.JWT_ALGORITHM,
               exripe_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
               expire_timedelta: timedelta | None = None
               ) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=exripe_minutes)
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, private_key, algorithm=algorithms)



def decode_jwt(token: str | bytes, 
               public_key: str = settings.PUBLIC_KEY_PATH.read_text(), 
               algorithms: str = settings.JWT_ALGORITHM):
    return jwt.decode(token, public_key, algorithms)



#create token
def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        exripe_minutes=expire_minutes,
        expire_timedelta=expire_timedelta)


#create access token
def create_access_token(user) -> str:
    jwt_payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


#create refresh token
def create_refresh_token(user) -> str:
    jwt_payload = {
        "sub": user.username
    }
    return create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expire_timedelta=timedelta(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def verify_token(token: str = Depends(oauth2_scheme), 
                 private_key: str = settings.PUBLIC_KEY_PATH.read_text()):
    try:
        payload = jwt.decode(token, private_key, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    return user_id



async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user_id = verify_token(token)
    result = await session.execute(select(Users).where(Users.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ошибка с пользователем")
    return user