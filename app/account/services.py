from fastapi import HTTPException
from sqlalchemy import select, update

from app.account.models import User
from app.library.models import Book
from core.db import AsyncSession


class UserService:
    def __init__(self, token_payload: dict, db: AsyncSession):
        self.email = token_payload.get("email")
        self.db = db

    async def get_current_user(self):
        query = select(User).where(User.email == self.email)

        user = await self.db.execute(query)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user.scalars().first()

    async def update_current_user(self, data: dict):
        query = (
            update(User).where(User.email == self.email).values(**data).returning(User)
        )
        user = (await self.db.execute(query)).scalars().first()
        await self.db.commit()
        return user

    async def get_user_books(self):
        query = select(Book).join(Book.user).where(User.email == self.email)

        books = await self.db.execute(query)

        return books.scalars().all()
