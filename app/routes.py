import datetime

from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError

from account.models import UserModel
from account.views import get_current_user
from app.models import BookModel
from app.schema import BookSchema, BookUpdateSchema
from db.database import SessionLocal, get_db

router = APIRouter()


@router.get('/books/')
async def get_books(
        title: str | None = None,
        author_name: str | None = None,
        db: SessionLocal = Depends(get_db)
):
    if not title and not author_name:
        books = db.query(BookModel).all()
    else:
        query = db.query(BookModel)
        if title:
            query = query.filter(BookModel.title == title)
        if author_name:
            query = query.join(BookModel.user).filter(
                UserModel.first_name == author_name
            )
        books = query.all()

    return books


@router.post('/books/')
async def create_book(book: BookSchema, db: SessionLocal = Depends(get_db)):
    try:
        new_book = BookModel(**book.dict())
        new_book.date = datetime.date.today()
        db.add(new_book)
        db.commit()
        return book
    except IntegrityError:
        raise HTTPException(status_code=404, detail='User with this id not found')


@router.patch('/books/{book_id}')
async def patch_book(book_id: int, book: BookUpdateSchema, db: SessionLocal = Depends(get_db)):

    book_data = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book_data:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = book.dict(exclude_unset=True)
    db.query(BookModel).filter(BookModel.id == book_id).update(update_data)

    return {"message": "Item updated successfully"}


@router.delete('/books/{book_id}')
async def delete_book( book_id: int, db: SessionLocal = Depends(get_db), user: dict = Depends(get_current_user)):
    book = db.query(BookModel).filter(BookModel.id == book_id)

    if user.get(id) != book.user_id:
        raise HTTPException(status_code=403, detail="You don't have permission")

    if not book:
        raise HTTPException(status_code=404, detail="Item not found")

    book.delete()
    return book




