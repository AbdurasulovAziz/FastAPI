from fastapi import Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import update, select

from app.account.models import User
from app.account.schema import UserUpdateSchema
from app.auth.token import security, decode_token
from app.library.models import Book
from core.db import AsyncSession, get_db
from app.account.services import UserService

router = APIRouter(prefix='/account')


@router.get("/profile")
async def get_profile(token_payload: dict = Depends(decode_token), db: AsyncSession = Depends(get_db)):
    return await UserService(token_payload, db).get_current_user()


@router.patch("/profile")
async def update_profile(
        data: UserUpdateSchema,
        token_payload: dict = Depends(decode_token),
        db: AsyncSession = Depends(get_db)
):
    return await UserService(token_payload, db).update_current_user(data.dict(exclude_unset=True))


@router.get("/mybooks")
async def get_mybooks(
        token_payload: dict = Depends(decode_token),
        db: AsyncSession = Depends(get_db)):

    return await UserService(token_payload, db).get_user_books()
