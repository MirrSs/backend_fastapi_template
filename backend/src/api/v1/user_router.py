from fastapi import APIRouter, Depends, status, File, UploadFile
from db.db import get_session
from typing import Annotated
from schemas.user_schema import (
    CreateUserSchema,
    GetUserSchema,
    GetByEmailSchema,
    PatchUserSchema,
    CreateUserOutputSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from managers.user_manager import UserManager
from services.auth_service import AuthService
from exceptions.exception import BadRequestError, ObjectNotFoundError
from models.user_model import User
from fastapi.exceptions import ResponseValidationError

user_router = APIRouter(tags=["users"])


@user_router.get(
    "/users/mine/", 
    response_model=GetUserSchema, 
    status_code=status.HTTP_200_OK
)
async def get_current_user(
    user=Depends(AuthService.get_current_user)
):
    return user


@user_router.get(
    "/users/", 
    status_code=status.HTTP_200_OK
)
async def get_user_by_email(
    email: GetByEmailSchema,
    session: AsyncSession = Depends(get_session)
) -> GetUserSchema:
    return await UserManager.get_by_email(email=email.email, session=session)


@user_router.get(
    "/users/{user_id}/", 
    response_model=GetUserSchema, 
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> GetUserSchema:
    return await UserManager.get_by_id(user_id=user_id, session=session)


@user_router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserOutputSchema,
)
async def register_user(
    user: CreateUserSchema, session: AsyncSession = Depends(get_session)
) -> CreateUserOutputSchema:
    try:
        user_db = await UserManager.get_by_email(email=user.email, session=session)
        if user_db:
            raise BadRequestError(detail="User with such email exists")
    except ObjectNotFoundError:
        response = await UserManager.create(data=user, session=session)
        return response


@user_router.patch(
    "/users/", 
    response_model=GetUserSchema, 
    status_code=status.HTTP_200_OK
)
async def update_user(
    data: PatchUserSchema,
    user: User = Depends(AuthService.get_current_user),
    session: AsyncSession = Depends(get_session),
) -> GetUserSchema:
    return await UserManager.update(
        user_id=user.id, name=data.name, email=data.email, session=session
    )


@user_router.patch(
    "/users/image/", 
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
    "/users/", 
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user: User = Depends(AuthService.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await UserManager.delete_user(user_id=user.id, session=session)
