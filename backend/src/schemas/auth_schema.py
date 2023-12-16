from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

auth_schema = OAuth2PasswordBearer(
    tokenUrl='token',
)


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str
