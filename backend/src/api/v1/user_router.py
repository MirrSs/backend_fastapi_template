from fastapi import APIRouter, Depends, status, File, UploadFile
from db.db import get_session
from typing import Annotated
from schemas.user_schema import (
    CreateUserSchema,
    GetUserSchema,
    PatchUserSchema,
    CreateUserOutputSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from managers.user_manager import UserManager
from services.auth_service import AuthService
from exceptions.exception import BadRequestError, ObjectNotFoundError
from models.user_model import User

user_router = APIRouter(tags=["users"])


@user_router.get('/users/mine/', response_model=GetUserSchema)
async def get_current_user(
        user=Depends(AuthService.get_current_user),
        session: AsyncSession = Depends(get_session)
) -> GetUserSchema:
    return await UserManager.retrieve(id=user.id, session=session)


@user_router.get('/users/{user_id}/', response_model=GetUserSchema)
async def get_user(
        user_id: int, session: AsyncSession = Depends(get_session)
) -> GetUserSchema:
    return await UserManager.retrieve(id=user_id, session=session)


@user_router.post('/users/', response_model=CreateUserOutputSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: CreateUserSchema, session: AsyncSession = Depends(get_session)
) -> CreateUserOutputSchema:
    try:
        user_db = await UserManager.retrieve(email=user.email, session=session)

        if user_db:
            raise BadRequestError(detail='User with such email exists')

    except ObjectNotFoundError:
        response = await UserManager.create(input_data=user, session=session)
        return response


@user_router.patch('/users/mine/', response_model=GetUserSchema)
async def update_info_about_current_user(
        user_info: PatchUserSchema,
        user=Depends(AuthService.get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await UserManager.update(
        session=session, pk=user.id, input_data=user_info.model_dump(exclude_unset=True)
    )


@user_router.patch(
    "/users/mine/image/", 
    status_code=status.HTTP_200_OK
)
async def update_user_profile_image(
    file: Annotated[UploadFile, File(description="Multiple files as UploadFile")],
    user: User = Depends(AuthService.get_current_user),
    session: AsyncSession = Depends(get_session),
) -> GetUserSchema:
    return await UserManager.update_profile_image(
        user_id=user.id, image=file, session=session
    )


@user_router.delete(
    "/users/mine/", 
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user: User = Depends(AuthService.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await UserManager.delete(id=user.id, session=session)
