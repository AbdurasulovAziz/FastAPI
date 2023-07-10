import datetime

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from account.models import UserModel
from account.views import get_current_user
from app.models import Book
from app.schema import BookSchema, BookUpdateSchema
from db.database import get_db

router = APIRouter(prefix='/books')


@router.get("/")
async def get_books(
        title: str | None = None,
        author_name: str | None = None,
        db: AsyncSession = Depends(get_db)):

    query = select(Book)

    if title:
        query = query.where(Book.title == title)

    if author_name:
        query = query.join(Book.user).where(
            UserModel.first_name == author_name
        )

    books = await db.execute(query)

    return books.scalars().all()


@router.post("/")
async def create_book(book: BookSchema,
                      user: UserModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    try:
        new_book = Book(
            title=book.title,
            description=book.description,
            date=datetime.date.today(),
            user_id=user.id
        )  # Лучше самому брать user_id из request или запрашивать у фронта
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    except IntegrityError:
        raise HTTPException(status_code=404, detail="User with this id not found")


@router.patch("/{book_id}")
async def patch_book(
        book_id: int,
        book: BookUpdateSchema,
        user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    book_data = (await db.execute(select(Book).where(Book.id == book_id))).scalars().first()

    if not book_data:
        raise HTTPException(status_code=404, detail="Item not found")

    if book_data.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission")

    update_data = book.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book_data, key, value)

    await db.commit()
    await db.refresh(book_data)

    return book_data


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), user: UserModel = Depends(get_current_user)):

    book = (await db.execute(select(Book).where(Book.id == book_id))).scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Item not found")

    if book.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission")

    await db.delete(book)
    await db.commit()

    return {'Result': 'Successfully deleted'}
