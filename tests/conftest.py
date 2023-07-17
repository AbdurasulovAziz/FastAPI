import asyncio
import datetime
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.account.models import User
from app.auth.token import create_token
from app.auth.views import hash_password
from app.library.models import Book
from core.config import settings
from core.db import Base, get_db
from main import app

DATABASE_URL_TEST = settings.DATABASE_URL_TEST

engine_test = create_async_engine(DATABASE_URL_TEST)

async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

Base.metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a new session to test database"""

    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    """Create tables at the start of tests and drop at the end"""

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user_data():
    data = {
        "email": "testemail@gmail.com",
        "token": f"Bearer {create_token('testemail@gmail.com')}",
        "password": "testpassword",
        "hashed_password": hash_password("testpassword"),
        "first_name": "testname",
        "second_name": "testsurname",
    }

    return data


@pytest.fixture(autouse=True, scope="function")
async def fill_db():
    async with async_session_maker() as session:
        user_instance = User(
            email="testemail@gmail.com",
            password=hash_password("testpassword"),
            first_name="testname",
            second_name="testsurname",
        )

        session.add(user_instance)
        await session.commit()

        book_instance = Book(  # TODO нужно ли разделять на разные фикстуры
            title="testtitle",
            description="testdescription",
            create_date=datetime.datetime.utcnow(),
            user_id=user_instance.id,
        )

        session.add(book_instance)
        await session.commit()

        yield

        await session.delete(book_instance)
        await session.delete(user_instance)
        await session.commit()


@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session
