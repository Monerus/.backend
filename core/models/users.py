from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime, func
from .base import Base
from typing import Literal


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())
    vote: Mapped[int] = mapped_column(default=0)


class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    message_text: Mapped[str] = mapped_column(String(50))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())



class Posts(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str] = mapped_column(String(300))
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())



class Comments(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text_comment: Mapped[str] = mapped_column(String(100))
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comments_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())

    

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int]= mapped_column(primary_key=True)
    transaction_id: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    votes_count: Mapped[int]
    status: Mapped[Literal['pending', 'completed', 'failed']] = mapped_column(server_default='pending')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
