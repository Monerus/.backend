from pydantic import BaseModel

class BuyVotesRequest(BaseModel):
    votes_count : int
    user_id: int

class BuyVotesResponse(BaseModel):
    transaction_id: str
    message: str