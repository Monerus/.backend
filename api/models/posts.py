from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PostBase(BaseModel):
    title: str
    image_url: str
    users_id: int
    
class PostsCreate(PostBase):
    pass

class PostsResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime