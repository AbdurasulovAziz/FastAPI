from datetime import datetime, timedelta
import os

import jwt
from fastapi.security import HTTPBearer

from config import settings


security = HTTPBearer()


def create_token(email: str) -> str:
    expiry = datetime.utcnow() + timedelta(hours=1)

    payload = {
        "email": email,
        "exp": expiry
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token

