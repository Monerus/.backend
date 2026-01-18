from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, APIRouter
from api.repositories.auth_utils_jwt import *

router = APIRouter(prefix="/group-posts", tags=["PostsGroup"])


@router.post('/test', response_model=PostsGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_post(posts_in: PostGroupBase,
                      current_user: PostsGroup = Depends(get_current_user),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):    
    
    post = PostsGroup(**posts_in.model_dump())
    
    post.author_id = current_user.id


    try:
        session.add(post)
        await session.commit()
        await session.refresh(post)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    
    return post