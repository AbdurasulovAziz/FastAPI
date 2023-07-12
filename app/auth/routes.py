from fastapi import APIRouter, Depends, HTTPException

from app.account.models import User
from app.account.services import UserService
from app.auth.schema import UserLoginSchema, UserRegistrationSchema
from app.auth.services import AuthService
from app.auth.views import hash_password, check_authentication_data
from core.db import AsyncSession, get_db

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(user_data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    return await AuthService(user_data, db).authenticate_user()


@router.post("/registration")
async def registration(user_data: UserRegistrationSchema, db: AsyncSession = Depends(get_db)):
    return await AuthService(user_data, db).registrate_user()

