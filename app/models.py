from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    media_url = Column(String, nullable=True)
    scheduled_time = Column(DateTime)
    posted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Create relationship (optional, but helpful)
    user = relationship("User", back_populates="scheduled_posts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String)
    api_secret = Column(String)
    access_token = Column(String)
    access_token_secret = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    scheduled_posts = relationship("ScheduledPost", back_populates="user")
