from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageBase(BaseModel):
    message_text: str
    sender_id: int
    recipient_id: int

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime