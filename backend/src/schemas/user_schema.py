from pydantic import BaseModel, validator
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
    class Config:
        from_attributes = True


class GetUserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    profile_picture_url: str

    @validator('profile_picture_url', always=True)
    def presigned_url(cls, value, values: dict):
        if value != '' or value is not None:
            return MinioService.create_presigned_url(value)
        
    class Config:
        from_attributes = True


class GetByEmailSchema(BaseModel):
    email: str


class PatchUserSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
