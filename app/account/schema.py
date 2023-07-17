from pydantic import BaseModel


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    second_name: str | None = None

    class Config:
        orm_mode = True
