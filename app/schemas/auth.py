from pydantic import BaseModel, EmailStr, constr

class RegisterIn(BaseModel):
    email: EmailStr
    password: constr(min_length=12) # pyright: ignore[reportInvalidTypeForm]
    name: constr(min_length=1, max_length=100) # pyright: ignore[reportInvalidTypeForm]


class RegisterOut(BaseModel):
    id: int
    email: EmailStr
    name: str