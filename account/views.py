from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import decode, PyJWTError

from account.models import UserModel
from auth.token import security, SECRET_KEY
from db.database import get_db, SessionLocal


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(security),
        db: SessionLocal = Depends(get_db)
):
    try:
        payload = decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        user = db.query(UserModel).filter(UserModel.email == email).first()

        return user

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
