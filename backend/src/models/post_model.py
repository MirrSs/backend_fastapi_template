import sqlalchemy
from models.base_model import BaseModel
from sqlalchemy.orm import relationship

class Post(BaseModel):
    __tablename__ = 'posts'
    
    text = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )

    user = relationship("User", backref="post_user", lazy="joined")


    def __str__(self):
        return self.text
