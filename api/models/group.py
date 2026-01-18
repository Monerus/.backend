from pydantic import BaseModel, ConfigDict
from datetime import datetime

class GroupBase(BaseModel):
    name: str
    title: str
    imageURL: str | None = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime



class SubscriptionsBase(BaseModel):
    subscriptions_id: int

class SubscriptionsResponse(SubscriptionsBase):
    model_config = ConfigDict(from_attributes=True)
    title: str = 'Успешно подписались'
    