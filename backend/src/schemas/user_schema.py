from pydantic import BaseModel, field_validator
from services.minio_service import MinioService

class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class CreateUserOutputSchema(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    is_active: bool
    is_banned: bool
    class Config:
        from_attributes = True


class GetUserSchema(BaseModel):
    id: int
    name: str
    email: str
    
    is_admin: bool
    is_active: bool
    is_banned: bool

    profile_picture_url: str | None

    @field_validator('profile_picture_url')
    @classmethod
    def presigned_url(cls, v):
        if v != None:
            return MinioService.create_presigned_url(v)
        return ''
    class Config:
        from_attributes = True
        

class PatchUserSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    profile_image_url: str | None = None
