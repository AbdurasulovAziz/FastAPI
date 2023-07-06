from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class BookUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None


