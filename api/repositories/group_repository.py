from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, APIRouter
from api.repositories.auth_utils_jwt import *


router = APIRouter(prefix='/group', tags=["Group"])

#Создать группу, может, только авторизованный пользователь. 
@router.post('/', response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(group_in: GroupCreate,
                       current_group: Group = Depends(get_current_user),
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    group = Group(**group_in.model_dump())
    group.created_user = current_group.id
    
    try:
        session.add(group)
        await session.commit()
        await session.refresh(group)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
    return group

    
    
#Подписаться на группу
@router.post('/connect-group/', response_model=None)
async def connect_group_user(connect_in: SubscriptionsBase,
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                             current_connect: Subscriptions = Depends(get_current_user)):
    connect = Subscriptions(**connect_in.model_dump())
    connect.user_id = current_connect.id
    try:
        session.add(connect)
        await session.commit()
        await session.refresh(connect)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    return connect



#Показать все группы пользователя
@router.get('/{user_id}/', response_model=None)
async def get_users(user_id: int, 
                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    stmt = select(Group).join(Subscriptions).where(Subscriptions.user_id == user_id)
    result = await session.execute(stmt)
    groups = result.scalars().all()
    return groups