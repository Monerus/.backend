from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime, func, UniqueConstraint
from .base import Base
from typing import Literal


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())
    vote: Mapped[int] = mapped_column(default=0)


class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    message_text: Mapped[str] = mapped_column(String(50))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())



class Posts(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    title: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str] = mapped_column(String(300))
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())



class Comments(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    text_comment: Mapped[str] = mapped_column(String(100))
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comments_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now())

    

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int]= mapped_column(primary_key=True, )
    transaction_id: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    votes_count: Mapped[int]
    status: Mapped[Literal['pending', 'completed', 'failed']] = mapped_column(server_default='pending')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))









# Группа 
class Group(Base):
    __tablename__ = "group"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    created_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    imageURL: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    
    
    
#Подписка на группу
class Subscriptions(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    subscriptions_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    
    __table_args__ = (UniqueConstraint('user_id', 'subscriptions_id'), )
    
    def __repr__(self):
        return f"<Subscription({self.user_id}, {self.subscriptions_id})>"



#Посты в группе, может оставлять любой желающий
class PostsGroup(Base):
    __tablename__ = "postsgroup"
    
    id: Mapped[int] = mapped_column(primary_key=True, )
    
    text: Mapped[str] = mapped_column(String(300), nullable=True)
    imageURL: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    created_at: Mapped[int] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    
    
    