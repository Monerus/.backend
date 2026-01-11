from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from fastapi import Depends, status, APIRouter, HTTPException, BackgroundTasks
from uuid import uuid4


router = APIRouter(prefix="/votes", tags=["Votes"])



async def save_transaction_to_db(session: AsyncSession, 
                                 transaction_id: str, 
                                 votes_count : int, 
                                 user_id: int):
    
    stmt = insert(Transaction).values(
        transaction_id=transaction_id,
        user_id = user_id,
        votes_count=votes_count,
    )
    
    await session.execute(stmt)
    await session.commit()



@router.post("/buy-votes/", status_code=status.HTTP_201_CREATED)
async def initiate_buying_voices(request: BuyVotesRequest, 
                                 background_tasks: BackgroundTasks, 
                                 session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    transaction_id = str(uuid4())
    
    background_tasks.add_task(save_transaction_to_db, 
                              session, transaction_id, 
                              request.votes_count, 
                              request.user_id)
    
    return {
        "transaction_id": transaction_id,
        "message": "Процесс покупки голосов запущен!"
    }


@router.post("/buying-votes/{transaction_id}", status_code=status.HTTP_200_OK)
async def complete_buying_voices(transaction_id: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    # Загружаем транзакцию из базы данных
    result = await session.execute(select(Transaction).where(Transaction.transaction_id == transaction_id))
    transaction = result.scalars().first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена!")

    user_result = await session.execute(select(Users).where(Users.id == transaction.user_id))
    
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    
    
    update_vote = user.vote + transaction.votes_count
    await session.execute(update(Users).where(Users.id == user.id).values(vote=update_vote))
    
    # Меняем статус транзакции на "завершено"
    transaction.status = "completed"
    await session.commit()
    
    return {"status": "ok", "detail": f"Транзакция {transaction_id} успешно завершена."}