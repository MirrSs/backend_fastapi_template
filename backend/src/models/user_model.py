import sqlalchemy
from models.base_model import BaseModel
from passlib import hash
from services.minio_service import MinioService

class User(BaseModel):
    __tablename__ = 'users'
    
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    profile_picture_url = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    
    @property
    def get_image(self):
        if self.image:
            return MinioService.create_presigned_url(self.profile_picture_url)
        return ''

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)
    
    def __str__(self):
        return self.email
