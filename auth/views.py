import hashlib

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from starlette import status

from account.models import UserModel
from auth.token import create_token
from db.database import AsyncSession


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    hash_object = hashlib.sha256(password_bytes)

    hashed_password = hash_object.hexdigest()

    return hashed_password


async def get_user(email: EmailStr, db: AsyncSession):
    query = select(UserModel).where(UserModel.email == email)

    user = await db.execute(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.scalars().first()


def authenticate_user(user: UserModel, password: str):

    if user.password != hash_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильное имя пользователя или пароль")

    access_token = create_token(user.email)

    return access_token
