from pydantic import BaseModel, ConfigDict
from typing import List
from .models import LikeType


class LikeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int
    user_id: int
    like_type: LikeType


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    

class PostId(PostBase):
    id: int
    author_id: int
    likes: List[LikeBase] = []