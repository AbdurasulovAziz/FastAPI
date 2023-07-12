import hashlib

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from starlette import status

from app.account.models import User
from app.auth.token import create_token
from core.db import AsyncSession


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    hash_object = hashlib.sha256(password_bytes)

    hashed_password = hash_object.hexdigest()

    return hashed_password


def check_authentication_data(user: User, password: str):

    if user.password != hash_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильное имя пользователя или пароль")

    access_token = create_token(user.email)

    return access_token
