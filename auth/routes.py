from fastapi import APIRouter, Depends, HTTPException

from account.models import UserModel
from auth.schema import UserLoginSchema, UserRegistrationSchema
from auth.views import hash_password, authenticate_user, get_user
from db.database import AsyncSession, get_db

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(data: UserLoginSchema, db: AsyncSession = Depends(get_db)):

    user = await get_user(data.email, db)

    token = authenticate_user(user, data.password)

    return token


@router.post("/registration")
async def registration(user: UserRegistrationSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_user = UserModel(**user.dict())
        password = hash_password(new_user.password)

        new_user.password = password

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except Exception:
        raise HTTPException(status_code=409, detail="User exists")

