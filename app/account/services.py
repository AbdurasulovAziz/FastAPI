from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import decode, PyJWTError
from pydantic import EmailStr
from sqlalchemy import select

from app.account.models import User
from app.account.schema import UserUpdateSchema
from app.auth.token import security, decode_token
from app.library.models import Book
from core.config import settings
from core.db import get_db, AsyncSession


class UserService:

    def __init__(self, token_payload: dict, db: AsyncSession):

        self.email = token_payload.get('email')
        self.db = db

    async def get_current_user(self):

        query = select(User).where(User.email == self.email)

        user = await self.db.execute(query)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user.scalars().first()

    async def update_current_user(self, data: dict):

        user = await self.db.merge(User(email=self.email, **data))

        return user

    async def get_user_books(self):

        query = select(Book).join(Book.user).where(User.email == self.email)

        books = await self.db.execute(query)

        return books.scalars().all()


