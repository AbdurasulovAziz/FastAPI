from httpx import AsyncClient
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import User
from app.library.models import Book


class TestLibraryRoutes:
    async def test_get_books(self, ac: AsyncClient, session: AsyncSession):
        request = await ac.get(url="/books/")

        query = select(Book)

        book_list = (await session.execute(query)).scalars().all()
        book_data = [book._to_dict() for book in book_list]

        assert request.status_code == 200
        assert book_data == request.json()

    async def test_get_books_with_author_name_filter(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        request = await ac.get(
            url="/books/", params={"author_name": test_user_data["first_name"]}
        )

        query = (
            select(Book)
            .join(User)
            .where(User.first_name == test_user_data["first_name"])
        )
        book_list = (await session.execute(query)).scalars().all()

        book_data = [book._to_dict() for book in book_list]

        assert request.status_code == 200
        assert book_data == request.json()

    async def test_get_books_with_title_filter(
        self, ac: AsyncClient, session: AsyncSession
    ):
        request = await ac.get(url="/books/", params={"title": "testtitle"})

        query = select(Book).where(Book.title == "testtitle")

        book_list = (await session.execute(query)).scalars().all()
        book_data = [book._to_dict() for book in book_list]

        assert request.status_code == 200
        assert book_data == request.json()

    async def test_get_books_with_title_and_author_name_filter(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        request = await ac.get(
            url="/books/",
            params={"title": "testtitle", "author_name": test_user_data["first_name"]},
        )

        query = (
            select(Book)
            .join(User)
            .where(User.first_name == test_user_data["first_name"])
            .where(Book.title == "testtitle")
        )

        book_list = (await session.execute(query)).scalars().all()
        book_data = [book._to_dict() for book in book_list]

        assert request.status_code == 200
        assert book_data == request.json()

    async def test_create_book(
        self, session: AsyncSession, ac: AsyncClient, test_user_data: dict
    ):
        request_body = {
            "title": "created book title",
            "description": "created book description",
        }

        request = await ac.post(
            url="/books/",
            json=request_body,
            headers={"Authorization": test_user_data["token"]},
        )

        query = select(Book).where(Book.title == "created book title")
        book = (await session.execute(query)).scalars().first()

        assert request.status_code == 201
        assert book._to_dict() == request.json()

        await session.delete(book)
        await session.commit()

    async def test_patch_book(
        self, session: AsyncSession, ac: AsyncClient, fill_db, test_user_data: dict
    ):
        query = select(Book).join(User).where(User.email == test_user_data["email"])
        book = (await session.execute(query)).scalars().first()

        previous_book = Book(**book._to_dict())

        request = await ac.patch(
            url=f"/books/{book.id}",
            headers={"Authorization": test_user_data["token"]},
            json={"title": "new book title", "description": "new book description"},
        )

        await session.refresh(book)

        assert previous_book != book._to_dict()
        assert request.status_code == 200
        assert book._to_dict() == request.json()

    async def test_delete_book(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        query = select(Book).where(Book.title == "testtitle")
        book = (await session.execute(query)).scalars().first()

        request = await ac.delete(
            url=f"/books/{book.id}", headers={"Authorization": test_user_data["token"]}
        )

        is_exists = await session.execute(
            select(exists().where(Book.title == "testtitle"))
        )

        assert request.status_code == 200
        assert is_exists.scalars().first() is False
        assert request.json() == {"Result": "Successfully deleted"}
