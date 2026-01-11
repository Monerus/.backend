from sqlalchemy.ext.asyncio import AsyncSession
from api.models import *
from fastapi import Depends, status, APIRouter
from core.models import *
from sqlalchemy import select
from sqlalchemy.sql.expression import and_, or_


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post('/', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_in: MessageCreate, 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    
    message = Message(**message_in.model_dump())
    session.add(message)
    await session.commit()

    return message


#Индивидуальные переписки
@router.get("/{sender_id}/{recipient_id}")
async def get_messages_users(sender_id: int, recipient_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    stmt = await session.execute(
    select(Message).filter(
        or_(
            and_(Message.sender_id == sender_id, 
                 Message.recipient_id == recipient_id),
            and_(Message.sender_id == recipient_id, 
                 Message.recipient_id == sender_id)
        )
    )
)
    messages = stmt.scalars().all()
    return messages 