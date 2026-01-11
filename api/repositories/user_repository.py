from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from api.repositories.auth_utils_jwt import *



router = APIRouter(prefix='/auth', tags=["Users"])
  

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, 
                     session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    hashed_password = hash_password(user_in.hashed_password)
    user_data = {
        **user_in.model_dump(exclude={'password'}),
        "hashed_password": hashed_password,
    }
    user = Users(**user_data)
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Почта уже занята')
    return UserResponse.from_orm(user) 
    
    
@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_in: UserBase,
                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    result = await session.execute(
        select(Users)
        .where(Users.email == user_in.email)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(user.hashed_password, user_in.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверные данные'
        )
    try:
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка авторизации.'
        )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/users/", response_model=None)
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    result = await session.execute(select(Users))
    stmt = result.scalars().all()
    return stmt
    

#Обновление имени пользователя
@router.patch('/update-username/', response_model=UserResponse)
async def update_username(updated_data: UserBase, 
                          current_user: Users = Depends(get_current_user), 
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        current_user.username = updated_data.username
        await session.commit()
        await session.refresh(current_user)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
    return current_user



#
@router.patch('/update-email/', response_model=UserResponse)
async def update_email(updated_data: UserBase,
                       current_user: Users = Depends(get_current_user),
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        current_user.email = updated_data.email
        await session.commit()
        await session.refresh(current_user)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return current_user
        
        
        

