from pydantic import EmailStr, BaseModel


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    second_name: str | None = None

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: EmailStr
    exp: int
