from datetime import datetime, timedelta
import os

import jwt
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from pydantic import EmailStr

load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')

security = HTTPBearer()


def create_token(email: str) -> str:
    expiry = datetime.utcnow() + timedelta(hours=1)

    payload = {
        "email": email,
        "exp": expiry
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

