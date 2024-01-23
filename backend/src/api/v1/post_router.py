from fastapi import APIRouter, Depends, status, File, UploadFile
from db.db import get_session
from schemas.post_schema import (
    CreatePostSchema,
    GetPostSchema,
    PatchPostSchema
)
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from managers.post_manager import PostManager
from services.auth_service import AuthService
from models.post_model import Post


post_router = APIRouter(tags=["posts"])


@post_router.get('/posts/mine/', response_model=List[GetPostSchema])
async def get_current_user_posts(
        user=Depends(AuthService.get_current_user),
        session: AsyncSession = Depends(get_session)
) -> List[GetPostSchema]:
    return await PostManager.list(filter_by={'user_id':user.id}, session=session)


@post_router.get('/posts/{post_id}/', response_model=GetPostSchema)
async def get_post(
        post_id: int, session: AsyncSession = Depends(get_session)
) -> GetPostSchema:
    return await PostManager.retrieve(id=post_id, session=session)


@post_router.post('/posts/', response_model=GetPostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
        post: CreatePostSchema,
        session: AsyncSession = Depends(get_session),
        user=Depends(AuthService.get_current_user)
) -> GetPostSchema:
    return await PostManager.create(input_data=post, session=session, user=user)



@post_router.patch('/posts/{post_id}/', response_model=PatchPostSchema)
async def update_post(
        post_id: int,
        data: PatchPostSchema,
        user=Depends(AuthService.get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await PostManager.update(
        session=session, pk=post_id, input_data=data.model_dump(exclude_unset=True)
    )
