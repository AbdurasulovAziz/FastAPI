import datetime

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError

from account.models import UserModel
from account.views import get_current_user
from app.models import BookModel
from app.schema import BookSchema, BookUpdateSchema
from db.database import SessionLocal, get_db

router = APIRouter()


@router.get("/books/")
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


@router.post("/books/")
async def create_book(book: BookSchema,
                      user: UserModel = Depends(get_current_user),
                      db: SessionLocal = Depends(get_db)):
    try:
        new_book = BookModel(**book.dict())     # Мне кажется хреново раскрываю book
        new_book.date = datetime.date.today()
        new_book.user_id = user.id              #Лучше самому брать user_id из request или запрашивать у фронта
        db.add(new_book)
        db.commit()
        return book
    except IntegrityError:
        raise HTTPException(status_code=404, detail="User with this id not found")


@router.patch("/books/{book_id}")
async def patch_book(
        book_id: int,
        book: BookUpdateSchema,
        user: UserModel = Depends(get_current_user),
        db: SessionLocal = Depends(get_db)
):

    book_data = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book_data:
        raise HTTPException(status_code=404, detail="Item not found")

    if book_data.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission")

    update_data = book.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book_data, key, value)

    db.commit()
    db.refresh(book_data)

    return book_data


@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: SessionLocal = Depends(get_db), user: UserModel = Depends(get_current_user)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if book.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission")

    if not book:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(book)
    db.commit()

    return {'Result': 'Successfully deleted'}
