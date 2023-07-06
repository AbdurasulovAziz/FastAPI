from pydantic import BaseModel, EmailStr


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
