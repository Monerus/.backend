from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    