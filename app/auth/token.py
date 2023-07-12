from datetime import datetime, timedelta
import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, PyJWTError

from core.config import settings


security = HTTPBearer()


def create_token(email: str) -> str:
    expiry = datetime.utcnow() + timedelta(hours=1)

    payload = {
        "email": email,
        "exp": expiry
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def decode_token(token: HTTPAuthorizationCredentials = Depends(security)):

    try:
        payload = decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        return payload

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

