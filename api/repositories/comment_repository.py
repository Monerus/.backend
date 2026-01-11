from api.models import *
from core.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, APIRouter

router = APIRouter(prefix='/comments', tags=["Comments"])

@router.post("/{posts_id}/{users_id}/", response_model=CommentsResponse, status_code=status.HTTP_200_OK)
async def create_comments(comments_in: CommentsCreate, 
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    comments = Comments(**comments_in.model_dump())
    session.add(comments)
    await session.commit()
    return comments