from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.account.models import User
from app.auth.views import hash_password


class TestAuthRoutes:
    async def test_registration(self, session: AsyncSession, ac: AsyncClient):
        request_data = {
            "email": "testuseremail@gmail.com",
            "password": "testuserpassword",
            "first_name": "test_first_name",
            "second_name": "test_second_name",
        }

        response = await ac.post(url="/auth/registration", json=request_data)

        query = select(User).where(User.email == request_data["email"])

        user = (await session.execute(query)).scalars().first()
        user._to_dict()["password"] = hash_password(request_data["password"])

        assert user is not None, "Пользователь не был создан"
        assert response.status_code == 201, "Статус код не равен 201"
        assert user._to_dict() == response.json(), "Данные не сходятся"

    async def test_login(
        self, session: AsyncSession, ac: AsyncClient, fill_db, test_user_data: dict
    ):
        response = await ac.post(
            url="/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )

        assert response.status_code == 200
        assert response.json().get("token") is not None
