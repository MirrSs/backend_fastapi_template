from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class GetByEmailSchema(BaseModel):
    email: str


class PatchUserSchema(BaseModel):
    name: str | None = None
    email: str | None = None
