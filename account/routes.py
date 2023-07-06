from fastapi import Depends, APIRouter

from account.models import UserModel
from account.schema import UserUpdateSchema
from app.models import BookModel
from db.database import SessionLocal, get_db
from account.views import get_current_user

router = APIRouter()


@router.get("/profile/")
async def get_profile(user: UserModel = Depends(get_current_user)):
    return user


@router.patch("/profile/")
async def update_profile(
        data: UserUpdateSchema,
        user: UserModel = Depends(get_current_user),
        db: SessionLocal = Depends(get_db)
):

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@router.get("/mybooks/")
async def get_mybooks(user: UserModel = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    return db.query(BookModel).filter(BookModel.user_id == user.id).all()



