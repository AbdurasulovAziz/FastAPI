from fastapi import APIRouter, Depends

from app.auth.schema import UserLoginSchema, UserRegistrationSchema
from app.auth.services import AuthService
from core.db import AsyncSession, get_db

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(user_data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    return await AuthService(user_data, db).authenticate_user()


@router.post("/registration", status_code=201)
async def registration(
    user_data: UserRegistrationSchema, db: AsyncSession = Depends(get_db)
):
    return await AuthService(user_data, db).registrate_user()
