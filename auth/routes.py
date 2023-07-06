from fastapi import APIRouter, Depends, HTTPException

from account.models import UserModel
from auth.schema import UserLoginSchema, UserRegistrationSchema
from auth.views import hash_password, authenticate_user, get_user
from db.database import SessionLocal, get_db

router = APIRouter()


@router.post("/auth/login/")
async def login(data: UserLoginSchema, db: SessionLocal = Depends(get_db)):

    user = get_user(data.email, db)

    token = authenticate_user(user, data.password)

    return token


@router.post("/auth/registration/")
async def registration(user: UserRegistrationSchema, db: SessionLocal = Depends(get_db)):
    try:
        new_user = UserModel(**user.dict())
        password = hash_password(new_user.password)

        new_user.password = password

        db.add(new_user)
        db.commit()

        return new_user
    except Exception:
        raise HTTPException(status_code=409, detail="User exists")

