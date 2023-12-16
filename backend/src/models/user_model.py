import sqlalchemy
from db import db
from sqlalchemy.orm import relationship
from passlib import hash


class User(db.Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)
