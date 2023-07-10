from fastapi import Depends, APIRouter
from sqlalchemy import update, select

from account.models import UserModel
from account.schema import UserUpdateSchema
from app.models import Book
from db.database import AsyncSession, get_db
from account.views import get_current_user

router = APIRouter()


@router.get("/profile/")
async def get_profile(user: UserModel = Depends(get_current_user)):
    return user


@router.patch("/profile/")
async def update_profile(
        data: UserUpdateSchema,
        user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.get("/mybooks/")
async def get_mybooks(
        user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    query = select(Book).where(Book.user_id == user.id)
    books = await db.execute(query)

    return books.scalars().all()
