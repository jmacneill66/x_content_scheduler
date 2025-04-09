from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    user_id: int = 1  # Default to the test user
    content: str
    media_url: Optional[str] = None
    scheduled_time: datetime
    posted: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
