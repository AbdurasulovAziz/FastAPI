import hashlib

from fastapi import Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from account.models import UserModel
from auth.schema import UserLoginSchema
from auth.token import create_token
from db.database import SessionLocal, get_db


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')

    hash_object = hashlib.sha256(password_bytes)

    hashed_password = hash_object.hexdigest()

    return hashed_password


def get_user(email:EmailStr, db: SessionLocal):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


def authenticate_user(user: UserModel, password: str):

    if user.password != hash_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неправильное имя пользователя или пароль')

    access_token = create_token(user.email)

    return access_token
