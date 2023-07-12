from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import User
from app.account.services import UserService
from app.library.models import Book


class LibraryService:

    def __init__(self, db: AsyncSession, token_payload: dict | None = None):
        self.token_payload = token_payload
        self.db = db

    async def get_book(self, book_id):

        query = select(Book).where(Book.id == book_id)

        book = await self.db.execute(query)

        return book.scalars().first()

    async def get_all_books(self,
                            title: str | None = None,
                            author_name: str | None = None):

        query = select(Book)

        if title:
            query = query.where(Book.title == title)

        if author_name:
            query = query.join(Book.user).where(
                User.first_name == author_name
            )

        books = await self.db.execute(query)

        return books.scalars().all()

    async def create_new_book(self, book_data):

        user = await UserService(self.token_payload, self.db).get_current_user()

        try:
            new_book = Book(
                title=book_data.get('title'),
                description=book_data.get('description'),
                create_date=datetime.utcnow(),
                user_id=user.id
            )

            self.db.add(new_book)

            await self.db.commit()
            await self.db.refresh(new_book)

            return new_book

        except IntegrityError:
            raise HTTPException(status_code=404, detail="User with this id not found")

    async def update_book(self, book_id: int, book_data: dict):

        book_instance = await self.get_book(book_id)

        user = await UserService(self.token_payload, self.db).get_current_user()

        if not book_instance:
            raise HTTPException(status_code=404, detail="Item not found")

        if book_instance.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission")

        for key, value in book_data.items():
            setattr(book_instance, key, value)

        await self.db.commit()
        await self.db.refresh(book_instance)

        return book_instance

    async def remove_book(self, book_id: int):

        user = await UserService(self.token_payload, self.db).get_current_user()

        book_instance = await self.get_book(book_id)

        if not book_instance:
            raise HTTPException(status_code=404, detail="Item not found")

        if book_instance.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission")

        await self.db.delete(book_instance)
        await self.db.commit()

        return {'Result': 'Successfully deleted'}
