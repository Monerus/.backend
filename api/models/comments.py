from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentsBase(BaseModel):
    text_comment: str
    users_id: int
    comments_id: int
    

class CommentsCreate(CommentsBase):
    pass


class CommentsResponse(CommentsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime