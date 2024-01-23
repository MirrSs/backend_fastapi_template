from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.mixins.base_mixin import TableType
from managers.crud_manager import CRUDManager
from models.post_model import Post
from schemas.post_schema import CreatePostSchema, PatchPostSchema


class PostManager(CRUDManager):
    table = Post
    create_scheme = CreatePostSchema
    update_scheme = PatchPostSchema

    @classmethod
    async def create(
            cls,
            input_data: CreatePostSchema,
            session: AsyncSession,
            user
    ) -> TableType:
        data = input_data.model_copy(update={'user_id':user.id})
        return await super().create(data, session)

