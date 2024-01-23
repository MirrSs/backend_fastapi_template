from pydantic import BaseModel
from datetime import datetime
from schemas.user_schema import GetUserSchema

class CreatePostSchema(BaseModel):
    title: str
    text: str

    class Config:
        from_attributes = True


class GetPostSchema(BaseModel):
    id: int
    title: str
    text: str

    user: GetUserSchema

    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

        
class PatchPostSchema(BaseModel):
    title: str | None = None
    text: str | None = None
    