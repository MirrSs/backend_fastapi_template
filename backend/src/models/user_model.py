import sqlalchemy
from db import db
from sqlalchemy.orm import relationship
from passlib import hash
from services.minio_service import MinioService

class User(db.Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    profile_picture_url = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    
    @property
    def get_image(self):
        if self.image:
            return MinioService.create_presigned_url(self.profile_picture_url)
        return ''

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)
