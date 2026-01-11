from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, APIRouter
from typing import List

router = APIRouter(prefix="/posts", tags=["Post"])

@router.post('/{user_id}/', response_model=PostsResponse, status_code=status.HTTP_201_CREATED)
async def create_post(posts_in: PostsCreate, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):    
    post = Posts(**posts_in.model_dump())
    session.add(post)
    await session.commit()
    return post


#Получение поста пользователя
@router.get("/{user_id}/", response_model=None, status_code=status.HTTP_200_OK)
async def get_posts(user_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[Posts]:
    result = await session.execute(select(Posts)
                                   .where(Posts.users_id == user_id)
                                   .order_by(Posts.created_at))
    posts = result.scalars().all()
    return list(posts)