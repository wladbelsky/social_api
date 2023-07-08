from database import Database
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from api.auth.router import check_token
from fastapi import APIRouter, Depends, HTTPException
from .models import Post, Like, LikeType
from api.auth.schemas import User as UserSchema
from .schemas import PostId, PostBase as PostSchema
from typing import List


router = APIRouter(
    prefix="/post",
)

@router.get('/', response_model=List[PostId])
async def get_posts(user = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).options(selectinload(Post.author), selectinload(Post.likes))
        result = await db.execute(stmt)
        posts = map(PostId.model_validate, result.scalars())
        return posts
        

@router.get('/{post_id}', response_model=PostId, responses={404: {"description": "Post not found"}})
async def get_post(post_id: int, user = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).options(selectinload(Post.author), selectinload(Post.likes)).where(Post.id == post_id)
        result = await db.execute(stmt)
        result = result.scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Post not found")
        post = PostId.model_validate(result)
        return post


@router.post('/', response_model=PostId)
async def create_post(post: PostSchema, user: UserSchema = Depends(check_token)):
    async with await Database.get_class_session() as db:
        post = Post(**post.model_dump())
        post.author_id = user.id
        db.add(post)
        await db.commit()
        await db.refresh(post, attribute_names=["author", "likes"])
        return PostId.model_validate(post)
    

@router.put('/{post_id}', response_model=PostId, responses={404: {"description": "Post not found"}})
async def update_post(post_id: int, post: PostSchema, user: UserSchema = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).options(selectinload(Post.author), selectinload(Post.likes)).where(Post.id == post_id)
        result = await db.execute(stmt)
        post_from_db = result.scalars().first()
        if not post_from_db:
            raise HTTPException(status_code=404, detail="Post not found")
        if post_from_db.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this post")
        for key, value in post.model_dump().items():
            setattr(post_from_db, key, value)
        await db.commit()
        await db.refresh(post_from_db)
        return PostId.model_validate(post_from_db)
    

@router.delete('/{post_id}', status_code=204, responses={404: {"description": "Post not found"}, 
                                                         403: {"description": "You are not the author of this post"}})
async def delete_post(post_id: int, user: UserSchema = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(stmt)
        post_from_db = result.scalars().first()
        if not post_from_db:
            raise HTTPException(status_code=404, detail="Post not found")
        if post_from_db.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the author of this post")
        await db.delete(post_from_db)
        await db.commit()
        return None
    

@router.post('/{post_id}/{like_type}', response_model=PostId, responses={404: {"description": "Post not found"}})
async def like_post(post_id: int, like_type: LikeType, user: UserSchema = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).options(selectinload(Post.author), selectinload(Post.likes)).where(Post.id == post_id)
        result = await db.execute(stmt)
        post_from_db = result.scalars().first()
        if not post_from_db:
            raise HTTPException(status_code=404, detail="Post not found")
        if post_from_db.author_id == user.id:
            raise HTTPException(status_code=400, detail="You can't react to your own post")
        like = next((like for like in post_from_db.likes if like.user_id == user.id), None)
        if like and like.like_type == like_type:
            raise HTTPException(status_code=400, detail="You already have reacted to this post with this type of reaction")
        if like:
            like.like_type = like_type
        else:
            like = Like(post_id=post_id, user_id=user.id, like_type=like_type.value)
            db.add(like)
        await db.commit()
        await db.refresh(post_from_db)
        return PostId.model_validate(post_from_db)
    

@router.delete('/{post_id}/', response_model=PostId, responses={404: {"description": "Post not found"}})
async def unlike_post(post_id: int, user: UserSchema = Depends(check_token)):
    async with await Database.get_class_session() as db:
        stmt = select(Post).options(selectinload(Post.author), selectinload(Post.likes)).where(Post.id == post_id)
        result = await db.execute(stmt)
        post_from_db = result.scalars().first()
        if not post_from_db:
            raise HTTPException(status_code=404, detail="Post not found")
        if post_from_db.author_id == user.id:
            raise HTTPException(status_code=400, detail="You can't react to your own post")
        like = next((like for like in post_from_db.likes if like.user_id == user.id), None)
        if not like:
            raise HTTPException(status_code=400, detail="You have not reacted to this post yet")
        await db.delete(like)
        await db.commit()
        await db.refresh(post_from_db)
        return PostId.model_validate(post_from_db)