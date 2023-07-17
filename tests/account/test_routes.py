from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import User
from app.library.models import Book


class TestAccountRoutes:
    async def test_get_profile(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        request = await ac.get(
            url="/account/profile", headers={"Authorization": test_user_data["token"]}
        )

        query = select(User).where(User.email == test_user_data["email"])

        user = (await session.execute(query)).scalars().first()

        assert request.status_code == 200
        assert request.json() == user._to_dict()

    async def test_update_profile(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        query = select(User).where(User.email == test_user_data["email"])

        user_instance = (await session.execute(query)).scalars().first()

        previous_user = User(**user_instance._to_dict())

        request = await ac.patch(
            url="/account/profile",
            headers={"Authorization": test_user_data["token"]},
            json={
                "first_name": "changed_test_name",
                "second_name": "changed_test_surname",
            },
        )

        await session.refresh(user_instance)

        assert request.status_code == 200
        assert previous_user != (user_instance._to_dict())
        assert request.json() == user_instance._to_dict()

    async def test_get_mybooks(
        self, ac: AsyncClient, session: AsyncSession, test_user_data: dict
    ):
        request = await ac.get(
            url="/account/mybooks", headers={"Authorization": test_user_data["token"]}
        )

        query = select(Book).join(User).where(User.email == test_user_data["email"])

        books = (await session.execute(query)).scalars().all()

        user_books = [book._to_dict() for book in books]

        assert request.status_code == 200
        assert request.json() == user_books
