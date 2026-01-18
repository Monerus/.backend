from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PostGroupBase(BaseModel):
    text: str
    imageURL: str
    group_id: int

class PostsGroupCreate(PostGroupBase):
    pass

class PostsGroupResponse(PostGroupBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    created_at: datetime