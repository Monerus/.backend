from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, APIRouter
from typing import List
from api.repositories.auth_utils_jwt import *

router = APIRouter(prefix="/posts", tags=["Post"])


@router.post('/', response_model=PostsResponse, status_code=status.HTTP_201_CREATED)
async def create_post(posts_in: PostBase,
                      current_posts: Posts = Depends(get_current_user),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):    
    post = Posts(**posts_in.model_dump())
    post.users_id = current_posts.id
    
    try:
        session.add(post)
        await session.commit()
        await session.refresh(post)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    
    return post


#Получение поста пользователя
@router.get("/{user_id}/", response_model=None, status_code=status.HTTP_200_OK)
async def get_posts(user_id: int, 
                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> List[Posts]:
    result = await session.execute(select(Posts)
                                   .where(Posts.users_id == user_id)
                                   .order_by(Posts.created_at))
    posts = result.scalars().all()
    return list(posts)