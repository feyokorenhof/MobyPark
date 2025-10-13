from pydantic import BaseModel, EmailStr, constr


class RegisterIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # pyright: ignore[reportInvalidTypeForm]
    name: constr(min_length=1, max_length=100)  # pyright: ignore[reportInvalidTypeForm]


class RegisterOut(BaseModel):
    id: int
    email: EmailStr
    name: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    model_config = {"from_attributes": True}
