from fastapi import FastAPI, Depends, APIRouter

from account.models import UserModel
from auth.token import create_token
from db.database import SessionLocal, get_db
from account.views import get_current_user

router = APIRouter()


@router.get('/profile/')
async def get_profile(db: SessionLocal = Depends(get_db), user: dict = Depends(get_current_user)):
    result = db.query(UserModel).all()
    return result

# @account.get("/author/")
# async def get_user_by_name(name: str, db: SessionLocal = Depends(get_db)):
#     authors = db.query(UserModel).filter(UserModel.email == name).first()
#     return authors
#
#

