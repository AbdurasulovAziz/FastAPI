from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import decode, PyJWTError
from sqlalchemy import select

from account.models import UserModel
from auth.token import security
from config import settings
from db.database import get_db, AsyncSession


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
):
    try:
        payload = decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        query = select(UserModel).where(UserModel.email == email)

        user = await db.execute(query)

        return user.scalars().first()

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
