from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.token import decode_token
from app.library.schema import BookCreationSchema, BookUpdateSchema
from app.library.services import LibraryService
from core.db import get_db

router = APIRouter(prefix="/books")


@router.get("/")
async def get_books(
    title: str | None = None,
    author_name: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await LibraryService(db).get_all_books(title, author_name)


@router.post("/", status_code=201)
async def create_book(
    book: BookCreationSchema,
    token_payload: dict = Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    return await LibraryService(db, token_payload).create_new_book(
        book.dict(exclude_unset=True)
    )


@router.patch("/{book_id}")
async def patch_book(
    book_id: int,
    book: BookUpdateSchema,
    token_payload: dict = Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    return await LibraryService(db, token_payload).update_book(
        book_id, book.dict(exclude_unset=True)
    )


@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    token_payload: dict = Depends(decode_token),
):
    return await LibraryService(db, token_payload).remove_book(book_id)
