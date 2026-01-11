from sqlalchemy.ext.asyncio import AsyncSession
from api.models import *
from fastapi import Depends, status, APIRouter
from core.models import *
from sqlalchemy import select
from sqlalchemy.sql.expression import and_, or_
from api.repositories.auth_utils_jwt import *


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post('/', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_in: MessageCreate,
    current_messages: Message = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    
    message = Message(**message_in.model_dump())
    message.sender_id = current_messages.id
    try:
        session.add(message)
        await session.commit()
        await session.refresh(message)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

    return message


#Индивидуальные переписки
@router.get("/{sender_id}/{recipient_id}")
async def get_messages_users(sender_id: int, 
                             recipient_id: int,
                             current_user: dict = Depends(get_current_user),
                             session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    
    current_user_id = current_user.id

    
    if current_user_id != sender_id and current_user_id != recipient_id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    
    stmt = select(Message).where(or_(
        and_(Message.sender_id == sender_id, Message.recipient_id == recipient_id),
        and_(Message.sender_id == recipient_id, Message.recipient_id == sender_id)
    ))

    # Выполняем запрос
    result = await session.execute(stmt)
    messages = result.scalars().all()
    
    return messages 