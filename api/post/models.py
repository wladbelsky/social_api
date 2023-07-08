from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship('User')
    likes = relationship('Like', back_populates='post')

    def __repr__(self):
        return f'<Post {self.title}>'
    

class LikeType(Enum):
    like = 'like'
    dislike = 'dislike'


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    like_type = Column(SQLEnum(LikeType), nullable=False)

    post = relationship('Post', back_populates='likes')
    user = relationship('User')
