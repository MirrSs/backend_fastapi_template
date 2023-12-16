from typing import List, Optional
from sqlalchemy import update, delete
from sqlalchemy.future import select
from exceptions.exception import ObjectNotFoundError
from models.user_model import User
from passlib import hash
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.user_schema import CreateUserSchema


class UserManager:
    @classmethod
    async def create(cls, data: CreateUserSchema, session: AsyncSession):
        password = hash.bcrypt.hash(data.password)
        user = User(name=data.name, email=data.email, hashed_password=password)
        session.add(user)
        await session.commit()
        return user

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[User]:
        q = await session.execute(select(User))
        result = q.scalars().all()
        if not result:
            raise ObjectNotFoundError(detail="Users not found")
        return result

    @classmethod
    async def get_by_email(cls, email: Optional[str], session: AsyncSession) -> User:
        q = await session.execute(select(User).where(User.email == email))
        result = q.scalar_one_or_none()
        if not result:
            raise ObjectNotFoundError(detail="User not found")
        return result

    @classmethod
    async def update(
        cls,
        user_id: int,
        name: Optional[str],
        email: Optional[str],
        session: AsyncSession,
    ):
        q = update(User).where(User.id == user_id)
        if name:
            q = q.values(name=name)
        if email:
            q = q.values(email=email)
        q.execution_options(synchronize_session="fetch")
        await session.execute(q)
        await session.commit()
        q = await session.execute(select(User).where(User.id == user_id))
        result = q.scalar_one_or_none()
        if not result:
            raise ObjectNotFoundError(detail="User not found")
        return result

    @classmethod
    async def get_by_id(cls, user_id: int, session: AsyncSession):
        q = await session.execute(select(User).where(User.id == user_id))
        result = q.scalar_one_or_none()
        if not result:
            raise ObjectNotFoundError(detail="User not found")
        return result

    @classmethod
    async def delete_user(cls, user_id, session: AsyncSession):
        q = await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
        return {"detail": f"User: {user_id} deleted"}
